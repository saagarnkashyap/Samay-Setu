import random
import time
import json
from datetime import datetime

# ------------------------
# Train Data
# ------------------------
trains = [
    {"id": "01101", "name": "Mumbai LTT - Gwalior (Weekly) Special"},
    {"id": "12951", "name": "Mumbai Rajdhani Express"},
    {"id": "22209", "name": "Mumbai Duronto Express"},
    {"id": "12009", "name": "Mumbai Shatabdi Express"},
    {"id": "19019", "name": "Mumbai Dehradun Express"}
]

routes = ["North", "South", "East", "West"]

train_priorities = {
    "Mumbai Rajdhani Express": 3,
    "Mumbai Duronto Express": 3,
    "Mumbai Shatabdi Express": 2,
    "Mumbai LTT - Gwalior (Weekly) Special": 2,
    "Mumbai Dehradun Express": 1
}

# ------------------------
# Shared State for Dashboard
# ------------------------
state = {
    "active_trains": [],
    "recommendations": [],
    "track_status": {}
}

# ------------------------
# Optimizer
# ------------------------
def optimize(batch):
    # Higher priority first, then higher delay, then earlier scheduled time
    sorted_events = sorted(
        batch,
        key=lambda e: (e["priority"], e["delay"], -e["scheduled"]),
        reverse=True
    )
    return sorted_events

# ------------------------
# Save state for dashboard
# ------------------------
def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)

# ------------------------
# Simulation Loop
# ------------------------
def run_simulation():
    print("🔄 Train simulation started...")
    while True:
        batch = []
        active = []
        track_status = {}

        for train in trains:
            event_type = random.choice(["Arrival", "Departure"])
            route = random.choice(routes)
            delay = random.choice([0, 5, 10, 15])
            scheduled_time = random.randint(1, 100)

            event = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "id": train["id"],
                "name": train["name"],
                "type": event_type,
                "route": route,
                "priority": train_priorities.get(train["name"], 1),
                "delay": delay,
                "scheduled": scheduled_time
            }

            active.append(event)
            track_status[train["name"]] = "Delayed" if delay > 0 else "On Time"

            if event_type == "Arrival":
                batch.append(event)

        # Optimizer: get top 3 recommendations
        recommendations = optimize(batch)[:3] if batch else []

        # Update shared state
        state["active_trains"] = active
        state["recommendations"] = recommendations
        state["track_status"] = track_status

        # ✅ Save state so Streamlit can read it
        save_state(state)

        print("Updated state at", datetime.now().strftime("%H:%M:%S"))
        time.sleep(5)  # every 5 seconds new cycle

if __name__ == "__main__":
    run_simulation()
