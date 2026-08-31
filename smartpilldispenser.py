import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import time
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Pill Dispenser",
    page_icon="💊",
    layout="centered"
)

# --------------------------------------------------
# ACCESSIBLE AND MODERN DESIGN
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f8fb;
    }

    .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .app-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .app-title {
        color: #12304a;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0.4rem 0;
    }

    .app-subtitle {
        color: #536b7c;
        font-size: 1.15rem;
        margin-bottom: 1rem;
    }

    .section-card {
        background-color: white;
        border: 1px solid #d9e4ec;
        border-radius: 18px;
        padding: 1.4rem;
        margin: 1rem 0;
        box-shadow: 0 4px 14px rgba(25, 61, 89, 0.06);
    }

    .schedule-time {
        background-color: #e9f7f3;
        border-left: 7px solid #16856f;
        border-radius: 12px;
        padding: 13px 18px;
        color: #12304a;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 2px;
    }

    .empty-schedule {
        background-color: #fff8e6;
        border: 1px solid #f0d78c;
        border-radius: 14px;
        padding: 1.3rem;
        text-align: center;
        color: #614d18;
        font-size: 1.1rem;
    }

    div[data-testid="stTimeInput"] label,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stButton"] button {
        font-size: 1.05rem;
    }

    div[data-testid="stButton"] button {
        min-height: 48px;
        border-radius: 10px;
        font-weight: 700;
    }

    .stButton > button[kind="primary"] {
        background-color: #16856f;
        border-color: #16856f;
    }

    @media (max-width: 600px) {
        .app-title {
            font-size: 1.8rem;
        }

        .schedule-time {
            font-size: 1.15rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# FIREBASE INITIALIZATION
# --------------------------------------------------
if not firebase_admin._apps:
    firebase_credentials = dict(st.secrets["FIREBASE"])

    firebase_credentials["private_key"] = (
        firebase_credentials["private_key"].replace("\\n", "\n")
    )

    certificate = credentials.Certificate(firebase_credentials)

    firebase_admin.initialize_app(
        certificate,
        {
            "databaseURL":
            "https://smartpill-46c99-default-rtdb.firebaseio.com/"
        }
    )

# Reference to the user's medicine schedule
ref_times = db.reference("pill_schedule/user1/times")

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def get_schedule():
    """Get, clean, and sort the current schedule."""
    saved_times = ref_times.get() or []

    if not isinstance(saved_times, list):
        return []

    # Remove empty or invalid database entries
    cleaned_times = [
        str(saved_time).strip()
        for saved_time in saved_times
        if saved_time
    ]

    return sorted(set(cleaned_times))


def add_schedule(new_time):
    """Add a schedule without replacing other saved times."""
    current_times = get_schedule()

    if new_time in current_times:
        return False

    current_times.append(new_time)
    current_times.sort()
    ref_times.set(current_times)

    return True


def delete_schedule(time_to_delete):
    """Remove the selected time from Firebase."""
    current_times = get_schedule()

    updated_times = [
        saved_time
        for saved_time in current_times
        if saved_time != time_to_delete
    ]

    ref_times.set(updated_times)


def display_time(time_string):
    """Convert 24-hour time to an easier-to-read 12-hour format."""
    parsed_time = time.fromisoformat(time_string)

    hour = parsed_time.hour
    minute = parsed_time.minute

    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12

    if display_hour == 0:
        display_hour = 12

    return f"{display_hour}:{minute:02d} {period}"


# --------------------------------------------------
# APP HEADER AND LOGO
# --------------------------------------------------
logo_path = Path("pill_dispenser_logo.png")

if logo_path.exists():
    left_space, logo_column, right_space = st.columns([1, 1.2, 1])

    with logo_column:
        st.image(str(logo_path), use_container_width=True)
else:
    st.markdown(
        "<div style='text-align:center; font-size:5rem;'>💊</div>",
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">Smart Pill Dispenser</div>
        <div class="app-subtitle">
            Set the times when your medicine should be dispensed.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# ADD A MEDICINE TIME
# --------------------------------------------------
st.markdown("### ➕ Add a dispensing time")

with st.container(border=True):
    selected_time = st.time_input(
        "What time should the medicine be dispensed?",
        value=time(8, 0),
        step=300,
        help="Select the hour and minute for the medicine."
    )

    selected_time_string = selected_time.strftime("%H:%M")

    st.info(
        f"Selected time: **{display_time(selected_time_string)}**"
    )

    if st.button(
        "➕ Add to Schedule",
        type="primary",
        use_container_width=True
    ):
        if add_schedule(selected_time_string):
            st.success(
                f"Medicine scheduled for "
                f"{display_time(selected_time_string)}."
            )
            st.rerun()
        else:
            st.warning(
                f"{display_time(selected_time_string)} is already "
                "in the schedule."
            )

# --------------------------------------------------
# DISPLAY CURRENT SCHEDULE
# --------------------------------------------------
st.markdown("### 📅 Current Medicine Schedule")

schedule = get_schedule()

if not schedule:
    st.markdown(
        """
        <div class="empty-schedule">
            <strong>No medicine times scheduled yet.</strong><br>
            Select a time above and press “Add to Schedule.”
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.caption(
        f"{len(schedule)} dispensing "
        f"{'time' if len(schedule) == 1 else 'times'} scheduled"
    )

    for index, scheduled_time in enumerate(schedule):
        time_column, delete_column = st.columns([4, 1.4])

        with time_column:
            st.markdown(
                f"""
                <div class="schedule-time">
                    ⏰ {display_time(scheduled_time)}
                </div>
                """,
                unsafe_allow_html=True
            )

        with delete_column:
            if st.button(
                "🗑️ Delete",
                key=f"delete_{index}_{scheduled_time}",
                use_container_width=True
            ):
                st.session_state["pending_delete"] = scheduled_time

# --------------------------------------------------
# DELETE CONFIRMATION
# --------------------------------------------------
if st.session_state.get("pending_delete"):
    pending_time = st.session_state["pending_delete"]

    st.warning(
        f"Remove the {display_time(pending_time)} dispensing schedule?"
    )

    confirm_column, cancel_column = st.columns(2)

    with confirm_column:
        if st.button(
            "Yes, Remove",
            type="primary",
            use_container_width=True
        ):
            delete_schedule(pending_time)
            del st.session_state["pending_delete"]

            st.success("The schedule was removed.")
            st.rerun()

    with cancel_column:
        if st.button(
            "Cancel",
            use_container_width=True
        ):
            del st.session_state["pending_delete"]
            st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Always check that the dispenser contains the correct medicine "
    "and that every scheduled time is correct."
)