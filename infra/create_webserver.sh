#!/bin/sh

# disable auto upgrades by apt - in dev mode only
cd /home/dave

# go with newer apt which gets dependency updates too (like linux-azure)
sudo apt-get update -y
sudo apt-get upgrade -y