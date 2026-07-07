import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

st.title("Job Search Tool")
search_keyword = st.text_input("Enter Job Title:")
location = st.text_input("Enter Location:")

if st.button("Search"):
    if search_keyword and location:
        with st.spinner('Searching...'):

            jobs = scrape_jobs(
                site_name=["indeed", "linkedin"],
                search_term=search_keyword,
                location=location,
                country_indeed='USA',
                results_wanted=20,
                hours_old=72
            )
cols = ['title'] + [c for c in jobs.columns if c not in ['title', 'id']] + ['id']            jobs = jobs[cols]
            st.success(f"Found {len(jobs)} jobs!")
            st.dataframe(
            jobs,
            column_config={
                "job_url": st.column_config.LinkColumn(
                "Job URL",
                display_text="View Job"
            ),
            "job_url_direct": st.column_config.LinkColumn(
            "Direct URL",
            display_text="Apply Here"
        ),
    },
    hide_index=True
)
            
            csv = jobs.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "jobs.csv", "text/csv")
    else:
        st.warning("Please enter both a job title and a location.")