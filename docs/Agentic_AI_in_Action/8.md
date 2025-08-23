# Leveraging Unstructured Data with LLMs: Practical Implementation Guide

⏱️ **Estimated reading time: 25 minutes**

## Introduction

Most enterprise data is unstructured - documents, emails, images, videos, and audio files that don't fit neatly into databases. This chapter provides practical, implementation-focused techniques for efficiently integrating unstructured data with Large Language Models (LLMs) for production AI systems.

## Core Approaches Overview

### 1. Retrieval-Augmented Generation (RAG)
- **Best for**: Dynamic data, frequent updates, cost-sensitive applications
- **Implementation**: External knowledge retrieval + LLM generation
- **Latency**: Higher (retrieval + generation)
- **Cost**: Lower per query

### 2. Fine-Tuning
- **Best for**: Domain-specific knowledge, consistent patterns, high-volume applications
- **Implementation**: Model training on specific datasets
- **Latency**: Lower (direct generation)
- **Cost**: Higher upfront, lower per query at scale

### 3. Hybrid Approaches
- **Best for**: Complex enterprise scenarios requiring both approaches
- **Implementation**: Combine fine-tuned base models with RAG systems

## Practical RAG Implementation

### Basic RAG Pipeline

```python
import os
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

class ProductionRAGSystem:
    def __init__(self, collection_name: str = "documents"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_documents(self, file_paths: List[str]) -> None:
        """Process and index documents efficiently"""
        documents = []
        metadatas = []
        ids = []
        
        for file_path in file_paths:
            # Load document based on file type
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding='utf-8')
            
            docs = loader.load()
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(docs)
            
            for i, chunk in enumerate(chunks):
                documents.append(chunk.page_content)
                metadatas.append({
                    "source": file_path,
                    "chunk_id": i,
                    "file_type": Path(file_path).suffix
                })
                ids.append(f"{Path(file_path).stem}_{i}")
        
        # Batch processing for efficiency
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """Retrieve relevant documents and generate response"""
        # Retrieve relevant chunks
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Build context from retrieved documents
        context = "\n\n".join(results['documents'][0])
        
        # Generate response using LLM
        llm = OpenAI(temperature=0)
        response = llm(f"""
        Based on the following context, answer the question:
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """)
        
        return {
            "answer": response,
            "sources": [meta['source'] for meta in results['metadatas'][0]],
            "confidence": 1 - min(results['distances'][0])
        }

# Usage example
rag_system = ProductionRAGSystem()
rag_system.process_documents(['docs/manual.pdf', 'docs/faq.txt'])
result = rag_system.query("How do I reset my password?")
```

### Advanced RAG Techniques

#### 1. Multi-Modal RAG with Images

```python
import base64
from PIL import Image
from langchain.schema import Document

class MultiModalRAG(ProductionRAGSystem):
    def process_image_documents(self, image_paths: List[str]) -> None:
        """Process images with OCR and visual understanding"""
        from easyocr import Reader
        import cv2
        
        reader = Reader(['en'])
        
        for image_path in image_paths:
            # Extract text using OCR
            ocr_results = reader.readtext(image_path)
            extracted_text = " ".join([result[1] for result in ocr_results])
            
            # Encode image for visual context
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode()
            
            # Add to vector store with both text and image data
            self.collection.add(
                documents=[extracted_text],
                metadatas=[{
                    "source": image_path,
                    "type": "image",
                    "encoded_image": encoded_image[:1000]  # Truncate for storage
                }],
                ids=[f"img_{Path(image_path).stem}"]
            )
```

#### 2. Hierarchical Document Processing

```python
class HierarchicalRAG(ProductionRAGSystem):
    def __init__(self):
        super().__init__()
        # Create separate collections for different granularities
        self.document_collection = self.client.get_or_create_collection("documents")
        self.section_collection = self.client.get_or_create_collection("sections")
        self.chunk_collection = self.client.get_or_create_collection("chunks")
    
    def process_hierarchical_documents(self, file_paths: List[str]):
        """Process documents at multiple levels of granularity"""
        for file_path in file_paths:
            doc_content = self._load_document(file_path)
            
            # Document level
            self.document_collection.add(
                documents=[doc_content],
                metadatas=[{"source": file_path, "level": "document"}],
                ids=[f"doc_{Path(file_path).stem}"]
            )
            
            # Section level (split by headers)
            sections = self._split_by_headers(doc_content)
            for i, section in enumerate(sections):
                self.section_collection.add(
                    documents=[section],
                    metadatas=[{"source": file_path, "level": "section", "section_id": i}],
                    ids=[f"sec_{Path(file_path).stem}_{i}"]
                )
            
            # Chunk level (fine-grained)
            chunks = self.text_splitter.split_text(doc_content)
            for i, chunk in enumerate(chunks):
                self.chunk_collection.add(
                    documents=[chunk],
                    metadatas=[{"source": file_path, "level": "chunk", "chunk_id": i}],
                    ids=[f"chunk_{Path(file_path).stem}_{i}"]
                )
```

