from mysql import connector


class DBConnection:
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
        conn = DBConnection().get_connection()
        cursor = conn.cursor()

        sql = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
        cursor.execute(sql)

        cursor.close()
        cursor.close()
        print("Database created successfully.")

    @staticmethod
    def create_tables():
        conn = DBConnection().get_connection()
        cursor = conn.cursor()

        sql_agents = """CREATE TABLE IF NOT EXISTS agents(
        id                  INT             PRIMARY KEY AUTO_INCREMENT,
        name                VARCHAR(50),
        specialty          VARCHAR(50),
        is_active           BOOLEAN         DEFAULT true,
        completed_missions  INT             DEFAULT 0,
        failed_missions     INT             DEFAULT 0,
        agent_rank          ENUM("Junior", "Senior", "Commander")
        )"""

        sql_missions = """CREATE TABLE IF NOT EXISTS missions(
        id                      INT             PRIMARY KEY AUTO_INCREMENT,
        title                   VARCHAR(50),
        description             TEXT,
        location                VARCHAR(100),
        difficulty              INT             CHECK (difficulty >= 1 AND difficulty <= 10),
        importance              INT             CHECK (importance >= 1 AND importance <= 10),
        status                  VARCHAR(10)     DEFAULT "NEW",
        risk_level              VARCHAR(10),
        assigned_by_agent_id    INT             DEFAULT NULL
        )"""



        cursor.execute(sql_agents)
        cursor.execute(sql_missions)
        
        conn.commit()

        cursor.close()
        conn.close()
        print("Tables created successfully.")


# DBConnection.create_database()
# DBConnection.create_tables()
