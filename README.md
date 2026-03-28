Recon Crew: Multi-Agent PhD Research Intelligence
Recon Crew is an autonomous, multi-agent reconnaissance framework designed to discover, analyze, and report on PhD opportunities across Europe. Unlike standard web scrapers, this system utilizes a State-Graph Architecture to manage long-running research tasks, ensuring high-fidelity data extraction from fragmented institutional portals.

![System Architecture](docs/architechture.png)

🏗 System Overview
The system follows a Controller-Agent-Tool pattern managed via a persistent state machine. It moves beyond simple keyword searching by executing a multi-stage cognitive workflow:
Strategic Planning: The Planner Agent identifies "Golden URLs" (verified government/university hubs) based on the target country and research field.
Autonomous Reconnaissance: The Research Agent (The Scout) performs deep-link discovery, recursively identifying vacancy portals, faculty directories, and lab-specific contact pages.
Structured Extraction: The Extractor Agent utilizes LLM-backed structured output (Pydantic) to parse raw HTML into a unified schema, capturing:
Contextual Deadlines: Descriptive application windows (e.g., "Rolling," "Requires PI contact").
Funding Intelligence: Specific grant identifiers (ERC, MSCA) and salary scales.
Contact Metadata: Professor names, emails, and physical lab addresses.
Automated Reporting: The PDFGenerator compiles the validated state into a professional, multi-page research report.
🚀 Key Features
Recursive Deep-Diving: Automatically spawns sub-tasks to crawl individual university sub-domains.
Intelligent Field Mapping: Eliminates "See website" placeholders by forcing the LLM to summarize qualitative context if quantitative data is missing.
State-Graph Handshake: Built with LangGraph to ensure data persistence and error recovery during complex crawls.
Scalable Discovery: Capable of parallelizing discovery across multiple target countries and institutions.
🛠 Tech Stack
Orchestration: LangGraph (State Machine Management)
LLM Integration: LangChain & Pydantic (Structured Data Models)
Web Automation: Playwright (Headless Browser) & BeautifulSoup4
Reporting: FPDF2