## Efficient Data Processing Strategies

### 1. Batch Processing Pipeline

```python
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncGenerator

class EfficientDataProcessor:
    def __init__(self, batch_size: int = 100, max_workers: int = 4):
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_files_batch(self, file_paths: List[str]) -> None:
        """Process files in batches for memory efficiency"""
        for i in range(0, len(file_paths), self.batch_size):
            batch = file_paths[i:i + self.batch_size]
            await self._process_batch(batch)
    
    async def _process_batch(self, file_paths: List[str]) -> None:
        """Process a single batch of files"""
        tasks = [self._process_single_file(path) for path in file_paths]
        await asyncio.gather(*tasks)
    
    async def _process_single_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single file asynchronously"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            self._sync_process_file, 
            file_path
        )
    
    def _sync_process_file(self, file_path: str) -> Dict[str, Any]:
        """Synchronous file processing"""
        # Implementation for file processing
        pass
```

### 2. Intelligent Chunking Strategies

```python
class SmartChunker:
    def __init__(self):
        self.semantic_splitter = None  # Initialize with sentence transformers
    
    def semantic_chunking(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """Chunk text based on semantic similarity"""
        sentences = self._split_into_sentences(text)
        embeddings = self._get_sentence_embeddings(sentences)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
            if current_size + len(sentence) > max_chunk_size and current_chunk:
                # Check semantic coherence before splitting
                if self._is_coherent_break(embeddings, i):
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [sentence]
                    current_size = len(sentence)
                else:
                    current_chunk.append(sentence)
                    current_size += len(sentence)
            else:
                current_chunk.append(sentence)
                current_size += len(sentence)
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def document_structure_chunking(self, text: str) -> List[Dict[str, Any]]:
        """Chunk based on document structure (headers, paragraphs, etc.)"""
        import re
        
        chunks = []
        
        # Split by markdown headers
        header_pattern = r'^(#{1,6})\s+(.*?)$'
        sections = re.split(header_pattern, text, flags=re.MULTILINE)
        
        current_section = {"level": 0, "title": "", "content": ""}
        
        for i in range(1, len(sections), 3):
            if i + 2 < len(sections):
                level = len(sections[i])
                title = sections[i + 1]
                content = sections[i + 2].strip()
                
                if content:
                    chunks.append({
                        "text": content,
                        "metadata": {
                            "section_level": level,
                            "section_title": title,
                            "chunk_type": "section"
                        }
                    })
        
        return chunks
```

## Production-Ready Vector Database Setup

### 1. Optimized ChromaDB Configuration

```python
import chromadb
from chromadb.config import Settings

class ProductionVectorDB:
    def __init__(self, persist_directory: str = "./production_db"):
        # Production-optimized settings
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=persist_directory,
                chroma_server_grpc_port=8000,
            )
        )
        
        # Create collection with optimized settings
        self.collection = self.client.get_or_create_collection(
            name="production_docs",
            metadata={
                "hnsw:space": "cosine",
                "hnsw:M": 16,  # Higher M for better recall
                "hnsw:ef_construction": 200,  # Higher for better indexing
                "hnsw:ef_search": 100  # Higher for better search quality
            }
        )
    
    def bulk_upsert(self, documents: List[str], metadatas: List[Dict], 
                   ids: List[str], batch_size: int = 1000) -> None:
        """Efficiently insert large amounts of data"""
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_meta = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            
            self.collection.upsert(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
```

### 2. Pinecone Integration for Scale

