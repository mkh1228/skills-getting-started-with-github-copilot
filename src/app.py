"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice teamwork, shooting, and game strategy on the court",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Develop footwork, passing, and competitive play in a team setting",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Explore acting, stage performance, and dramatic storytelling",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["zoe@mergington.edu", "lucas@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Create paintings, sketches, and mixed-media artwork in a collaborative studio",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["grace@mergington.edu", "ella@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Solve scientific problems and compete in challenges across multiple disciplines",
        "schedule": "Fridays, 2:30 PM - 4:00 PM",
        "max_participants": 20,
        "participants": ["henry@mergington.edu", "charlotte@mergington.edu"]
    },
    "Debate Team": {
        "description": "Build public speaking, argumentation, and critical thinking skills",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["william@mergington.edu", "amelia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # アクティビティが存在するかチェック
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # 対象のアクティビティを取得
    activity = activities[activity_name]

    # 既に登録済みか確認
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up for this activity")

    # アクティビティが定員に達していないか確認
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # 学生をアクティビティの参加者リストに追加
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def remove_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
