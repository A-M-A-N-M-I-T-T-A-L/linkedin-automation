import streamlit as st
from src.services.job_service import JobService
from src.core.filters import JobFilter
import plotly.express as px
from typing import List

class JobListPage:
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    def render(self):
        st.title("Job Listings")
        
        # Filters sidebar
        with st.sidebar:
            filters = self._render_filters()

        # Main content
        self._render_job_stats()
        self._render_job_list(filters)

    def _render_filters(self) -> JobFilter:
        st.sidebar.header("Filters")
        
        min_experience = st.sidebar.slider("Minimum Experience", 0, 15, 0)
        required_skills = st.sidebar.multiselect(
            "Required Skills", 
            options=self._get_available_skills(),
            default=None
        )
        job_types = st.sidebar.multiselect(
            "Job Types", 
            options=["Full-time", "Part-time", "Contract", "Remote"],
            default=None
        )
        excluded_companies = set(st.sidebar.text_area(
            "Excluded Companies (one per line)", 
            value="",
            help="Enter company names to exclude"
        ).split('\n'))
        
        remote_only = st.sidebar.checkbox("Remote Only", False)
        
        return JobFilter(
            min_experience=min_experience,
            required_skills=required_skills if required_skills else None,
            job_types=job_types if job_types else None,
            excluded_companies=excluded_companies if excluded_companies != {''} else None,
            remote_only=remote_only
        )

    def _get_available_skills(self) -> List[str]:
        try:
            skills = self.job_service.get_all_skills()
            return sorted(list(set(skills)))
        except Exception:
            return ["Python", "JavaScript", "Java", "C++", "SQL"]

    def _render_job_stats(self):
        jobs = self.job_service.get_all_jobs()
        if jobs:
            fig = px.histogram(
                [job.company for job in jobs], 
                title="Jobs by Company"
            )
            st.plotly_chart(fig)

    def _render_job_list(self, filters: JobFilter):
        jobs = self.job_service.get_filtered_jobs(filters)
        
        if not jobs:
            st.info("No jobs found matching your filters.")
            return
            
        for job in jobs:
            with st.expander(f"{job.title} at {job.company}"):
                self._render_job_card(job)

    def _render_job_card(self, job):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Location:** {job.location}")
            st.write(f"**Type:** {job.job_type}")
        with col2:
            st.write(f"**Required Experience:** {job.experience_years} years")
            st.write(f"**Posted:** {job.created_at.strftime('%Y-%m-%d')}")