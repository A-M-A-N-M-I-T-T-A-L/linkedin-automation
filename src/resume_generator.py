from fpdf import FPDF
import logging
from config.config import RESUME_TEMPLATE

logger = logging.getLogger(__name__)

class ResumeGenerator:
    def __init__(self):
        self.template = RESUME_TEMPLATE

    def generate(self, original_resume, job_details, analysis):
        try:
            # Generate optimized content based on job and analysis
            optimized_content = {
                'contact_info': self._extract_contact_info(original_resume),
                'summary': self._generate_summary(original_resume, job_details),
                'experience': self._optimize_experience(original_resume, job_details),
                'skills': self._optimize_skills(original_resume, job_details, analysis),
                'education': self._extract_education(original_resume)
            }
            
            return optimized_content
            
        except Exception as e:
            logger.error(f"Error generating resume: {str(e)}")
            return None

    def convert_to_pdf(self, content):
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Add content to PDF
            self._add_section(pdf, "Contact Information", content['contact_info'])
            self._add_section(pdf, "Professional Summary", content['summary'])
            self._add_section(pdf, "Experience", content['experience'])
            self._add_section(pdf, "Skills", content['skills'])
            self._add_section(pdf, "Education", content['education'])
            
            return pdf.output(dest='S').encode('latin-1')
            
        except Exception as e:
            logger.error(f"Error converting to PDF: {str(e)}")
            return None

    def _add_section(self, pdf, title, content):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, content)
        pdf.ln()
