import streamlit as st
from src.services import JobService
from src.core.filters import JobFilter
import plotly.express as px

class JobListPage:
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    def render(self):
        st.title("Job Listings")
        
        # Filters sidebar
        with st.sidebar:
            self._render_filters()

        # Main content
        self._render_job_stats()
        self._render_job_list()

    def _render_filters(self):
        st.sidebar.header("Filters")
        filters = JobFilter(
            min_experience=st.sidebar.slider("Minimum Experience", 0, 15, 0),
            required_skills=st.sidebar.multiselect("Required Skills", self._get_available_skills()),
            job_types=st.sidebar.multiselect("Job Types", ["Full-time", "Part-time", "Contract"])
        )
        return filters

    def _render_job_stats(self):
        jobs = self.job_service.get_all_jobs()
        if jobs:
            fig = px.histogram(
                [job.company for job in jobs], 
                title="Jobs by Company"
            )
            st.plotly_chart(fig)

    def _render_job_list(self):
        jobs = self.job_service.get_all_jobs()
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
