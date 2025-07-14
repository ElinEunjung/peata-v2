### 1. Clone this repo
```bash
git clone https://github.com/ElinEunjung/peata-v2.git
cd peata-v2
```

### 2. Install Python 3.11 system-wide
```bash
brew install python@3.11
python3.11 --version
# Output: Python 3.11.x

```

### 3. Setup virtual environment
```bash
python3.11 -m venv venv
source venv-mac/bin/activate
```

### 4. Install dependencies (pyinstaller included in requirements.txt)
```bash
pip install -r requirements.txt
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

