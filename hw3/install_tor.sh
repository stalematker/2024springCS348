#!/bin/bash
set -euo pipefail 

# tor's dependencies:
echo "installing tor's dependencies via apt-get"
sudo apt-get install -y \
    automake \
    libevent-dev \
    libssl-dev


# installing tor
echo "installing tor"
git clone https://gitlab.torproject.org/tpo/core/tor.git
cd tor
./autogen.sh
chmod +x ./scripts/build/combine_libs ./doc/asciidoc-helper.sh 
./configure --disable-asciidoc
make
sudo make install

echo "successfully installed tor"

