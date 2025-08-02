### 1. Clone this repo
```bash
git clone https://github.com/ElinEunjung/peata-v2.git
cd peata-v2
```

### 2. Download & Install Python 3.10.x s

download from:https://www.python.org/downloads/release/python-31011/downloads/release/python-3100rc2/
→ Install macOS "universal2" .pkg

reconfirm the version
```bash
pyton 3.10 --version

# Should output: Python 3.10.11
```

### 3. Setup virtual environment
```bash
cd ~/Desktop/Eunjung/peata-v2
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -m venv venv-mac310
source venv-mac310/bin/activate


```

### 4. Install dependencies (pyinstaller included in requirements.txt)
```bash
pip install -r requirements-mac.txt
```

### 5. Run PyInstaller with the PEATA.spec file
```bash
pyinstaller PEATA.spec
```

### 5-1. Run test PEATA.app before zipping
What to test: 
- log in
- run comment query
- export to excel
- check downloaded data in `username/PEATA/data/excel/`

### 6. Bundle into a .dmg generated .app
```bash
brew install create - dmg

create-dmg \
  --volname "PEATA" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "PEATA.app" 175 120 \
  --hide-extension "PEATA.app" \
  --app-drop-link 425 120 \
  "PEATA-v2.0.0-mac.dmg" \
  "dist/PEATA.app"

```

