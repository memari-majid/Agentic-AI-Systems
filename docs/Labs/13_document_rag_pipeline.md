# Lab 13: Document RAG with Agents

⏱️ **Estimated completion time: 90 minutes** | 🎯 **Difficulty: Intermediate**

## Lab Overview

In this hands-on lab, you'll build a complete Retrieval-Augmented Generation (RAG) pipeline that can process documents, create embeddings, and answer questions based on the content. This lab complements the theoretical knowledge from the "Unstructured Data & LLMs" module with practical implementation experience.

!!! info "What You'll Build"
    - **Document Processing Pipeline**: Ingest and process various document formats
    - **Vector Database Integration**: Store and retrieve document embeddings
    - **RAG Query System**: Answer questions using retrieved context
    - **Evaluation Framework**: Assess system performance and quality

## Learning Objectives

By completing this lab, you will:

- ✅ Implement a complete RAG pipeline from scratch
- ✅ Integrate vector databases for semantic search
- ✅ Build evaluation metrics for RAG system performance
- ✅ Handle real-world challenges like document chunking and context management
- ✅ Deploy a functional question-answering system

## Prerequisites

- **Python 3.8+** with virtual environment capability
- **Basic familiarity** with LLMs and vector databases
- **API access** to OpenAI or similar LLM service
- **Local development environment** with Jupyter notebooks or Python IDE

## Lab Setup

### 1. Environment Preparation

```bash
# Create virtual environment
python -m venv rag_lab
source rag_lab/bin/activate  # On Windows: rag_lab\Scripts\activate

# Install required packages
pip install \
    langchain>=0.1.0 \
    langchain-openai \
    langchain-community \
    chromadb \
    pypdf2 \
    python-docx \
    sentence-transformers \
    tiktoken \
    streamlit \
    python-dotenv
```

### 2. API Configuration

Create a `.env` file in your working directory:

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
# Optional: Add other LLM provider keys
ANTHROPIC_API_KEY=your_anthropic_key_here
COHERE_API_KEY=your_cohere_key_here
```

### 3. Sample Documents

Create a `documents/` folder and add sample documents:

```
documents/
├── company_policy.pdf
├── technical_manual.docx  
├── research_paper.pdf
└── faq_document.txt
```

## Part 1: Document Processing Pipeline

### Step 1: Document Loader Implementation

```python
# document_processor.py
import os
from typing import List, Dict
from pathlib import Path
import PyPDF2
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class DocumentProcessor:
    """Handles loading and processing of various document formats"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def load_docx(self, file_path: str) -> str:
        """Extract text from Word document"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def load_txt(self, file_path: str) -> str:
        """Load text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def process_document(self, file_path: str) -> List[Document]:
        """Process a document and return chunked documents"""
        file_extension = Path(file_path).suffix.lower()
        
        # Load content based on file type
        if file_extension == '.pdf':
            content = self.load_pdf(file_path)
        elif file_extension == '.docx':
            content = self.load_docx(file_path)
        elif file_extension == '.txt':
            content = self.load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Create metadata
        metadata = {
            "source": file_path,
            "filename": Path(file_path).name,
            "file_type": file_extension
        }
        
        # Split into chunks
        texts = self.text_splitter.split_text(content)
        
        # Create Document objects
        documents = []
        for i, text in enumerate(texts):
            doc_metadata = metadata.copy()
            doc_metadata["chunk_id"] = i
            documents.append(Document(page_content=text, metadata=doc_metadata))
        
        return documents
    
    def process_directory(self, directory_path: str) -> List[Document]:
        """Process all supported documents in a directory"""
        documents = []
        supported_extensions = {'.pdf', '.docx', '.txt'}
        
        for file_path in Path(directory_path).iterdir():
            if file_path.suffix.lower() in supported_extensions:
                print(f"Processing: {file_path.name}")
                try:
                    docs = self.process_document(str(file_path))
                    documents.extend(docs)
                    print(f"  Created {len(docs)} chunks")
                except Exception as e:
                    print(f"  Error processing {file_path.name}: {e}")
        
        return documents

# Test the document processor
if __name__ == "__main__":
    processor = DocumentProcessor()
    documents = processor.process_directory("documents/")
    print(f"Total documents processed: {len(documents)}")
```

### Step 2: Vector Database Setup

```python
# vector_store.py
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List, Optional

class VectorStore:
    """Manages vector database operations"""
    
    def __init__(self, collection_name: str = "rag_documents", 
                 persist_directory: str = "./chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        
    def initialize_store(self):
        """Initialize or load existing vector store"""
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        
    def add_documents(self, documents: List[Document]):
        """Add documents to the vector store"""
        if not self.vector_store:
            self.initialize_store()
            
        # Add documents in batches to avoid memory issues
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            self.vector_store.add_documents(batch)
            print(f"Added batch {i//batch_size + 1}, documents {i+1}-{min(i+batch_size, len(documents))}")
        
        # Persist the changes
        self.vector_store.persist()
        print(f"Successfully added {len(documents)} documents to vector store")
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents"""
        if not self.vector_store:
            self.initialize_store()
        return self.vector_store.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = 5):
        """Search with similarity scores"""
        if not self.vector_store:
            self.initialize_store()
        return self.vector_store.similarity_search_with_score(query, k=k)

