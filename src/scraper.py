
from datetime import date
import json
import os
import requests
import html
from bs4 import BeautifulSoup

from src.models import Job


def _get_jobs() -> list:
    """Fetches job listings from the Greenhouse API for the configured board.

    Returns:
        list: A list of job dictionaries.
    """
    board_token = os.environ.get("GREENHOUSE_BOARD_TOKEN", "airbnb")
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['jobs']
    else:
        raise Exception(f"Failed to fetch jobs: {response.status_code} - {response.text}")

def _clean_job_content(raw_html) -> str:
    """Cleans and removes HTML characters from job content

    Args:
        raw_html (str): The raw HTML content of the job description.

    Returns:
        str: The cleaned text content of the job description.
    """
    # 1. Decode HTML entities (e.g., &lt; becomes <)
    decoded_html = html.unescape(raw_html)
    
    # 2. Parse with BeautifulSoup
    soup = BeautifulSoup(decoded_html, 'html.parser')
    
    # 3. Get clean text
    # separator=' ' ensures words don't get smashed together when tags are removed
    clean_text = soup.get_text(separator=' ', strip=True)
    
    return clean_text

def _load_seen_jobs(filename="seen_jobs.json") -> list:
    """Loads the seen jobs ID from a JSON file. If the file doesn't exist, it returns an empty list.
    
    Args:
        filename (str, optional): The name of the file to load the seen jobs from. Defaults to "seen_jobs.json".

    Returns:
        list: A list of seen job IDs.
    """
    directory = "./data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def _save_seen_jobs(seen_jobs, filename="seen_jobs.json") -> None:
    """Saves the seen jobs ID as a list

    Args:
        seen_jobs (list): List of seen job IDs.
        filename (str, optional): The name of the file to save the seen jobs. Defaults to "seen_jobs.json".
    
    Returns:
        None
    """
    directory = "./data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as f:
        json.dump(seen_jobs, f, indent=4)

def scrape_jobs() -> list:
    """Scrape jobs and return a list of job objects if any new jobs were found.

    Returns:
        list: A list of found jobs that were not previously surfaced.
    """
    jobs = _get_jobs()
    seen_jobs = _load_seen_jobs()
    new_jobs = []
    
    for job in jobs:
        if job["location"]["name"] == "Canada" or "remote" in job["location"]["name"].lower():
            if job['id'] not in seen_jobs:
                clean_content = _clean_job_content(job["content"])
                department_name = None
                if job['departments'] and len(job['departments']) > 1:
                    department_name = f"{job['departments'][0]['name']} - {job['departments'][1]['name']}"
                elif job['departments'] and len(job['departments']) == 1:
                    department_name = job['departments'][0]['name']
                new_jobs.append(Job(
                    greenhouse_id=int(job['id']),
                    internal_id=job['internal_job_id'],
                    title=job['title'],
                    department=department_name,
                    location=job['location']['name'],
                    content=clean_content,
                    url=job["absolute_url"],
                    date_updated=date.fromisoformat(job["updated_at"].split("T")[0])
                ))
                seen_jobs.append(job['id'])
    
    _save_seen_jobs(seen_jobs)
    return new_jobs

if __name__ == "__main__":
    new_jobs = scrape_jobs()
    for job in new_jobs:
        print(job.title, job.location)