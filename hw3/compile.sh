#!/bin/bash
set -euo pipefail

cd tor

# ./configure --disable-asciidoc
make
sudo make install

cd ../
echo "succesfully compiled tor"
