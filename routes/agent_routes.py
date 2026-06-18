from fastapi import APIRouter, HTTPException
from database import agent_db
from utils import pydantic_classes

manage_agents = agent_db.AgentDB()
router = APIRouter()


@router.post("/", status_code=201)
def add_agent(body: pydantic_classes.NewAgent):
    try:
        agent = manage_agents.create_agent(body.model_dump())
        return agent
    except KeyError as e:
        raise HTTPException(
            status_code=422, detail=f"you entered: {body.agent_rank}, {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.get("/")
def read_all_agents():
    agents = manage_agents.get_all_agents()
    return agents


@router.get("/{id}")
def read_agent_by_id(id: int):
    try:
        agent = manage_agents.get_agent_by_id(id)
        if agent:
            return agent
        raise HTTPException(status_code=404, detail="Agent not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.get("/{id}/performance")
def read_agents_performance(id: int):
    try:
        agent = manage_agents.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        performance = manage_agents.get_agent_performance(id)
        print(performance)
        return performance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.put("/{id}", status_code=201)
def update_agent(id: int, body: pydantic_classes.UpdateAgent):
    try:
        agent = manage_agents.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        update = manage_agents.update_agent(id, body.model_dump(exclude_none=True))
        if update["status"] == "No change took effect.":
            raise HTTPException(status_code=400, detail="Failed to update")
        return update
    except ValueError as e:
        raise HTTPException(
            status_code=422, detail=f"you entered: {body.agent_rank}, {e}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.put("/{id}/deactivate", status_code=201)
def deactivate_agent(id: int):
    try:
        agent = manage_agents.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        deactivate = manage_agents.deactivate_agent(id)
        if deactivate["status"] == "Failed to deactivate.":
            raise HTTPException(status_code=400, detail="Failed to deactivate")
        return deactivate
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")
