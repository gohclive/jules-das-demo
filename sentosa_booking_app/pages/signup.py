import streamlit as st
from database import get_booking_by_name, get_slot_availability, create_booking, update_booking, cancel_booking
from utils import validate_name, format_time_slot_display
from config import TIME_SLOTS

def app():
    st.title("Book or Manage Your Massage")

    name = st.text_input("Enter your full name")

    if "name_checked" not in st.session_state:
        st.session_state.name_checked = False

    if st.button("Check My Booking / Proceed to Book"):
        if validate_name(name):
            st.session_state.name_checked = True
            st.session_state.name = name
        else:
            st.error("Please enter a valid name (letters and spaces only).")
            st.session_state.name_checked = False

    if st.session_state.name_checked:
        booking = get_booking_by_name(st.session_state.name)

        if booking:
            st.write(f"Welcome back, {st.session_state.name}! You have a booking at {booking[2]}.")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Modify Booking"):
                    st.session_state.modify = True
            with col2:
                if st.button("Cancel Booking"):
                    st.session_state.cancel = True

            if "modify" in st.session_state and st.session_state.modify:
                availability = get_slot_availability()
                available_slots = {k: v for k, v in availability.items() if v > 0 or k == booking[2]}

                if not available_slots:
                    st.warning("No other slots available for modification.")
                else:
                    new_time_slot = st.radio(
                        "Select a new time slot:",
                        options=available_slots.keys(),
                        format_func=lambda slot: format_time_slot_display(slot, available_slots[slot])
                    )
                    if st.button("Update My Booking"):
                        update_booking(st.session_state.name, new_time_slot)
                        st.success(f"Your booking has been updated to {new_time_slot}.")
                        st.session_state.modify = False
                        st.experimental_rerun()

            if "cancel" in st.session_state and st.session_state.cancel:
                if st.button("Confirm Cancellation", type="primary"):
                    cancel_booking(st.session_state.name)
                    st.success("Your booking has been cancelled.")
                    st.session_state.cancel = False
                    st.experimental_rerun()
        else:
            st.write("No existing booking found. Let's get you signed up!")
            availability = get_slot_availability()
            available_slots = {k: v for k, v in availability.items() if v > 0}

            if not available_slots:
                st.warning("Unfortunately, all massage slots are currently full.")
            else:
                time_slot = st.radio(
                    "Select a time slot:",
                    options=available_slots.keys(),
                    format_func=lambda slot: format_time_slot_display(slot, available_slots[slot])
                )
                if st.button("Book My Massage"):
                    # Re-check availability before booking
                    current_availability = get_slot_availability()
                    if current_availability.get(time_slot, 0) > 0:
                        create_booking(st.session_state.name, time_slot)
                        st.success(f"Thank you, {st.session_state.name}! Your massage is booked for {time_slot}.")
                        st.experimental_rerun()
                    else:
                        st.error("Sorry, this time slot was just filled. Please select another one.")
                        st.experimental_rerun()
