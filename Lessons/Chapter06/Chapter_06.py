#!/usr/bin/env python3
# Chapter 6 – Exploring the Coordinator, Worker, and Delegator Approach

# Required dependencies:
# pip install -U crewai langchain-openai

import os
from textwrap import dedent
from typing import Dict, List, Any

class CWDTravelPlanner:
    """
    Implements the Coordinator, Worker, Delegator (CWD) pattern for a travel planning system.
    
    This class demonstrates how to structure agents in three key roles:
    - Coordinator: Understands user requests and creates high-level plans
    - Workers: Specialized agents that perform specific tasks
    - Delegator: Assigns tasks to appropriate workers and synthesizes results
    """
    
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """
        Initialize the CWD Travel Planner system.
        
        Args:
            api_key: OpenAI API key
            model: Model to use for LLM
        """
        try:
            from crewai import Agent, Task, Crew, Process
            from langchain_openai import ChatOpenAI
            
            # Set up API key
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                
            # Initialize LLM
            self.llm = ChatOpenAI(model=model)
            
            # Create tools
            self.tools = self._create_tools()
            
            # Create agents
            self._create_agents()
            
        except ImportError:
            print("Required modules not found. Please install crewai and langchain-openai.")
    
    def _create_tools(self):
        """Create and return tools for the agents."""
        try:
            from crewai.tools import tool
            
            @tool("Search for available flights between cities")
            def search_flights(origin: str, destination: str, date: str) -> Dict:
                """
                Search for available flights between cities.
                
                Args:
                    origin: Departure city
                    destination: Arrival city
                    date: Travel date (YYYY-MM-DD)
                
                Returns:
                    Dictionary containing flight options and prices
                """
                # Emulate JSON data from an API
                return {
                    "flights": [
                        {"airline": "Air France", "price": 850, "departure": "New York (JFK)", "arrival": "Paris (CDG)", "duration": "7h 30m", "departure_time": "10:30 AM", "arrival_time": "11:00 PM"},
                        {"airline": "Delta Airlines", "price": 780, "departure": "New York (JFK)", "arrival": "Paris (CDG)", "duration": "7h 45m", "departure_time": "5:30 PM", "arrival_time": "6:15 AM"},
                        {"airline": "United Airlines", "price": 920, "departure": "New York (EWR)", "arrival": "Paris (CDG)", "duration": "7h 55m", "departure_time": "8:45 PM", "arrival_time": "9:40 AM"}
                    ]}             

            @tool("Find available hotels in a location") 
            def find_hotels(location: str, check_in: str, check_out: str) -> Dict:
                """
                Search for available hotels in a location.
                
                Args:
                    location: City name
                    check_in: Check-in date (YYYY-MM-DD)
                    check_out: Check-out date (YYYY-MM-DD)
                
                Returns:
                    Dictionary containing hotel options and prices
                """
                # Emulate JSON data from an API
                return {
                    "hotels": [
                        {"name": "Paris Marriott Champs Elysees", "price": 450, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.5, "location": "Central Paris", "amenities": ["Spa", "Restaurant", "Room Service"]},
                        {"name": "Citadines Saint-Germain-des-Prés", "price": 320, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.2, "location": "Saint-Germain", "amenities": ["Kitchenette", "Laundry", "Wifi"]},
                        {"name": "Ibis Paris Eiffel Tower", "price": 380, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.0, "location": "Near Eiffel Tower", "amenities": ["Restaurant", "Bar", "Wifi"]}
                    ]}

            @tool("Find available activities in a location")
            def find_activities(location: str, date: str, preferences: str) -> Dict:
                """
                Find available activities in a location.
                
                Args:
                    location: City name
                    date: Activity date (YYYY-MM-DD)
                    preferences: Activity preferences/requirements
                    
                Returns:
                    Dictionary containing activity options
                """
                # Implement actual activity search logic here
                return {
                    "activities": [
                        {"name": "Eiffel Tower Skip-the-Line", "description": "Priority access to the Eiffel Tower with guided tour of 1st and 2nd floors", "price": 65, "duration": "2 hours", "start_time": "10:00 AM", "meeting_point": "Eiffel Tower South Entrance"},
                        {"name": "Louvre Museum Guided Tour", "description": "Expert-guided tour of the Louvre's masterpieces including Mona Lisa", "price": 85, "duration": "3 hours", "start_time": "2:00 PM", "meeting_point": "Louvre Pyramid"},
                        {"name": "Seine River Dinner Cruise", "description": "Evening cruise along the Seine with 3-course French dinner and wine", "price": 120, "duration": "2.5 hours", "start_time": "7:30 PM", "meeting_point": "Port de la Bourdonnais"}
                    ]}

            @tool("Find local transportation options")
            def find_transportation(location: str, origin: str, destination: str) -> Dict:
                """
                Find local transportation options between locations.
                
                Args:
                    location: City name
                    origin: Starting point (e.g., "Airport", "Hotel", "Eiffel Tower")
                    destination: End point (e.g., "City Center", "Museum", "Restaurant")
                
                Returns:
                    Dictionary containing transportation options
                """
                # Return a simple JSON with transportation options
                return {
                    "options": [
                        { "type": "Metro", "cost": 1.90, "duration": "25 minutes", "frequency": "Every 5 minutes", "route": "Line 1 to Châtelet, then Line 4 to destination", "pros": "Fast, avoids traffic", "cons": "Can be crowded during peak hours"},
                        { "type": "Taxi", "cost": 22.50, "duration": "20 minutes", "frequency": "On demand", "route": "Direct", "pros": "Door-to-door service, comfortable", "cons": "More expensive, subject to traffic"},
                        { "type": "Bus", "cost": 1.90, "duration": "35 minutes", "frequency": "Every 10 minutes", "route": "Route 42 direct to destination", "pros": "Scenic route, above ground", "cons": "Slower than metro, subject to traffic"},
                        { "type": "Walking", "cost": 0, "duration": "45 minutes", "frequency": "Anytime", "route": "Through city center", "pros": "Free, healthy, scenic", "cons": "Takes longer, weather dependent"}
                    ],
                    "passes": [
                        { "name": "Day Pass", "cost": 7.50, "valid_for": "Unlimited travel for 24 hours", "recommended_if": "Making more than 4 trips in a day" },
                        { "name": "Paris Visite",  "cost": 12.00, "valid_for": "Unlimited travel for 1 day, includes discounts to attractions", "recommended_if": "Planning to visit multiple tourist sites" }
                    ]
                }
                
            return {
                "search_flights": search_flights,
                "find_hotels": find_hotels,
                "find_activities": find_activities,
                "find_transportation": find_transportation
            }
            
        except ImportError:
            print("CrewAI not installed. Run 'pip install crewai' to use these tools.")
            return {}
    
    def _create_agents(self):
        """Create the coordinator, worker, and delegator agents."""
        try:
            from crewai import Agent
            
            # Create worker agents
            self.flight_booking_worker = Agent(
                role="Flight Booking Specialist",
                goal="Find and book the optimal flights for the traveler",
                backstory="""You are an experienced flight booking specialist with extensive knowledge of airlines, 
                routes, and pricing strategies. You excel at finding the best flight options balancing cost, 
                convenience, and comfort according to the traveler's preferences.""",
                verbose=True,
                allow_delegation=False,
                tools=[self.tools["search_flights"]],
                llm=self.llm,
                max_iter=1,
                max_retry_limit=3
            )
            
            self.hotel_booking_worker = Agent(
                role="Hotel Accommodation Expert",
                goal="Secure the ideal hotel accommodations for the traveler",
                backstory="""You have worked in the hospitality industry for over a decade and have deep knowledge 
                of hotel chains, boutique accommodations, and local lodging options worldwide. You're skilled at 
                matching travelers with accommodations that meet their budget, location preferences, and amenity requirements.""",
                verbose=True,
                allow_delegation=False,
                tools=[self.tools["find_hotels"]],
                llm=self.llm,
                max_iter=1,
                max_retry_limit=3
            )
            
            self.activity_planning_worker = Agent(
                role="Activities and Excursions Planner",
                goal="Curate personalized activities and experiences for the traveler",
                backstory="""You're a well-traveled activities coordinator with insider knowledge of attractions, 
                tours, and unique experiences across numerous destinations. You're passionate about creating 
                memorable itineraries that align with travelers' interests, whether they seek adventure, culture, 
                relaxation, or culinary experiences.""",
                verbose=True,
                allow_delegation=False,
                tools=[self.tools["find_activities"]],
                llm=self.llm,
                max_iter=1,
                max_retry_limit=3
            )
            
            self.transportation_worker = Agent(
                role="Local Transportation Coordinator",
                goal="Arrange efficient and convenient local transportation",
                backstory="""You specialize in local transportation logistics across global destinations. Your expertise 
                covers public transit systems, private transfers, rental services, and navigation, ensuring travelers 
                can move smoothly between destinations and activities.""",
                verbose=True,
                allow_delegation=False,
                tools=[self.tools["find_transportation"]],
                llm=self.llm,
                max_iter=1,
                max_retry_limit=3
            )
            
            # Create coordinator agent
            self.coordinator_agent = Agent(
                role="Coordinator Agent",
                goal="Ensure cohesive travel plans and maintain high customer satisfaction",
                backstory="""A seasoned travel industry veteran with 15 years of experience in luxury travel planning 
                and project management. Known for orchestrating seamless multi-destination trips for high-profile clients 
                and managing complex itineraries across different time zones and cultures.""",
                verbose=False,
                llm=self.llm,
                max_iter=1,
                max_retry_limit=3
            )
            
            # Create delegator agent
            self.delegator_agent = Agent(
                role="Delegator Agent",
                goal="Efficiently assign tasks to specialists and compile results into a comprehensive travel plan",
                backstory="""You are a skilled project manager with expertise in the travel industry. Your role is to interpret 
                the travel plan, delegate specific tasks to the appropriate specialist workers, and compile their outputs into a 
                comprehensive, cohesive travel package. You excel at understanding which specialist is best suited for each 
                component of the travel plan.""",
                verbose=False,
                llm=self.llm,
                max_iter=1,
                max_retry_limit=3
            )
            
        except ImportError as e:
            print(f"Error creating agents: {e}")
    
    def _create_worker_tasks(self):
        """Create tasks for worker agents."""
        try:
            from crewai import Task
            
            flight_search_task = Task(
                description="""
                Use the search_flights tool to find flight options from origin to destination.
                Review the returned JSON data and recommend the best option based on the traveler's priorities, if any.
                
                Compare the available options and recommended choice best meets their needs.
                """,
                agent=self.flight_booking_worker,
                expected_output="A flight itinerary for booking based on the traveler's preferences."
            )
            
            hotel_search_task = Task(
                description="""
                Use the find_hotels tool to search for accommodations in the destination.
                Review the returned JSON data and recommend the best option considering budget.
                
                Explain why your recommended choice is the best match for this traveler.
                """,
                agent=self.hotel_booking_worker,
                expected_output="A hotel recommendation based on the traveler's preferences and budget."
            )
            
            activity_planning_task = Task(
                description="""
                Use the find_activities tool to identify options in the destination for each day of the of the entire trip duration.
                The traveler's interests are: {activity_interests} with a {activity_pace} pace preference.
                
                Create a day-by-day plan using the returned JSON data, ensuring activities flow logically and match the traveler's interests.
                """,
                agent=self.activity_planning_worker,
                expected_output="A day-by-day activity plan that matches the traveler's interests and pace preferences."
            )
            
            transportation_planning_task = Task(
                description="""
                Use the find_transportation tool to identify options at the destination for:
                1. Airport to hotel transfer
                2. Transportation between daily activities
                3. Hotel to airport transfer
                
                Consider the traveler's preferences where possible.
                
                Based on the returned JSON data, recommend the best transportation options for each segment of their trip.
                """,
                agent=self.transportation_worker,
                expected_output="A transportation plan covering all necessary transfers during the trip."
            )
            
            return {
                "flight_search": flight_search_task,
                "hotel_search": hotel_search_task,
                "activity_planning": activity_planning_task,
                "transportation_planning": transportation_planning_task
            }
            
        except Exception as e:
            print(f"Error creating worker tasks: {e}")
            return {}
    
    def _coordinate_request(self, traveler_request):
        """Use the coordinator agent to process the request and create a plan."""
        try:
            from crewai import Task, Crew, Process
            
            coordinator_to_delegator_task = Task(
                description=dedent(f"""\
                As the Coordinator Agent, you've received a travel planning request.
                
                Traveler request:
                {traveler_request}
                
                Create a clear, concise travel planning steps for this trip. Only plan
                for the things requested by the traveler, DO NOT assume or add things not requested. Provide a 
                short overview, followed by the steps required for flight booking, hotel booking, activities,
                and local transportation.
                
                Your output should be a step-by-step plan along with preference details that the Delegator Agent 
                can use to effectively assign tasks to the specialist workers. Do not provide any summary or mention 
                "Delegator" or "coordinator".
                """),
                expected_output="A detailed step-by-step travel plan for the delegator agent",
                agent=self.coordinator_agent
            )
            
            # Execute the coordinator's initial planning task
            coordinator_crew = Crew(
                agents=[self.coordinator_agent],
                tasks=[coordinator_to_delegator_task],
                verbose=False,
                process=Process.sequential
            )
            
            coordinator_plan = coordinator_crew.kickoff(inputs={'traveler_request': traveler_request})
            print("\n=== Coordinator Planning Complete ===\n")
            return coordinator_plan
            
        except Exception as e:
            print(f"Error in coordination: {e}")
            return "Error: Unable to coordinate request"
    
    def _delegate_tasks(self, coordinator_plan, traveler_request):
        """Use the delegator agent to assign tasks to workers and compile results."""
        try:
            from crewai import Task, Crew, Process
            
            # Create a delegator task
            delegator_task = Task(
                description=dedent(f"""\
                As the Delegator Agent, you're responsible for creating a comprehensive travel package based on the coordinator's plan.
                
                Original traveler request:
                {traveler_request}
                
                Coordinator's plan:
                {coordinator_plan}
                
                Your job is to:
                1. Analyze the plan and identify which specialists should handle each component
                2. Delegate appropriately to flight, hotel, activity, and transportation specialists
                3. Compile their outputs into a cohesive travel package
                4. Ensure all traveler preferences are addressed
                
                Format your final output as a comprehensive travel itinerary that could be presented to the customer.
                """),
                expected_output="A complete travel package ready for the customer",
                agent=self.delegator_agent
            )
            
            # Execute the delegator task
            delegator_crew = Crew(
                agents=[
                    self.delegator_agent, 
                    self.flight_booking_worker,
                    self.hotel_booking_worker,
                    self.activity_planning_worker,
                    self.transportation_worker
                ],
                tasks=[delegator_task],
                verbose=False,
                process=Process.sequential
            )
            
            final_travel_plan = delegator_crew.kickoff(
                inputs={
                    'traveler_request': traveler_request,
                    'coordinator_plan': coordinator_plan
                }
            )
            
            print("\n=== Delegation Complete ===\n")
            return final_travel_plan
            
        except Exception as e:
            print(f"Error in delegation: {e}")
            return "Error: Unable to delegate tasks"
    
    def plan_travel(self, traveler_request):
        """
        Process a travel request using the CWD pattern.
        
        Args:
            traveler_request: String containing the traveler's requirements
            
        Returns:
            A comprehensive travel plan
        """
        # 1. Coordinator creates a plan
        coordinator_plan = self._coordinate_request(traveler_request)
        
        # 2. Delegator assigns tasks and compiles results
        final_travel_plan = self._delegate_tasks(coordinator_plan, traveler_request)
        
        return final_travel_plan


