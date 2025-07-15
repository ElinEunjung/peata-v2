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
pyinstaller PEATA-mac.spec
```

### 5-1. Run test PEATA.app before zipping
What to test: 
- log in
- run comment query
- export to excel
- check downloaded data in `data/excel/`

### 6. Zip the generated .app
```bash
cd dist
zip -r PEATA-macOS.zip PEATA.app
```

