# 1. Clone this repo
git clone https://github.com/ElinEunjung/peata-v2.git
cd peata-v2

# 2. Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install pyinstaller
pip install pyinstaller

# 5. Run PyInstaller with the PEATA.spec file
pyinstaller PEATA.spec

# 5-1. Run test PEATA.app before zipping
# What to test: log in / run comment query /export to excel / check downloaded data in data/excel/

# 6. Zip the generated .app
cd dist
zip -r PEATA-macOS.zip PEATA.app

