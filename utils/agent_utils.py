def is_alowed_agent_columns(k: str):
    alowed_agent_columns =["name", "specialty", "is_active", "completed_missions", "failed_missions", "agent_rank"]
    return k in alowed_agent_columns