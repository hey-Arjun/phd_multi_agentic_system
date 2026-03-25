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
    Analyze the query to extract the country and field.

    ALLOWED COUNTRIES: {valid_countries}

    STRATEGY RULES:
    1. focus_field: Identify the subject (e.g., Electronics).
    2. search_strategy: You MUST include a mandate to find:
       - Active PhD vacancies.
       - Funding/Scholarship details.
       - **PI/Professor contact info and lab addresses for the 'Other Info' column.**
    3. initial_url: Get the first portal from COUNTRY_SOURCES.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "User Query: {query}")
    ])

    return prompt | llm.with_structured_output(RoutePlan)