echo '------------------  Start client  ------------------'
cd client/
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
