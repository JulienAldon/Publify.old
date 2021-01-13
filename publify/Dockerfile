FROM python:3.9

WORKDIR /app/publify
#config
# RUN  apk add -U gcc linux-headers musl-dev libffi-dev openssl-dev
RUN  pip3 install pipenv
COPY Pipfile Pipfile.lock /app/publify/
RUN  pipenv install
COPY . /app/publify/

EXPOSE 8000
#commande a lancer par default
CMD ["pipenv", "run", "uwsgi", "--ini", "/app/publify/uwsgi.ini"]
# ENTRYPOINT pipenv run uwsgi --socket 127.0.0.1:3031 --wsgi-file /opt/publify/app --chdir /opt/publify --callable /opt/publify --processes 4 --threads 2