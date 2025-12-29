import json
from crewai import Crew, Task, Process
from agents.claim_agent import claim_agent
from memory.redis.writer import store_agent1_output


claim_analysis_task = Task(
    description=(
        "You are given a claim below:\n\n"
        "{claim}\n\n"
        "You MUST call the `spacy_claim_analyzer_tool` using the claim text above as input. "
        "Do not analyze the task instructions or expected output.\n\n"
        "After using the tool, return the result exactly as JSON."
    ),
    expected_output=(
        
    "Return ONLY valid JSON with keys: "
    "entities, sensationalism_score, analysis. "
    "No explanation, no markdown."
        ),
    agent=claim_agent
)


claim_crew = Crew(
    agents=[claim_agent],
    tasks=[claim_analysis_task],
    process=Process.sequential
)

if __name__ == "__main__":
    result = claim_crew.kickoff(
        inputs={"claim": "On Monday, President Joe Biden met Elon Musk at the White House in Washington to discuss a new SpaceX project with NASA"}
    )
    print(result)
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            raise ValueError(
            "Agent-1 output is a string but not valid JSON. "
            "Ensure the agent returns strict JSON.")
        
    store_agent1_output(claim_id="001", output=result)