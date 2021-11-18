# Welcome to Shredhub!

### Project Configurations:

```bash
$ python3 -m virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ flask run
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
(venv) $ flask db migrate
(venv) $ flask db upgrade
```

#### How to run the server:
Visit local server to see the app in action via:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

(or)

[http://127.0.0.1:5000/index](http://127.0.0.1:5000/index)
