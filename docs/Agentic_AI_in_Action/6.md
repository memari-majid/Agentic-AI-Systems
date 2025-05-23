## 6. State Management and Persistence with Checkpointers
For many agentic systems, especially those that are long-running, involve human-in-the-loop, or need to recover from interruptions, it's crucial to save and restore the agent's state. LangGraph provides checkpointers for this purpose.

### 6.1. Why Persistence?
- **Long-Running Tasks:** If an agent takes hours or days to complete a task, you don't want to lose all progress if the system restarts.
- **Human-in-the-Loop (HITL):** When an agent pauses for human input, its current state must be saved so it can be resumed later, potentially on a different server or after a delay.
- **Resilience:** Recover from crashes or unexpected interruptions.
- **Debugging and Analysis ("Time Travel"):** Load a past state to understand why an agent behaved a certain way or to explore alternative execution paths from a specific point.

### 6.2. LangGraph Checkpointers
A checkpointer in LangGraph automatically saves the state of your graph at specified points (typically after each node execution or as configured). When you run a graph compiled with a checkpointer, you provide a configurable dictionary, often including a `thread_id`. This `thread_id` acts as a key to save and load the conversation or task state.

LangGraph offers several checkpointer backends: 
- `MemorySaver`: Stores checkpoints in memory. Useful for testing and simple cases, but state is lost when the process ends. 
- `SqliteSaver`: Stores checkpoints in a SQLite database file. Good for local persistence. 
- `RedisSaver`: Stores checkpoints in a Redis instance. Suitable for distributed systems. 
- Other backends can be implemented for different databases or storage systems.

### 6.3. Using a Checkpointer (Conceptual Example with MemorySaver)
Let's adapt our basic research assistant graph from Section 4 to use `MemorySaver`.

```python
from langgraph.checkpoint.memory import MemorySaver
# Assume ResearchAgentState, planner_node, tool_executor_node, 
# route_after_planner, route_after_tool_executor are defined as in Section 4.
# Assume HumanMessage is imported: from langchain_core.messages import HumanMessage
# Assume StateGraph, END are imported: from langgraph.graph import StateGraph, END

# 1. Initialize a checkpointer
memory_saver = MemorySaver()

# 2. Create the graph (same structure as before)
# For this to run, planner_node and tool_executor_node and their dependencies need to be defined
# This is a conceptual illustration of adding a checkpointer.
# workflow_with_checkpoint = StateGraph(ResearchAgentState) 
# workflow_with_checkpoint.add_node("planner", planner_node)
# workflow_with_checkpoint.add_node("tool_executor", tool_executor_node)
# workflow_with_checkpoint.set_entry_point("planner")
# workflow_with_checkpoint.add_conditional_edges("planner", route_after_planner, {"tool_executor": "tool_executor", END: END})
# workflow_with_checkpoint.add_conditional_edges("tool_executor", route_after_tool_executor, {"planner": "planner", END: END})

# 3. Compile the graph with the checkpointer
# The checkpointer will save the state after each step for a given thread_id.
# research_app_persistent = workflow_with_checkpoint.compile(checkpointer=memory_saver)

# 4. Invoke the graph with a configurable thread_id
if __name__ == '__main__':
    # This section is conceptual and assumes research_app_persistent is a compiled graph
    # with a checkpointer, and that planner_node, etc. are fully defined elsewhere.
    pass
    # thread_id_1 = "my_research_task_123" # Unique ID for this conversation/task
    # initial_input_persistent = "What is LangGraph and how does it help with agent memory?"
    # initial_state_persistent = {
    #     "input_question": initial_input_persistent,
    #     "messages": [HumanMessage(content=initial_input_persistent)]
    # }

    # print(f"Starting persistent research for: '{initial_input_persistent}' with Thread ID: {thread_id_1}
")

    # First invocation - graph runs and state is saved under thread_id_1
    # for event in research_app_persistent.stream(initial_state_persistent, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10}):
    #     # print(event) # Print events to see flow
    #     pass # Simplified for brevity
    # final_state_run1 = research_app_persistent.invoke(initial_state_persistent, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10})
    # print(f"
--- Final Result (Run 1, Thread ID: {thread_id_1}) ---")
    # print(f" Summary: {final_state_run1.get('summary', 'N/A')}")

    # Imagine some time passes, or another user interacts with the same thread.
    # The graph can be invoked again with the same thread_id. It will resume from the last saved state.
    # For MemorySaver, this only works if the Python process is still running.
    # For persistent savers (SQLite, Redis), it works across process restarts.

    # follow_up_input = "Can you elaborate on its checkpointer system?"
    # # Note: We don't pass the full initial_state again for subsequent calls on the same thread.
    # # We just pass the new input that should be added to the message history.
    # # The checkpointer handles loading the previous state for this thread_id.
    # current_state_before_follow_up = research_app_persistent.get_state({"configurable": {"thread_id": thread_id_1}})
    # follow_up_messages = current_state_before_follow_up.values["messages"] + [HumanMessage(content=follow_up_input)]

    # follow_up_state_input = {
    #     "input_question": follow_up_input, # Update input question if relevant for planner
    #     "messages": [HumanMessage(content=follow_up_input)] # Only the new message to be appended
    # }

    # print(f"
--- Invoking with Follow-up (Thread ID: {thread_id_1}) ---")
    # # When invoking with a checkpointer and an existing thread_id,
    # # LangGraph appends the new messages to the history and continues.
    # for event in research_app_persistent.stream(follow_up_state_input, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10}):
    #     # print(event)
    #     pass
    # final_state_run2 = research_app_persistent.invoke(follow_up_state_input, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10})
    # print(f"
--- Final Result (Run 2, Thread ID: {thread_id_1}) ---")
    # print(f" Summary: {final_state_run2.get('summary', 'N/A')}")
    # print(f" Full message history for thread {thread_id_1}:")
    # final_thread_state = research_app_persistent.get_state({"configurable": {"thread_id": thread_id_1}})
    # for msg in final_thread_state.values["messages"]:
    #     print(f"  {msg.type}: {msg.content[:100]}...")
```
Key points for using checkpointers: 
- When compiling, pass the checkpointer instance. 
- When invoking (`.invoke()`, `.stream()`), pass a `configurable` dictionary containing a `thread_id`. This ID groups all states for a single, continuous interaction or task. 
- For follow-up interactions on the same `thread_id`, you usually just provide the new input (e.g., new messages). LangGraph, using the checkpointer, will load the prior state for that thread and continue.

