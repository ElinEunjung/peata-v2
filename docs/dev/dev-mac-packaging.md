### 1. Clone this repo
```bash
git clone https://github.com/ElinEunjung/peata-v2.git
cd peata-v2
```

### 2. Setup virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install pyinstaller
```bash
pip install pyinstaller
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
- check downloaded data in `data/excel/`

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

