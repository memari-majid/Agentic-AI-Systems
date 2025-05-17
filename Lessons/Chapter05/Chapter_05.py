#!/usr/bin/env python3
# Chapter 5 – Enabling Tool Use and Planning in Agents

# Required dependencies:
# pip install -U openai ipywidgets crewai langchain-openai autogen-agentchat autogen-ext[openai]

import os
from typing import Dict

# Sample implementation of a Hierarchical Task Network (HTN) travel planning agent
# using CrewAI framework

class HTNTravelPlanner:
    def __init__(self, api_key=None):
        try:
            from crewai import Agent, Task, Crew, Process
            from langchain_openai import ChatOpenAI

            # Set up API key
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key

            # Create specialized agents for different aspects of travel planning
            self.flight_specialist = Agent(
                role='Flight Planning Specialist',
                goal='Handle all aspects of flight arrangements',
                backstory="Expert in airline bookings and flight logistics.",
                verbose=False
            )
            
            self.accommodation_specialist = Agent(
                role='Accommodation Specialist',
                goal='Manage all accommodation-related planning',
                backstory="Expert in hotel and accommodation arrangements.",
                verbose=False
            )

            self.activity_specialist = Agent(
                role='Vacation Activity Specialist',
                goal='Manage all activity-related planning',
                backstory="Expert in recreational activity arrangements.",
                verbose=False
            )
            
            # Define the manager LLM for hierarchical process
            self.manager_llm = ChatOpenAI(model="gpt-4o-mini")
        except ImportError:
            print("Required modules not found. Please install crewai and langchain-openai.")

    def plan_travel(self, request: str) -> Dict:
        try:
            from crewai import Task, Crew, Process
            
            # Define the top-level task for travel planning
            travel_planning_task = Task(
                description=f"""
                Plan a comprehensive flight itinerary based on the following request:
                {request}
                
                The plan should include:
                - Flight arrangements
                - Accommodation bookings
                - Any other relevant travel components
                """,
                expected_output="A detailed flight itinerary covering all requested aspects.",
                agent=None  # No specific agent; the manager will delegate subtasks
            )

            # Create the crew with a hierarchical process
            crew = Crew(
                agents=[self.flight_specialist, self.accommodation_specialist, self.activity_specialist],
                tasks=[travel_planning_task],
                process=Process.hierarchical,
                manager_llm=self.manager_llm,
                verbose=False
            )

            # Execute the hierarchical plan
            return crew.kickoff()
        except Exception as e:
            return f"Error planning travel: {str(e)}"


# Implementing tool use in agents with CrewAI
# Tools for travel planning agent

def define_travel_tools():
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
                    {"name": "Citadines Saint-Germain-des-Prés", "price": 280, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.2, "location": "Saint-Germain", "amenities": ["Kitchenette", "Laundry", "Wifi"]},
                    {"name": "Ibis Paris Eiffel Tower", "price": 180, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.0, "location": "Near Eiffel Tower", "amenities": ["Restaurant", "Bar", "Wifi"]}
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
                
        return search_flights, find_hotels, find_activities
    except ImportError:
        print("CrewAI not installed. Run 'pip install crewai' to use these tools.")
        return None, None, None


# Implementation with CrewAI and tools
class TravelPlannerCrewAI:
    def __init__(self, api_key=None):
        try:
            from crewai import Agent, Process
            
            # Set up API key
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                
            # Get the tools
            search_flights, find_hotels, find_activities = define_travel_tools()
            
            if not all([search_flights, find_hotels, find_activities]):
                raise ImportError("Could not define tools properly")

            # Create specialized agents for different aspects of travel planning
            self.travel_specialist = Agent(
                role='An expert travel concierge',
                goal='Handle all aspects of travel planning',
                backstory="Expert in airline bookings and flight logistics, hotel bookings, and booking vacation activities.",
                tools=[search_flights, find_hotels, find_activities],
                verbose=False
            )
        except ImportError as e:
            print(f"Required modules not found: {e}")
            
    def plan_travel(self, request: str) -> Dict:
        try:
            from crewai import Task, Crew, Process
            
            # Define the top-level task for travel planning
            travel_planning_task = Task(
                description=f"""
                Plan a comprehensive travel and leisure itinerary based on the following request:
                {request}
                
                The plan should include:
                - Flight arrangements
                - Accommodation bookings
                - Any other relevant travel components
                """,
                expected_output="A detailed travel itinerary covering all requested aspects.",
                agent=self.travel_specialist 
            )

            # Create the crew with a sequential process
            crew = Crew(
                agents=[self.travel_specialist],
                tasks=[travel_planning_task],
                process=Process.sequential,
                verbose=False
            )

            # Execute the plan
            return crew.kickoff()
        except Exception as e:
            return f"Error planning travel: {str(e)}"


