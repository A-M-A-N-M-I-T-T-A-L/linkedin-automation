import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from src.db_manager import DBManager
from src.connection_tracker import ConnectionTracker
import logging

logger = logging.getLogger(__name__)

class Dashboard:
    def __init__(self):
        self.db_manager = DBManager()
        self.connection_tracker = ConnectionTracker()
        
    def run(self):
        st.set_page_config(page_title="LinkedIn Automation Dashboard", layout="wide")
        st.title("LinkedIn Automation Dashboard")
        
        # Sidebar filters
        st.sidebar.header("Filters")
        date_range = st.sidebar.date_input(
            "Date Range",
            [datetime.now() - timedelta(days=30), datetime.now()]
        )
        
        # Main metrics
        self.show_key_metrics()
        
        # Detailed sections
        col1, col2 = st.columns(2)
        
        with col1:
            self.show_job_stats()
            self.show_skills_analysis()
        
        with col2:
            self.show_connection_stats()
            self.show_success_rate()
            
        # Resume Optimization Recommendations
        st.header("Resume Optimization Recommendations")
        self.show_resume_recommendations()
        
        # Recent Activity Log
        st.header("Recent Activity")
        self.show_activity_log()
        
    def show_key_metrics(self):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            jobs_parsed = len(self.db_manager.get_all_jobs())
            st.metric("Total Jobs Parsed", jobs_parsed)
            
        with col2:
            stats = self.connection_tracker.get_connection_stats()
            st.metric("Connection Requests Sent", stats.get('SENT', 0))
            
        with col3:
            st.metric("Accepted Connections", stats.get('ACCEPTED', 0))
            
        with col4:
            acceptance_rate = (stats.get('ACCEPTED', 0) / stats.get('SENT', 1)) * 100
            st.metric("Acceptance Rate", f"{acceptance_rate:.1f}%")
            
    def show_job_stats(self):
        st.subheader("Jobs by Company")
        jobs_df = pd.DataFrame(self.db_manager.get_all_jobs())
        if not jobs_df.empty:
            fig = px.bar(
                jobs_df['company'].value_counts().head(10),
                title="Top Companies with Open Positions"
            )
            st.plotly_chart(fig)
            
    def show_skills_analysis(self):
        st.subheader("Most Requested Skills")
        skills = self.db_manager.get_required_skills()
        if skills:
            fig = px.pie(
                values=list(skills.values()),
                names=list(skills.keys()),
                title="Top Required Skills"
            )
            st.plotly_chart(fig)
            
    def show_connection_stats(self):
        st.subheader("Connection Request Status")
        stats = self.connection_tracker.get_connection_stats()
        fig = go.Figure(data=[
            go.Bar(x=list(stats.keys()), y=list(stats.values()))
        ])
        st.plotly_chart(fig)
        
    def show_resume_recommendations(self):
        recommendations = self.db_manager.get_resume_recommendations()
        if recommendations:
            for rec in recommendations:
                with st.expander(f"Recommendation for {rec['job_title']} at {rec['company']}"):
                    st.write(f"**Missing Skills:** {', '.join(rec['missing_skills'])}")
                    st.write(f"**Experience Gap:** {rec['experience_gap']} years")
                    st.write(f"**Suggested Improvements:** {rec['suggestions']}")
                    
    def show_activity_log(self):
        activities = self.connection_tracker.get_recent_activities()
        if activities:
            for activity in activities:
                st.text(f"{activity['timestamp']} - {activity['action']}: {activity['details']}")

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()