### 6.4. Time Travel and State Inspection
Checkpointers also enable powerful debugging and analytical capabilities:

- `get_state(config)`: Retrieve the latest state for a given `thread_id`.
- `list_states(config)` (or similar, e.g., `list_checkpoints` for some savers): Get a history of all saved states (checkpoints) for a `thread_id`.
- `update_state(config, values)`: Manually update the state for a `thread_id`. Useful for correcting errors or injecting information.
- Invoking from a past checkpoint: Some checkpointers allow you to get a specific checkpoint and then invoke the graph from that point in the past, potentially with modified input, to explore different paths. This is invaluable for debugging complex agent behaviors or for A/B testing different responses from a certain state.

```python
# Conceptual: Time Travel / Inspection
# if __name__ == '__main__' and memory_saver: # Assuming research_app_persistent is compiled with memory_saver
#     thread_id_inspect = "my_research_task_123" # Use an existing thread_id

#     # Get the current state
#     current_state = research_app_persistent.get_state({"configurable": {"thread_id": thread_id_inspect}})
#     if current_state:
#         print(f"
--- Current State for Thread ID: {thread_id_inspect} ---")
#         # print(current_state.values) # The actual state dictionary
#         print(f"  Current messages: {len(current_state.values['messages'])} total")
#         print(f"  Next node was to be: {current_state.values.get('next_node')}")

    # List all checkpoints (MemorySaver might require specific methods or may not fully support listing all historical checkpoints easily without a persistent backend like SQLite)
    # For SQLiteSaver, it would be like: checkpoints = memory_saver.list(configurable={"thread_id": thread_id_inspect})
    # And then you could pick a checkpoint from the list to resume from.
    # Refer to specific checkpointer documentation for exact methods.
```
Using a persistent checkpointer like `SqliteSaver` is highly recommended for any agent that needs to maintain state beyond a single in-memory session. You would replace `MemorySaver()` with `SqliteSaver.from_conn_string(":memory:")` (for in-memory SQLite) or `SqliteSaver.from_conn_string("my_agent_db.sqlite")` (for a file-based database). 

