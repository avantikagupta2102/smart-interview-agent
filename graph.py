import os
from dotenv import load_dotenv

# Load keys before anything else
load_dotenv()

# Direct module file imports
from agents.resume_agent import analyze_resume
from agents.interview_agent import generate_questions
from agents.skill_gap import analyze_skill_gap
from agents.roadmap_agent import generate_roadmap


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