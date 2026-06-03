import os
import sys
from typing import TypedDict
from dotenv import load_dotenv

# 1. ADD THIS MISSING IMPORT LINE TO FIX THE NAMEERROR
from langgraph.graph import StateGraph, START, END

# Load keys before anything else
load_dotenv()

# Force python path mapping to clear out broken internal cloud cache keys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Direct clean module script imports
import agents.resume_agent as resume_agent
import agents.interview_agent as interview_agent
import agents.skill_gap as skill_gap
import agents.roadmap_agent as roadmap_agent

# Point your workflow actions to use the exact object targets
analyze_resume = resume_agent.analyze_resume
generate_questions = interview_agent.generate_questions
analyze_skill_gap = skill_gap.analyze_skill_gap
generate_roadmap = roadmap_agent.generate_roadmap

class InterviewState(TypedDict):
    resume_text: str
    target_role: str
    analysis: str
    questions: str
    skill_gap: str
    roadmap: str

class InterviewState(TypedDict):
    resume_text: str
    target_role: str
    # ... rest of your state fields ...


# Now this class declaration will work perfectly!
class InterviewState(TypedDict):
    resume_text: str
    target_role: str
    # ... rest of your existing fields and StateGraph definition ...


class InterviewState(TypedDict):
    resume_text: str
    target_role: str

    analysis: str
    questions: str
    skill_gap: str
    roadmap: str


# --------------------------
# Resume Agent Node
# --------------------------

def resume_node(state):

    analysis = analyze_resume(
        state["resume_text"]
    )

    state["analysis"] = analysis

    return state


# --------------------------
# Interview Agent Node
# --------------------------

def interview_node(state):

    questions = generate_questions(
        state["resume_text"]
    )

    state["questions"] = questions

    return state


# --------------------------
# Skill Gap Agent Node
# --------------------------

def skill_gap_node(state):

    gap = analyze_skill_gap(
        state["resume_text"],
        state["target_role"]
    )

    state["skill_gap"] = gap

    return state


# --------------------------
# Roadmap Agent Node
# --------------------------

def roadmap_node(state):

    roadmap = generate_roadmap(
        state["skill_gap"]
    )

    state["roadmap"] = roadmap

    return state


# --------------------------
# Build Graph
# --------------------------

workflow = StateGraph(
    InterviewState
)

workflow.add_node(
    "resume",
    resume_node
)

workflow.add_node(
    "interview",
    interview_node
)

workflow.add_node(
    "skill_gap",
    skill_gap_node
)

workflow.add_node(
    "roadmap",
    roadmap_node
)

workflow.set_entry_point(
    "resume"
)

workflow.add_edge(
    "resume",
    "interview"
)

workflow.add_edge(
    "interview",
    "skill_gap"
)

workflow.add_edge(
    "skill_gap",
    "roadmap"
)

workflow.set_finish_point(
    "roadmap"
)

app_graph = workflow.compile()