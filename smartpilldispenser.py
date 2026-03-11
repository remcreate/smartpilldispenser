import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import re

# ---------- STREAMLIT PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Pill Dispenser",
    page_icon="💊",
    layout="centered"
)

# ---------- FIREBASE INITIALIZATION ----------
if not firebase_admin._apps:
    # Copy secrets from Streamlit
    cred_dict = dict(st.secrets["FIREBASE"])
    # Fix private_key line breaks
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    # Initialize Firebase Admin
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartpill-46c99-default-rtdb.firebaseio.com/"
    })

# Reference to user's pill schedule
ref = db.reference("pill_schedule/user1")

# ---------- TITLE ----------
st.title("💊 Smart Pill Dispenser")
st.write("Add medicine and schedule time:")

# ---------- INPUT FORM ----------
medicine_name = st.text_input("Medicine Name")
pill_time_str = st.text_input("Enter Time (HH:MM)", value="08:00")

# Function to validate time format
def is_valid_time(t):
    return re.match(r'^([01]?\d|2[0-3]):([0-5]\d)$', t)

if st.button("Add Medicine"):
    if medicine_name.strip() == "":
        st.warning("Enter medicine name!")
    elif not is_valid_time(pill_time_str.strip()):
        st.warning("Enter a valid time in HH:MM format!")
    else:
        ref.push({"name": medicine_name, "time": pill_time_str.strip()})
        st.success(f"{medicine_name} added at {pill_time_str.strip()}")

# ---------- DISPLAY CURRENT SCHEDULE ----------
schedule = ref.get()
if schedule:
    st.subheader("📅 Current Schedule")
    # Sort by time
    sorted_schedule = sorted(schedule.items(), key=lambda x: x[1]["time"])
    for key, entry in sorted_schedule:
        st.write(f"⏰ {entry['time']} - {entry['name']}")