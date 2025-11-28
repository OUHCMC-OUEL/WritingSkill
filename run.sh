#!/usr/bin/env bash

#Frontend
echo "=== cài đặt npm ==="
cd frontend
npm install

echo "=== Chạy server Reactjs ==="
npm run dev &


#Backend
echo "=== Tạo môi trường ảo... ==="
cd ../backend
python -m venv venv
. venv/Scripts/activate

echo "=== cài đặt thư viện từ requirements.txt ==="
pip install -r requirements.txt

echo "=== Chạy server Django ==="
python manage.py runserver
