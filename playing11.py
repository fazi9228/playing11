# playing11/app.py
import streamlit as st
import sqlite3
from datetime import date

# Connect to SQLite database
conn = sqlite3.connect("playing11.db", check_same_thread=False)
c = conn.cursor()

# Ensure tables exist
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

# Tabs as main page menu (not sidebar)
menu = ["Submit Availability", "Match Roster", "Split Expenses", "Delete Entries"]
choice = st.radio("Choose an option:", menu, horizontal=True)

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
        available = []
        maybe = []
        not_available = []
        
        for player, status in rows:
            if status == "Available":
                available.append(player)
            elif status == "Maybe":
                maybe.append(player)
            else:
                not_available.append(player)
        
        st.write("### Available Players:")
        for player in available:
            st.write(f"- {player}")
            
        st.write("### Maybe:")
        for player in maybe:
            st.write(f"- {player}")
            
        st.write("### Not Available:")
        for player in not_available:
            st.write(f"- {player}")
    else:
        st.info("No entries for this date yet.")

# Add & split expenses
elif choice == "Split Expenses":
    st.subheader("Post-Match Expense Split")
    match_date = st.date_input("Match Date")
    total_amount = st.number_input("Total Expense (e.g. booking fee)", min_value=0.0)

    # Get available players for dropdown
    c.execute("SELECT player_name FROM availability WHERE match_date=? AND status='Available'", (match_date.isoformat(),))
    players = [row[0] for row in c.fetchall()]

    if players:
        selected_players = st.multiselect("Select Players to Split Expense With", players, default=players)
        paid_by = st.selectbox("Paid By", players)

        if selected_players:
            amount_per_player = round(total_amount / len(selected_players), 2)
            st.write(f"Each player owes: RM {amount_per_player}")

            if st.button("Save Expense"):
                c.execute("""
                    INSERT INTO expenses (match_date, total_amount, paid_by, amount_per_player, settled_by)
                    VALUES (?, ?, ?, ?, ?)
                """, (match_date.isoformat(), total_amount, paid_by.strip(), amount_per_player, ",".join(selected_players)))
                conn.commit()
                st.success("Expense saved successfully!")
        else:
            st.info("Please select at least one player to split the cost with.")
    else:
        st.info("No confirmed players for this match date.")
        
    # Show expenses for this date
    st.subheader("Existing Expenses")
    c.execute("SELECT paid_by, total_amount, amount_per_player FROM expenses WHERE match_date=?", (match_date.isoformat(),))
    expense_rows = c.fetchall()
    if expense_rows:
        for paid_by, total, per_player in expense_rows:
            st.write(f"- {paid_by} paid RM {total} (RM {per_player} per player)")
    else:
        st.info("No expenses recorded for this date.")

elif choice == "Delete Entries":
    st.subheader("🗑️ Delete Records")

    delete_type = st.radio("What would you like to delete?", ["Availability", "Expenses"])

    match_date = st.date_input("Select Match Date")
    if delete_type == "Availability":
        c.execute("SELECT id, player_name, status FROM availability WHERE match_date = ?", (match_date.isoformat(),))
        records = c.fetchall()
        for record_id, name, status in records:
            if st.button(f"❌ Delete {name} ({status})", key=f"del_avail_{record_id}"):
                c.execute("DELETE FROM availability WHERE id = ?", (record_id,))
                conn.commit()
                st.success(f"Deleted: {name}")
                st.experimental_rerun()
    else:
        c.execute("SELECT id, total_amount, paid_by FROM expenses WHERE match_date = ?", (match_date.isoformat(),))
        expenses = c.fetchall()
        for record_id, amount, payer in expenses:
            if st.button(f"❌ Delete Expense: RM{amount} by {payer}", key=f"del_exp_{record_id}"):
                c.execute("DELETE FROM expenses WHERE id = ?", (record_id,))
                conn.commit()
                st.success(f"Deleted expense by {payer}")
                st.rerun()

# Funny quote at the end
st.markdown("---")
st.caption("Legends show up. Rest post stories.")
