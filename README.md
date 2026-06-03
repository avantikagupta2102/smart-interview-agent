#  Smart Interview Agent

An AI-powered interview preparation platform that analyzes resumes, generates personalized interview questions, conducts voice-based mock interviews, evaluates answers, and tracks interview performance.


## Features

###  Resume Analysis
- Upload PDF resumes
- Extract resume content
- Analyze skills, strengths, weaknesses
- Suggest suitable job roles
- Resume improvement recommendations

###  AI Question Generation
- Generates interview questions based on resume content
- Personalized technical and HR questions
- Dynamic question generation using LLMs

###  Voice Mock Interview
- AI asks interview questions using Text-to-Speech
- User answers through microphone
- Speech-to-Text converts spoken responses into text

###  AI Answer Evaluation
- Evaluates interview responses
- Provides detailed feedback
- Generates interview scores

###  Performance Dashboard
- Stores interview history
- Tracks scores over time
- Displays interview analytics

###  LangGraph Workflow
- Multi-agent workflow orchestration
- Resume Analysis Agent
- Question Generation Agent
- Evaluation Agent


##  Project Architecture

```text
Resume Upload
      │
      ▼
PDF Reader
      │
      ▼
Resume Analysis Agent
      │
      ▼
Question Generation Agent
      │
      ▼
Voice Interview Agent
      │
      ▼
Speech-to-Text
      │
      ▼
Evaluation Agent
      │
      ▼
Dashboard & Analytics
```



## Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Models
- Groq API
- Llama 3.3 70B

### AI Framework
- LangGraph

### Voice Processing
- SpeechRecognition
- gTTS
- PyAudio

### Data Handling
- Pandas

### PDF Processing
- PyPDF



## Project Structure

```text
smart-interview-agent/
│
├── agents/
│   ├── resume_agent.py
│   ├── interview_agent.py
│   ├── evaluator_agent.py
│   ├── voice_agent.py
│   ├── skill_gap.py
│
├── pages/
│   ├── voice_interview.py
│   ├── dashboard.py
│
├── utils/
│   ├── pdf_reader.py
│   ├── speech_to_text.py
│   ├── save_results.py
│   ├── score_parser.py
│
├── data/
│   └── interview_history.csv
│
├── graph.py
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/avantikagupta2102/smart-interview-agent.git
```

Move into project:

```bash
cd smart-interview-agent
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

##  Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```


##  Run Application

```bash
streamlit run app.py
```

##  Future Improvements

- Real-time interview scoring
- Emotion analysis
- Video interview support
- Job-role specific interview tracks
- PDF interview report generation
- Interview performance trends
- ATS Resume Score
##  Author

**Avantika Gupta**

B.Tech Computer Science Engineering

