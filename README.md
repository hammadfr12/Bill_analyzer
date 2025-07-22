Bill Analyzer is a Streamlit web-app that turns piles of invoices, receipts, and fee slips into structured data you can search, sort, and analyse — all offline, on Windows, macOS, or Linux.  Page	What it shows Upload	Drag-and-drop PNG / JPEG / PDF / TXT receipts. OCR is run locally; totals, vendor, date & currency are auto-detected. Records	Live table (sortable & searchable) of every parsed receipt. Includes an 🗑️ Delete faulty rows button. Insights	Monthly spend totals, currency breakdowns, and other quick stats (powered by Pandas).

- **Upload**: Drag-and-drop PNG, JPG, PDF or TXT files.  
- **Records**: Sort, filter and delete faulty rows in your receipts table.  
- **Insights**: View monthly spend totals, currency breakdowns and other quick stats.

<p align="center">
  <img src="https://user-images.githubusercontent.com/.../upload-page.png" width="600"/>
</p>

---

## 🚀 Features

- 🔍 **OCR** of images/PDFs via [pytesseract](https://github.com/madmaze/pytesseract) and [pdf2image](https://github.com/Belval/pdf2image).  
- 💱 **Currency detection** for INR (₹/Rs), USD ($), EUR (€), GBP (£), JPY (¥).  
- 📊 **SQLite** backend (`data/receipts.db`) with SQLAlchemy + Pydantic models.  
- 🗄️ **Records** page with demo sorting algorithms (Timsort, Quick-, Merge-).  
- 📈 **Insights** page powered by Pandas: monthly totals, per-currency charts.  
- 🧹 **Cleanup**: “Delete faulty rows” button removes zero/unknown entries.  

---

## 📦 Installation

### Prerequisites

- **Python 3.9+** (tested on 3.10.11)  
- **Git** (for cloning)  
- **Tesseract-OCR** (v5.x+) and **Poppler** (for PDF support) on your `PATH`.

<details>
<summary><strong>Windows install hints</strong></summary>

1. **Tesseract**  
   - Download & install from https://github.com/UB-Mannheim/tesseract  
   - Add `C:\Program Files\Tesseract-OCR` to your **System** → **Environment Variables** → **Path**

2. **Poppler**  
   - Download from https://poppler.freedesktop.org  
   - Unzip, add the `bin` folder (e.g. `C:\poppler-24.08.0\Library\bin`) to `Path`

3. **Restart** your terminal to pick up these PATH changes.
</details>

### Clone & Setup

```bash
git clone https://github.com/hammadfr12/Bill_analyzer.git
cd Bill_analyzer

# Create & activate venv
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# Install deps
pip install --upgrade pip
pip install -r requirements.txt
▶️ Run the app
bash
Copy
Edit
streamlit run app/main.py
Point your browser to http://localhost:8501.

🗂️ Project structure
bash
Copy
Edit
Bill_analyzer/
├── app/
│   ├── main.py          # Streamlit router + CSS loader
│   ├── styles.css       # Global styles
│   └── views/           # Upload / Records / Insights pages
├── backend/
│   ├── ocr.py           # PDF/image → text
│   ├── parser.py        # Vendor/date/amount extractor
│   ├── currency.py      # Currency detection & parsing
│   ├── models.py        # Pydantic & SQLAlchemy models
│   ├── database.py      # SQLite + session setup
│   └── utils.py         # Helpers (create data/ folder, logging)
├── algorithms/          # Sorting & aggregation demos
├── data/                # Auto-created: receipts.db + uploaded files
├── tests/               # Pytest suites
├── .gitignore
├── requirements.txt
└── README.md
🤝 Contributing
Fork this repository

Create a feature branch: git checkout -b feat/your-feature

Commit your changes & tests

Push & open a Pull Request

Please ensure all tests pass and add new tests for any new functionality.

📄 License
This project is licensed under the MIT License.

Made with ♥︎ by hammadfr12

