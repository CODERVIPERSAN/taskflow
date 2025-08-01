#!/bin/bash

echo "🛑 Stopping Self-Balancing Task Manager..."

# Kill Flask backend
echo "Stopping Flask backend..."
pkill -f "python app.py"

# Kill Frontend server
echo "Stopping frontend server..."
pkill -f "python -m http.server 8080"

echo "✅ All servers stopped!"
