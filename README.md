![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.13.5-yellow)

<p align="center">
  <img src="docs/screenshots/banner.png" alt="PEATA Banner" width="800"/>
</p>

# PEATA: Packages for Easier Access To APIs

**PEATA** is a Python-based research assistant tool that simplifies access to TikTok’s official Research API. Designed for social science researchers, it provides an intuitive GUI to search, preview and download public TikTok video, comment and user data with minimal technical setup.

More minimalist version built with Tkinter (GUI v1) is available here: https://github.com/amalie246/PEATA

> This version (GUI v2) was independently developed using **PyQt** for a modern and responsive desktop interface. While it shares initial backend logic with GUI v1, the codebase has since been extensively restructured and redesigned to support a more advanced and researcher-friendly experience.

---

## 🧩 What Makes PEATA Different?

Unlike traditional API tools, PEATA bridges the gap between researchers and complex APIs by offering:

- Real-time query previews
- Modular filter-building tools
- Export-ready data structures (Result table)
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
  Review data in batches of up to 100 rows before downloading the full dataset - ideal for validating data quality

- **Prefetch Before Export**: 
  Supports quick data inspection through paginated results before downloading all.

- **Dynamic Filter Builder** *(Video Query)*: 
  Combine logic operators (AND/OR/NOT), field operators (EQ, IN, GT...), user defined values (username, keyword...), and region filters for precise control.

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

## 👨‍🔬 For Researchers (No Python Needed)

> Coming soon: Executable version for Windows.

To use the PEATA app:

