#!/usr/bin/env bash

# Setup env vars
APP_SETTINGS=config.Development
SECRET_KEY=SOME-sUpEr-SeCrEt-KeY
APP_DB_USER=devadmin
APP_DB_NAME=lessonshare
APP_DB_PASS=password
DATABASE_URL="postgresql://$APP_DB_USER:$APP_DB_PASS@localhost:5432/$APP_DB_NAME"
echo "export APP_SETTINGS='$APP_SETTINGS'" >> /home/vagrant/.profile
echo "export SECRET_KEY='$SECRET_KEY'" >> /home/vagrant/.profile
echo "export DATABASE_URL='$DATABASE_URL'" >> /home/vagrant/.profile
source /home/vagrant/.profile

# Install aptitude packages, node
add-apt-repository -y ppa:chris-lea/node.js
apt-get -y update
apt-get -y install postgresql postgresql-contrib python-psycopg2 libpq-dev python-dev libffi-dev g++ nodejs

# Install pip, bower, and dependencies
curl -s https://bootstrap.pypa.io/get-pip.py --output get-pip.py
python get-pip.py
pip install cffi
pip install virtualenv
npm install bower -g

cd /flask-lessonshare
virtualenv flask
flask/bin/pip install -U pip
flask/bin/pip install -r requirements.txt
bower install --allow-root

# Setup postgresql
PG_VERSION=9.3
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# pg_hba.conf to allow local password auth
LOCAL_AUTH_STR="local   all             all                                     peer"
NEW_LOCAL_AUTH_STR="local   all             all                                     md5"
sed -i "s/$LOCAL_AUTH_STR/$NEW_LOCAL_AUTH_STR/" "$PG_HBA"

# Append to pg_hba.conf to add password auth:
echo "host     all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Restart so that all new config is loaded:
service postgresql restart

cat << EOF | su - postgres -c psql
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';

CREATE DATABASE $APP_DB_NAME WITH OWNER=$APP_DB_USER
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF

# Migrate the db
/flask-lessonshare/flask/bin/python manage.py db upgrade