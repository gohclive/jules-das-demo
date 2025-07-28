import sqlite3
from sqlite3 import Error

DATABASE_NAME = "bookings.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except Error as e:
        print(e)
    return conn

def initialize_database():
    """Create the bookings table if it doesn't exist."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    time_slot TEXT NOT NULL,
                    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'active'
                )
            ''')
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

def create_booking(name, time_slot):
    """Create a new booking."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO bookings (name, time_slot) VALUES (?, ?)", (name, time_slot))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

def get_booking_by_name(name):
    """Get an active booking by name."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM bookings WHERE name = ? AND status = 'active'", (name,))
            return c.fetchone()
        except Error as e:
            print(e)
        finally:
            conn.close()

def get_bookings_for_slot(time_slot):
    """Get all active bookings for a specific time slot."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM bookings WHERE time_slot = ? AND status = 'active'", (time_slot,))
            return c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()

def get_slot_availability():
    """Get the number of available spots for each time slot."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT time_slot, COUNT(*) FROM bookings WHERE status = 'active' GROUP BY time_slot")
            counts = dict(c.fetchall())
            from config import TIME_SLOTS, MAX_CAPACITY_PER_SLOT
            availability = {slot: MAX_CAPACITY_PER_SLOT - counts.get(slot, 0) for slot in TIME_SLOTS}
            return availability
        except Error as e:
            print(e)
        finally:
            conn.close()

def update_booking(name, new_time_slot):
    """Update the time slot for an existing booking."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("UPDATE bookings SET time_slot = ? WHERE name = ? AND status = 'active'", (new_time_slot, name))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

def cancel_booking(name):
    """Cancel a booking."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("UPDATE bookings SET status = 'cancelled' WHERE name = ? AND status = 'active'", (name,))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()
