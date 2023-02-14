#!/bin/sh

sh -c "pip3 install -r tests/functional/requirements.txt \
    && python3 -m pytest tests/functional/src"