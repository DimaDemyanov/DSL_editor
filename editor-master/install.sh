#/bin/bash

# Run this script only at once to setup environment for DSL-Editor server

# install python requirements
pip3 install -r requirements.txt

apt-get update

# install Graphviz
apt-get -y install graphviz

# install ANTLR
apt-get -y install antlr4

# report everything's fine
echo "Editor installation finish"

