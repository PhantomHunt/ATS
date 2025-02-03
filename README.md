ATS Using LLM
Description
This is an implementation of an Applicant Tracking System (ATS) using Large Language Models (LLM). The system parses job descriptions and resumes in different formats (PDF, DOC, TXT), extracts structured details from resumes, and analyzes them against job descriptions. The analysis includes a suitability score and breakdown based on specific criteria, such as skills, experience, and education.

Author
B M Vinjit
Date: 29th January 2025
Features
Parse job descriptions and resumes in PDF, DOC, and TXT formats.
Extract structured details from resumes, including name, skills, experience, education, and certifications.
Analyze resume alignment with the job description using OpenAI's GPT model.
Generate analysis results and save them as text files.
Visualize suitability scores for all candidates (optional).
Prerequisites
To run this project, you need to have the following installed:

Python 3.x
pip (Python's package installer)
Additionally, you'll need the following Python libraries:

openai
pdfplumber
matplotlib
python-dotenv
logging
You can install the required libraries using the following command:
pip install -r requirements.txt 

Setup
Clone the repository:

git clone https://github.com/PhantomHunt/ATS.git
cd ATS
Create a .env file to store your OpenAI API key:

API_KEY=your-openai-api-key
Place your resumes and job description:

Store resumes in the Resumes/ folder.
Add your job description file (JD.pdf or .txt) in the root directory of the project.
Usage
Running the ATS
To run the ATS, execute the main.py script:

python main.py
This will:

Parse resumes and job descriptions.
Analyze the resumes against the job description.
Save the analysis in individual .txt files in the Analysis/ folder.
Visualize Scores (Optional)
To visualize the suitability scores of all candidates, uncomment the visualize_scores() function in the main() function of the script.

Folder Structure
The folder structure should look like this:

ATS/
│
├── Resumes/                 # Folder containing resume files
│   ├── candidate1.pdf
│   ├── candidate2.txt
│   └── ...
├── JD.pdf                   # Job description file
├── weightage_config.json    # Scoring weights configuration (optional)
├── .env                     # API Key configuration
├── main.py                  # Main script to run the ATS
├── requirements.txt         # Python libraries that are required
└── README.md                # Project documentation
Functions
1. parse_pdf(file_path: str) -> str
Extracts text from a PDF file.
2. parse_text_file(file_path: str) -> str
Reads and extracts text from a text file.
3. extract_resume_details(resume_text: str) -> Dict[str, Any]
Extracts structured details from resume text using an LLM.
4. parse_resumes_and_jd(resume_folder: str, jd_file: str) -> Tuple[str, List[Dict[str, Any]]]
Parses the job description and resumes from specified folders and files.
5. get_scoring_weights() -> Dict[str, Any]
Loads scoring weights from the 'weightage_config.json' file.
6. analyze_resumes_with_llm(job_description: str, resumes: List[Dict[str, Any]]) -> List[Dict[str, Any]]
Analyzes resumes against the job description using an LLM.
7. display(results: List[Dict[str, Any]])
Saves the analysis of candidates to individual text files in the 'Analysis' folder.
8. visualize_scores(results: List[Dict[str, Any]])
(Optional) Visualizes suitability scores for all candidates using a bar chart.
Logging
Logs are stored using Python's built-in logging module. You can modify the logging level or configuration as needed to capture more or less detailed logs.

Notes
Ensure your OpenAI API key is properly set in the .env file.
The model gpt-4o-mini is used for resume analysis. You can modify the model depending on your OpenAI account's capabilities.
The weightage_config.json file is optional and used for scoring weights configuration.
License
This project is licensed under the MIT License - see the LICENSE file for details.
