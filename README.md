## Setup

### Enviroment

```
python3.10 -m venv ~/venv/flask-env
source ~/venv/flask-env/bin/activate
pip install -r requirements.txt
```

### Database
1. Open commandline:

`mongosh -u mongodbuser -p`

2. Switch to your database: `use flaskdb`
3. Create your database user with access:

`db.createUser({user: 'flask', pwd: 'flaskpass', roles: [{role: 'readWrite', db: 'flaskdb'}]})`

## How to Run
```
gunicorn -w 1 --bind 127.0.0.1:5000 app.wsgi --reload
```
