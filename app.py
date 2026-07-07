import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

st.title("Job Search Tool")
search_keyword = st.text_input("Enter Job Title:")

# Create buttons in a row
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    usa_btn = st.button("All Over USA")
with col2:
    remote_btn = st.button("Remote Only")

# Dynamic location handling
if usa_btn:
    location = "USA"
else:
    location = st.text_input("Enter Location:")

if st.button("Search"):
    if search_keyword and (location or remote_btn):
        with st.spinner('Searching...'):
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin"],
                search_term=search_keyword,
                location=location if not usa_btn else "USA",
                is_remote=remote_btn,
                country_indeed='USA',
                results_wanted=20,
                hours_old=72
            )
            
            cols = ['title'] + [c for c in jobs.columns if c not in ['title', 'id']] + ['id']
            jobs = jobs[cols]
            
            st.success(f"Found {len(jobs)} jobs!")
            
            st.dataframe(
                jobs,
                column_config={
                    "job_url": st.column_config.LinkColumn("Job URL", display_text="View Job"),
                    "job_url_direct": st.column_config.LinkColumn("Direct URL", display_text="Apply Here"),
                },
                hide_index=True,
                use_container_width=True
            )
    else:
        st.warning("Please enter a job title and select a location or remote option.")