# Advanced Multi-Agent System Implementation
from enum import Enum
from typing import TypedDict, List, Dict, Any, Optional, Set, Tuple
import time


class AgentRole(str, Enum):
    """Roles for the advanced multi-agent system."""
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    CRITIC = "critic"
    EXECUTOR = "executor"
    EVALUATOR = "evaluator"


class AgentMessage(TypedDict):
    """Structured message format for agent communication."""
    from_agent: AgentRole
    to_agent: Optional[AgentRole]  # None means broadcast to all
    content: str
    timestamp: float
    msg_type: str  # e.g., "request", "response", "critique", "plan", etc.
    iteration: int


class MultiAgentState(TypedDict, total=False):
    """State representation for advanced multi-agent system."""
    task: str
    messages: List[AgentMessage]
    artifacts: Dict[str, Any]
    current_agent: AgentRole
    current_phase: str
    convergence_score: float
    solution: Optional[str]
    evaluation: Optional[Dict[str, float]]
    max_iterations: int
    current_iteration: int


class AdvancedMultiAgentSystem:
    """
    Implements an advanced multi-agent collaboration system beyond basic CWD.
    
    Features:
    - Structured communication protocols
    - Feedback loops and critic roles
    - Multi-dimensional specialization
    - Convergence and consensus mechanisms
    - Dynamic routing based on state
    """
    
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """Initialize the advanced multi-agent system."""
        try:
            from langchain_openai import ChatOpenAI
            import os
            
            # Set up API key
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                
            # Initialize LLM
            self.llm = ChatOpenAI(model=model)
            
        except ImportError:
            print("Required modules not found. Please install langchain-openai.")
    
    def coordinator_agent(self, state: MultiAgentState) -> MultiAgentState:
        """
        Coordinator agent that manages the collaboration process.
        - Assigns tasks to specialized agents
        - Tracks progress and ensures convergence
        - Makes final decisions when needed
        """
        current_iteration = state.get("current_iteration", 0)
        max_iterations = state.get("max_iterations", 5)
        messages = state.get("messages", [])
        artifacts = state.get("artifacts", {})
        
        # First iteration: initialize the task
        if current_iteration == 0:
            task = state.get("task", "")
            print(f"\n🧠 Coordinator: Initializing task '{task}'")
            
            # Create initial plan
            initial_plan = "1. Research phase: Gather information\n2. Analysis phase: Evaluate options\n3. Planning phase: Develop solution\n4. Execution phase: Implement solution"
            artifacts["plan"] = initial_plan
            
            # Send initial message to researcher
            messages.append({
                "from_agent": AgentRole.COORDINATOR,
                "to_agent": AgentRole.RESEARCHER,
                "content": f"Please research the following task: {task}",
                "timestamp": time.time(),
                "msg_type": "request",
                "iteration": current_iteration
            })
            
            # Update state
            state["messages"] = messages
            state["artifacts"] = artifacts
            state["current_iteration"] = current_iteration + 1
            state["current_agent"] = AgentRole.RESEARCHER
            state["current_phase"] = "research"
            
        # Middle iterations: manage the process
        elif current_iteration < max_iterations - 1:
            print(f"\n🧠 Coordinator: Managing iteration {current_iteration}")
            
            # Analyze recent messages
            recent_messages = [m for m in messages if m["iteration"] == current_iteration - 1]
            
            # Determine next phase based on iteration and task progress
            phase = current_iteration % 4
            
            if phase == 0:  # Research phase
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.RESEARCHER,
                    "content": "Please continue researching and provide additional information.",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.RESEARCHER
                state["current_phase"] = "research"
            
            elif phase == 1:  # Critique phase
                # Get the latest research
                research = next((m["content"] for m in reversed(messages) 
                               if m["from_agent"] == AgentRole.RESEARCHER 
                               and m["msg_type"] == "response"), "")
                
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.CRITIC,
                    "content": f"Please critique this research and suggest improvements:\n\n{research}",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.CRITIC
                state["current_phase"] = "critique"
            
            elif phase == 2:  # Execution planning phase
                # Get the latest critique
                critique = next((m["content"] for m in reversed(messages) 
                               if m["from_agent"] == AgentRole.CRITIC 
                               and m["msg_type"] == "response"), "")
                
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.EXECUTOR,
                    "content": f"Based on our research and critique, please develop a solution:\n\n{critique}",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.EXECUTOR
                state["current_phase"] = "execution"
                
            else:  # Evaluation phase
                # Early evaluation to gauge progress
                execution_results = [m["content"] for m in messages 
                                   if m["from_agent"] == AgentRole.EXECUTOR 
                                   and m["msg_type"] == "response"]
                
                if execution_results:
                    latest_execution = execution_results[-1]
                    messages.append({
                        "from_agent": AgentRole.COORDINATOR,
                        "to_agent": AgentRole.EVALUATOR,
                        "content": f"Please evaluate this solution draft:\n\n{latest_execution}",
                        "timestamp": time.time(),
                        "msg_type": "request",
                        "iteration": current_iteration
                    })
                    state["current_agent"] = AgentRole.EVALUATOR
                    state["current_phase"] = "evaluation"
                else:
                    # Fallback if we don't have execution results yet
                    messages.append({
                        "from_agent": AgentRole.COORDINATOR,
                        "to_agent": AgentRole.RESEARCHER,
                        "content": "Let's explore the problem space further. Please provide more detailed research.",
                        "timestamp": time.time(),
                        "msg_type": "request",
                        "iteration": current_iteration
                    })
                    state["current_agent"] = AgentRole.RESEARCHER
                    state["current_phase"] = "research"
        
            # Update state
            state["messages"] = messages
            state["current_iteration"] = current_iteration + 1
            
        # Final iteration: conclude the task
        else:
            print(f"\n🧠 Coordinator: Finalizing task at iteration {current_iteration}")
            
            # Collect all execution results
            execution_results = [m["content"] for m in messages 
                                if m["from_agent"] == AgentRole.EXECUTOR 
                                and m["msg_type"] == "response"]
            
            # Create final solution
            solution = "FINAL SOLUTION:\n\n"
            solution += "\n".join(execution_results[-2:]) if execution_results else "No solution developed."
            
            # Request evaluation
            messages.append({
                "from_agent": AgentRole.COORDINATOR,
                "to_agent": AgentRole.EVALUATOR,
                "content": f"Please evaluate this final solution:\n\n{solution}",
                "timestamp": time.time(),
                "msg_type": "request",
                "iteration": current_iteration
            })
            
            # Store the solution
            state["solution"] = solution
            state["messages"] = messages
            state["current_iteration"] = current_iteration + 1
            state["current_agent"] = AgentRole.EVALUATOR
            state["current_phase"] = "final_evaluation"
        
        return state
    
    def researcher_agent(self, state: MultiAgentState) -> MultiAgentState:
        """
        Researcher agent that gathers and synthesizes information.
        - Collects relevant data
        - Organizes information
        - Identifies knowledge gaps
        """
        # Get current state
        task = state.get("task", "")
        messages = state.get("messages", [])
        current_iteration = state.get("current_iteration", 0)
        
        # Get the latest request from the coordinator
        request = next((msg["content"] for msg in reversed(messages) 
                       if msg["to_agent"] == AgentRole.RESEARCHER 
                       and msg["msg_type"] == "request"), "")
        
        print(f"\n📚 Researcher: Working on iteration {current_iteration}")
        
        # In a real implementation, would use the LLM here to generate research
        # For demonstration, we'll use a template
        if current_iteration <= 1:
            research = f"Initial research on '{task}':\n\n"
            research += "1. Key aspects of the problem:\n"
            research += "   - The problem involves multiple stakeholders\n"
            research += "   - There are technical and non-technical components\n"
            research += "   - Time constraints will affect the solution\n\n"
            research += "2. Potential approaches:\n"
            research += "   - Approach A: Quick implementation, moderate results\n"
            research += "   - Approach B: Longer timeline, more comprehensive\n"
            research += "   - Approach C: Hybrid solution with phased delivery"
        else:
            # Later iterations add more detailed information
            research = f"Additional research on '{task}':\n\n"
            research += "3. Detailed analysis of approaches:\n"
            research += "   - Approach A strengths: faster implementation, lower cost\n"
            research += "   - Approach B strengths: more complete solution, better long-term results\n"
            research += "   - Approach C strengths: balances time constraints with solution quality\n\n"
            research += "4. Related case studies:\n"
            research += "   - Case Study X demonstrated a 40% improvement using a hybrid approach\n"
            research += "   - Case Study Y showed technical challenges with rapid implementation\n\n"
            research += "5. Recommended approach based on research: Approach C (Hybrid solution)"
        
        # Send response back to coordinator
        messages.append({
            "from_agent": AgentRole.RESEARCHER,
            "to_agent": AgentRole.COORDINATOR,
            "content": research,
            "timestamp": time.time(),
            "msg_type": "response",
            "iteration": current_iteration - 1
        })
        
        # Update state
        state["messages"] = messages
        state["current_agent"] = AgentRole.COORDINATOR
        
        return state
    
    def critic_agent(self, state: MultiAgentState) -> MultiAgentState:
        """
        Critic agent that identifies weaknesses and suggests improvements.
        - Analyzes proposals for flaws
        - Suggests alternative approaches
        - Provides constructive feedback
        """
        # Get current state
        messages = state.get("messages", [])
        current_iteration = state.get("current_iteration", 0)
        
        # Get the latest request from the coordinator
        request = next((msg["content"] for msg in reversed(messages) 
                       if msg["to_agent"] == AgentRole.CRITIC 
                       and msg["msg_type"] == "request"), "")
        
        print(f"\n🔍 Critic: Working on iteration {current_iteration}")
        
        # In a real implementation, would use the LLM here to generate critique
        # For demonstration, we'll use a template
        critique = "Critique of the research:\n\n"
        critique += "Strengths:\n"
        critique += "- Good identification of multiple approaches\n"
        critique += "- Consideration of stakeholder needs\n"
        critique += "- Evidence-based recommendations\n\n"
        
        critique += "Weaknesses:\n"
        critique += "- Insufficient detail on implementation steps\n"
        critique += "- Limited consideration of resource constraints\n"
        critique += "- Missing risk assessment for each approach\n\n"
        
        critique += "Suggestions for improvement:\n"
        critique += "1. Develop a more detailed implementation plan for the hybrid approach\n"
        critique += "2. Add a section on required resources and potential constraints\n"
        critique += "3. Include a risk assessment and mitigation strategies\n"
        critique += "4. Consider a phased implementation with clear milestones\n\n"
        
        critique += "Recommended focus: Develop a phased implementation plan with risk mitigation strategies."
        
        # Send response back to coordinator
        messages.append({
            "from_agent": AgentRole.CRITIC,
            "to_agent": AgentRole.COORDINATOR,
            "content": critique,
            "timestamp": time.time(),
            "msg_type": "response",
            "iteration": current_iteration - 1
        })
        
        # Update state
        state["messages"] = messages
        state["current_agent"] = AgentRole.COORDINATOR
        
        return state
    
    def executor_agent(self, state: MultiAgentState) -> MultiAgentState:
        """
        Executor agent that implements solutions.
        - Turns plans into actionable steps
        - Identifies implementation details
        - Provides concrete solutions
        """
        # Get current state
        messages = state.get("messages", [])
        current_iteration = state.get("current_iteration", 0)
        task = state.get("task", "")
        
        # Get the latest request from the coordinator
        request = next((msg["content"] for msg in reversed(messages) 
                       if msg["to_agent"] == AgentRole.EXECUTOR 
                       and msg["msg_type"] == "request"), "")
        
        print(f"\n⚙️ Executor: Working on iteration {current_iteration}")
        
        # In a real implementation, would use the LLM here to generate solution
        # For demonstration, we'll use a template
        solution = f"Implementation plan for task '{task}':\n\n"
        
        solution += "Phase 1: Setup and Initial Implementation (Weeks 1-2)\n"
        solution += "- Action 1.1: Establish project team and roles\n"
        solution += "- Action 1.2: Define success metrics and KPIs\n"
        solution += "- Action 1.3: Set up basic infrastructure\n"
        solution += "- Milestone: Basic framework operational\n\n"
        
        solution += "Phase 2: Core Development (Weeks 3-6)\n"
        solution += "- Action 2.1: Implement primary functionality\n"
        solution += "- Action 2.2: Develop integration points\n"
        solution += "- Action 2.3: Create monitoring system\n"
        solution += "- Milestone: Core system operational\n\n"
        
        solution += "Phase 3: Refinement and Expansion (Weeks 7-10)\n"
        solution += "- Action 3.1: Add advanced features\n"
        solution += "- Action 3.2: Optimize performance\n"
        solution += "- Action 3.3: Implement feedback from early phases\n"
        solution += "- Milestone: Complete solution deployed\n\n"
        
        solution += "Risk Mitigation:\n"
        solution += "- Risk 1: Resource constraints → Prioritization framework established\n"
        solution += "- Risk 2: Technical challenges → Expert advisors identified\n"
        solution += "- Risk 3: Timeline pressure → Buffer periods built into schedule"
        
        # Send response back to coordinator
        messages.append({
            "from_agent": AgentRole.EXECUTOR,
            "to_agent": AgentRole.COORDINATOR,
            "content": solution,
            "timestamp": time.time(),
            "msg_type": "response",
            "iteration": current_iteration - 1
        })
        
        # Update state
        state["messages"] = messages
        state["current_agent"] = AgentRole.COORDINATOR
        
        return state
    
    def evaluator_agent(self, state: MultiAgentState) -> MultiAgentState:
        """
        Evaluator agent that assesses the quality of solutions.
        - Measures solutions against requirements
        - Identifies strengths and weaknesses
        - Provides an objective assessment
        """
        # Get current state
        messages = state.get("messages", [])
        current_iteration = state.get("current_iteration", 0)
        
        # Get the solution to evaluate
        solution = state.get("solution", "")
        if not solution:
            # If we don't have a final solution, look for the latest execution result
            solution = next((msg["content"] for msg in reversed(messages) 
                           if msg["from_agent"] == AgentRole.EXECUTOR 
                           and msg["msg_type"] == "response"), "")
        
        print(f"\n⭐ Evaluator: Working on iteration {current_iteration}")
        
        # In a real implementation, would use the LLM here to generate evaluation
        # For demonstration, we'll use a template
        
        # Generate evaluation metrics
        evaluation = {
            "comprehensiveness": 0.85,
            "feasibility": 0.78,
            "clarity": 0.91,
            "risk_management": 0.72,
            "resource_allocation": 0.80,
            "overall_quality": 0.82
        }
        
        # Generate evaluation text
        evaluation_text = "Solution Evaluation:\n\n"
        
        evaluation_text += "Strengths:\n"
        evaluation_text += "- Well-structured phased approach\n"
        evaluation_text += "- Clear milestones and deliverables\n"
        evaluation_text += "- Good consideration of risks\n\n"
        
        evaluation_text += "Areas for improvement:\n"
        evaluation_text += "- More detail needed on specific technologies\n"
        evaluation_text += "- Budget estimates could be more precise\n"
        evaluation_text += "- Additional contingency planning recommended\n\n"
        
        evaluation_text += "Metrics:\n"
        for metric, score in evaluation.items():
            evaluation_text += f"- {metric.replace('_', ' ').title()}: {score:.2f}/1.00\n"
        
        evaluation_text += f"\nOverall assessment: {evaluation['overall_quality'] * 100:.1f}% optimal solution"
        
        # Send response back to coordinator
        messages.append({
            "from_agent": AgentRole.EVALUATOR,
            "to_agent": AgentRole.COORDINATOR,
            "content": evaluation_text,
            "timestamp": time.time(),
            "msg_type": "response",
            "iteration": current_iteration - 1
        })
        
        # Set convergence score based on current phase
        # If we're in the final evaluation, mark as complete
        convergence_score = 1.0 if state.get("current_phase") == "final_evaluation" else 0.5
        
        # Update state
        state["messages"] = messages
        state["evaluation"] = evaluation
        state["convergence_score"] = convergence_score
        state["current_agent"] = AgentRole.COORDINATOR
        
        return state
    
    def router(self, state: MultiAgentState) -> str:
        """Route to the next agent based on the current_agent field."""
        return state.get("current_agent", AgentRole.COORDINATOR)
    
    def decide_if_finished(self, state: MultiAgentState) -> bool:
        """Determine if the multi-agent process has finished."""
        # Check if we've reached a convergence score threshold
        if state.get("convergence_score", 0) >= 0.9:
            return True
        
        # Check if we've done a complete final iteration
        if state.get("current_iteration", 0) >= state.get("max_iterations", 5):
            return True
            
        return False
    
    def build_multi_agent_graph(self):
        """Build the multi-agent collaboration graph using LangGraph."""
        try:
            from langgraph.graph import StateGraph
            
            g = StateGraph(MultiAgentState)
            
            # Add all agent nodes
            g.add_node(AgentRole.COORDINATOR, self.coordinator_agent)
            g.add_node(AgentRole.RESEARCHER, self.researcher_agent)
            g.add_node(AgentRole.CRITIC, self.critic_agent)
            g.add_node(AgentRole.EXECUTOR, self.executor_agent)
            g.add_node(AgentRole.EVALUATOR, self.evaluator_agent)
            
            # Connect via dynamic routing
            g.add_conditional_edges(
                AgentRole.COORDINATOR,
                self.router,
                {
                    AgentRole.RESEARCHER: AgentRole.RESEARCHER,
                    AgentRole.CRITIC: AgentRole.CRITIC,
                    AgentRole.EXECUTOR: AgentRole.EXECUTOR,
                    AgentRole.EVALUATOR: AgentRole.EVALUATOR,
                }
            )
            
            # All other agents return to coordinator
            for role in [AgentRole.RESEARCHER, AgentRole.CRITIC, 
                        AgentRole.EXECUTOR, AgentRole.EVALUATOR]:
                g.add_edge(role, AgentRole.COORDINATOR)
            
            # Set entry and terminal state
            g.set_entry_point(AgentRole.COORDINATOR)
            g.add_edge(AgentRole.COORDINATOR, "end", self.decide_if_finished)
            
            return g
            
        except ImportError:
            print("LangGraph not installed. Run 'pip install langgraph' to use this feature.")
            return None
    
    def solve_problem(self, task_description, max_iterations=5):
        """
        Process a problem using the advanced multi-agent approach.
        
        Args:
            task_description: String containing the problem description
            max_iterations: Maximum number of iterations (default: 5)
            
        Returns:
            A solution and evaluation
        """
        # Initialize state
        state = MultiAgentState(
            task=task_description,
            messages=[],
            artifacts={},
            current_agent=AgentRole.COORDINATOR,
            current_iteration=0,
            max_iterations=max_iterations
        )
        
        # Build and run the graph
        graph = self.build_multi_agent_graph()
        if not graph:
            return "Error: Could not build multi-agent graph. Is LangGraph installed?"
        
        try:
            # In a real implementation, we would use the async version
            # For demonstration, we'll manually run through iterations
            current_state = state
            
            while not self.decide_if_finished(current_state):
                current_agent = self.router(current_state)
                
                if current_agent == AgentRole.COORDINATOR:
                    current_state = self.coordinator_agent(current_state)
                elif current_agent == AgentRole.RESEARCHER:
                    current_state = self.researcher_agent(current_state)
                elif current_agent == AgentRole.CRITIC:
                    current_state = self.critic_agent(current_state)
                elif current_agent == AgentRole.EXECUTOR:
                    current_state = self.executor_agent(current_state)
                elif current_agent == AgentRole.EVALUATOR:
                    current_state = self.evaluator_agent(current_state)
            
            # Extract solution and evaluation
            solution = current_state.get("solution", "No solution generated")
            evaluation = current_state.get("evaluation", {})
            
            # Format results
            result = f"SOLUTION:\n{solution}\n\n"
            if evaluation:
                result += "EVALUATION:\n"
                for metric, score in evaluation.items():
                    result += f"- {metric.replace('_', ' ').title()}: {score:.2f}/1.00\n"
            
            return result
            
        except Exception as e:
            print(f"Error running multi-agent system: {e}")
            return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    print("Chapter 6 - Exploring the Coordinator, Worker, and Delegator Approach\n")
    
    print("This chapter demonstrates the Coordinator, Worker, Delegator (CWD) pattern for agent systems.")
    print("The CWD pattern divides agent responsibilities into three key roles:")
    print("- Coordinator: Processes user requests and creates high-level plans")
    print("- Workers: Specialized agents that perform specific tasks")
    print("- Delegator: Assigns tasks to appropriate workers and compiles results")
    
    print("\nTo use the CWD Travel Planner:")
    print("""
    import os
    from Chapter_06 import CWDTravelPlanner
    
    # Set your OpenAI API key
    api_key = "your-api-key-here"
    
    # Create the planner
    planner = CWDTravelPlanner(api_key=api_key)
    
    # Define a travel request
    request=\"\"\"Traveler Alex Johnson is planning to travel to Paris from New York for his anniversary for 7 days and 2 people. 
    - His total budget is about $8000, with hotel budget being $300.
    - Direct flights preferred, morning departure if possible.
    - Hotel in Paris under $400 with wifi preferred. Check in at 5/7/2025 and checkout at 5/14/2025
    - Activities in paris should be moderate pace with some relaxation time built in
    - Mix of walking and public transit, with occasional taxis for evening outings
    \"\"\"
    
    # Process the travel request
    travel_plan = planner.plan_travel(request)
    
    # Print the final travel plan
    print(travel_plan)
    """) 