# Initialize and populate vector store
def setup_vector_store(documents: List[Document]) -> VectorStore:
    """Set up vector store with documents"""
    store = VectorStore()
    store.add_documents(documents)
    return store
```

## Part 2: RAG Query System

### Step 3: RAG Pipeline Implementation

```python
# rag_system.py
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import Dict, List
import time

class RAGSystem:
    """Complete RAG system for question answering"""
    
    def __init__(self, vector_store: VectorStore, model_name: str = "gpt-3.5-turbo"):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.1)
        self.setup_qa_chain()
    
    def setup_qa_chain(self):
        """Set up the question-answering chain"""
        # Custom prompt template
        prompt_template = """
        You are a helpful assistant that answers questions based on provided context.
        Use the following pieces of context to answer the question at the end.
        
        If you don't know the answer based on the context provided, say "I don't have enough information to answer this question based on the provided context."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer: """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.vector_store.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
    
    def query(self, question: str) -> Dict:
        """Process a question and return answer with sources"""
        start_time = time.time()
        
        result = self.qa_chain({"query": question})
        
        response = {
            "question": question,
            "answer": result["result"],
            "source_documents": result["source_documents"],
            "response_time": time.time() - start_time
        }
        
        return response
    
    def query_with_context_analysis(self, question: str, k: int = 5) -> Dict:
        """Enhanced query with context analysis"""
        # Get relevant documents with scores
        docs_with_scores = self.vector_store.similarity_search_with_score(question, k=k)
        
        # Analyze retrieved context
        context_analysis = {
            "retrieved_chunks": len(docs_with_scores),
            "sources": list(set([doc.metadata.get("filename", "unknown") 
                               for doc, score in docs_with_scores])),
            "relevance_scores": [float(score) for doc, score in docs_with_scores],
            "avg_relevance": sum(score for doc, score in docs_with_scores) / len(docs_with_scores)
        }
        
        # Get the answer
        result = self.query(question)
        result["context_analysis"] = context_analysis
        
        return result

