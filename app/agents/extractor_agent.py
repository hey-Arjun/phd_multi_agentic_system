from pydantic import BaseModel, Field
from typing import List
from app.llm.llm import get_llm
from app.config.filters import clean_text

# 1. The Schema for a single PhD listing
class PhDData(BaseModel):
    university: str = Field(description="Name of the University")
    program_title: str = Field(description="Specific PhD or Research Area")
    application_deadline: str = Field(description="The date applications close")
    funding_details: str = Field(description="Scholarship, stipend, or grant info")
    tuition_fees: str = Field(description="Cost per year or 'Exempt/Free'")
    country: str = Field(description="The country of the university")
    source_url: str = Field(description="The direct link to the admissions/funding page")

# 2. THE FIX: A container to extract MULTIPLE programs at once
class PhDListingResponse(BaseModel):
    programs: List[PhDData] = Field(description="A list of all PhD programs found in the text")

class ExtractorAgent:
    def __init__(self):
        self.llm = get_llm()

    async def parse_data(self, raw_text: str, field: str):
        processed_text = clean_text(raw_text)
        prompt = f"""
        You are a PhD Admissions Officer. Analyze the text to find PhD opportunities in {field}.
        
        IMPORTANT RULES:
        1. Look specifically for 'Tuition Fees'. In many European countries , 
        PhD tuition is often 'Exempt' or 'approx 400 EUR/year'. Report this specifically.
        2. Look for 'Application Deadlines'. If a specific date isn't found, look for 
        terms like 'Rolling' or 'Contact supervisor'.
        3. Look for 'Funding'. Identify if it mentions 'ERC Grants', 'Doctoral Contracts', or 'Stipends'.
        4. If the info is NOT in the text, do not say 'None'. Say 'See website' or 'Check portal'.
        
        TEXT TO ANALYZE:
        {processed_text[:15000]}
        """
        # Use the ListingResponse class to get multiple results
        structured_llm = self.llm.with_structured_output(PhDListingResponse)
        result = await structured_llm.ainvoke(prompt)
        return result.programs if result else []