
import streamlit as st
from jobspy import scrape_jobs

st.title("Job Search Tool")

search_keyword = st.text_input("Enter Job Title:")
location = st.text_input("Enter Location:")

usa_only = st.checkbox("All Over USA")
remote_only = st.checkbox("Remote Only")

if st.button("Search"):
    if search_keyword and (location or usa_only or remote_only):
        with st.spinner('Searching...'):
            
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
        st.warning("Please enter a job title and select a location or filtering option.")