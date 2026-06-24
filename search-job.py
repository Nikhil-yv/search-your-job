from jobspy import scrape_jobs
import pandas as pd

def get_jobs(search_keyword, location):
    print(f"Searching for {search_keyword} in {location}...")
    
    # Scrape jobs from multiple platforms
    jobs = scrape_jobs(
        site_name=["dice", "indeed", "linkedin", "zip_recruiter", "monster"],
        search_term=search_keyword,
        location=location,
        results_wanted=20,
        hours_old=72 # Limits to jobs posted in last 3 days (Recent)
    )
    
    # Save to a CSV file
    jobs.to_csv("jobs_output.csv", index=False)
    print(f"Success! Found {len(jobs)} jobs. Saved to jobs_output.csv")
    return jobs

# Example: Run the search
if __name__ == "__main__":
    kw = input("Enter Job Title: ")
    loc = input("Enter Location: ")
    get_jobs(kw, loc)