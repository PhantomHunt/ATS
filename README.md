# ATS Using LLM

## Description
This project implements an Applicant Tracking System (ATS) using Large Language Models (LLM). The system processes job descriptions and resumes in multiple formats (PDF, DOC, TXT), extracts structured information from resumes, and evaluates candidates against the job description. The evaluation includes a suitability score and detailed analysis based on skills, experience, education, and other criteria.

### Features
- Parse job descriptions and resumes in **PDF**, **TXT**, and **DOC** formats.
- Extract structured details such as **name**, **skills**, **experience**, **education**, and **certifications** from resumes.
- Use OpenAI's GPT model to analyze the alignment of resumes with the job description.
- Generate **suitability scores** and **analysis** for each candidate.
- Save the analysis of candidates into individual `.txt` files.
- Optionally, visualize the suitability scores of all candidates.

### Author
- **B M Vinjit**
- **Date**: 29th January 2025

---

## Prerequisites

To run the project, you will need:
- **Python 3.x** installed.
- **pip** (Python package installer).

### Dependencies

The following Python libraries are required:
- `openai`
- `pdfplumber`
- `matplotlib`
- `python-dotenv`
- `logging`

You can install the required libraries using:
```bash
pip install -r requirements.txt
```

## Setup
1. Clone the repository
   ```bash
   git clone https://github.com/PhantomHunt/ATS.git
   cd ATS
   ```
2. In the project directory, add OpenAI API key in the .env file:
   ```text
   API_KEY=your-openai-api-key
   ```
3. Place your job description and resumes:
   - Place your job description file (JD.pdf) in the root directory.
   - Store your resumes in the Resumes/ folder.

## Usage
Running the ATS
To run the ATS and generate the candidate analysis, execute the main.py script:
```bash
python main.py
```
This will:
- Parse the job description and resumes.
- Analyze the resumes against the job description.
- Save the analysis of each candidate as a .txt file in the Analysis/ folder.
- Visualizing Scores (Optional)
  (To visualize the suitability scores for all candidates, uncomment the visualize_scores() function in the main() function of main.py)

## Folder Structure
Ensure your project folder structure looks like this:
```bash
ATS/
│
├── Resumes/                 # Folder containing resume files
│   ├── candidate1.pdf
│   ├── candidate2.txt
│   └── ...
├── JD.pdf                   # Job description file
├── weightage_config.json    # Scoring weights configuration (optional)
├── .env                     # API Key configuration
├── requirements.txt         # List of required dependencies
├── main.py                  # Main script to run the ATS
└── README.md                # Project documentation
```

## Notes
- API Key: Make sure to set your OpenAI API key in the .env file.
- Model: This project uses gpt-4o-mini for resume analysis. You can change the model depending on your OpenAI account’s capabilities.
- Scoring Weights: The weightage_config.json file is optional and can be used for adjusting the scoring weights for analysis.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
