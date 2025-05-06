# playing11/app.py
import streamlit as st
import sqlite3
from datetime import date

# Connect to SQLite database
conn = sqlite3.connect("playing11.db", check_same_thread=False)
c = conn.cursor()

# Connect to SQLite database
conn = sqlite3.connect("playing11.db", check_same_thread=False)
c = conn.cursor()

# ✅ Ensure tables exist before anything else
c.execute("""
CREATE TABLE IF NOT EXISTS availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT NOT NULL,
    player_name TEXT NOT NULL,
    status TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    paid_by TEXT NOT NULL,
    amount_per_player REAL,
    settled_by TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# Page config
st.set_page_config(page_title="Weekend Cricket Squad", layout="centered")
st.title("🏏 Playing 11 – Weekend Cricket App")

# Tabs
menu = ["Submit Availability", "Match Roster", "Split Expenses"]
choice = st.sidebar.selectbox("Menu", menu)

# Create availability form
if choice == "Submit Availability":
    st.subheader("Submit Your Availability")
    match_date = st.date_input("Select Match Date", min_value=date.today())
    player_name = st.text_input("Your Name")
    status = st.radio("Are you playing?", ["Available", "Not Available", "Maybe"])
    if st.button("Submit"):
        if player_name.strip() == "":
            st.warning("Please enter your name.")
        else:
            c.execute("""
                INSERT INTO availability (match_date, player_name, status)
                VALUES (?, ?, ?)
            """, (match_date.isoformat(), player_name.strip(), status))
            conn.commit()
            st.success("Availability submitted!")

# Show list of players for selected date
elif choice == "Match Roster":
    st.subheader("Match Roster")
    match_date = st.date_input("Select Match Date to View")
    c.execute("SELECT player_name, status FROM availability WHERE match_date=?", (match_date.isoformat(),))
    rows = c.fetchall()
    if rows:
        for player, status in rows:
            st.write(f"- {player}: **{status}**")
    else:
        st.info("No entries for this date yet.")

# Add & split expenses
elif choice == "Split Expenses":
    st.subheader("Post-Match Expense Split")
    match_date = st.date_input("Match Date")
    total_amount = st.number_input("Total Expense (e.g. booking fee)", min_value=0.0)
    paid_by = st.text_input("Paid By")

    # Get attendees for split
    c.execute("SELECT player_name FROM availability WHERE match_date=? AND status='Available'", (match_date.isoformat(),))
    players = [row[0] for row in c.fetchall()]
    if players:
        amount_per_player = round(total_amount / len(players), 2)
        if st.button("Save Expense"):
            c.execute("""
                INSERT INTO expenses (match_date, total_amount, paid_by, amount_per_player, settled_by)
                VALUES (?, ?, ?, ?, ?)
            """, (match_date.isoformat(), total_amount, paid_by.strip(), amount_per_player, ",".join(players)))
            conn.commit()
            st.success(f"Expense saved. Each player owes: RM {amount_per_player}")
            st.write("Players:", ", ".join(players))
    else:
        st.info("No confirmed players for this match date.")
