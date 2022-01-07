# Welcome to Shredhub!

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
![Build][build-badge]
</br>

## Table of Contents

- [Overview](#overview)
- [Tools Utilized](#framework)
- [Contributors](#contributors)
- [Project Configurations](#project-configurations)
- [Acknowledgements](#acknowledgements)

------

### <ins>Overview</ins>
<img src="https://user-images.githubusercontent.com/58891447/148166008-ef7e6527-9145-4f82-8405-a8fa3976fd38.gif" width=50%/>  

</br>

**Shredhub** is a `Flask` application in which users can write about their favorite places to shred, follow their fellow shredders, check out weather reports for their favorite resorts, and search blog posts to track down those hidden powder stashes... assuming folks decide to share them! 😎

### <ins>Framework</ins>
<p>
  <img src="https://img.shields.io/badge/Flask-181717.svg?&style=flaste&logo=flask&logoColor=white" />
</p>

#### Languages
<p>
  <img src="https://img.shields.io/badge/Python-1572B6.svg?&style=flaste&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-0EB201.svg?&style=flaste&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-0EB201.svg?&style=flaste&logo=css3&logoColor=white" />
</p>

#### Tools
<p>
  <img src="https://img.shields.io/badge/Atom-66595C.svg?&style=flaste&logo=atom&logoColor=white" />  
  <img src="https://img.shields.io/badge/Git-FF6E4F.svg?&style=flaste&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-181717.svg?&style=flaste&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Heroku-430098.svg?&style=flaste&logo=heroku&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?&style=flaste&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Sendgrid-4169E1.svg?&style=flaste&logo=twilio&logoColor=white" />
  <img src="https://img.shields.io/badge/CircleCI-181717.svg?&style=flat&logo=circle&logoColor=white" />
</p>

#### Packages
<p>
  <img src="https://img.shields.io/badge/Flask-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask--Login-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask--Mail-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask--Moment-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask--WTF-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/Jinja2-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  </br>
  <img src="https://img.shields.io/badge/psycopg2-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/python--dotenv-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/PyJWT-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/pytest--cov-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/pytest--vcr-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  </br>
  <img src="https://img.shields.io/badge/Werkzeug-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/gunicorn-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/requests-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/numpy-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
  <img src="https://img.shields.io/badge/scipy-1572B6.svg?&style=flaste&logo=pypi&logoColor=white" />
</p>

#### Development Principles
<p>
  <img src="https://img.shields.io/badge/OOP-b81818.svg?&style=flaste&logo=OOP&logoColor=white" />
  <img src="https://img.shields.io/badge/TDD-b87818.svg?&style=flaste&logo=TDD&logoColor=white" />
</p>

### <ins>Contributors</ins>

👤  **Taylor Varoglu**
- Github: [Taylor Varoglu](https://github.com/tvaroglu)
- LinkedIn: [Taylor Varoglu](https://www.linkedin.com/in/taylorvaroglu/)


### <ins>Project Configurations</ins>
This project requires a local installation of `Python3` and `Flask`


```bash
$ python3 -m virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

#### Database Creation:
```bash
$ psql
 create database shredhub;
CREATE DATABASE
 \q
```

#### Database Initialization:
```bash
$ source venv/bin/activate
(venv) $ flask db migrate
(venv) $ flask db upgrade
```

<img src="https://user-images.githubusercontent.com/58891447/148485667-6504813d-7688-4228-babc-172777d5bcde.png" width=100%/>  

#### How to run the test suite:
```bash
$ source venv/bin/activate
(venv) $ pytest --cov
```

#### How to run the server:
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

#### Link to deployed application:
Check it out [here](https://shredhub.herokuapp.com/login)!

</br>

### <ins>Acknowledgements</ins>
- [Background Image](https://unsplash.com/): Unsplash
- [Email Server](https://signup.sendgrid.com/): Sendgrid
- [Weather Data](https://openweathermap.org/api/one-call-api): OpenWeather One Call API

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/tvaroglu/shredhub.svg?style=flat
[contributors-url]: https://github.com/tvaroglu/shredhub/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/tvaroglu/shredhub.svg?style=flat
[forks-url]: https://github.com/tvaroglu/shredhub/network/members
[stars-shield]: https://img.shields.io/github/stars/tvaroglu/shredhub.svg?style=flat
[stars-url]: https://github.com/tvaroglu/shredhub/stargazers
[issues-shield]: https://img.shields.io/github/issues/tvaroglu/shredhub.svg?style=flat
[issues-url]: https://github.com/tvaroglu/shredhub/issues
[build-badge]: https://img.shields.io/circleci/build/github/tvaroglu/shredhub?style=flat
