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
pnpm install --frozen-lockfile

pnpm update

pnpm build