## Production Data Architecture for Multi-Agent Systems

Beyond basic state persistence, production agentic systems require sophisticated data architecture that supports complex workflows, multi-agent coordination, audit trails, and high-throughput operations. This section covers comprehensive data patterns and architectures for building scalable, reliable agentic systems.

### Database Design Patterns for Agent Systems

**Agent Session and State Management Schema**:
Design database schemas that efficiently support complex agent workflows and state transitions.

```sql
-- Core agent session management
CREATE TABLE agent_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    agent_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active', -- active, paused, completed, failed
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    
    INDEX idx_user_sessions (user_id, status),
    INDEX idx_agent_type (agent_type, status),
    INDEX idx_session_priority (priority DESC, created_at),
    INDEX idx_session_expiry (expires_at)
);

-- Agent state snapshots for checkpointing
CREATE TABLE agent_states (
    state_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES agent_sessions(session_id),
    checkpoint_name VARCHAR(255),
    state_data JSONB NOT NULL,
    state_hash VARCHAR(64), -- For deduplication
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_current BOOLEAN DEFAULT false,
    
    INDEX idx_session_states (session_id, created_at),
    INDEX idx_current_state (session_id, is_current) WHERE is_current = true,
    INDEX idx_checkpoint_name (session_id, checkpoint_name),
    UNIQUE (session_id, state_hash) -- Prevent duplicate states
);

-- Agent conversation and message history
CREATE TABLE agent_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES agent_sessions(session_id),
    message_type VARCHAR(50) NOT NULL, -- human, ai, tool, system
    role VARCHAR(50),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    parent_message_id UUID REFERENCES agent_messages(message_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_session_messages (session_id, created_at),
    INDEX idx_message_tree (parent_message_id),
    INDEX idx_message_type (session_id, message_type)
);

-- Tool execution tracking
CREATE TABLE tool_executions (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES agent_sessions(session_id),
    tool_name VARCHAR(255) NOT NULL,
    tool_version VARCHAR(50),
    input_data JSONB NOT NULL,
    output_data JSONB,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, running, completed, failed
    error_message TEXT,
    execution_time_ms INTEGER,
    cost_estimate DECIMAL(10, 6),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    INDEX idx_session_tools (session_id, started_at),
    INDEX idx_tool_performance (tool_name, status, execution_time_ms),
    INDEX idx_tool_costs (tool_name, completed_at, cost_estimate)
);

-- Agent memory and knowledge base
CREATE TABLE agent_memory (
    memory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES agent_sessions(session_id),
    user_id VARCHAR(255), -- For cross-session memory
    memory_type VARCHAR(50) NOT NULL, -- episodic, semantic, procedural, working
    content_text TEXT NOT NULL,
    content_vector vector(1536), -- For semantic search
    importance_score FLOAT DEFAULT 0.0,
    access_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    
    INDEX idx_user_memory (user_id, memory_type, importance_score DESC),
    INDEX idx_session_memory (session_id, memory_type),
    INDEX idx_memory_access (last_accessed_at, access_count),
    INDEX idx_memory_expiry (expires_at) WHERE expires_at IS NOT NULL
);

-- Create vector index for semantic search (PostgreSQL with pgvector)
CREATE INDEX idx_memory_vector ON agent_memory USING ivfflat (content_vector vector_cosine_ops);
```

**Multi-Agent Coordination Schema**:
Support complex multi-agent workflows with proper coordination and communication tracking.

