![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.13.5-yellow)

# PEATA: Packages for Easier Access To APIs

**PEATA** is a Python-based research assistant tool that simplifies access to TikTok’s official Research API. Designed for social science researchers, it provides an intuitive GUI to search, preview and download public TikTok video, comment and user data with minimal technical setup.

More minimalist version built with Tkinter(GUI v1) is available here: https://github.com/amalie246/PEATA

> This version (GUI v2) was independently developed using **PyQt** for a modern and responsive desktop interface. While it shares initial backend logic with GUI v1, the codebase has since been extensively restructured and redesigned to support a more advanced and researcher-friendly experience.

---

## 🧩 What Makes PEATA Different?

Unlike traditional API tools, PEATA bridges the gap between researchers and complex APIs by offering:

- Real-time query previews
- Modular filter-building tools
- Export-ready data structures
- Error-resilient and user-friendly UX

---

## 🔍 Key Features

- **Flexible Search Mode Architecture**: 
  Built to support both *Simple* and *Advanced* modes across query types.

    ✅ **Video Query**: Advanced mode implemented

    ✅ **Comment Query**: Simple mode implemented

    ✅ **User Info Query**: Simple mode only

   > Internal architecture is fully prepared for future dual-mode expansion.

- **Real-Time Query Preview**: 
  Instantly displays the generated query JSON for easier debugging and transparency.

- **Result Table with “Load More” Pagination**: 
  Review up to 100 rows at a time before downloading full datasets - ideal for validating data quality

- **Prefetch Before Export**: 
  Supports quick data inspection through paginated results before downloading all.

- **Dynamic Filter Builder** *(Video Query)*: 
  Combine logic operators (AND/OR/NOT), field operatiors (EQ, IN, GT...), user defined values (username, keyword...), and region filters for precise control.

- **Customizable Field Selection**: 
  Select from 23+ TikTok fields using grouped checkboxes, tailored to your research needs.

- **Max Results Control**: 
  Select data volume limits to fetch (100 / 500 / 1000 / ALL) for efficient API requests.

- **Progress Tracking**: 
  Visual progress bar during data export operations.

- **Modular and Reusable UI**: 
  Built with consistent, clean PyQt components across query types.

- **Data Export to `.csv` / `.xlsx`**: 
  Download query results in well-structured format with predefined column ordering.

- **Robust Error Handling**: 
  User-friendly error messages with clear recovery paths and API error explanations

- **Standalone Executable (Coming Soon)**: 
  A `.exe` version for Windows users is in development—no Python required.

---

## 🚀 Getting Started

### 📦 Requirements (For developer):

- Python 3.9+
- python packages listed in `requirements.txt`

### 🔧 Installation

> Coming soon: Executable version for Windows.

To run from source (developer setup):

```bash
git clone https://github.com/ElinEunjung/PEATA.git
cd PEATA
pip install -r requirements.txt
python -m app.main
```

---

## 🧑‍💻 Usage
1. Launch the app.

2. Choose a query type from the left menu (e.g., Video, Comment, User).

3. Fill in your filters and select fields. (Best query practice will be available soon)

4. Click Run Query to fetch data.

5. View results and export as needed.

---

### 📝 Note: Make sure that your TikTok Research API credentials are valid to use this program.

---

## 🗃 Project Structure (v2.0.0)

```bash
PEATA/
│
├── README.md
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
    └── requirements.txt

```
---

## 📖 Documentation
❌ docs/usage.md: step-by-step guide (will be available soon)
❌ docs/fields_video.md: full field reference (will be available soon)
❌ docs/changelog.md: version history (will be available soon)

---

## 📄 License
MIT License — see LICENSE file (will be available soon)

---

## 👤 Author & Contributors

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

> **Original Author**: PEATA Team
> **Refactored & Extended by**: Elin (2025)
> For bug reports, questions, or feature requests, please open an [issue](https://github.com/ElinEunjung/PEATA/issues) or contact Elin directly.

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