```python
import pinecone
from sentence_transformers import SentenceTransformer

class ScalableVectorSearch:
    def __init__(self, api_key: str, environment: str):
        pinecone.init(api_key=api_key, environment=environment)
        
        # Create index with optimal settings
        if "production-docs" not in pinecone.list_indexes():
            pinecone.create_index(
                name="production-docs",
                dimension=768,  # sentence-transformers dimension
                metric="cosine",
                pods=1,
                replicas=1,
                pod_type="p1.x1"
            )
        
        self.index = pinecone.Index("production-docs")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def upsert_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Upsert documents with metadata"""
        vectors = []
        
        for doc in documents:
            embedding = self.encoder.encode(doc['text']).tolist()
            vectors.append({
                "id": doc['id'],
                "values": embedding,
                "metadata": doc['metadata']
            })
        
        # Batch upsert
        self.index.upsert(vectors=vectors)
    
    def search(self, query: str, top_k: int = 10, 
               filter_dict: Dict = None) -> List[Dict]:
        """Search with optional metadata filtering"""
        query_embedding = self.encoder.encode(query).tolist()
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            filter=filter_dict,
            include_metadata=True
        )
        
        return results['matches']
```

## Fine-Tuning for Specialized Tasks

### 1. Domain-Specific Fine-Tuning

```python
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    TrainingArguments, Trainer, DataCollatorForLanguageModeling
)
from datasets import Dataset
import torch

class DomainSpecificFineTuner:
    def __init__(self, base_model: str = "microsoft/DialoGPT-medium"):
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.model = AutoModelForCausalLM.from_pretrained(base_model)
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def prepare_dataset(self, texts: List[str], max_length: int = 512) -> Dataset:
        """Prepare dataset for fine-tuning"""
        def tokenize_function(examples):
            return self.tokenizer(
                examples['text'],
                truncation=True,
                padding=True,
                max_length=max_length,
                return_tensors="pt"
            )
        
        dataset = Dataset.from_dict({"text": texts})
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        return tokenized_dataset
    
    def fine_tune(self, train_dataset: Dataset, output_dir: str = "./fine_tuned_model"):
        """Fine-tune the model"""
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=2,
            warmup_steps=100,
            logging_steps=50,
            save_steps=500,
            evaluation_strategy="steps",
            eval_steps=500,
            save_total_limit=2,
            prediction_loss_only=True,
            fp16=torch.cuda.is_available(),
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=train_dataset,  # Use validation split in practice
        )
        
        trainer.train()
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
```

### 2. LoRA (Low-Rank Adaptation) for Efficient Fine-Tuning

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import BitsAndBytesConfig

class EfficientFineTuner:
    def __init__(self, base_model: str):
        # 4-bit quantization config
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        # Load model with quantization
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        
        # Prepare model for training
        self.model = prepare_model_for_kbit_training(self.model)
        
        # LoRA configuration
        lora_config = LoraConfig(
            r=16,  # rank
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        self.model = get_peft_model(self.model, lora_config)
    
    def train_lora(self, dataset: Dataset):
        """Train using LoRA adapter"""
        training_args = TrainingArguments(
            output_dir="./lora_model",
            num_train_epochs=3,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            optim="paged_adamw_32bit",
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            save_strategy="epoch"
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer, 
                mlm=False
            )
        )
        
        trainer.train()
```

## Hybrid RAG + Fine-Tuning Architecture

```python
class HybridRAGFineTuned:
    def __init__(self, fine_tuned_model_path: str, vector_db_path: str):
        # Load fine-tuned model
        self.tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_path)
        self.model = AutoModelForCausalLM.from_pretrained(fine_tuned_model_path)
        
        # Initialize RAG system
        self.rag_system = ProductionRAGSystem()
        
    def hybrid_query(self, question: str, use_retrieval: bool = True) -> Dict[str, Any]:
        """Combine retrieval and fine-tuned generation"""
        context = ""
        sources = []
        
        if use_retrieval:
            rag_result = self.rag_system.query(question)
            context = rag_result.get('context', '')
            sources = rag_result.get('sources', [])
        
        # Generate using fine-tuned model
        if context:
            prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        else:
            prompt = f"Question: {question}\n\nAnswer:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = response.split("Answer:")[-1].strip()
        
        return {
            "answer": answer,
            "sources": sources,
            "used_retrieval": use_retrieval,
            "context_length": len(context)
        }
```

## Performance Optimization & Monitoring

### 1. Caching Strategy

```python
import redis
import pickle
from functools import wraps
import hashlib

class RAGCache:
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        self.redis_client = redis.Redis(
            host=redis_host, 
            port=redis_port, 
            decode_responses=False
        )
        
    def cache_key(self, query: str, top_k: int) -> str:
        """Generate cache key from query parameters"""
        key_string = f"{query}:{top_k}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get_cached_result(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Get cached result if available"""
        key = self.cache_key(query, top_k)
        cached = self.redis_client.get(key)
        
        if cached:
            return pickle.loads(cached)
        return None
    
    def cache_result(self, query: str, result: Dict[str, Any], 
                    top_k: int = 5, ttl: int = 3600) -> None:
        """Cache query result"""
        key = self.cache_key(query, top_k)
        self.redis_client.setex(
            key, 
            ttl, 
            pickle.dumps(result)
        )