```sql
-- Agent workflow definitions
CREATE TABLE agent_workflows (
    workflow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_name VARCHAR(255) NOT NULL,
    workflow_version VARCHAR(50) NOT NULL,
    definition JSONB NOT NULL, -- LangGraph definition or similar
    is_active BOOLEAN DEFAULT true,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE (workflow_name, workflow_version),
    INDEX idx_active_workflows (workflow_name, is_active)
);

-- Multi-agent session coordination
CREATE TABLE agent_coordination (
    coordination_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES agent_workflows(workflow_id),
    coordinator_session_id UUID REFERENCES agent_sessions(session_id),
    status VARCHAR(50) NOT NULL DEFAULT 'initializing',
    current_step VARCHAR(255),
    step_sequence INTEGER DEFAULT 0,
    coordination_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_workflow_coordination (workflow_id, status),
    INDEX idx_coordinator_sessions (coordinator_session_id)
);

-- Agent participation in coordinated workflows
CREATE TABLE agent_participants (
    participant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coordination_id UUID NOT NULL REFERENCES agent_coordination(coordination_id),
    session_id UUID NOT NULL REFERENCES agent_sessions(session_id),
    agent_role VARCHAR(100) NOT NULL, -- coordinator, worker, delegator, specialist
    status VARCHAR(50) NOT NULL DEFAULT 'assigned',
    capabilities JSONB DEFAULT '[]',
    assignment_data JSONB DEFAULT '{}',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_coordination_participants (coordination_id, agent_role),
    INDEX idx_participant_status (session_id, status),
    UNIQUE (coordination_id, session_id)
);

-- Inter-agent communication
CREATE TABLE agent_communications (
    communication_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coordination_id UUID REFERENCES agent_coordination(coordination_id),
    sender_session_id UUID NOT NULL REFERENCES agent_sessions(session_id),
    receiver_session_id UUID REFERENCES agent_sessions(session_id), -- NULL for broadcast
    message_type VARCHAR(50) NOT NULL, -- task_assignment, status_update, result, error
    message_content JSONB NOT NULL,
    priority INTEGER DEFAULT 0,
    requires_response BOOLEAN DEFAULT false,
    response_timeout TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    
    INDEX idx_coordination_comms (coordination_id, created_at),
    INDEX idx_receiver_messages (receiver_session_id, processed_at),
    INDEX idx_pending_responses (requires_response, response_timeout) 
        WHERE requires_response = true AND processed_at IS NULL
);
```

### Event Sourcing for Agent Systems

**Event-Driven Architecture Implementation**:
Implement event sourcing to maintain complete audit trails and enable complex workflow patterns.

