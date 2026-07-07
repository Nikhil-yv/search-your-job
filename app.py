import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

# Use Streamlit widgets instead of input()
st.title("Job Search Tool")
search_keyword = st.text_input("Enter Job Title:")
location = st.text_input("Enter Location:")

if st.button("Search"):
    if search_keyword and location:
        with st.spinner('Searching...'):
            # Call your scraping function
            jobs = scrape_jobs(
                site_name=["indeed"],
                search_term=search_keyword,
                location=location,
                results_wanted=20,
                hours_old=72
            )
            st.success(f"Found {len(jobs)} jobs!")
            st.dataframe(jobs) # Display results in the app
            
            # Optional: Provide a download button
            csv = jobs.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "jobs.csv", "text/csv")
    else:
        st.warning("Please enter both a job title and a location.")