#/bin/bash

# Run this script only at once to setup environment for Editor

# install Graphviz
sudo apt-get install graphviz

# install ANTLR
sudo apt-get install antlr4

# install python requirements
cd editor-master
pip3 install -r requirements.txt

# install node dependencies
cd ../front
npm install

# report everything's fine
echo "Editor installation finish"