```python
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid
from datetime import datetime
import asyncio
import asyncpg

class EventType(Enum):
    SESSION_CREATED = "session_created"
    MESSAGE_RECEIVED = "message_received"
    TOOL_EXECUTED = "tool_executed"
    STATE_UPDATED = "state_updated"
    AGENT_ASSIGNED = "agent_assigned"
    WORKFLOW_STARTED = "workflow_started"
    COORDINATION_UPDATED = "coordination_updated"
    ERROR_OCCURRED = "error_occurred"

@dataclass
class AgentEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = None
    aggregate_id: str = None  # session_id, coordination_id, etc.
    aggregate_type: str = None  # session, coordination, workflow
    event_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

class EventStore:
    def __init__(self, db_connection_string: str):
        self.connection_string = db_connection_string
        self.event_handlers = {}
        
    async def initialize(self):
        """Initialize event store schema."""
        self.pool = await asyncpg.create_pool(self.connection_string)
        
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_events (
                    event_id UUID PRIMARY KEY,
                    event_type VARCHAR(100) NOT NULL,
                    aggregate_id VARCHAR(255) NOT NULL,
                    aggregate_type VARCHAR(100) NOT NULL,
                    event_data JSONB NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    timestamp TIMESTAMP NOT NULL,
                    version INTEGER NOT NULL,
                    correlation_id UUID,
                    causation_id UUID,
                    
                    INDEX idx_aggregate_events (aggregate_id, version),
                    INDEX idx_event_type (event_type, timestamp),
                    INDEX idx_correlation (correlation_id),
                    INDEX idx_timestamp (timestamp)
                );
                
                CREATE TABLE IF NOT EXISTS event_snapshots (
                    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    aggregate_id VARCHAR(255) NOT NULL,
                    aggregate_type VARCHAR(100) NOT NULL,
                    snapshot_data JSONB NOT NULL,
                    version INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    UNIQUE (aggregate_id, version),
                    INDEX idx_latest_snapshot (aggregate_id, version DESC)
                );
            """)
    
    async def append_event(self, event: AgentEvent) -> bool:
        """Append an event to the event store."""
        async with self.pool.acquire() as conn:
            try:
                await conn.execute("""
                    INSERT INTO agent_events (
                        event_id, event_type, aggregate_id, aggregate_type,
                        event_data, metadata, timestamp, version,
                        correlation_id, causation_id
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """, 
                    event.event_id,
                    event.event_type.value,
                    event.aggregate_id,
                    event.aggregate_type,
                    json.dumps(event.event_data),
                    json.dumps(event.metadata),
                    event.timestamp,
                    event.version,
                    event.correlation_id,
                    event.causation_id
                )
                
                # Trigger event handlers asynchronously
                await self._notify_handlers(event)
                return True
                
            except Exception as e:
                print(f"Failed to append event: {e}")
                return False
    
    async def get_events(self, 
                        aggregate_id: str, 
                        from_version: int = 0) -> List[AgentEvent]:
        """Retrieve events for an aggregate."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM agent_events 
                WHERE aggregate_id = $1 AND version > $2
                ORDER BY version ASC
            """, aggregate_id, from_version)
            
            events = []
            for row in rows:
                event = AgentEvent(
                    event_id=str(row['event_id']),
                    event_type=EventType(row['event_type']),
                    aggregate_id=row['aggregate_id'],
                    aggregate_type=row['aggregate_type'],
                    event_data=json.loads(row['event_data']),
                    metadata=json.loads(row['metadata']),
                    timestamp=row['timestamp'],
                    version=row['version'],
                    correlation_id=str(row['correlation_id']) if row['correlation_id'] else None,
                    causation_id=str(row['causation_id']) if row['causation_id'] else None
                )
                events.append(event)
            
            return events
    
    async def save_snapshot(self, 
                           aggregate_id: str, 
                           aggregate_type: str,
                           snapshot_data: Dict[str, Any], 
                           version: int):
        """Save a snapshot of aggregate state."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO event_snapshots 
                (aggregate_id, aggregate_type, snapshot_data, version)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (aggregate_id, version) 
                DO UPDATE SET snapshot_data = $3
            """, aggregate_id, aggregate_type, json.dumps(snapshot_data), version)
    
    async def get_latest_snapshot(self, aggregate_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest snapshot for an aggregate."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM event_snapshots 
                WHERE aggregate_id = $1 
                ORDER BY version DESC 
                LIMIT 1
            """, aggregate_id)
            
            if row:
                return {
                    'snapshot_data': json.loads(row['snapshot_data']),
                    'version': row['version']
                }
            return None
    
    def register_event_handler(self, event_type: EventType, handler):
        """Register an event handler for a specific event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def _notify_handlers(self, event: AgentEvent):
        """Notify registered event handlers."""
        handlers = self.event_handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                print(f"Event handler error: {e}")
```

### Workflow Orchestration and Data Flow

**Distributed Workflow Management**:
Implement sophisticated workflow orchestration that can handle complex multi-agent scenarios.

