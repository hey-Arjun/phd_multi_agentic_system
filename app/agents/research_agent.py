import asyncio
from typing import List, Dict
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from app.tools.scrapper_tool import ScraperTool
from app.llm.llm import get_llm

class RelevantLinks(BaseModel):
    urls: List[str] = Field(description="A list of 3-5 high-priority URLs for PhD/Scholarship info")

class ResearchAgent:
    def __init__(self):
        self.scraper = ScraperTool()
        self.llm = get_llm()

    async def find_phd_listings(self, country: str, root_url: str) -> List[str]:
        """
        Scrapes a single root URL and uses LLM to find the 'Gold' sub-links.
        """
        try:
            print(f"--- [Started] {country.upper()}: {root_url} ---")
            
            # 1. Extract all links using the ScraperTool
            all_links = await self.scraper.extract_links(root_url)
            
            # 2. Filter noise
            noise = ["facebook", "twitter", "linkedin", "instagram", "cookie", "privacy", "login", "contact", "about"]
            candidates = [l for l in all_links if not any(n in l.lower() for n in noise)]
            
            if not candidates:
                return []

            # 3. LLM Selection
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a PhD Recruitment Expert. Out of these links from {country}, "
                           "pick the 3-5 most likely to lead to specific PhD program listings, "
                           "admission portals, or funding/scholarship details."),
                ("human", "Available Links: {links}")
            ])
            
            chain = prompt | self.llm.with_structured_output(RelevantLinks)
            # We send a chunk of candidates to stay within context limits
            selected = await chain.ainvoke({"country": country, "links": candidates[:50]})
            
            return selected.urls
        except Exception as e:
            print(f"Error researching {country} at {root_url}: {e}")
            return []

    async def discover_all_paths(self, tasks: List[Dict[str, str]]) -> List[str]:
        """
        Executes multiple 'find_phd_listings' tasks in parallel.
        tasks = [{'country': 'france', 'url': '...'}, {'country': 'germany', 'url': '...'}]
        """
        print(f"--- Launching Parallel Discovery for {len(tasks)} target URLs ---")
        
        # Create a list of asynchronous coroutines
        coroutines = [self.find_phd_listings(t['country'], t['url']) for t in tasks]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*coroutines)
        
        # Flatten the list of lists into a single unique list of URLs
        flattened_paths = [url for sublist in results for url in sublist]
        return list(set(flattened_paths)) # Deduplicate