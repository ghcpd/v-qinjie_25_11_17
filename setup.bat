@echo off
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete. Activate the virtualenv with: .venv\Scripts\activate