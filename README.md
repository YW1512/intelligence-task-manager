# ShadowNet - Intelligence task manager

## An inteligence task manger system:<br>Built to create and manage agents, missons, and statistics.

<br>

## File structure:
```
intelligence-task-manager/
|
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
|
├── README.md
├── requirements.txt
└── .gitignore
```

<br>

## Table structures:

<br>

Agents table
| # | Column | Type | Constraints |
| :- | :- | :- | :- |
| 1 | `id` | INT | Primary Key, Auto Increment |
| 2 | `name` | VARCHAR(25) |
| 3 | `speciality` | VARCHAR(25) | 
| 4 | `is_active` | BOOLEAN | Default: True |
| 5 | `completed_missions` | INT | Default: 0 |
| 6 | `failed_missions` | INT | Default: 0 |
| 7 | `agent_rank` | ENUM | Allowed ranks: Junior / Senior / Commander |

<br>

Missions table
| # | Column | Type | Constraints |
| :- | :- | :- | :- |
| 1 | `id` | INT | Primary Key, Auto Increment |
| 2 | `title` | VARCHAR(25) |
| 3 | `description` | TEXT |
| 4 | `location` | VARCHAR(100) |
| 5 | `difficulty` | INT | Between 1 - 10 only |
| 6 | `importance` | INT | Between 1 - 10 only |
| 7 | `status` | VARCHER | Default: NEW |
| 8 | `risk_level` | VARCHER(8) | Calculated by system |
| 9 | `assigned_by_agent_id` | INT | Default: NULL


<br>

## Classes:

Class DB_connection:
| Method | Responsability | 
| :- | :- |
| `get_connection()` | Returns a connection to the MYSQL database |
| `create_database()` | Creates Intelligence_db if it does not exist when loading the server |
| `create_tables()` | Creates both tables if they do not exist when loading the server |

 <br>

Class AgentDB:
<br> Responsible for all SQL queries from agents table.
| Method | Responsability | 
| :- | :- |
| `create_agent(data)` | Creates a new agent, and returns his object |
| `get_all_agents()` | Returns a list of all agents |
| `get_agent_by_id(id`) | Returns an agent by ID, None if not found |
| `update_agent(id, data)` | Updates an agents info, cnnot update an id |
| `deactivate_agent(id)` | Updates an agent to not active |
| `increment_completed(id)` | Updates an agent's completed tasks amount |
| `increment_failed(id)` | Updates an agent's failed tasks amount |
| `get_agent_performance(id)` | Returns a dictionary with completed, failed, total, success_rate, keys for an agent |
| `count_active_agents()` | Returns a count of active agents |

<br>

Class MissionDB:
<br> Responsible for all SQL queries from missions table.

| Method | Responsability | 
| :- | :- |
| `create_mission(data)` | Creates a new mission, and returns it's object |
| `get_all_missions()` | Returns all missions |
| `get_mission_by_id(id)` | Returns a mission by ID, None if not found |
| `assign_mission(m_id, a_id)` | Assigns a mission to an agent |
| `update_mission_status(id, status)` | Updates a missions status |
| `get_open_missions_by_agent(id)` | Returns open missions for a given agent (With status: ASSIGNED or IN_PROGRESS) |
| `count_all_missions()` | Returns a count of all missions |
| `count_by_status(status)` | Returns a count of all missions with a given status |
| `count_open_missions()` | Returns a count of open missions |
| `count_critical_missions()` | Returns a count of CRITICAL missions |
| `get_top_agent()` | Returns the agent with the highest count of completed missions |

<br>

## System rules:

-	`rank` Must be: `Junior` or `Senior` or `Commander` - any other value raises an exception.
-   `difficulty` and `importance` Must be between `1` - `10` - any other value raises an exception.
-   `risk_level` is calculated automaticaly at mission creation, user does not send it.
-   An inactive agent (`is_active=False`) cannot be assigned missions.
-   An agent cannot have more than 3 open missions (`ASSIGNED` or `IN_PROGRESS`) at once.
-   Only a Commander ranked agent can be assigned a mission with `CRITICAL` risk level.
-   You can only assign a mission with `NEW` status.
-   An agent can only start a mission after he is assigned to it (mission's `status=ASSIGNED`), than the missions status will be `status=IN_PROGRESS`.
-   An agent can only finish a mission with `IN_PROGRESS` status, and change the status to `failed` or `completed`.
-   Only missions with status `NEW` or `ASSIGNED` can be canceled, any other status will raise an exception.

<br>

## How to run:
Before starting, make sure docker desktop is running in the background.


### 1. Create a docker container by running this command in your CMD:
`docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0`

### 2. Create a virtual environment in the proper folder, by running:
`python -m venv venv`

### 3. Enter the virtual environment, by running:
`.\venv\Scripts\Activate`

### 4. Install modules, by running:
`pip install -r requirements.txt`

### 5. Run main file:
`python main.py`