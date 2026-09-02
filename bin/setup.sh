#!/usr/bin/env bash

set -e

echo "== CASHCOW SETUP =="

cd backend

if [! -d ".venv"]; then
    echo "Virtual Environment not found. Creating new .venv..."
    python -m venv .venv
fi

source .venv/Scripts/activate
pip install -r requirements.txt

if [! -f ".env"]; then
    echo ".env not found. Copying from .env.example..."
    echo "Fill in real values in backend/.env before running this application"
    cp .env.example .env
fi

cd ../frontend
npm install

echo "Setup Complete!"