1. Download the latest `.exe` file from the [Releases](https://github.com/ElinEunjung/peata-v2/releases).
2. Double-click to open. No Python or setup needed.
3. Make sure you have valid TikTok Research API credentials.
4. Follow the in-app instructions.

> ℹ️ If Windows shows a security warning, click "More info" → "Run anyway". The app is unsigned but safe.

---

## 🛠️ For Developers

If you want to run or modify the source code:

### 📦 Understanding the Requirements Files

We maintain two separate requirements files:

| File | Purpose |
|------|---------|
| `requirements.txt` | Runtime dependencies — minimal set needed to run or package the app (e.g., into `.exe`). |
| `requirements-dev.txt` | Development environment — includes `requirements.txt` + formatting, testing, and linting tools. |


### Requirements

- Python 3.9+
- python packages listed in `requirements.txt` or `requirements-dev.txt`


### Developer Setup

To set up your local development environment:

```bash
git clone https://github.com/ElinEunjung/peata-v2.git
cd peata-v2
pip install -r requirements-dev.txt
```
This installs: 
- ✅ Runtime dependencies (PyQt5, pandas, requests, etc.)
- ✅ Dev tools: flake8, black, isort, pytest, and pre-commit
    
### Set Up Pre-Commit Hooks

To ensure clean code before every commit, run:

```bash
pre-commit install
```

This installs Git hooks that automatically check and fix your code formatting every time you commit.

### Start the app

To run the app:

```bash
python -m app.main
```

---

## 🧑‍💻 How to Use the App 
1. **Launch** the app.
2. **Sign in** with valid TikTok Research API credentials. 
3. **Select a query type** from the left menu (Video, Comment, or User) 

▶️ For a complete guide including how to run queries, set filters, and export results:
👉 see [PEATA app usage](docs/usage.md)

▶️ For visual reference, see [Interface Overview (Screenshots)](#-interface-overview-screenshots) section below.

---

## 🎇 Interface Overview (Screenshots)

| Login Screen | Home Screen | Exported Table |
|--------------|-------------|----------------|
| ![login](docs/screenshots/login.png) | ![home](docs/screenshots/home.png) | ![table](docs/screenshots/table.png) |


**Query Preview Screens**

<table>
<tr>
<td><img src="docs/screenshots/preview-video.png" alt="Video Preview" width="500"/></td>
<td><img src="docs/screenshots/preview-comment.png" alt="Comment Preview" width="500"/></td>
<td><img src="docs/screenshots/preview-user.png" alt="User Preview" width="500"/></td>
</tr>
<tr>
<td><p align="center">Video Query</p></td>
<td><p align="center">Comment Query</p></td>
<td><p align="center">User Info Query</p></td>
</tr>
</table>

---

## 🎬 Live Demo

Watch PEATA in action *(coming soon)*:  
👉 [View Demo on YouTube](https://youtu.be/your_video_link_here)

---

### 📝 Note: Make sure that your TikTok Research API credentials are valid to use this program.

---

## 🗃 Project Structure (v2.0.0)

```bash
peata-v2/
│
├── README.md
├── requirements.txt
├── requirements-dev.txt
│
├── app/
│   ├── main.py               # App entry point
│   ├── assets/               # Icons, fonts, images for UI
│   ├── bin/                  # [Reserved for executables/scripts]
│   ├── controller/           # Query builder, error handlers
│   ├── model/                # API handling, file processing, config
│   └── view/                 # PyQt5 GUI components
│
├── data/
│   ├── csv/                  # Exported CSV results
│   └── excel/                # Exported Excel results
│
└── docs/                     # Additional guides, screenshots, and debug info
   
```
---

## 📖 Documentation
❌ [TikTok Video Filter Guide](docs/video-filter-guide.md) *(coming soon)* <br>
❌ [TikTok API Codebook Summary](docs/codebook-summary.md) *(coming soon)* <br>
❌ [PEATA app usage](docs/usage.md): step-by-step guide and filtering tips  <br>
❌ [Video Fileds Reference Guide](docs/fields-video.md) *(coming soon)* <br>
❌ [Query Design Best Practice](docs/query-best-practices.md) *(coming soon)* <br>
❌ [Version History](docs/changelog.md) *(coming soon)* <br>
⭕ [Server Behavior And Debugging](docs/server-behavior-and-debugging.md) <br>
⭕ [Preferred Field Order Summary](docs/preferred-field-orders.md) <br>

---

## 📄 License
MIT License — see `LICENSE` file *(will be available soon)*

---

## 👤 Project Credits (GUI v2 Repository Only)

This repository documents and contains the GUI v2 version of PEATA, implemented in PyQt5.
It is based on the initial Tkinter-based GUI v1 (available [here](https://github.com/amalie246/PEATA)). 
All roles listed below refer to this version (GUI v2) only.


| Name      | Version | Role                                                                                     |
|-----------|---------|------------------------------------------------------------------------------------------|
| Elin      | GUI v2  | Full PyQt GUI development, API integration, data handling, error handling, testing, documentation, setup |
| Ibrahim   | GUI v2  | Menu integration, login flow, UI coordination                                            |
| Amalie    | GUI v1  | (Not contributor to this repo — see original v1 repository) |
| Oda       | GUI v1  | (Not contributor to this repo — see original v1 repository) |


> **Original Author**: PEATA Team (GUI v1) <br>
> **Refactored & Extended by**: Elin, Ibrahim (GUI v2, 2025) <br>
> This project was funded by Kristiania University of Applied Sciences, Spring 2025. <br>
> For bug reports, questions, or feature requests, please open an [issue](https://github.com/ElinEunjung/peata-v2/issues) or contact Elin directly. <br>

---

## 🧼 Query Design Best Practices  *(Experimental – Needs Further Testing)*

> The logic below is based on observed API behavior and may be updated after further testing.

When filtering videos by `keyword`, it is strongly recommended to combine it with either a `username` or a specific `region_code`. 
Otherwise, the TikTok Research API may return an `invalid_params` error, especially if the query is too broad.

| Condition | Result |
|:---|:---|
| `region_code` + `keyword` (rare keyword, small region) | ✅  |
| `region_code` + `keyword` (common keyword, large region) | ✅  |
| `username` + `keyword` | ✅  |
| `keyword` only | ❌ May fail with invalid_params |

**Best practice:** Always start with broad search with single filter. Normally, multiple `keyword` values ensures a successful query.

▶️ For full Query Design Practices, see [Query Design Best Practice](docs/query-best-practices.md) *(coming soon)*