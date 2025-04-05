import streamlit as st
import json
from src.db_manager import DBManager
from src.llm_manager import LLMManager
from src.resume_generator import ResumeGenerator
import pandas as pd
import io
import base64

class JobDetailsPage:
    def __init__(self):
        self.db_manager = DBManager()
        self.llm_manager = LLMManager()
        self.resume_generator = ResumeGenerator()

    def run(self):
        st.title("Job Details")

        # Get all jobs for selection
        jobs = self.db_manager.get_all_jobs()
        if not jobs:
            st.warning("No jobs found in database")
            return

        # Job selector
        selected_job = st.selectbox(
            "Select Job",
            options=jobs,
            format_func=lambda x: f"{x['title']} at {x['company']}"
        )

        if selected_job:
            self._show_job_details(selected_job)
            self._show_resume_section(selected_job)

    def _show_job_details(self, job):
        with st.expander("Job Details", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(job['title'])
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location']}")
                
            with col2:
                if 'required_skills' in job:
                    st.write("**Required Skills:**")
                    for skill in job['required_skills']:
                        st.write(f"- {skill}")

            st.write("**Job Description:**")
            st.write(job['description'])

            if 'analysis' in job:
                st.write("**Job Analysis:**")
                st.json(job['analysis'])

    def _show_resume_section(self, job):
        st.header("Resume Optimization")

        # Resume upload
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])
        
        if uploaded_file:
            resume_text = self._extract_resume_text(uploaded_file)
            
            if resume_text:
                # Analyze resume against job
                analysis = self.llm_manager.analyze_resume_job_match(resume_text, job)
                
                # Show analysis
                self._show_resume_analysis(analysis)
                
                # Option to generate optimized resume
                if st.button("Generate Optimized Resume"):
                    optimized_resume = self.resume_generator.generate(
                        original_resume=resume_text,
                        job_details=job,
                        analysis=analysis
                    )
                    
                    # Provide download link
                    pdf_data = self.resume_generator.convert_to_pdf(optimized_resume)
                    self._create_download_link(pdf_data, "optimized_resume.pdf")

    def _extract_resume_text(self, file):
        try:
            # Add resume text extraction logic here
            return "Resume text extraction placeholder"
        except Exception as e:
            st.error(f"Error extracting resume text: {str(e)}")
            return None

    def _show_resume_analysis(self, analysis):
        st.subheader("Resume Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Match Score", f"{analysis['match_percentage']}%")
            
        with col2:
            st.metric("Missing Skills", len(analysis.get('missing_skills', [])))

        # Show detailed analysis
        with st.expander("Detailed Analysis"):
            st.write("**Missing Skills:**")
            for skill in analysis.get('missing_skills', []):
                st.write(f"- {skill}")
                
            st.write("**Improvement Suggestions:**")
            for suggestion in analysis.get('suggestions', []):
                st.write(f"- {suggestion}")

    def _create_download_link(self, pdf_data, filename):
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download Optimized Resume</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    page = JobDetailsPage()
    page.run()
