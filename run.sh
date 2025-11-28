#!/usr/bin/env bash

# Frontend
echo "=== Cài đặt npm ==="
cd frontend

# Xóa node_modules nếu bị lỗi
if [ -d "node_modules/vite" ] && [ ! -f "node_modules/vite/dist/node/cli.js" ]; then
    echo "=== Phát hiện Vite bị lỗi, đang cài lại... ==="
    rm -rf node_modules package-lock.json
    npm cache clean --force
fi

npm install

echo "=== Chạy server Reactjs ==="
npm run dev &

# Backend
echo "=== Tạo môi trường ảo... ==="
cd ../backend
python -m venv venv
source venv/Scripts/activate

echo "=== Cài đặt thư viện từ requirements.txt ==="
pip install -r requirements.txt

echo "=== Chạy server Django ==="
python manage.py runserver
