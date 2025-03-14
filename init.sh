#!/bin/bash

ansible-vault  view .credentials > credentials.py \
    && python main.py \
    && rm -rf credentials.py
