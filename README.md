# PEATA: Packages for Easier Access To APIs

PEATA is a Python-based research assistant tool designed to simplify access to TikTok’s official Research API. Built with a user-friendly GUI using PyQt, PEATA enables social science researchers to query and download public TikTok video, comment and user data.

More minimalist version built with Tkinter(GUI v1) is available here: 
https://github.com/amalie246/PEATA

This version (GUI v2) was independently developed using PyQt from the ground up.
While it was initially based on the same backend logic, the codebase has since been extensively restructured and redesigned to support a more advanced and resercher-friendly interface.

---


## 🔍 Key Features

- Simple or Advanced search modes for each query type (Video, Comment, User)
- Live query preview for transparency
- Dynamic filter builder with support for logic operators (AND/OR/NOT)
- TikTok-specific field selectors, region filtering or field operations (EQ, IN, GT, etc.)
- Pagination support with “Load More” functionality
- Export results to `.csv` or `.xlsx`
- Error handling with user-friendly feedback
- Lightweight standalone `.exe` (available soon)

---

## 📦 Installation

> Coming soon: Executable version for Windows.

To run from source:

```
git clone https://github.com/ElinEunjung/PEATA.git
cd PEATA
pip install -r requirements.txt
python main.py
```

Requirements:

Python 3.9+
PyQt5
requests, pandas, openpyxl

---
## 🧑‍💻 Usage
1. Launch the app.

2. Choose a query type from the left menu (e.g., Video, Comment, User).

3. Fill in your filters and select fields. (Best query practice will be available soon)

4. Click Run Query to fetch data.

5. View results and export as needed.

---

### 📝 Note: Make sure your TikTok Research API credentials are correct to use this program.

---
## 🗃 Directory Structure (v2.0.0)

```
bash
PEATA/
│
├── .env, .gitignore, README.md, setup.cfg, ...
│
├── app/
│   ├── main.py               # App entry point
│   ├── assets/               # Icons, fonts, images for UI
│   ├── bin/                  # [Reserved for executables/scripts]
│   ├── controller/           # Query builder, error handlers
│   ├── data/                 # Query result data (csv/excel)
│   ├── model/                # API handling, file processing, config
│   └── view/                 # PyQt5 GUI components
│
├── data/
│   ├── csv/                  # Exported CSV results
│   └── excel/                # Exported Excel results
│
└── docs/
    ├── preferred_field_orders.md
    ├── RELEASE_NOTE.md
    ├── server_behavior_and_debugging.md
    └── TODO.md

```
---

## 📖 Documentation
docs/usage.md: step-by-step guide (will be available soon)
docs/fields_video.md: full field reference (will be available soon)
docs/changelog.md: version history (will be available soon)

---

## 📄 License
MIT License — see LICENSE file (will be available soon)

---

## 👤 Contributors

This project was developed in two parallel versions:  
- **GUI v1**: A simplified version using Tkinter  
- **GUI v2**: A redesigned and feature-rich version using PyQt (this repository)


| Name      | Version | Role                                                                                     |
|-----------|---------|------------------------------------------------------------------------------------------|
| Elin      | GUI v2  | Full PyQt GUI development, API integration, data handling, error handling, testing, documentation, setup |
| Ibrahim   | GUI v2  | Menu integration, login flow, UI coordination                                            |
| Amalie    | GUI v1  | Initial API integration and backend prototyping                                          |
| Oda       | GUI v1  | Login flow and early data handling                                                       |

> This project was funded by Kristiania University of Applied Sciences, Spring 2025.
---

## 🧼 Query Design Best Practices  <-- NEED TO BE TESTED AGAIN

When filtering videos by `keyword`, it is strongly recommended to combine it with either a `username` or a specific `region_code`. 
Otherwise, the TikTok Research API may return an `invalid_params` error, especially if the query is too broad.

| Condition | Result |
|:---|:---|
| `region_code` + `keyword` (rare keyword, small region) |  |
| `region_code` + `keyword` (common keyword, large region) |  |
| `username` + `keyword` |  |
| `keyword` only |  |

**Best practice:** Always start with broad search with single filter. Normally, multiple `keyword` ensures a successful query.

