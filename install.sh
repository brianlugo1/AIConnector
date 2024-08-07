#!/bin/bash

chmod +x ./AIConnector.py

sudo mkdir /usr/local/bin/AIConnector/

sudo cp *.py /usr/local/bin/AIConnector

ln /usr/local/bin/AIConnector/AIConnector.py /usr/local/bin/aicp

