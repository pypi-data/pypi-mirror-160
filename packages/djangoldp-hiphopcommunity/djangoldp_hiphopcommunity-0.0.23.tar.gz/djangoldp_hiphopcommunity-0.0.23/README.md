# djangoldp_hiphopcommunity


## Installation

How to install the project locally

1- create virtual environement
`python -m venv venv`

2- activate venv
`venv\Scripts\activate.bat`

3- update pip & wheel
`python -m pip install -U pip wheel`

4- install djangoldp V2
`pip install djangoldp`

5- init server 
`djangoldp initserver [SERVER NAME]`

7- update settings.yml
dependencies: 
  - djangoldp-account
  - djangoldp-uploader
  - django-tinymce
  - dj-stripe

ldppackages: 
  - djangoldp_stripe
  - djangoldp_account
  - djangoldp_uploader
  - djangoldp_blog
  - djangoldp_hiphopcommunity


8- create a virtual link in sibserver : 
ln -s ../djangoldp-hiphopcommunity/djangoldp_hiphopcommunity djangoldp_hiphopcommunity

9- install the server in sibserver:
`djangoldp install`

10- install all packages
`djangoldp configure`

11- create rsa key
`python manage.py creatersakey`

12- launch the server
`djangoldp runserver`

## congrats ! You've made it. :)

This is great.