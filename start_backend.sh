echo '-------------------------------------------------------'
echo '------------------  Odpalam warcaby  ------------------'
echo '-------------------------------------------------------'
cd backend/
pip3 install -r requirements.txt
FLASK_APP=app.py FLASK_ENV=development flask run -h 0.0.0.0 -p 5000