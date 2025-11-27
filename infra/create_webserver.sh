#!/bin/sh

# disable auto upgrades by apt - in dev mode only
cd /home/dave

# go with newer apt which gets dependency updates too (like linux-azure)
sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install unzip -y

# /home/dave/server
# /home/dave/client
# o for overwrite
# q for quiet
unzip -oq all.zip



## FRONTEND Client 

# need node installed to do a build

# nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


# node 24.11.1 and npm 11.6.2 on 26th Nov 25
nvm install --lts --latest-npm

npm install --global corepack@latest

# pnpm
corepack enable pnpm
corepack prepare pnpm@latest --activate

cd /home/dave/client
# todo don't upload them
rm -rf node_modules

pnpm install --frozen-lockfile

pnpm update

pnpm build


## BACKEND Server

cd /home/dave/server

# todo - tidy this up ie don't zip all this up to copy 
rm -rf __pycache__
rm -rf .venv

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env 

uv lock --upgrade
uv sync

 Set production environment
export ENVIRONMENT=production

# see notes on workers for production deployment
# uv run uvicorn main:app --host 0.0.0.0 --port 3000 --workers 4
# uv run uvicorn main:app --host 0.0.0.0 --port 3000

# no idea why above didn't work.. but this does and runs 3000 from config

# RUN THIS MANUALLY NOW
# uv run python -m uvicorn main:app --host 0.0.0.0


## MySQL

sudo apt-get install mysql-server -y

# create database and user and tables and sample data
# run the file create_db.sql    
sudo mysql < /home/dave/infra/create_db.sql


# nginx
sudo apt-get install nginx -y

sudo cp /home/dave/infra/nginx.conf /etc/nginx/sites-available/default

sudo systemctl enable nginx
sudo systemctl restart nginx

# **TODO - create db
# create prod user - doug
# create tables