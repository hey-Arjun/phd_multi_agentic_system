# PhD Multi-Agentic System (Recon Crew)

![System Architecture](docs/architechture.png)

An autonomous, multi-agent reconnaissance framework designed to discover, extract, and report on PhD opportunities across Europe. 

## 🏗 System Overview
The system utilizes a state-graph architecture to coordinate three specialized agents:
* **Planner Agent:** Formulates a search strategy based on verified "Golden URLs."
* **Research Agent:** Conducts deep-web reconnaissance to find specific lab and contact pages.
* **Extractor Agent:** Converts raw HTML into structured JSON/PDF data including PI contacts and funding details.

... [Rest of your content]olden URLs" (verified government/university portals) and recursively explores institutional sub-domains.

🚀 Key Features
Recursive Deep-Diving: Unlike standard scrapers, the ResearchAgent identifies university hubs and automatically spawns sub-tasks to crawl individual lab pages.
Intelligent Extraction: Uses LLM-backed structured output to capture:
Contextual Deadlines: Moves beyond "See website" to describe application windows (Rolling, Spring Intake, etc.).
Funding Intelligence: Identifies specific grant types (ERC, MSCA, MSCA-PF) and salary scales.
PI & Metadata: Automatically extracts Professor names, emails, phone numbers, and lab addresses.
State-Graph Orchestration: Built with LangGraph to ensure a robust "Handshake" between agents and to prevent data loss during long-running crawls.
🛠 Tech Stack
Language: Python 3.10+
Orchestration: LangGraph (State Machine)
LLM Integration: LangChain & Pydantic (Structured Output)
Web Scraping: Playwright & BeautifulSoup4
Reporting: FPDF2 (Automated PDF Generation)