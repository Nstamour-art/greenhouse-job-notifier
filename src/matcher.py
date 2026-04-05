from google import genai
from dotenv import load_dotenv
import json
import re
from pydantic import BaseModel
from src.models import Job, MatchedJob, UserProfile, JobMatchResult
import os

from google.genai import types

def match_jobs_to_user(jobs: list[Job], user_profile: UserProfile, resume: str) -> list[MatchedJob]:
    """Matches jobs to a user profile and resume using GenAI.

    Args:
        jobs (list[Job]): A list of Job objects to match against.
        user_profile (UserProfile): The user's profile containing their information.
        resume (str): The user's resume content.

    Returns:
        list[MatchedJob]: A list of MatchedJob objects containing the job, relevance score, and LLM explanation.
    """
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    matched_jobs = []
    
    for job in jobs:
        print(f"Matching job: {job.title} at {job.location} ...")
        # Create a prompt for the GenAI model
        prompt = f"""
        You are a job matching assistant.
        
        Given the following job description, user profile, and resume, determine how relevant the job is to the user and provide an explanation for your relevance score.
        
        Job Description:
        Title: {job.title}
        Department: {job.department}
        Location: {job.location}
        Description: {job.content}
        
        User Profile:
        Name: {user_profile.name}
        Resume Text: {resume}
        
        Please provide a relevance score between 0 and 1, where 0 means not relevant at all and 1 means highly relevant. Also, provide a brief explanation for the score.
        Return as a JSON object with the following format:
{{    "relevance_score": float,
    "explanation": string
}}
        """
        
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW)
            )
        )
        
        relevance_score = 0.0
        llm_explanation = ""
        
        if response.text:
            try:
                text = re.sub(r"```json?\s*|```\s*$", "", response.text).strip()
                result = JobMatchResult.model_validate_json(text)
                relevance_score = result.relevance_score
                llm_explanation = result.explanation
            except Exception as e:
                print(f"Failed to parse response: {e}\nRaw: {response.text}")
                continue
        if relevance_score < 0.5:
            continue
        matched_jobs.append(MatchedJob(job=job, relevance_score=relevance_score, llm_explanation=llm_explanation))
    
    return matched_jobs

if __name__ == "__main__":
    # Example usage
    user_profile = UserProfile(id=1, name="Alice")
    resume = "Experienced software engineer with a background in Python and machine learning."
    # This would normally come from the scraper
    from datetime import date
    jobs = [
        Job(
            greenhouse_id=123, 
            internal_id=456,
            title="Software Engineer", 
            department="Engineering", 
            location="San Francisco, CA", 
            content="We are looking for a skilled software engineer with experience in Python and machine learning.",
            url="https://example.com/job/123",
            date_updated=date.today(),
        )
    ]

    matched_jobs = match_jobs_to_user(jobs, user_profile, resume)
    for matched_job in matched_jobs:
        print(f"Job: {matched_job.job.title}, Relevance Score: {matched_job.relevance_score}, Explanation: {matched_job.llm_explanation}")

