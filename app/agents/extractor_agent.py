from pydantic import BaseModel, Field
from typing import List, Optional
from app.llm.llm import get_llm
from app.config.filters import clean_text

# 1. The Schema for a single PhD listing
class PhDData(BaseModel):
    university: str = Field(description="Exact name of the university or 'Various' if not specified.")
    program_title: str = Field(description="The PhD title or research area (e.g., 'PhD in Mathematics').")
    application_deadline: str = Field(description="Extract the exact date. If no date, describe the window (e.g., 'Rolling', 'Contact PI', '4 months before start'). DO NOT use 'See website'.")
    funding_details: str = Field(description="Identify the funding source (ERC, MSCA, etc.) or type (Salary, Stipend). If unknown, describe the likely funding model for that country. DO NOT use 'Check portal'.")
    additional_metadata: str = Field(description="Include PI/Professor names, contact emails, phone numbers, lab/office addresses, or specific prerequisites (e.g., 'Master's required').")
    application_link: str = Field(description="The direct URL for application or information.")
    source: str = Field(description="The root domain of the portal.")

# 2. THE FIX: A container to extract MULTIPLE programs at once
class PhDListingResponse(BaseModel):
    programs: List[PhDData] = Field(description="A list of all PhD programs found in the text")

class ExtractorAgent:
    def __init__(self):
        self.llm = get_llm()

    async def parse_data(self, raw_text: str, field: str):
        processed_text = clean_text(raw_text)
        prompt = f"""
        Analyze the text to find PhD opportunities in {field}.
        
        STRICT RULES:
        1. NEVER use 'See website' or 'Check portal'.
        2. DEADLINE: If no date, describe the process (e.g., 'Rolling' or 'Requires supervisor contact').
        3. OTHER INFO: You MUST extract Professor names, emails, phone numbers, and lab addresses into the 'additional_metadata' field.
        
        TEXT: {processed_text[:25000]}
        """
        
        structured_llm = self.llm.with_structured_output(PhDListingResponse)
        result = await structured_llm.ainvoke(prompt)
        
        # Add a final safety check to clean any stray "See website" if the LLM slips up
        if result:
            for p in result.programs:
                if "website" in p.application_deadline.lower():
                    p.application_deadline = "Rolling / Contact Supervisor"
                if "portal" in p.funding_details.lower():
                    p.funding_details = "Institutional funding (Review required)"
            return result.programs
        return []