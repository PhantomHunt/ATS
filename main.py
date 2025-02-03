"""
Description : Implementation of ATS Using LLM
@Author : B M Vinjit
Date : 29 Jan 2025
"""

import openai
import logging
import json
import os
import pdfplumber
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def parse_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF file.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

    
def parse_text_file(file_path: str) -> str:
    """
    Reads and extracts text from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The extracted text with leading and trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def extract_resume_details(resume_text: str) -> Dict[str, Any]:
    """
    Extracts structured details from resume text using an LLM.

    Args:
        resume_text (str): The raw text extracted from a resume.

    Returns:
        Dict[str, Any]: A dictionary containing extracted resume details, 
                        including name, skills, experience, education, and certifications.
    """
    prompt = f"""
    Extract the following details from the resume text:
    - Name
    - Skills
    - Experience
    - Education
    - Certifications
    
    Resume Text:
    {resume_text}
    
    Provide the output in JSON format.
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in HR and resume parsing."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    try:
        extracted_data = json.loads(response.choices[0].message.content.strip("```json").strip("```"))
    except (json.JSONDecodeError, AttributeError):
        raise ValueError("Failed to parse JSON response from LLM.")

    return extracted_data


def parse_resumes_and_jd(resume_folder: str, jd_file: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Parses a job description and resumes from various file formats.

    Args:
        resume_folder (str): Path to the folder containing resume files.
        jd_file (str): Path to the job description file (PDF or text).

    Returns:
        Tuple[str, List[Dict[str, Any]]]: 
            - The job description text.
            - A list of dictionaries containing extracted resume details.
    """
    job_description = parse_pdf(jd_file) if jd_file.endswith(".pdf") else parse_text_file(jd_file)

    resumes = []
    for file_name in os.listdir(resume_folder):
        file_path = os.path.join(resume_folder, file_name)

        resume_text = None
        if file_name.endswith(".pdf"):
            resume_text = parse_pdf(file_path)
        elif file_name.endswith(".txt") or file_name.endswith(".doc"):
            resume_text = parse_text_file(file_path)

        if resume_text: 
            resume_json = extract_resume_details(resume_text)
            resume_json["name"] = file_name.rsplit(".", 1)[0]
            resumes.append(resume_json)

    return job_description, resumes


def get_scoring_weights() -> Dict[str, Any]:
    """
    Loads scoring weights from the 'weightage_config.json' file.

    Returns:
        Dict[str, Any]: A dictionary containing scoring weight configurations.
    
    Raises:
        FileNotFoundError: If the 'weightage_config.json' file is missing.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open("weightage_config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: 'weightage_config.json' file not found.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse 'weightage_config.json'. Ensure it contains valid JSON.")


def analyze_resumes_with_llm(job_description: str, resumes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyzes resumes using an LLM by comparing them against a job description.

    Args:
        job_description (str): The job description text.
        resumes (List[Dict[str, Any]]): A list of dictionaries containing parsed resume details.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the candidate name and analysis.

    Raises:
        ValueError: If the LLM response cannot be parsed or is missing expected content.
    """
    results = []
    for resume in resumes:
        prompt = f"""
        Job Description:
        {job_description}

        Candidate Resume:
        {json.dumps(resume, indent=2)}

        Analyze the candidate's alignment with the job description based on the following criteria:
        1. Match on skills.
        2. Match on experience.
        3. Match on education and certifications.
        4. Identify missing requirements.

        Provide:
        - A suitability score (out of 100) based on the criteria.
        - A breakdown of the score.
        - Recommendations for the candidate to address gaps.
        """
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        try:
            analysis = response.choices[0].message.content.strip()
        except (AttributeError, IndexError):
            raise ValueError("Error: Failed to retrieve analysis from LLM response.")

        results.append({"name": resume["name"], "analysis": analysis})
    return results


def display(results: List[Dict[str, Any]]):
    """
    Saves the analysis of candidates to individual text files in the 'Analysis' folder.

    Args:
        results (List[Dict[str, Any]]): A list of dictionaries containing candidate details,
                                         including 'name' and 'analysis'.
    
    This function creates an 'Analysis' folder (if it doesn't already exist), and saves 
    each candidate's analysis in a separate `.txt` file, named after the candidate.
    """
    os.makedirs("Analysis", exist_ok=True)

    for result in results:
        candidate_name = str(result['name']).replace(" ", "_")
        file_path = os.path.join("Analysis", f"{candidate_name}.txt")
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Candidate: {result['name']}\n")
            file.write(result['analysis'])
        
        logging.info(f"Saved analysis for {result['name']} in {file_path}")

# def visualize_scores(results: List[Dict[str, Any]]):
#     candidates = [result['name'] for result in results]
#     scores = [int(result['analysis'].split("Suitability Score:")[1].split("/100")[0]) for result in results]
#     plt.bar(candidates, scores, color='skyblue')
#     plt.xlabel('Candidates')
#     plt.ylabel('Suitability Score')
#     plt.title('Resume Suitability Scores')
#     plt.show()

def main():
    resume_folder = "Resumes"
    jd_file = "JD.pdf"
    job_description, resumes = parse_resumes_and_jd(resume_folder, jd_file)
    results = analyze_resumes_with_llm(job_description, resumes)
    display(results)
    # visualize_scores(results)

if __name__ == '__main__':
    main()
