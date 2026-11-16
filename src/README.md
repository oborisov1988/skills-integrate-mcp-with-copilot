# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Join a waitlist when an activity is full
- Automatically promote the first waitlisted student when a confirmed participant unregisters

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get activities, confirmed participants, and waitlists               |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up or join the waitlist when full                               |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister or leave the waitlist                                     |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of confirmed student emails
   - Ordered list of waitlisted student emails

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
