import streamlit as st

def app():
    st.title("Sentosa Beach Day Massage Booking")
    st.subheader("July 28, 2025")
    st.subheader("Siloso Beach, Sentosa")

    st.table({
        "Time": ["12:00 PM", "1:00 PM", "2:00 PM - 5:00 PM", "6:00 PM"],
        "Event": ["Arrival & Welcome", "Lunch", "Free & Easy (Massage)", "Dinner & Departure"]
    })

    with st.expander("Directions to Sentosa"):
        st.write("Placeholder text for directions to Sentosa.")

    with st.expander("Directions to Siloso Beach"):
        st.write("Placeholder text for directions to Siloso Beach.")

    st.image("assets/qr_code_placeholder.png", caption="Scan for more details")

    st.info("Ready to book your massage? Navigate to the Sign Up page!")
