#!/bin/bash

chmod +x ./AIConnector.py

sudo mkdir -p /usr/local/bin/AIConnector/

sudo cp *.py /usr/local/bin/AIConnector

sudo ln -s /usr/local/bin/AIConnector/AIConnector.py /usr/local/bin/aicp

