#!/bin/bash
set -euo pipefail

# shadow's requiring dependencies:
echo "installing shadow's dependencies via apt-get"
sudo apt-get install -y \
    cmake \
    findutils \
    libclang-dev \
    libc-dbg \
    libglib2.0-0 \
    libglib2.0-dev \
    libigraph-dev \
    make \
    netbase \
    python3 \
    python3-networkx \
    xz-utils \
    util-linux \
    gcc \
    g++

# rustup: https://rustup.rs
echo "installing cargo"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# shadow
echo "installing shadow"
git clone https://github.com/shadow/shadow.git
cd shadow
./setup build --clean --test
./setup test
./setup install
echo 'export PATH="${PATH}:/home/${USER}/.local/bin"' >> ~/.bashrc && source ~/.bashrc

echo "successfully installed shadow"
