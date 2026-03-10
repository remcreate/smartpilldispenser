import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import time
import json

# ---------- FIREBASE INITIALIZATION ----------
if not firebase_admin._apps:
    # Load Firebase secrets from Streamlit
    cred_dict = st.secrets["FIREBASE"]

    # Convert private_key from string with literal \n to actual newlines
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    # Initialize Firebase Admin
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartpill-46c99-default-rtdb.firebaseio.com/"
    })

# Reference to database
ref = db.reference("pill_schedule/user1")

# ---------- STREAMLIT UI ----------
st.title("💊 Smart Pill Dispenser")
st.write("Add medicine and schedule time:")

# Input medicine name
medicine_name = st.text_input("Medicine Name")

# Input time
pill_time = st.time_input("Select Time", value=time(8, 0))

# Add medicine button
if st.button("Add Medicine"):
    if medicine_name.strip() == "":
        st.warning("Enter medicine name!")
    else:
        t_str = pill_time.strftime("%H:%M")
        ref.push({"name": medicine_name, "time": t_str})
        st.success(f"{medicine_name} added at {t_str}")

# Display current schedule
schedule = ref.get()
if schedule:
    st.subheader("📅 Current Schedule")
    for key, entry in schedule.items():
        st.write(f"⏰ {entry['time']} - {entry['name']}")