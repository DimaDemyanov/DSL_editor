#/bin/bash

# Run this script only at once to setup environment for Editor

# install Graphviz
./editor-master/install.sh

# install node dependencies
cd front
npm install

# report everything's fine
echo "Editor installation finish"

