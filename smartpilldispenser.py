import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
from datetime import time

# ---------- FIREBASE INITIALIZATION ----------

if not firebase_admin._apps:
    # Load Firebase credentials from Streamlit secrets
    cred_dict = st.secrets["FIREBASE"]
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartpill-46c99-default-rtdb.firebaseio.com/"
    })

# Reference to database
ref = db.reference("pill_schedule/user1")