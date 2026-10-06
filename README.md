# 📒 Moudakira.ma — Daily Lesson Journal

> Prepare your daily lesson journal in minutes, not hours!

**Moudakira.ma** is a web application designed for primary school teachers. It simplifies the creation of the *cahier journal* (daily lesson journal): pick your levels, textbooks, units and schedules, then download the finished journal as an Excel file.

🔗 **Live app:** [app.moudakira.ma](https://app.moudakira.ma/Cahier_journal)

---

## ✨ Features

- **Fast journal creation**: subjects, durations, lesson elements and number of sessions in a few clicks.
- **Timetable**: create a timetable in the app, or import your own as a CSV file.
- **Guided selection**: school levels or groups, textbooks used, unit and schedules.
- **Excel export**: download the final journal as an `.xlsx` file.
- **Authentication**: sign-in and account creation via `streamlit-signin-auth-ui`.
- **Teacher reviews**: comment and star-rating section, stored in Google Sheets.

## 🧰 Tech stack

| Area | Tools |
|---|---|
| Web UI | [Streamlit](https://streamlit.io/) (multipage app), `streamlit-extras`, `streamlit-modal`, `st_star_rating` |
| Data | `pandas`, `numpy`, `openpyxl`, `xlwings` |
| Storage / auth | Google Sheets (`gspread`, `oauth2client`, `google-api-python-client`) |
| Misc | `Pillow`, `requests`, `beautifulsoup4`, `Babel`, `validators` |

## 📁 Project structure

```
cahier-journal/
├── 🚩Accueil.py          # Home page (Streamlit entry point)
├── pages/                # Additional app pages (multipage)
├── static/               # Logo, banners and screenshots
├── app-images/           # App images
├── wb_swap_macro/        # Excel workbook / macro resources
├── .devcontainer/        # Development environment configuration
├── .github/workflows/    # GitHub Actions workflows
└── requirements.txt      # Python dependencies
```

## 🚀 Installation

**Requirements:** Python 3.10+ (adjust to your version) and `git`.

```bash
# 1. Clone the repository
git clone https://github.com/GitSamad88/cahier-journal.git
cd cahier-journal

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

The app reads its secrets from **environment variables** (never commit them):

| Variable | Purpose |
|---|---|
| `google_sheets_api_credentials` | Google service account key, as JSON |
| `smtp_gmail` | Gmail address used to send authentication emails |
| `smtp_password` | Associated app password |

The service account needs access to a Google Sheets workbook named `mydb` (its second sheet stores the reviews).

Example (Linux / macOS):

```bash
export google_sheets_api_credentials='{"type": "service_account", ...}'
export smtp_gmail="your.address@gmail.com"
export smtp_password="your-app-password"
```

## ▶️ Run the app

```bash
streamlit run "🚩Accueil.py"
```

Then open <http://localhost:8501> in your browser.

## 🧭 Usage

1. Create an account or sign in.
2. Create your **timetable** (or import it as CSV).
3. Create your **daily journal**: levels/groups, textbooks, unit, schedules.
4. Save your selections.
5. **Download** the journal as an Excel file.

## 🤝 Contributing

Suggestions and fixes are welcome: open an issue or submit a pull request.

## 👤 Author

**TAOUFIQ ABDESSAMAD** — [LinkedIn](https://www.linkedin.com/in/abdessamad-taoufiq-082013209) · [GitHub](https://github.com/GitSamad88)

## 📄 License

All rights reserved © 2026. *(Add a `LICENSE` file if you want to open-source the project, e.g. MIT.)*