# Interactive query function
def interactive_query_loop(rag_system: RAGSystem):
    """Interactive loop for testing queries"""
    print("RAG System ready! Type 'quit' to exit.")
    
    while True:
        question = input("\nEnter your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        if not question:
            continue
        
        try:
            result = rag_system.query_with_context_analysis(question)
            
            print(f"\n{'='*50}")
            print(f"Question: {result['question']}")
            print(f"{'='*50}")
            print(f"Answer: {result['answer']}")
            print(f"\nContext Analysis:")
            print(f"  - Sources used: {result['context_analysis']['sources']}")
            print(f"  - Chunks retrieved: {result['context_analysis']['retrieved_chunks']}")
            print(f"  - Avg relevance: {result['context_analysis']['avg_relevance']:.3f}")
            print(f"  - Response time: {result['response_time']:.2f}s")
            
        except Exception as e:
            print(f"Error processing query: {e}")
```

## Part 3: Evaluation Framework

### Step 4: RAG System Evaluation

```python
# evaluation.py
import json
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RAGEvaluator:
    """Evaluation framework for RAG systems"""
    
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system
        self.embeddings = rag_system.vector_store.embeddings
    
    def create_test_questions(self) -> List[Dict]:
        """Create test questions for evaluation"""
        # In practice, these would be created by domain experts
        test_cases = [
            {
                "question": "What is the company's remote work policy?",
                "expected_sources": ["company_policy.pdf"],
                "category": "policy"
            },
            {
                "question": "How do I troubleshoot connection issues?",
                "expected_sources": ["technical_manual.docx"],
                "category": "technical"
            },
            {
                "question": "What are the main findings of the research?",
                "expected_sources": ["research_paper.pdf"], 
                "category": "research"
            }
        ]
        return test_cases
    
    def evaluate_answer_quality(self, question: str, answer: str, 
                              ground_truth: str = None) -> Dict:
        """Evaluate the quality of a generated answer"""
        metrics = {}
        
        # Length analysis
        metrics["answer_length"] = len(answer.split())
        
        # Coherence check (basic heuristics)
        metrics["has_definitive_answer"] = not any(phrase in answer.lower() 
            for phrase in ["i don't know", "not enough information", "cannot answer"])
        
        # If ground truth is available, compute similarity
        if ground_truth:
            answer_emb = self.embeddings.embed_query(answer)
            truth_emb = self.embeddings.embed_query(ground_truth)
            similarity = cosine_similarity([answer_emb], [truth_emb])[0][0]
            metrics["semantic_similarity"] = float(similarity)
        
        return metrics
    
    def evaluate_retrieval_quality(self, question: str, retrieved_docs: List, 
                                 expected_sources: List[str]) -> Dict:
        """Evaluate the quality of document retrieval"""
        retrieved_sources = [doc.metadata.get("filename", "") for doc in retrieved_docs]
        
        # Source coverage
        expected_found = sum(1 for source in expected_sources 
                           if any(source in ret_source for ret_source in retrieved_sources))
        source_recall = expected_found / len(expected_sources) if expected_sources else 0
        
        # Diversity of sources
        unique_sources = len(set(retrieved_sources))
        source_diversity = unique_sources / len(retrieved_docs) if retrieved_docs else 0
        
        return {
            "source_recall": source_recall,
            "source_diversity": source_diversity,
            "retrieved_sources": retrieved_sources,
            "expected_sources": expected_sources
        }
    
    def run_evaluation(self, test_cases: List[Dict] = None) -> Dict:
        """Run comprehensive evaluation"""
        if test_cases is None:
            test_cases = self.create_test_questions()
        
        results = []
        
        for test_case in test_cases:
            print(f"Evaluating: {test_case['question'][:50]}...")
            
            # Get system response
            response = self.rag_system.query_with_context_analysis(test_case["question"])
            
            # Evaluate answer quality
            answer_metrics = self.evaluate_answer_quality(
                test_case["question"], 
                response["answer"]
            )
            
            # Evaluate retrieval quality
            retrieval_metrics = self.evaluate_retrieval_quality(
                test_case["question"],
                response["source_documents"],
                test_case.get("expected_sources", [])
            )
            
            # Combine results
            result = {
                "test_case": test_case,
                "response": response,
                "answer_metrics": answer_metrics,
                "retrieval_metrics": retrieval_metrics
            }
            
            results.append(result)
        
        # Aggregate metrics
        aggregate_metrics = self.aggregate_results(results)
        
        return {
            "individual_results": results,
            "aggregate_metrics": aggregate_metrics
        }
    
    def aggregate_results(self, results: List[Dict]) -> Dict:
        """Aggregate evaluation results"""
        metrics = {
            "total_questions": len(results),
            "avg_response_time": np.mean([r["response"]["response_time"] for r in results]),
            "avg_source_recall": np.mean([r["retrieval_metrics"]["source_recall"] for r in results]),
            "avg_source_diversity": np.mean([r["retrieval_metrics"]["source_diversity"] for r in results]),
            "definitive_answer_rate": np.mean([r["answer_metrics"]["has_definitive_answer"] for r in results])
        }
        
        return metrics

# Generate evaluation report
def generate_evaluation_report(evaluation_results: Dict, output_file: str = "evaluation_report.json"):
    """Generate a comprehensive evaluation report"""
    with open(output_file, 'w') as f:
        json.dump(evaluation_results, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "="*50)
    print("EVALUATION SUMMARY")
    print("="*50)
    
    metrics = evaluation_results["aggregate_metrics"]
    print(f"Total Questions Evaluated: {metrics['total_questions']}")
    print(f"Average Response Time: {metrics['avg_response_time']:.2f}s")
    print(f"Source Recall Rate: {metrics['avg_source_recall']:.2%}")
    print(f"Source Diversity: {metrics['avg_source_diversity']:.2%}")
    print(f"Definitive Answer Rate: {metrics['definitive_answer_rate']:.2%}")
    
    print(f"\nDetailed results saved to: {output_file}")
```

## Part 4: Complete System Integration

### Step 5: Main Application

```python
# main.py
import os
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from vector_store import VectorStore, setup_vector_store
from rag_system import RAGSystem, interactive_query_loop
from evaluation import RAGEvaluator, generate_evaluation_report

def main():
    """Main function to orchestrate the RAG pipeline"""
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY in your .env file")
        return
    
    print("🚀 Starting RAG Pipeline Setup...")
    
    # Step 1: Process documents
    print("\n📄 Processing documents...")
    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    
    if not os.path.exists("documents"):
        os.makedirs("documents")
        print("Created documents/ directory. Please add some documents and run again.")
        return
    
    documents = processor.process_directory("documents/")
    
    if not documents:
        print("No documents found. Please add PDF, DOCX, or TXT files to the documents/ directory.")
        return
    
    print(f"✅ Processed {len(documents)} document chunks")
    
    # Step 2: Set up vector store
    print("\n🗄️ Setting up vector database...")
    vector_store = setup_vector_store(documents)
    print("✅ Vector store ready")
    
    # Step 3: Initialize RAG system
    print("\n🤖 Initializing RAG system...")
    rag_system = RAGSystem(vector_store)
    print("✅ RAG system ready")
    
    # Step 4: Run evaluation
    print("\n📊 Running system evaluation...")
    evaluator = RAGEvaluator(rag_system)
    evaluation_results = evaluator.run_evaluation()
    generate_evaluation_report(evaluation_results)
    
    # Step 5: Interactive mode
    print("\n💬 Starting interactive mode...")
    interactive_query_loop(rag_system)

if __name__ == "__main__":
    main()
```

### Step 6: Streamlit Web Interface (Optional)

```python
# streamlit_app.py
import streamlit as st
import os
from dotenv import load_dotenv
from main import DocumentProcessor, VectorStore, RAGSystem

load_dotenv()

@st.cache_resource
def load_rag_system():
    """Load and cache the RAG system"""
    if not os.path.exists("./chroma_db"):
        return None
    
    vector_store = VectorStore()
    vector_store.initialize_store()
    return RAGSystem(vector_store)

def main():
    st.title("🤖 Document RAG System")
    st.write("Ask questions about your documents!")
    
    # Load RAG system
    rag_system = load_rag_system()
    
    if rag_system is None:
        st.error("RAG system not initialized. Please run main.py first to process documents.")
        return
    
    # Query interface
    question = st.text_input("Enter your question:", placeholder="What is the main topic of the documents?")
    
    if st.button("Get Answer") and question:
        with st.spinner("Searching and generating answer..."):
            result = rag_system.query_with_context_analysis(question)
        
        # Display results
        st.subheader("Answer")
        st.write(result["answer"])
        
        # Display context analysis
        with st.expander("Context Analysis"):
            st.write(f"**Response Time:** {result['response_time']:.2f}s")
            st.write(f"**Sources Used:** {', '.join(result['context_analysis']['sources'])}")
            st.write(f"**Chunks Retrieved:** {result['context_analysis']['retrieved_chunks']}")
            st.write(f"**Average Relevance:** {result['context_analysis']['avg_relevance']:.3f}")
        
        # Display source documents
        with st.expander("Source Documents"):
            for i, doc in enumerate(result["source_documents"]):
                st.write(f"**Source {i+1}:** {doc.metadata.get('filename', 'Unknown')}")
                st.write(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
                st.write("---")

if __name__ == "__main__":
    main()
```

## Lab Exercises

### Exercise 1: Basic Implementation

1. **Set up the environment** and process sample documents
2. **Run the complete pipeline** and test with sample questions
3. **Analyze the evaluation results** and identify areas for improvement

### Exercise 2: Performance Optimization

1. **Experiment with different chunk sizes** (500, 1000, 2000 tokens)
2. **Test different embedding models** (OpenAI, Sentence Transformers)
3. **Compare retrieval performance** with different K values (3, 5, 10)

### Exercise 3: Advanced Features

1. **Implement hybrid search** combining semantic and keyword search
2. **Add document metadata filtering** by file type or date
3. **Create custom evaluation metrics** for your specific use case

### Exercise 4: Production Readiness

1. **Add error handling** and logging throughout the pipeline
2. **Implement caching** for frequently asked questions
3. **Add monitoring** for response times and accuracy metrics

## Expected Outcomes

After completing this lab, you should have:

- ✅ **Working RAG System**: Complete pipeline from documents to answers
- ✅ **Evaluation Framework**: Metrics to assess system performance
- ✅ **Practical Experience**: Hands-on understanding of RAG challenges and solutions
- ✅ **Production Insights**: Knowledge of optimization and monitoring strategies

## Next Steps

- **Lab 14**: Advanced RAG with Agents - Add intelligent routing and multi-step reasoning
- **Lab 15**: AWS Unstructured Data Pipeline - Scale your system to enterprise level

---

!!! tip "Troubleshooting"
    **Common Issues:**
    
    - **Import errors**: Ensure all packages are installed in your virtual environment
    - **API key issues**: Verify your .env file is properly configured  
    - **Memory issues**: Reduce batch size or chunk size for large document sets
    - **Slow performance**: Consider using local embeddings or caching strategies

!!! success "Lab Complete!"
    Congratulations! You've built a complete RAG system from scratch. This foundation will serve you well as you explore more advanced implementations in the following modules.
