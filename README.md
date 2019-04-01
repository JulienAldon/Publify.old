# Spotify Tools

 This app purpose is to synchronize spotify collaborative playlist and public playlist in order to share collaborative playlist without letting everyone modify your playlist.

Python dependences
- Spotipy
- Oauth2
- SqlAlchemy-Flask

Application made with
- Python3.6
- HTML, CSS

Install

- clone the repository
- create an environment with virtualenv or anything else with python3.6 with virtualenv:
````virtualenv venv/````
- activate the environment with fish for example:
````source venv/bin/activate.fish````
- install the requirements using pip : 
````pip install -r requirements.txt````
- create app/myconfig.py and put CLIENTKEY and CLIENTSECRET given in spotify dashboard for your application
- then you can ````flask run```` and access to localhost:5000!
