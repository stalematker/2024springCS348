#!/bin/bash
set -euo pipefail

rm -rf shadow.data/
shadow --template-directory shadow.data.template shadow.yaml > shadow.log