# Example implementation with AutoGen
def autogen_travel_planner(api_key=None, request=None):
    """
    Create a travel planning system using AutoGen framework.
    
    Args:
        api_key: OpenAI API key
        request: Travel planning request
        
    Returns:
        None, prints the conversation
    """
    try:
        import autogen
        
        # Set up API key
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            
        # Configuration
        config_list = [
            {
                "model": "gpt-4o-mini",
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
        
        # Create the agents
        user_proxy = autogen.UserProxyAgent(
            name="user",
            system_message="A user who needs help planning a trip.",
            human_input_mode="NEVER"
        )
        
        flight_planner = autogen.AssistantAgent(
            name="flight_planner",
            system_message="You are a flight planning expert. Your job is to recommend flights and itineraries.",
            llm_config={"config_list": config_list}
        )
        
        hotel_planner = autogen.AssistantAgent(
            name="hotel_planner",
            system_message="You are a hotel planning expert. Your job is to recommend accommodation options.",
            llm_config={"config_list": config_list}
        )
        
        activities_planner = autogen.AssistantAgent(
            name="activities_planner",
            system_message="You are an activities planning expert. Your job is to recommend local activities and attractions.",
            llm_config={"config_list": config_list}
        )
        
        travel_summary_agent = autogen.AssistantAgent(
            name="travel_summary_agent",
            system_message="""You are a travel summary expert. 
            Your job is to compile all information from the other agents and create a comprehensive travel plan.
            Include flight details, accommodation options, and suggested activities in a well-formatted plan.""",
            llm_config={"config_list": config_list}
        )
        
        # Create a group chat
        groupchat = autogen.GroupChat(
            agents=[user_proxy, flight_planner, hotel_planner, activities_planner, travel_summary_agent],
            messages=[],
            max_round=10,
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": config_list}
        )
        
        # Initiate the conversation
        if request:
            user_proxy.initiate_chat(manager, message=request)
            
    except ImportError:
        print("AutoGen not installed. Run 'pip install autogen-agentchat autogen-ext[openai]' to use this function.")


if __name__ == "__main__":
    print("Chapter 5 - Enabling Tool Use and Planning in Agents\n")
    
    print("Example implementations available:")
    print("1. HTNTravelPlanner - Hierarchical Task Network approach")
    print("2. TravelPlannerCrewAI - Tool-using agent with CrewAI")
    print("3. autogen_travel_planner - Multi-agent planning with AutoGen")
    
    print("\nTo run an example, ensure you have the required dependencies installed:")
    print("pip install -U openai ipywidgets crewai langchain-openai")
    print("pip install autogen-agentchat==0.4.0.dev11 autogen-ext[openai]==0.4.0.dev11")
    
    print("\nSample usage:")
    print("""
    import os
    from Chapter_05 import HTNTravelPlanner
    
    # Set your OpenAI API key
    api_key = "your-api-key-here"
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Create the planner
    planner = HTNTravelPlanner()
    
    # Define a travel request
    request = \"\"\"
    I need to plan a trip to Paris from New York for 5 days.
    The plan should include:
    - Flights for 2 adults
    - Hotel accommodations in central Paris with breakfast
    - Airport transfers
    - A day trip to Versailles.
    \"\"\"
    
    # Execute the planning process
    result = planner.plan_travel(request)
    
    # Print the result
    print("Final Travel Plan:")
    print(result)
    """) 