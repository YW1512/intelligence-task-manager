from fastapi import APIRouter, HTTPException
from database import agent_db
from utils import pydantic_classes
from logs.log_config import get_custom_logger

logger = get_custom_logger(__name__)

manage_agents = agent_db.AgentDB()
router = APIRouter()


@router.post("/", status_code=201)
def add_agent(body: pydantic_classes.NewAgent):
    logger.info("POST /agents called")
    try:
        logger.info("Creating agent")
        agent = manage_agents.create_agent(body.model_dump())
        logger.info(f"Agent created successfully: id={agent["id"]}")
        return agent
    except KeyError as e:
        logger.error("User entered an invalid rank")
        raise HTTPException(
            status_code=422, detail=f"you entered: {body.agent_rank}, {e}"
        )
    except Exception as e:
        logger.exception(f"An error has ocurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.get("/")
def read_all_agents():
    logger.info("GET /agents called")
    try:
        logger.info("Reading all agents")
        agents = manage_agents.get_all_agents()
        logger.info(f"Agents viewed successfully")
        return agents
    except Exception as e:
        logger.exception(f"An error has ocurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.get("/{id}")
def read_agent_by_id(id: int):
    logger.info("GET /agents/{id} called ")
    try:
        logger.info("Getting agent")
        agent = manage_agents.get_agent_by_id(id)
        if agent:
            logger.info(f"Agent viewed successfully: id={id}")
            return agent
        logger.error(f"Agent not found: {id}")
        raise HTTPException(status_code=404, detail="Agent not found")
    except HTTPException:
        
        raise
    except Exception as e:
        logger.exception(f"An error has ocurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.get("/{id}/performance")
def read_agents_performance(id: int):
    logger.info("GET /agents/{id}/performance called")
    try:
        logger.info("Getting agent's performance")
        agent = manage_agents.get_agent_by_id(id)
        if not agent:
            logger.error(f"Agent not found: {id}")
            raise HTTPException(status_code=404, detail="Agent not found")
        performance = manage_agents.get_agent_performance(id)
        logger.info(f"Agent's performance viewed successfully: id={id}")
        return performance
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"An error has ocurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.put("/{id}", status_code=201)
def update_agent(id: int, body: pydantic_classes.UpdateAgent):
    logger.info("PUT /agents/{id} called")
    try:
        agent = manage_agents.get_agent_by_id(id)
        if not agent:
            logger.error(f"Agent not found: {id}")
            raise HTTPException(status_code=404, detail="Agent not found")

        logger.info("Updating agent")
        update = manage_agents.update_agent(id, body.model_dump(exclude_none=True))
        if update["status"] == "No change took effect.":
            logger.error("Unable to update")
            raise HTTPException(status_code=400, detail="Failed to update")
        logger.info(f"Agent updated successfully: id={id}")
        return update
    except ValueError as e:
        raise HTTPException(
            status_code=422, detail=f"you entered: {body.agent_rank}, {e}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"An error has ocurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")


@router.put("/{id}/deactivate", status_code=201)
def deactivate_agent(id: int):
    logger.info("PUT /agents/{id}/deactivate called")
    try:
        agent = manage_agents.get_agent_by_id(id)
        if not agent:
            logger.error(f"Agent not found: {id}")
            raise HTTPException(status_code=404, detail="Agent not found")

        logger.info("Deactivating agent")
        deactivate = manage_agents.deactivate_agent(id)
        if deactivate["status"] == "Failed to deactivate.":
            logger.error("Unable to deactivate")
            raise HTTPException(status_code=400, detail="Failed to deactivate")
        logger.info(f"Agent deactivated successfully: id={id}")
        return deactivate
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"An error has ocurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error has ocurred: {e}")
