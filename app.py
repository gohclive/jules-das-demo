import streamlit as st
import sqlite3
import datetime

DB_NAME = "bookings.db"

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create slots table
    c.execute('''
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY,
            time_slot TEXT NOT NULL UNIQUE,
            capacity INTEGER NOT NULL,
            bookings_count INTEGER NOT NULL DEFAULT 0
        )
    ''')
    # Create bookings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            slot_id INTEGER,
            FOREIGN KEY (slot_id) REFERENCES slots (id)
        )
    ''')
    conn.commit()
    conn.close()

def populate_slots():
    """Populates the slots table with initial time slots if it's empty."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM slots")
    if c.fetchone()[0] == 0:
        slots = [
            ("3:00 PM - 3:15 PM", 15),
            ("3:15 PM - 3:30 PM", 15),
            ("3:30 PM - 3:45 PM", 15),
            ("3:45 PM - 4:00 PM", 15),
            ("4:00 PM - 4:15 PM", 15),
            ("4:15 PM - 4:30 PM", 15),
            ("4:30 PM - 4:45 PM", 15),
        ]
        c.executemany("INSERT INTO slots (time_slot, capacity) VALUES (?, ?)", slots)
        conn.commit()
    conn.close()


def main():
    st.title("🎉 Event Information and Massage Booking 🎉")

    # --- Event Information Section ---
    st.header("Event Details")
    st.markdown("**Place:** Sentosa")
    st.markdown("**Time:** 3pm - 5pm")

    st.header("Layout of Event")
    st.image("https://placehold.co/600x400", caption="Event Layout Placeholder")

    st.header("Activities")
    st.markdown("""
    - Activity 1: Welcome & Registration
    - Activity 2: Keynote Speech
    - Activity 3: Interactive Workshops
    - Activity 4: Networking Session
    - Activity 5: Closing Remarks
    """)

    st.header("Schedule of Event")
    schedule_data = {
        "Time": ["3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM"],
        "Event Name": ["Welcome & Registration", "Keynote Speech", "Massage Sessions Begin", "Networking", "Closing Remarks"]
    }
    st.table(schedule_data)

    # --- Divider ---
    st.markdown("---")

    # --- Massage Booking System ---
    st.header("Massage Booking")

    available_slots = get_available_slots()
    if not available_slots:
        st.warning("All massage slots are fully booked.")
        return

    slot_options = [f"{slot[1]} ({slot[3]}/{slot[2]} booked)" for slot in available_slots]
    selected_slot_str = st.selectbox("Select a time slot:", slot_options)

    user_name = st.text_input("Enter your name to book:")

    if st.button("Book Massage"):
        # Extract the time slot string from the selection
        time_slot_str = selected_slot_str.split(" (")[0]

        # Get the corresponding slot from the database
        slot_to_book = get_slot_by_time(time_slot_str)

        handle_booking(user_name, slot_to_book)

def get_available_slots():
    """Fetches all slots that are not yet full."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM slots WHERE bookings_count < capacity ORDER BY id")
    slots = c.fetchall()
    conn.close()
    return slots

def get_slot_by_time(time_slot_str):
    """Fetches a single slot's details by its time string."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM slots WHERE time_slot=?", (time_slot_str,))
    slot = c.fetchone()
    conn.close()
    return slot

def is_user_booked(name):
    """Checks if a user has already booked a slot."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE name=?", (name,))
    booking = c.fetchone()
    conn.close()
    return booking is not None

def create_booking(name, slot_id):
    """Creates a new booking and updates the slot count."""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, slot_id) VALUES (?, ?)", (name, slot_id))
        c.execute("UPDATE slots SET bookings_count = bookings_count + 1 WHERE id=?", (slot_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False

def handle_booking(name, slot):
    """Handles the logic for booking a massage slot."""
    if not name.strip():
        st.warning("Please enter your name.")
        return

    if is_user_booked(name.strip()):
        st.error(f"'{name.strip()}' has already booked a massage. Each person can only book one slot.")
        return

    if slot[3] >= slot[2]:
        st.error(f"Sorry, the {slot[1]} slot is now full.")
        return

    if create_booking(name.strip(), slot[0]):
        st.success(f"Success! You have booked the {slot[1]} massage slot.")
        st.balloons()


if __name__ == "__main__":
    init_db()
    populate_slots()
    main()