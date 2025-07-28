import re

def validate_name(name):
    """Checks if a name is not empty and contains only letters and spaces."""
    if not name:
        return False
    return bool(re.match("^[A-Za-z ]+$", name))

def format_time_slot_display(slot, availability):
    """Takes a time slot and its current availability and returns a formatted string for display."""
    return f"{slot} ({availability} spots left)"