```python
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio
import json

class WorkflowStepType(Enum):
    AGENT_TASK = "agent_task"
    PARALLEL_EXECUTION = "parallel_execution"
    CONDITIONAL_BRANCH = "conditional_branch"
    HUMAN_APPROVAL = "human_approval"
    DATA_TRANSFORMATION = "data_transformation"
    EXTERNAL_API = "external_api"

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WAITING_APPROVAL = "waiting_approval"

@dataclass
class WorkflowStep:
    step_id: str
    step_name: str
    step_type: WorkflowStepType
    agent_requirements: Dict[str, Any]
    input_mappings: Dict[str, str]
    output_mappings: Dict[str, str]
    dependencies: List[str]
    timeout_seconds: int = 300
    retry_policy: Dict[str, Any] = None
    condition: Optional[str] = None  # For conditional steps

@dataclass
class WorkflowDefinition:
    workflow_id: str
    workflow_name: str
    version: str
    steps: List[WorkflowStep]
    global_timeout_seconds: int = 3600
    error_handling_policy: Dict[str, Any] = None

class WorkflowOrchestrator:
    def __init__(self, event_store: EventStore, agent_registry):
        self.event_store = event_store
        self.agent_registry = agent_registry
        self.active_workflows = {}
        self.step_executors = {
            WorkflowStepType.AGENT_TASK: self._execute_agent_task,
            WorkflowStepType.PARALLEL_EXECUTION: self._execute_parallel_steps,
            WorkflowStepType.CONDITIONAL_BRANCH: self._execute_conditional_branch,
            WorkflowStepType.HUMAN_APPROVAL: self._execute_human_approval,
            WorkflowStepType.DATA_TRANSFORMATION: self._execute_data_transformation,
            WorkflowStepType.EXTERNAL_API: self._execute_external_api
        }
    
    async def start_workflow(self, 
                           workflow_def: WorkflowDefinition,
                           initial_data: Dict[str, Any],
                           correlation_id: str) -> str:
        """Start a new workflow execution."""
        
        workflow_instance_id = str(uuid.uuid4())
        
        # Create workflow state
        workflow_state = {
            "workflow_id": workflow_instance_id,
            "definition": workflow_def,
            "status": "running",
            "current_step": None,
            "step_states": {},
            "global_data": initial_data.copy(),
            "step_outputs": {},
            "correlation_id": correlation_id,
            "created_at": datetime.utcnow().isoformat(),
            "started_at": datetime.utcnow().isoformat()
        }
        
        self.active_workflows[workflow_instance_id] = workflow_state
        
        # Emit workflow started event
        event = AgentEvent(
            event_type=EventType.WORKFLOW_STARTED,
            aggregate_id=workflow_instance_id,
            aggregate_type="workflow",
            event_data={
                "workflow_name": workflow_def.workflow_name,
                "version": workflow_def.version,
                "initial_data": initial_data
            },
            correlation_id=correlation_id
        )
        await self.event_store.append_event(event)
        
        # Start workflow execution
        asyncio.create_task(self._execute_workflow(workflow_instance_id))
        
        return workflow_instance_id
    
    async def _execute_workflow(self, workflow_instance_id: str):
        """Execute workflow steps according to dependencies and conditions."""
        
        workflow_state = self.active_workflows[workflow_instance_id]
        workflow_def = workflow_state["definition"]
        
        try:
            # Build dependency graph
            dependency_graph = self._build_dependency_graph(workflow_def.steps)
            
            # Execute steps in dependency order
            while not self._is_workflow_complete(workflow_state):
                ready_steps = self._get_ready_steps(workflow_state, dependency_graph)
                
                if not ready_steps:
                    break  # No more steps can be executed
                
                # Execute ready steps (potentially in parallel)
                tasks = []
                for step in ready_steps:
                    task = asyncio.create_task(
                        self._execute_step(workflow_instance_id, step)
                    )
                    tasks.append(task)
                
                # Wait for at least one step to complete
                if tasks:
                    done, pending = await asyncio.wait(
                        tasks, 
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    # Cancel pending tasks if needed based on error policy
                    for task in pending:
                        if not self._should_continue_on_error(workflow_state):
                            task.cancel()
            
            # Finalize workflow
            await self._finalize_workflow(workflow_instance_id)
            
        except Exception as e:
            await self._handle_workflow_error(workflow_instance_id, str(e))
    
    async def _execute_step(self, workflow_instance_id: str, step: WorkflowStep):
        """Execute a single workflow step."""
        
        workflow_state = self.active_workflows[workflow_instance_id]
        
        # Update step status
        workflow_state["step_states"][step.step_id] = {
            "status": StepStatus.RUNNING,
            "started_at": datetime.utcnow().isoformat()
        }
        
        try:
            # Prepare step input data
            step_input = self._prepare_step_input(workflow_state, step)
            
            # Execute step based on type
            executor = self.step_executors.get(step.step_type)
            if not executor:
                raise ValueError(f"No executor for step type: {step.step_type}")
            
            step_output = await executor(
                workflow_instance_id, 
                step, 
                step_input
            )
            
            # Store step output
            workflow_state["step_outputs"][step.step_id] = step_output
            workflow_state["step_states"][step.step_id].update({
                "status": StepStatus.COMPLETED,
                "completed_at": datetime.utcnow().isoformat(),
                "output": step_output
            })
            
            # Emit step completed event
            event = AgentEvent(
                event_type=EventType.STATE_UPDATED,
                aggregate_id=workflow_instance_id,
                aggregate_type="workflow",
                event_data={
                    "step_id": step.step_id,
                    "step_name": step.step_name,
                    "status": "completed",
                    "output": step_output
                },
                correlation_id=workflow_state["correlation_id"]
            )
            await self.event_store.append_event(event)
            
        except Exception as e:
            # Handle step failure
            workflow_state["step_states"][step.step_id].update({
                "status": StepStatus.FAILED,
                "failed_at": datetime.utcnow().isoformat(),
                "error": str(e)
            })
            
            # Emit step failed event
            event = AgentEvent(
                event_type=EventType.ERROR_OCCURRED,
                aggregate_id=workflow_instance_id,
                aggregate_type="workflow",
                event_data={
                    "step_id": step.step_id,
                    "step_name": step.step_name,
                    "error": str(e)
                },
                correlation_id=workflow_state["correlation_id"]
            )
            await self.event_store.append_event(event)
            
            # Handle retry if configured
            if step.retry_policy:
                await self._handle_step_retry(workflow_instance_id, step, e)
    
    async def _execute_agent_task(self, 
                                workflow_instance_id: str,
                                step: WorkflowStep, 
                                step_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent task step."""
        
        # Find suitable agent based on requirements
        agent = await self.agent_registry.find_agent(
            step.agent_requirements
        )
        
        if not agent:
            raise ValueError(f"No suitable agent found for step {step.step_id}")
        
        # Execute agent task
        result = await agent.execute_task(step_input)
        
        return {
            "agent_id": agent.agent_id,
            "agent_type": agent.agent_type,
            "result": result
        }
    
    def _build_dependency_graph(self, steps: List[WorkflowStep]) -> Dict[str, List[str]]:
        """Build a dependency graph from workflow steps."""
        graph = {}
        for step in steps:
            graph[step.step_id] = step.dependencies.copy()
        return graph
    
    def _get_ready_steps(self, workflow_state: Dict[str, Any], 
                        dependency_graph: Dict[str, List[str]]) -> List[WorkflowStep]:
        """Get steps that are ready to execute."""
        ready_steps = []
        
        for step in workflow_state["definition"].steps:
            step_id = step.step_id
            step_state = workflow_state["step_states"].get(step_id, {})
            
            # Skip if already completed or running
            if step_state.get("status") in [StepStatus.COMPLETED, StepStatus.RUNNING]:
                continue
            
            # Check if all dependencies are completed
            dependencies = dependency_graph.get(step_id, [])
            dependencies_met = all(
                workflow_state["step_states"].get(dep_id, {}).get("status") == StepStatus.COMPLETED
                for dep_id in dependencies
            )
            
            if dependencies_met:
                # Check condition if present
                if step.condition:
                    if self._evaluate_condition(workflow_state, step.condition):
                        ready_steps.append(step)
                else:
                    ready_steps.append(step)
        
        return ready_steps
```

