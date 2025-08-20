import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from .tools.generaltools import get_current_date
from .tools.bravesearchtool import brave_search_tool



# def get_weather(city: str, time: str) -> dict:
#     """Retrieves the current weather report for a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the weather report.
#         time (str): The time for which to retrieve the weather report.


#     Returns:
#         dict: status and result or error msg.
#     """
#     if city.lower() == "new york":
#         return {
#             "status": "success",
#             "report": (
#                 "The weather in New York is sunny with a temperature of 25 degrees"
#                 " Celsius (77 degrees Fahrenheit). The time in  New York is "
#                 f"{time}"
#             ),
#         }
#     else:
#         return {
#             "status": "error",
#             "error_message": f"Weather information for '{city}' is not available.",
#         }


# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the current time.

#     Returns:
#         dict: status and result or error msg.
#     """

#     if city.lower() == "new york":
#         tz_identifier = "America/New_York"
#     else:
#         return {
#             "status": "error",
#             "error_message": (
#                 f"Sorry, I don't have timezone information for {city}."
#             ),
#         }

#     tz = ZoneInfo(tz_identifier)
#     now = datetime.datetime.now(tz)
#     report = (
#         f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
#     )
#     return {"status": "success", "report": report}

google_search_agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to search about anything"
    ),
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    tools=[google_search]
)

brave_search_agnet = Agent(
    name="brave_search_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to search for insurance policies"
    ),
    instruction="""You can search for insurance policies of different insurnace companies
    Use the intial prompt from the users to formulate a search query that uses the search tool to 
    find insurance policy documents on the web. When searching polices make sure you search for pdf files
    and search for products from each insurance company.""",
    tools=[brave_search_tool]
)

box_report_agent = Agent(
    name="box_report_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to create a 4 box report"
    ),
    instruction=(
        """SWOT Analysis: of the policies.
            Strengths (Internal, Positive)
            Weaknesses (Internal, Negative)
            Opportunities (External, Positive)
            Threats (External, Negative)
            
            use the above to create a box report of the different insurance policies analysed by the agent"""
    )
)

analysis_agent = Agent(
    name="analysis_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to analyse insurance policies"
    ),
    instruction=(
        "You are an agent that assesses the differnt terms of insurance policies"
        "You should create a summary of the comparisons of policies"
        "when asked you should use your understanding of the polices to create a new insuranece product"
        "the new product should identify gaps in the currenty polilcies and create a new policy"
        "the new policy should create a new market that the company can leverage to get new customers"
    ),
    # sub_agents=[report_agent]
)

seq_agent = Agent(
    name="seq_agent",
    description=(
        "you are the agent that runs the process for collecting the data and creating the report"
        "USe the brave_search_agent to get the documents and then create the analysis and reports"
    ),
    sub_agents=[brave_search_agnet, analysis_agent, box_report_agent]
)

root_agent = Agent(
    name="insurance_policy_analysis_agent",
    model="gemini-2.5-flash",
    description=(
        "You are an agent helping analyse insurance policies"
    ),
    instruction=(
        # "You are an investment analyst agent that creates an analysis of assets and stock"
        # "You use the tools and subagents at your disposal to get the data and summarise the data"
        # "Include a detailed summary in the response"
        # "use the get_current_date tool to get the current data in order to use with any of the subagents"
        # "use the symbol_lookup_agent to get a stock symbol from a company name"
        # "use the news subagent to get company news"
        # "In the response include a detailed section on the news"
        # "If the user does not specify a start date or end date, use the current date as the start date using the get_current_date tool"
        # "use the date from 6 months ago as the end date"
        # "If the user specifies the date as a duration, use get_current_date to get the start date and calculate it"
        # "make sure to always use the get_current_date tool to do the date calculation"
        # "use all the sub agnets to create a report on the investment"
        """You are a general purpose agent that uses the search sub agent to get a list of insurance policy documents and compares them
        create formatded output based on the users request of how to do the comparison. Use the brave_search_agnet to get the policy
        details"""

    ),
    tools=[get_current_date],
    sub_agents=[seq_agent]
)