# 🗂️ PEATA ver.2 – Public Release Notes

---

## 📦 Version: `v2.0.0`

📅 Released: 2025-07-10  
💻 Platform: Windows (.exe) only

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
- macOS and Linux builds are not yet available
- No automatic update feature 
- Demo video not yet linked (YouTube link to be updated)

---

## 📦 Files Included in `.zip`

- `PEATA.exe` (Windows executable)
- `LICENSE`
- `README.md`
- `docs/` folder with full documentation and screenshots
- `release-v2.0.0.txt` (this file in text format)

---

## 📺 Live Demo (Coming Soon)

YouTube Demo: [Watch PEATA Demo](https://youtu.be/demo_link_here)

---