### Data Consistency and Transaction Management

**Distributed Transaction Coordination**:
Implement patterns for maintaining data consistency across multiple agents and systems.

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import uuid
from datetime import datetime, timedelta

class TransactionStatus(Enum):
    PENDING = "pending"
    COMMITTED = "committed"
    ABORTED = "aborted"
    PREPARING = "preparing"
    PREPARED = "prepared"

@dataclass
class TransactionOperation:
    operation_id: str
    participant_id: str
    operation_type: str
    operation_data: Dict[str, Any]
    compensation_data: Optional[Dict[str, Any]] = None

class DistributedTransactionManager:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.active_transactions = {}
        self.participants = {}
        
    async def begin_transaction(self, 
                               operations: List[TransactionOperation],
                               transaction_id: Optional[str] = None) -> str:
        """Begin a distributed transaction using saga pattern."""
        
        if not transaction_id:
            transaction_id = str(uuid.uuid4())
        
        transaction_state = {
            "transaction_id": transaction_id,
            "status": TransactionStatus.PENDING,
            "operations": operations,
            "completed_operations": [],
            "failed_operations": [],
            "created_at": datetime.utcnow(),
            "timeout_at": datetime.utcnow() + timedelta(minutes=30)
        }
        
        self.active_transactions[transaction_id] = transaction_state
        
        # Execute saga
        asyncio.create_task(self._execute_saga(transaction_id))
        
        return transaction_id
    
    async def _execute_saga(self, transaction_id: str):
        """Execute saga pattern for distributed transaction."""
        
        transaction_state = self.active_transactions[transaction_id]
        operations = transaction_state["operations"]
        
        try:
            # Forward execution phase
            for operation in operations:
                success = await self._execute_operation(transaction_id, operation)
                
                if success:
                    transaction_state["completed_operations"].append(operation)
                else:
                    transaction_state["failed_operations"].append(operation)
                    # Start compensation
                    await self._compensate_transaction(transaction_id)
                    return
            
            # All operations succeeded
            transaction_state["status"] = TransactionStatus.COMMITTED
            await self._emit_transaction_event(
                transaction_id, 
                "transaction_committed"
            )
            
        except Exception as e:
            transaction_state["failed_operations"].extend(
                [op for op in operations 
                 if op not in transaction_state["completed_operations"]]
            )
            await self._compensate_transaction(transaction_id)
    
    async def _execute_operation(self, 
                                transaction_id: str,
                                operation: TransactionOperation) -> bool:
        """Execute a single operation in the transaction."""
        
        try:
            participant = self.participants.get(operation.participant_id)
            if not participant:
                raise ValueError(f"Unknown participant: {operation.participant_id}")
            
            # Execute operation
            result = await participant.execute_operation(
                operation.operation_type,
                operation.operation_data
            )
            
            # Log successful operation
            await self._emit_transaction_event(
                transaction_id,
                "operation_completed",
                {
                    "operation_id": operation.operation_id,
                    "participant_id": operation.participant_id,
                    "result": result
                }
            )
            
            return True
            
        except Exception as e:
            # Log failed operation
            await self._emit_transaction_event(
                transaction_id,
                "operation_failed",
                {
                    "operation_id": operation.operation_id,
                    "participant_id": operation.participant_id,
                    "error": str(e)
                }
            )
            
            return False
    
    async def _compensate_transaction(self, transaction_id: str):
        """Execute compensation operations for failed transaction."""
        
        transaction_state = self.active_transactions[transaction_id]
        transaction_state["status"] = TransactionStatus.ABORTED
        
        # Execute compensations in reverse order
        for operation in reversed(transaction_state["completed_operations"]):
            if operation.compensation_data:
                try:
                    participant = self.participants.get(operation.participant_id)
                    await participant.compensate_operation(
                        operation.operation_id,
                        operation.compensation_data
                    )
                    
                    await self._emit_transaction_event(
                        transaction_id,
                        "compensation_completed",
                        {"operation_id": operation.operation_id}
                    )
                    
                except Exception as e:
                    await self._emit_transaction_event(
                        transaction_id,
                        "compensation_failed",
                        {
                            "operation_id": operation.operation_id,
                            "error": str(e)
                        }
                    )
        
        await self._emit_transaction_event(
            transaction_id,
            "transaction_aborted"
        )
    
    async def _emit_transaction_event(self, 
                                    transaction_id: str,
                                    event_type: str,
                                    event_data: Dict[str, Any] = None):
        """Emit transaction-related events."""
        
        event = AgentEvent(
            event_type=EventType.STATE_UPDATED,  # Or create specific transaction events
            aggregate_id=transaction_id,
            aggregate_type="transaction",
            event_data={
                "event_type": event_type,
                **(event_data or {})
            }
        )
        
        await self.event_store.append_event(event)
```

This production data architecture framework provides the foundation for building robust, scalable multi-agent systems that can handle complex workflows, maintain data consistency, and provide comprehensive audit trails. The combination of sophisticated database design, event sourcing, workflow orchestration, and distributed transaction management ensures reliable operation at enterprise scale.

⏱️ **Estimated reading time: 15 minutes**