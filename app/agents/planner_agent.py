from app.llm.llm import get_llm
from app.config.country_sources import COUNTRY_SOURCES
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class RoutePlan(BaseModel):
    country: str = Field(description="The specific country identified ")
    focus_field: str = Field(description="The specific subject or field of study")
    initial_url: str = Field(description="The full URL (https://...) of the primary portal")
    search_strategy: str = Field(description="Brief plan on what categories to look for")

def get_planner_agent():
    llm = get_llm()
    valid_countries = ", ".join(COUNTRY_SOURCES.keys())

    system_message = f"""You are a PhD Research Planner. 
    Analyze the user's query to extract the target country and the specific field of study.

    ALLOWED COUNTRIES: {valid_countries}

    RULES:
    1. Extract the 'focus_field' (e.g., if they ask for 'physics', focus_field is 'Physics').
    2. If the user mentions a specific country from the list, use it.
    3. If they say 'Europe', use 'europe' as the country name.
    4. Provide the first 'portal' URL from COUNTRY_SOURCES for that country.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "User Query: {query}")
    ])

    return prompt | llm.with_structured_output(RoutePlan)