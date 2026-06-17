from mysql import connector


class DB_connection:
    @staticmethod
    def get_connection():
        return connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="1234",
            database="Intelligence_db",
        )

    @staticmethod
    def create_database():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        sql = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
        cursor.execute(sql)

        cursor.close()
        cursor.close()
        print("Database created successfully.")

    @staticmethod
    def create_tables():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        sql_agents = """CREATE TABLE IF NOT EXISTS agents(
        id                  INT             PRIMARY KEY AUTO_INCREMENT,
        name                VARCHAR(25),
        speciality          VARCHAR(25),
        is_active           BOOLEAN         DEFAULT true,
        completed_missions  INT             DEFAULT 0,
        failed_missions     INT             DEFAULT 0,
        agent_rank          ENUM("Junior", "Senior", "Commander")
        )"""

        sql_missions = """CREATE TABLE IF NOT EXISTS missions(
        id                  INT             PRIMARY KEY AUTO_INCREMENT,
        title               VARCHAR(25),
        description         TEXT,
        | 1 | `id` | INT | Primary Key, Auto Increment |
# | 2 | `title` | VARCHAR(25) |
# | 3 | `description` | TEXT |
# | 4 | `location` | VARCHAR(100) |
# | 5 | `difficulty` | INT | Between 1 - 10 only |
# | 6 | `importance` | INT | Between 1 - 10 only |
# | 7 | `status` | VARCHER | Default: NEW |
# | 8 | `risk_level` | VARCHER(8) | Calculated by system |
# | 9 | `assigned_by_agent_id` | INT | Default: NULL
        )"""


        cursor.execute(sql_agents)
        cursor.execute(sql_missions)

        cursor.close()
        cursor.close()
        print("Tables created successfully.")


DB_connection.create_database()
