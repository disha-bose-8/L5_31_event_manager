"""manage event creation, guest registration, and event reports"""

import os
import pickle
import random
from datetime import date

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """create an event and return its details"""
    if guests is None:
        guests = []
    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": guests,
    }
    return events[event_name]


def register_guest(event_name, guest):
    """register a guest for an event"""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """return the number of seats remaining at an event"""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """return whether an event is upcoming or completed"""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order="name"):
    """return a sorted list of guests for an event"""
    names = sorted(events[event_name]["guests"],
                   reverse=sort_order == "reverse")
    return ", ".join(names)


def save_events(file_name="events.pkl"):
    """Save all events to a file."""
    with open(file_name, "wb") as f:
        pickle.dump(events, f)


def load_events(file_name="events.pkl"):
    """Load events from a file and return them."""
    with open(file_name, "rb") as f:
        return pickle.load(f)


def print_badges(event_name):
    """Print badges for the specified event."""
    os.system("lp badges_" + event_name + ".txt")


def main():
    """Run the event management demonstration."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop",2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "name"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    winner = random.choice(events["Tech Meetup"]["guests"])
    print("Lucky draw winner:", winner)
    save_events()
    restored = load_events() # reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])

main()
