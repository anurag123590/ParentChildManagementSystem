# Parent-Child Management Application

This application allows parents to register, manage their profiles, and add child information. The application consists of several functionalities including parent registration, login, profile management, and child management. Below are the functional requirements and the setup instructions.

## Functional Requirements

### 1. Parent Registration
- **Endpoint for parent registration:** Allows a new parent user to create an account by providing necessary details such as email, password, etc.
- **Send an email to the parent with an activation link:** After registration, the system sends an email containing an activation link to the provided email address to ensure it is valid.

curl --location --request PUT 'http://localhost:8000/children/12/' \
--header 'Content-Type: application/json' \
--header 'accept: application/json' \
--data '{
  "name": "Gobi"
}

HOST:localhost
PORT: 8000
ENDPOINT: /register
PAYLOAD: {
    "first_name": "Satish JI",
    "email":"nomadmodeon@gmail.com",
    "password":"1298434",
    "pincode": "704160",
    "last_name":"Kanjilal",
    "body":"yahoo"
}


### 2. Account Activation

 **Send an email to the parent with an activation link:** After registration, the system sends an email containing an activation link to the provided email address to ensure it is valid.

HOST:localhost
PORT: 8000
ENDPOINT: /activate/{activation key}
PAYLOAD: {
    "first_name": "Satish JI",
    "email":"nomadmodeon@gmail.com",
    "password":"1298434",
    "pincode": "704160",
    "last_name":"Kanjilal",
    "body":"yahoo"

}


- 
### 2. Parent Login
- **Endpoint for parent login using email and password:** Authenticates the parent by verifying the email and password against the records in the database. Upon successful authentication, the parent can access their account and other secured endpoints.
- **Implement authentication and authorization using JWT tokens.**

HOST:localhost
PORT: 8000
ENDPOINT: /login
PAYLOAD: {[{"key":"username","value":"nomadmodeon@gmail.com","description":"","type":"default","enabled":true},{"key":"password","value":"1298434","description":"","type":"default","enabled":true}]}

### 3. Parent Profile Management
- **Endpoint for updating the parent's profile:** Allows parents to update their profile information, such as personal details and profile photo. The profile fields include:
  - Profile photo
  - First name
  - Last name
  - Age
  - Address
  - City
  - Country
  - Pincode
- **All profile updates must be done in a single API request:** Ensures atomicity (either all updates are applied, or none are).

    HOST:localhost
    PORT: 8000
    ENDPOINT: /loginparent/profile/25/





### 4. Child Management
- **Child Information listing with search and filters:** Endpoint to list child information with filters for parent, date of addition, etc.
- **Endpoint for adding child information:** Allows parents to add information about their children. Each child is linked to the parent in the database.
- **Edit Child:** Endpoint to allow parents to edit the information of their children.
- **Notify the admin after 5 minutes of adding a child:** After adding a child, the system waits for 5 minutes and sends an email notification to the admin. This delay can be implemented using background tasks or scheduled jobs.

    HOST:localhost
    PORT: 8000
    ENDPOINT: /loginparent/profile/25/

    HOST:localhost
    PORT: 8000
    ENDPOINT: parents/25/children/

    HOST:localhost
    PORT: 8000
    ENDPOINT:parents/12/children/?skip=0&limit=10

    HOST:localhost
    PORT: 8000
    ENDPOINT:children/12/

    HOST:localhost
    PORT: 8000
    ENDPOINT:children/?parent_id=24
    

    



## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- FastAPI
- SQLAlchemy

### Installation


1. **Create and activate a virtual environment:**
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   - Install PostgreSQL and create a database.
   - Update the database configuration in `config.py` or your environment variables.

5. **Apply database migrations:**
   alembic upgrade head
   ```

### Running the Application

1. **Start the FastAPI server:**
   uvicorn main:app --reload
   ```

2. **Access the API documentation:**
   - Open your web browser and navigate to `http://localhost:8000/docs` to view the interactive API documentation.

### Additional Setup

1. **Email configuration:**
   - Set up email service configuration (SMTP settings) in `config.py` or your environment variables for sending activation and notification emails.

2. **Background tasks for email notifications:**
   - Implement background tasks using FastAPI's `BackgroundTasks` or a task queue like Celery for delayed notifications.

### Project Structure

```
parent-child-management-app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── dependencies.py
│   ├── email.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── parent.py
│   │   ├── child.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   ├── core/
│       ├── config.py
│       ├── security.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│
├── tests/
│   ├── __init__.py
│   ├── test_parent.py
│   ├── test_child.py
│
├── Dockerfile
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

### Important Files

- **`main.py`**: Entry point of the application.
- **`models.py`**: Contains the SQLAlchemy models for the database.
- **`schemas.py`**: Pydantic models for request and response bodies.
- **`crud.py`**: CRUD operations for database interactions.
- **`email.py`**: Functions for sending emails.
- **`config.py`**: Configuration settings.
- **`test_parent.py`** and **`test_child.py`**: Unit tests for the application.

By following these instructions, you should be able to set up and run the Parent-Child Management Application. Make sure to review and update the configurations as needed for your specific environment and requirements.