def cached_rag_query(cache: RAGCache):
    """Decorator for caching RAG queries"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, query: str, top_k: int = 5, *args, **kwargs):
            # Try cache first
            cached_result = cache.get_cached_result(query, top_k)
            if cached_result:
                return cached_result
            
            # Execute query
            result = func(self, query, top_k, *args, **kwargs)
            
            # Cache result
            cache.cache_result(query, result, top_k)
            
            return result
        return wrapper
    return decorator
```

### 2. Quality Metrics & Monitoring

```python
import logging
from datetime import datetime
from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RAGQualityMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = {
            "total_queries": 0,
            "avg_response_time": 0,
            "avg_relevance_score": 0,
            "cache_hit_rate": 0
        }
        
    def log_query(self, query: str, result: Dict[str, Any], 
                 response_time: float, relevance_score: float = None):
        """Log query performance metrics"""
        self.metrics["total_queries"] += 1
        
        # Update response time
        current_avg = self.metrics["avg_response_time"]
        new_avg = (current_avg * (self.metrics["total_queries"] - 1) + response_time) / self.metrics["total_queries"]
        self.metrics["avg_response_time"] = new_avg
        
        # Update relevance score if provided
        if relevance_score:
            current_relevance = self.metrics["avg_relevance_score"]
            new_relevance = (current_relevance * (self.metrics["total_queries"] - 1) + relevance_score) / self.metrics["total_queries"]
            self.metrics["avg_relevance_score"] = new_relevance
        
        # Log to file
        self.logger.info({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response_time": response_time,
            "relevance_score": relevance_score,
            "sources_count": len(result.get("sources", [])),
            "answer_length": len(result.get("answer", ""))
        })
    
    def evaluate_relevance(self, query: str, retrieved_docs: List[str]) -> float:
        """Calculate relevance score using embeddings"""
        if not retrieved_docs:
            return 0.0
        
        # This would use your actual embedding model
        query_embedding = self._get_embedding(query)
        doc_embeddings = [self._get_embedding(doc) for doc in retrieved_docs]
        
        # Calculate average cosine similarity
        similarities = [
            cosine_similarity([query_embedding], [doc_emb])[0][0] 
            for doc_emb in doc_embeddings
        ]
        
        return np.mean(similarities)
```

## Real-World Use Cases

### 1. Legal Document Analysis

```python
class LegalRAGSystem(ProductionRAGSystem):
    def __init__(self):
        super().__init__(collection_name="legal_documents")
        self.legal_patterns = {
            "contract": r"AGREEMENT|CONTRACT|TERMS|CONDITIONS",
            "statute": r"USC|CFR|SECTION|SUBSECTION",
            "case_law": r"v\.|versus|COURT|DECIDED"
        }
    
    def process_legal_documents(self, file_paths: List[str]):
        """Process legal documents with specialized handling"""
        for file_path in file_paths:
            content = self._load_document(file_path)
            
            # Classify document type
            doc_type = self._classify_legal_document(content)
            
            # Extract legal entities and dates
            entities = self._extract_legal_entities(content)
            dates = self._extract_dates(content)
            
            # Create structured chunks with legal context
            chunks = self._create_legal_chunks(content, doc_type, entities, dates)
            
            self._index_legal_chunks(chunks, file_path)
    
    def legal_query(self, question: str) -> Dict[str, Any]:
        """Query with legal-specific processing"""
        # Extract legal concepts from question
        legal_concepts = self._extract_legal_concepts(question)
        
        # Enhanced query with legal context
        enhanced_query = f"{question} {' '.join(legal_concepts)}"
        
        result = self.query(enhanced_query)
        
        # Add legal-specific metadata
        result["legal_concepts"] = legal_concepts
        result["case_references"] = self._extract_case_references(result["answer"])
        
        return result
```

### 2. Customer Support Knowledge Base

```python
class CustomerSupportRAG(ProductionRAGSystem):
    def __init__(self):
        super().__init__(collection_name="support_kb")
        self.intent_classifier = None  # Load intent classification model
        
    def process_support_documents(self, file_paths: List[str]):
        """Process support documents with ticket categorization"""
        categories = ["billing", "technical", "account", "product"]
        
        for file_path in file_paths:
            content = self._load_document(file_path)
            
            # Classify content by support category
            category = self._classify_support_category(content)
            
            # Extract common issues and solutions
            issues_solutions = self._extract_issues_solutions(content)
            
            # Create targeted chunks
            chunks = self.text_splitter.split_text(content)
            
            for i, chunk in enumerate(chunks):
                metadata = {
                    "source": file_path,
                    "category": category,
                    "chunk_id": i,
                    "issues": issues_solutions.get("issues", []),
                    "solutions": issues_solutions.get("solutions", [])
                }
                
                self.collection.add(
                    documents=[chunk],
                    metadatas=[metadata],
                    ids=[f"support_{Path(file_path).stem}_{i}"]
                )
    
    def support_query(self, question: str, customer_tier: str = "standard") -> Dict[str, Any]:
        """Query with customer support context"""
        # Classify customer intent
        intent = self._classify_intent(question)
        
        # Filter by customer tier if needed
        filter_dict = {"category": intent}
        if customer_tier == "premium":
            filter_dict["priority"] = "high"
        
        result = self.query(question)
        
        # Add support-specific features
        result["intent"] = intent
        result["escalation_needed"] = self._needs_escalation(question, result["answer"])
        result["suggested_actions"] = self._suggest_actions(intent, result["answer"])
        
        return result
```

## Best Practices & Production Considerations

### 1. Data Security & Privacy

```python
import hashlib
from cryptography.fernet import Fernet

class SecureRAGSystem(ProductionRAGSystem):
    def __init__(self, encryption_key: bytes = None):
        super().__init__()
        self.fernet = Fernet(encryption_key or Fernet.generate_key())
        
    def add_sensitive_document(self, content: str, metadata: Dict[str, Any]):
        """Add document with PII scrubbing and encryption"""
        # Scrub PII
        cleaned_content = self._scrub_pii(content)
        
        # Encrypt sensitive metadata
        if "sensitive" in metadata:
            metadata["sensitive"] = self.fernet.encrypt(
                metadata["sensitive"].encode()
            ).decode()
        
        # Hash original content for deduplication
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        metadata["content_hash"] = content_hash
        
        # Add to collection
        self.collection.add(
            documents=[cleaned_content],
            metadatas=[metadata],
            ids=[content_hash]
        )
    
    def _scrub_pii(self, text: str) -> str:
        """Remove personally identifiable information"""
        import re
        
        # Email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Phone numbers
        text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', text)
        
        # Social Security Numbers
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        
        # Credit card numbers (basic pattern)
        text = re.sub(r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b', '[CARD]', text)
        
        return text
```

### 2. Error Handling & Fallbacks

```python
class RobustRAGSystem(ProductionRAGSystem):
    def __init__(self):
        super().__init__()
        self.fallback_responses = {
            "no_results": "I couldn't find specific information about that. Could you rephrase your question?",
            "low_confidence": "I found some information but I'm not entirely confident. Here's what I found:",
            "error": "I'm experiencing some technical difficulties. Please try again or contact support."
        }
        
    def query_with_fallback(self, question: str) -> Dict[str, Any]:
        """Query with comprehensive error handling"""
        try:
            result = self.query(question)
            
            # Check result quality
            if not result.get("sources"):
                return {
                    "answer": self.fallback_responses["no_results"],
                    "confidence": 0.0,
                    "fallback_used": True
                }
            
            # Check confidence threshold
            if result.get("confidence", 0) < 0.5:
                result["answer"] = f"{self.fallback_responses['low_confidence']} {result['answer']}"
                result["low_confidence"] = True
            
            return result
            
        except Exception as e:
            self.logger.error(f"RAG query failed: {str(e)}")
            return {
                "answer": self.fallback_responses["error"],
                "error": str(e),
                "fallback_used": True,
                "confidence": 0.0
            }
```

## Conclusion

Leveraging unstructured data with LLMs requires careful consideration of your specific use case, data characteristics, and performance requirements. RAG excels for dynamic, frequently updated information, while fine-tuning works best for domain-specific applications with consistent patterns.

Key takeaways:
- **Start with RAG** for most use cases - it's more flexible and cost-effective
- **Use fine-tuning** for specialized domains or high-volume applications
- **Implement hybrid approaches** for complex enterprise scenarios
- **Monitor performance** continuously and optimize based on real usage patterns
- **Prioritize security** and privacy from the beginning

The choice between RAG, fine-tuning, or hybrid approaches should be based on your specific requirements for accuracy, latency, cost, and maintenance complexity.

## Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Pinecone Vector Database Guide](https://docs.pinecone.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering)
- [PEFT Library for Efficient Fine-tuning](https://github.com/huggingface/peft)