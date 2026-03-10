import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import time

# ---------- FIREBASE INITIALIZATION ----------
if not firebase_admin._apps:
    cred_dict = dict(st.secrets["FIREBASE"])
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartpill-46c99-default-rtdb.firebaseio.com/"
    })

ref = db.reference("pill_schedule/user1")

# ---------- STREAMLIT PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Pill Dispenser",
    page_icon="💊",
    layout="centered"
)

# ---------- CENTERED LOGO ----------
logo_url = "https://YOUR_LOGO_URL_HERE.png"  # Replace with your logo URL or use st.image with local file

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{logo_url}" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- TITLE ----------
st.title("💊 Smart Pill Dispenser")
st.write("Add medicine and schedule time:")

# ---------- INPUT FORM ----------
medicine_name = st.text_input("Medicine Name")
pill_time = st.time_input("Select Time", value=time(8, 0))

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