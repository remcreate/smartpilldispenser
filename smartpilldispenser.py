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
    cred_dict = dict(st.secrets["FIREBASE"])
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartpill-46c99-default-rtdb.firebaseio.com/"
    })

# Reference to user's pill schedule (array of strings)
ref_times = db.reference("pill_schedule/user1/times")

# ---------- TITLE ----------
st.title("💊 Smart Pill Dispenser")
st.write("Add medicine schedule time:")

# ---------- INPUT FORM ----------
pill_time_str = st.text_input("Enter Time (HH:MM)", value="08:00")

# Validate time format
def is_valid_time(t):
    return re.match(r'^([01]?\d|2[0-3]):([0-5]\d)$', t)

if st.button("Add Medicine Time"):
    if not is_valid_time(pill_time_str.strip()):
        st.warning("Enter a valid time in HH:MM format!")
    else:
        # Get current list from Firebase (as a simple array)
        current_times = ref_times.get() or []
        if pill_time_str.strip() not in current_times:
            current_times.append(pill_time_str.strip())
            ref_times.set(current_times)
            st.success(f"Medicine scheduled at {pill_time_str.strip()}")
        else:
            st.info(f"Time {pill_time_str.strip()} is already scheduled.")

# ---------- DISPLAY CURRENT SCHEDULE ----------
schedule = ref_times.get()
if schedule:
    st.subheader("📅 Current Schedule")
    sorted_schedule = sorted(schedule)
    for t in sorted_schedule:
        st.write(f"⏰ {t}")