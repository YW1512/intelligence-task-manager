from database import db_connection
from utils.agent_utils import is_alowed_agent_columns


class AgentDB:

    @staticmethod
    def create_agent(data):
        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor()

            sql = """
    INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)
    """
            values = (data["name"], data["specialty"], data["agent_rank"])

            cursor.execute(sql, values)

            conn.commit()

            agents_id = cursor.lastrowid

            return AgentDB.get_agent_by_id(agents_id)
        except KeyError as e:
            raise (f"Data missing: {e}")
        except Exception as e:
            if e.__dict__["errno"] == 1265:
                raise KeyError(
                    "Invalid agent rank, please enter one of these ranks: Junior / Senior / Commander"
                )
            else:
                raise

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_agents():
        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)

            sql = """
    SELECT * FROM agents
    """
            cursor.execute(sql)

            agents = cursor.fetchall()

            return agents
        except Exception as e:
            raise

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_agent_by_id(id):
        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)

            sql = """
    SELECT * FROM agents
    WHERE  id = %s
    """
            value = (id,)
            cursor.execute(sql, value)

            agent = cursor.fetchone()

            return agent
        except Exception:
            raise

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_agent(id, data):

        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor()
            for k, v in data.items():
                if is_alowed_agent_columns(k):
                    sql = f"""
        UPDATE agents SET  {k} = %s
        WHERE  id = %s
        """
                    values = (v, id)
                    cursor.execute(sql, values)
                else:
                    print(f"Invalid column: {k} ")

            conn.commit()

            change = cursor.rowcount

            if change:
                return {"status": f"Agent {id} successfully updated."}
            else:
                return {"status": "No change took effect."}

        except Exception as e:
            if e.__dict__["errno"] == 1265:
                raise ValueError(
                    "Invalid agent rank, please enter one of these ranks: Junior / Senior / Commander"
                )
            else:
                raise
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deactivate_agent(id):

        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor()

            sql = """
UPDATE agents SET is_active = false
WHERE  id = %s
"""
            value = (id,)
            cursor.execute(sql, value)

            conn.commit()
            change = cursor.rowcount

            if change:
                return {"status": f"Agent {id} successfully deactivated."}
            return {"status": "Failed to deactivate."}

        except Exception:
            raise

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def increment_completed(id):

        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor()

            get_number = """SELECT completed_missions
            FROM agents
            WHERE id = %s
            """
            value = (id,)
            cursor.execute(get_number, value)
            number = cursor.fetchone()[0]

            sql = """
UPDATE agents SET completed_missions = %s
WHERE id = %s
"""
            values = (number + 1, id)
            cursor.execute(sql, values)

            conn.commit()
            change = cursor.rowcount
            if change:
                return {
                    "status": f" successfully incremented agent {id}'s completed_missions."
                }
            return {"status": "Failed to increment."}

        except Exception:
            raise

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def increment_failed(id):

        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor()

            get_number = """SELECT failed_missions
            FROM agents
            WHERE id = %s
            """
            value = (id,)
            cursor.execute(get_number, value)
            number = cursor.fetchone()[0]

            sql = """
UPDATE agents SET failed_missions = %s
WHERE id = %s
"""
            values = (number + 1, id)
            cursor.execute(sql, values)

            conn.commit()
            change = cursor.rowcount
            if change:
                return {
                    "status": f" successfully incremented agent {id}'s failed_missions."
                }
            return {"status": "Failed to increment."}

        except Exception:
            raise

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_agent_performance(id):

        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)

            get_info = """SELECT completed_missions, failed_missions
            FROM agents
            WHERE id = %s
            """

            cursor.execute(get_info, (id,))
            initial_info = cursor.fetchone()

            total = initial_info["completed_missions"] + initial_info["failed_missions"]
            success_rate = 0 if total == 0 else 100 / total * initial_info["completed_missions"]

            info = {
                "completed": initial_info["completed_missions"],
                "failed": initial_info["failed_missions"],
                "total": total,
                "success_rate": success_rate,
            }

            return info

        except Exception:
            raise

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def count_active_agents():

        try:
            conn = db_connection.DBConnection.get_connection()
            cursor = conn.cursor()

            get_number = """SELECT COUNT(is_active)
            FROM agents
            WHERE is_active = true
            """

            cursor.execute(get_number)
            number = cursor.fetchone()[0]
            return number

        except Exception:
            raise

        finally:
            cursor.close()
            conn.close()
