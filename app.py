import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

st.set_page_config(page_title="Job Search Tool", page_icon="🔍", layout="wide")

st.title("🔍 Job Search Tool")
st.markdown("Find the latest job postings from top platforms.")

with st.sidebar:
    st.header("Filters")
    with st.form("search_form"):
        search_keyword = st.text_input("Job Title", placeholder="e.g. Data Scientist")
        location = st.text_input("Location", placeholder="e.g. New York")
        
        col1, col2 = st.columns(2)
        with col1:
            usa_only = st.checkbox("All Over USA")
        with col2:
            remote_only = st.checkbox("Remote Only")
        
        submitted = st.form_submit_button("Search Jobs", type="primary")

st.divider()

if submitted:
    if search_keyword and (location or usa_only or remote_only):
        with st.spinner('Scraping the latest jobs for you...'):
            try:
                final_location = "USA" if usa_only else location
                
                jobs = scrape_jobs(
                    site_name=["indeed", "linkedin"],
                    search_term=search_keyword,
                    location=final_location,
                    is_remote=remote_only,
                    country_indeed='USA',
                    results_wanted=20,
                    hours_old=72
                )
                
                if remote_only and not jobs.empty:
                    if 'is_remote' in jobs.columns:
                        jobs = jobs[jobs['is_remote'] == True]
                
                if not jobs.empty:
                    st.success(f"Found {len(jobs)} jobs!")
                    
                    def format_salary(row):
                        min_val = row.get('min_amount')
                        max_val = row.get('max_amount')
                        
                        if pd.notnull(min_val) and pd.notnull(max_val):
                            return f"${min_val:,.0f} - ${max_val:,.0f}"
                        elif pd.notnull(min_val):
                            return f"${min_val:,.0f}+"
                        else:
                            return "Not Disclosed"

                    jobs['salary_range'] = jobs.apply(format_salary, axis=1)
                    
                    cols = ['title', 'company', 'location', 'salary_range', 'is_remote', 'job_url'] 
                    display_df = jobs[[c for c in cols if c in jobs.columns]]
                    
                    st.dataframe(
                        display_df,
                        column_config={
                            "job_url": st.column_config.LinkColumn("Apply", display_text="Open Link"),
                            "salary_range": "Salary Range",
                            "is_remote": st.column_config.CheckboxColumn("Remote"),
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("No jobs found matching your criteria. Try adjusting your filters.")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a Job Title and a Location (or check USA/Remote).")

st.markdown("---")

st.divider()

st.markdown(
"""
    <div style='text-align: center; color: #808080;'>
        <p> Developed by <b>Nikhil Elpula</b></p>
        <p>
            <a href="https://www.linkedin.com/in/nikhil-elpula-6686a9180/" style='color: #4A90E2; text-decoration: none;'>LinkedIn</a> | 
            <a href="https://nikhil-yv.github.io/nikhil-yv/" style='color: #4A90E2; text-decoration: none;'>Portfolio</a> | 
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)