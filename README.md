# Streamlit Event Information and Massage Booking App

This is a simple, single-page Streamlit web application that displays event information and includes a massage booking system with a SQLite backend.

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.6+
    *   pip

2.  **Install dependencies:**
    This project requires the `streamlit` library. You can install it using pip:
    ```bash
    pip install streamlit
    ```

## How to Run the Application

1.  **Navigate to the project directory** where the `app.py` file is located.

2.  **Run the Streamlit application** from your terminal:
    ```bash
    streamlit run app.py
    ```

3.  The application will automatically open in your default web browser.

## Database

The application uses a local SQLite database file named `bookings.db`, which will be created automatically in the same directory when you run the app for the first time. It stores the time slots and user bookings.