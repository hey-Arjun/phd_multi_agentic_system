from fpdf import FPDF
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=20)
        self.font_name = "Arial" 

    def _sanitize(self, text: str) -> str:
        """Removes or replaces characters that break PDF encoding."""
        if not text:
            return "N/A"
        text = text.replace('\u2013', '-').replace('\u2014', '-')
        return text.encode('latin-1', 'ignore').decode('latin-1')

    def create_report(self, reports: list, country: str, query: str):
        self.pdf.add_page()
        self.pdf.set_margins(15, 20, 15)
        
        # Header
        self.pdf.set_font("Helvetica", "B", 16)
        self.pdf.cell(0, 10, self._sanitize(f"PhD Research Report: {country.upper()}"), ln=True, align='C')
        self.pdf.ln(10)

        for i, program in enumerate(reports, 1):
            # Check for page break
            if self.pdf.get_y() > 230:
                self.pdf.add_page()

            # 1. Program Title
            self.pdf.set_font("Helvetica", "B", 12)
            self.pdf.set_fill_color(245, 245, 245)
            title = program.get('program_title') or program.get('title') or "PhD Program"
            self.pdf.multi_cell(0, 8, f"{i}. {self._sanitize(title)}", fill=True)
            
            self.pdf.ln(2)
            
            # We use .get() to support the new field names from the updated Extractor
            fields = [
                ("University", program.get('university_name') or program.get('university')),
                ("Country", program.get('country_name') or country.capitalize()),
                ("Deadline", program.get('application_deadline') or program.get('deadline')),
                ("Funding", program.get('funding_details') or program.get('funding')),
                ("Tuition", program.get('tuition_fees')),
                ("Source Portal", program.get('source')),
                ("Other Info", program.get('additional_metadata')) 
            ]

            for label, value in fields:
                if value and str(value).lower() not in ["none", "n/a", ""]:
                    self.pdf.set_font("Helvetica", "B", 10)
                    # Use multi_cell for all values now, because "Deadline" and "Funding" 
                    # will contain longer descriptions instead of just "See website"
                    self.pdf.write(6, f"{label}: ")
                    self.pdf.set_font("Helvetica", "", 10)
                    self.pdf.multi_cell(0, 6, self._sanitize(str(value)))

            # 3. Application Link
            link = program.get('application_link') or program.get('link')
            if link and str(link).lower() != "none":
                self.pdf.set_font("Helvetica", "B", 10)
                self.pdf.write(6, "Apply Here: ")
                self.pdf.set_text_color(0, 0, 255) # Blue Link
                self.pdf.multi_cell(0, 6, self._sanitize(str(link)))
                self.pdf.set_text_color(0, 0, 0) # Back to Black

            self.pdf.ln(5)
            self.pdf.line(15, self.pdf.get_y(), 195, self.pdf.get_y())
            self.pdf.ln(5)

        filename = f"Report_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.pdf.output(filename)
        return filename