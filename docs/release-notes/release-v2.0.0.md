# 🗂️ PEATA ver.2 – Public Release Notes

---

## 📦 Version: `v2.0.0`

📅 Released: 2025-07-11  
💻 Platform: Windows 10/11 (64-bit only)

---

## 🎉 Highlights

- ✅ Packaged as a standalone Windows `.exe` — no Python or setup required
- ✅ Fully refactored PyQt5 GUI with support for:
  - Video Query (Advanced Mode)
  - Comment Query (Simple Mode)
  - User Info Query (Simple Mode)
- ✅ Real-time Query Preview with advanced filtering and logic builder in Video Query
- ✅ "Load More" + full result export as `.csv` or `.xlsx`
- ✅ Visual progress bar with cancel option during data export
- ✅ Clear error messages with TikTok API response handling
- ✅ All major TikTok query fields included, customizable field selection in Video Query
- ✅ Auto-generated export folders (`data/csv`, `data/excel`) at runtime location
- ✅ Consistent styling applied via external `style.qss`
- ✅ Font, icon, and layout polish for a modern researcher-facing app

---

## 🧰 Changes Since v1.4.1

- Integrated login flow
- Added navigation menu (left-aligned animated navbar)
- Refactored `VideoQueryUI`, `CommentQueryUI` and `UserInfoQueryUI` layouts and API logic
- Connected `Download All` button to progress bar and API
- Added **cancel button** to safely stop long-running downloads
- Enabled **partial downloads** if API fails midway
- Unified error feedback via `QMessageBox` (e.g. token expired, invalid filters)
- App now detects access token expiration (401) and prompts re-login
- Project documentation finalized in `docs/`, including:
  - Usage guide
  - TikTok API field reference
  - Query design tips
  - Query test log
  - Video filter guide
  - API codebook summary
  - Server behavior and debugging guide
  - preferred field order summary

---

## 📝 Known Limitations

- Only Windows executable provided (`.exe`)
- Compatible with Windows 10/11 (64-bit only)
- ❌ Not supported on 32-bit Windows systems
- ❌ macOS and Linux builds are not yet available
- No automatic update feature 


---

## 📦 Files Included in `.zip`

- `PEATA.exe` (Windows executable)
- `LICENSE`
- `README.md`
- `docs/` folder with full documentation and screenshots
- `_internal/`

> ⚠️ **Important Note**: Do not move `PEATA.exe` out of the unzipped folder. The app relies on internal files and will not work if run from another location.

> 💡 **Tip**: After launching `PEATA.exe`, you can right-click its icon in the taskbar and choose **"Pin to taskbar"** or **"Pin to Start Menu"** for easier future access.

---

## 📺 Live Demo

YouTube Demo: [Watch PEATA Demo](https://www.youtube.com/watch?v=niTPJAbzYD0&ab_channel=ElinP)

---

## 🧑‍💻 Project Credits

- **Amalie & Oda** – Developed GUI v1 (Tkinter prototype) with basic login and API query logic (2025)
- **Ibrahim** – Contributed to GUI v2 software design, implemented login flow, and integrated navigation menu in PyQt (2025)
- **Elin** – Led GUI v2 development: implemented full interface, integrated all API queries, handled data processing, error handling, documentation, and release packaging (2025)

---

