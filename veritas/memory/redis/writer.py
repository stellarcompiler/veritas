import json
from .client import r
from .keys import agent1_key

def store_agent1_output(claim_id: str, output: dict) -> str:

    if not isinstance(output, dict):
        raise TypeError(
            f"store_agent1_output expects dict, got {type(output)}"
        )

    key = agent1_key(claim_id)

    r.hset(
        key,
        mapping={
            "entities": json.dumps(output.get("entities", [])),
            "sensationalism_score": output.get("sensationalism_score", 0),
            "analysis": output.get("analysis", "")
        }
    )

    r.expire(key, 3600)

    print(f"[REDIS] Agent-1 memory stored at → {key}")
    return key
