import asyncio
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph, END, START

# Import Agents
from app.agents.planner_agent import get_planner_agent
from app.agents.research_agent import ResearchAgent
from app.agents.extractor_agent import ExtractorAgent
from app.tools.pdf_generator import PDFGenerator
from app.config.country_sources import COUNTRY_SOURCES

class AgentState(TypedDict):
    query: str
    country: str
    target_countries: List[str]
    task_queue: List[str]
    golden_paths: List[str]
    final_reports: List[dict]
    focus_field: str

# 1 planning phase
async def planning_node(state: AgentState):
    query = state["query"]
    
    # Call the updated agent
    planner = get_planner_agent()
    plan = await planner.ainvoke({"query": query})
    
    current_country = plan.country.lower()
    extracted_field = plan.focus_field 

    if current_country == "europe" or "all countries" in query.lower():
        countries = list(COUNTRY_SOURCES.keys())
        # Use the first portal for every country
        urls = [f"https://{COUNTRY_SOURCES[c]['portals'][0]}" for c in countries if COUNTRY_SOURCES[c].get('portals')]
    else:
        countries = [current_country]
        sources = COUNTRY_SOURCES.get(current_country, {})
        # Combine portals, official sites, and universities for the specific country deep-dive
        urls = [f"https://{u}" for u in (sources.get('portals', []) + sources.get('official', []) + sources.get('universities', []))]

    return {
        "country": current_country,
        "target_countries": countries,
        "task_queue": urls,
        "focus_field": extracted_field 
    }

# 2 Research Phase
async def research_node(state: AgentState):
    researcher = ResearchAgent()
    
    # Use the task_queue we built in the planning_node
    tasks = []
    for url in state["task_queue"]:
        # We assign the country context to each URL task
        tasks.append({"country": state["country"], "url": url})

    # Run parallel discovery
    all_golden_paths = await researcher.discover_all_paths(tasks)
    
    return {"golden_paths": all_golden_paths[:20]}

# 3. Extraction Phase
# 3. Extraction Phase
async def extraction_node(state: AgentState):
    # Initialize agents locally to ensure they are fresh for this node
    extractor = ExtractorAgent()
    researcher = ResearchAgent() 
    results = []

    # Use 'golden_paths' discovered in the research_node
    for link in state.get("golden_paths", []):
        # 1. IMMEDIATE FILTER: Skip junk URLs before scraping to save time/memory
        if any(x in link.lower() for x in ["contact", "news", "hirek", "press", "about"]):
            continue
            
        print(f"--- Deep Extracting PhD Info: {link} ---")
        
        try:
            # Step 1: Scrape the content using the researcher's tool
            # (This clears the red line by ensuring researcher is defined above)
            content = await researcher.scraper.scrape_url(link)
            
            # Step 2: Use the dynamic focus_field from the planner
            field = state.get("focus_field", "Research")
            programs = await extractor.parse_data(content, field)
            
            if not programs:
                continue

            for p in programs:
                p_dict = p.model_dump()
                
                # Step 3: Map to the EXACT 7 columns for the PDF
                full_entry = {
                    "university_name": p_dict.get("university") or "See Website",
                    "program_title": p_dict.get("program_title") or f"PhD in {field}",
                    "application_deadline": p_dict.get("application_deadline") or "Check Portal",
                    "funding_details": p_dict.get("funding_details") or "See Website",
                    "tuition_fees": p_dict.get("tuition_fees") or "Exempt/Free",
                    "application_link": link, # Use current link as the direct source
                    "source": link.split('/')[2], # Domain name
                    "country_name": state["country"].capitalize()
                }
                results.append(full_entry)
        except Exception as e:
            print(f"Skipping {link} due to error: {e}")
            continue
            
    return {"final_reports": results}

# 4.  Reporting phase
async def report_node(state: AgentState):
    generator = PDFGenerator()
    file_path = generator.create_report(
        reports=state["final_reports"],
        country=state["country"],
        query=state["query"]
    )
    print(f"\n--- PDF Successfully Generated: {file_path} ---")
    return state

def create_graph():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("planner", planning_node)
    workflow.add_node("researcher", research_node)
    workflow.add_node("extractor", extraction_node)
    workflow.add_node("report_node", report_node)

    # set Entry point
    workflow.set_entry_point("planner")

    # Define Edges (Linear Flow)
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "extractor")
    workflow.add_edge("extractor", "report_node") 
    workflow.add_edge("report_node", END)


    return workflow.compile()

# Main Execution
if __name__ == "__main__":
    async def run_app():
        app = create_graph()
        inputs = {"query": "find phd in Material Science in portugese"}

        async for output in app.astream(inputs):
            for key, value in output.items():
                print(f"Finished Node: {key}")

        # Final Output
        # Here you would call your PDF generation tool
        print("\n--- FINAL RESEARCH REPORT ---")
        print(output)
    
    asyncio.run(run_app())