# Welcome to Shredhub!

### Project Configurations:
```bash
$ python3 -m virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

### Database Creation:
```bash
$ psql
 create database shredhub;
CREATE DATABASE
 \q
```

### Database Initialization:
```bash
$ source venv/bin/activate
(venv) $ flask db migrate
(venv) $ flask db upgrade
```

### How to run the test suite:
```bash
$ source venv/bin/activate
(venv) $ pytest --cov
```

### How to run the server:
```bash
$ source venv/bin/activate
(venv) $ flask run
* Serving Flask app 'shredhub.py' (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
[2021-12-21 16:20:00,420] INFO in __init__: Shredhub startup
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Link to deployed application:
Check it out [here](https://shredhub.herokuapp.com/login)!
