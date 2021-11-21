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
```
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
