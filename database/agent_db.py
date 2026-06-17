import db_connection

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

            # return AgentDB.get_agent_by_id(agents_id)
            return agents_id
        except KeyError as e:
            raise(f"Data missing: {e}")
        except Exception as e:
            if e.__dict__["errno"] == 1265:
                raise KeyError("Invalid agent rank, please enter one of these ranks: Junior / Senior / Commander")
        
        finally:
            cursor.close()
            conn.close()

# new_agent = {"name": "david", "specialty": "a reports", "agent_rank": "Junior"}
# print(AgentDB.create_agent(new_agent))