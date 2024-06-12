#!/bin/bash
set -euo pipefail

# tgen
echo "installing tgen"
git clone https://github.com/shadow/tgen.git

cd tgen
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/.local
make
sudo make install

echo "successfully installed tgen"

