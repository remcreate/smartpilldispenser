import streamlit as st
import pyrebase4
from datetime import time

# ---------- FIREBASE CONFIG ----------
firebaseConfig = {
    "apiKey": "AIzaSyDIbnJZqYQPsZrOeRL-t50kVtm6GUI7ij8",
    "authDomain": "smartpill-46c99.firebaseapp.com",
    "databaseURL": "https://smartpill-46c99-default-rtdb.firebaseio.com/",
    "storageBucket": "smartpill-46c99.firebasestorage.app"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

st.title("💊 Smart Pill Dispenser")
st.write("Add medicine and schedule time:")

# Input medicine name
medicine_name = st.text_input("Medicine Name")

# Input time
pill_time = st.time_input("Select Time", value=time(8, 0))

# Button to add
if st.button("Add Medicine"):
    if medicine_name.strip() == "":
        st.warning("Enter medicine name!")
    else:
        # Convert time to HH:MM format
        t_str = pill_time.strftime("%H:%M")
        # Push to Firebase
        db.child("pill_schedule").child("user1").push({"name": medicine_name, "time": t_str})
        st.success(f"{medicine_name} added at {t_str}")

# Display current schedule
schedule = db.child("pill_schedule").child("user1").get().val()
if schedule:
    st.subheader("📅 Current Schedule")
    for key, entry in schedule.items():
        st.write(f"⏰ {entry['time']} - {entry['name']}")
