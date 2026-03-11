import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import time

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

# Allow any minute by setting step=60 (seconds)
pill_time = st.time_input("Select Time", value=time(8, 0), step=60)

if st.button("Add Medicine"):
    if medicine_name.strip() == "":
        st.warning("Enter medicine name!")
    else:
        t_str = pill_time.strftime("%H:%M")
        ref.push({"name": medicine_name, "time": t_str})
        st.success(f"{medicine_name} added at {t_str}")

# ---------- DISPLAY CURRENT SCHEDULE ----------
schedule = ref.get()
if schedule:
    st.subheader("📅 Current Schedule")
    for key, entry in schedule.items():
        st.write(f"⏰ {entry['time']} - {entry['name']}")