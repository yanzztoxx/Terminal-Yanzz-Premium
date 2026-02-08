#!/bin/bash

echo "[+] Installing"

pkg install -y python git nodejs nano

chmod +x yanzz.py
cp yanzz.py /data/data/com.termux/files/usr/bin/yanzz

echo ""
echo "[✓] Install selesai"
echo "Ketik: yanzz"
