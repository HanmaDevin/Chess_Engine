#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    pip install ./requirements.txt
    python3 ../Chess/src/main/Main.py
fi
# Mac OSX
if [[ "$OSTYPE" == "darwin"* ]]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    export PATH="/usr/local/opt/python/libexec/bin:$PATH"
    brew install python
    pip install ./requirements.txt
    python3 ../Chess/src/main/Main.py
fi