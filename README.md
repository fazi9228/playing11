# 🏏 Playing 11 – Weekend Cricket Coordination App

A simple Streamlit web app to manage weekend cricket games with friends.  
Track player availability, view match rosters, and split post-match expenses easily — all with a clean interface and backed by a lightweight SQLite database.

---

## 🚀 Features

- ✅ Submit your availability for weekend matches
- 📋 View match rosters by date
- 💸 Log total expenses and automatically split the cost among attendees
- 🗃️ Data stored locally in SQLite (`playing11.db`)
- 🌐 Deployed easily via Streamlit Cloud

---

## 📦 Project Structure
playing11/
├── app.py # Streamlit app
├── playing11.db # SQLite database (auto-created on first run)
├── requirements.txt # Python dependencies
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/playing11-app.git
cd playing11-app
2. Create a virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the app locally
bash
Copy
Edit
streamlit run app.py

