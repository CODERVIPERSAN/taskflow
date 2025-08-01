#!/bin/bash

echo "🚀 Starting Self-Balancing Task Manager..."

# Start Flask Backend
echo "Starting Flask backend..."
cd backend
nohup venv/bin/python app.py > app.log 2>&1 &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Start Frontend Server
echo "Starting frontend server..."
cd ../frontend
nohup python -m http.server 8080 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

# Wait for frontend to start
sleep 2

echo ""
echo "✅ Self-Balancing Task Manager is now running!"
echo ""
echo "🔗 Application URLs:"
echo "   Frontend: http://127.0.0.1:8080"
echo "   Backend API: http://127.0.0.1:5000/api"
echo ""
echo "📊 Features Available:"
echo "   ✓ View task scores and neutrality balance"
echo "   ✓ Complete tasks to decrease scores"
echo "   ✓ Add new tasks with custom increments"
echo "   ✓ Apply daily increments to all tasks"
echo "   ✓ Delete tasks"
echo "   ✓ View activity logs"
echo "   ✓ Real-time score updates"
echo ""
echo "🎯 Goal: Keep your total score at 0 or below for perfect balance!"
echo ""
echo "To stop the servers, run: ./stop_app.sh"
echo ""
echo "Open http://127.0.0.1:8080 in your browser to use the app!"
