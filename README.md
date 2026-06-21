# CarboTrack — Carbon Footprint Awareness Platform

EcoTrack is a full-stack web application built to help individuals log, visualize, and systematically reduce their daily greenhouse gas environmental footprint. The platform tracks parameters across four primary lifestyle vectors: **Mobility (Transport)**, **Utilities (Home Energy)**, **Nutrition (Diet)**, and **Material Loops (Waste Management)**. 

Calculations are modeled utilizing standard global carbon intensity factors ($kgCO_2e$), backed by a persistent relational database engine to display rolling historical trend lines.

---

## 📂 Project Architecture & Core Blueprint

```text
Carbon-Footprint-Platform/
│
├── carbon_tracker/
│   ├── app.py                  # Core Application Engine & API Router
│   ├── seed_db.py              # Database Initialization Script
│   ├── requirements.txt        # Third-Party Dependencies Manifest
│   │
│   └── templates/
│       └── index.html          # Dynamic Dashboard, Charts, & UI Layout
│
└── .gitignore                  # Excluded runtime and binary targets

⚡ Technical Stack Specification
Backend: Python 3.10+ / Flask Micro-framework

Database Layer: SQLite via Flask-SQLAlchemy ORM

Frontend UI: Responsive Tailwind CSS Layout Component Engine

Visualizations: Real-time data processing via Chart.js (Polar Area Matrix)

🚀 Execution & Local Development Setup
Follow these exact steps to launch the platform locally on your machine.

1. Initialize Project Directory & Dependencies
Open your terminal (PowerShell/Command Prompt) and navigate into the application core:

Bash
cd carbon_tracker
pip install -r requirements.txt
2. Populate the Ledger Registry (Database Seeding)
Execute the seeding script to compile local binary database fragments and preload 7 days of historical tracking data:

Bash
python seed_db.py
(This auto-generates the instance/database.db structure safely).

3. Launch the Server Engine
Run the primary Flask framework instance:

Bash
python app.py
4. Open Interface Canvas
Open your web browser and navigate to the local environment portal:

Plaintext
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
📊 Core System Workflow
The architecture operates via an asynchronous, event-driven data loop:

User Action: The user adjusts lifestyle sliders or dropdown inputs on the Tailwind interface.

Async API Request: JavaScript captures input states dynamically and submits an asynchronous POST network transaction to the backend /api/log endpoint.

Algorithmic Computation: The Flask engine extracts the parameters, computes individual resource category values, and aggregates the total daily sum.

Data Persistence: SQLite writes the processed row to database.db, maintaining transaction integrity.

UI Rendering Update: The backend returns a data package, prompting Chart.js to smoothly re-render the distribution metrics without a page reload.

🌐 Production Cloud Deployment (Render Framework)
This platform is configured out of the box for direct deployment to Render.com:

Push your latest code changes to your GitHub repository (ensuring instance/ and *.db files are kept out via your .gitignore).

Log in to your Render Dashboard and create a new Web Service.

Link your public or private GitHub code repository.

Input the following target environmental deployment configurations:

Language: Python

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Click Deploy Web Service to launch your live platform link.


### 🚀 Finalizing Your Repository Steps
Now that your `README.md` is complete, run these commands in your PowerShell to push it straight up to your GitHub page:

```powershell
git add README.md
git commit -m "docs: add comprehensive system architecture README"
git push origin main
