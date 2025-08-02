# 🗂️ PEATA v2.0.0 – macOS Packaging Release

📅 Released: 2025-08-02  
💻 Platform: macOS 12+ (tested on Sequoia 15.0.1)  
📦 Format: Standalone `.dmg` installer

---

## 🎉 What's Included

- Same feature set as Windows version (`v2.0.0`)
- Bundled as `.app` inside `.dmg` for easy installation
- Tested on macOS Sequoia 15.0.1
- Known Issue: Main window may temporarily disappear while the progress bar  is active. (macOS only)

---

## 💡 Installation Instructions (macOS)

1. Download the `.dmg` file
2. Open and drag `PEATA.app` into the `Applications` folder
3. You may need to right-click → **Open** the first time due to macOS Gatekeeper

---

## ⚠️ Exported Files Location (macOS)

On macOS, files exported by the PEATA app (e.g., CSV/Excel query results) are saved to your personal **Home** folder, not inside the `.app` bundle.

To access them:

1. Open **Finder**
2. In the top menu bar, click **Go** → **Home**
3. Open the `PEATA/data/csv/` or `PEATA/data/excel/` folder

---

## 🔗 Related

- [Windows release note](https://github.com/ElinEunjung/peata-v2/releases/tag/v2.0.0)
