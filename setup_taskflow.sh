#!/bin/bash

echo "🎯 Setting up TaskFlow - Self-Balancing Task Manager"
echo "=================================================="

# Create backup directory
echo "📁 Creating backup directory..."
mkdir -p ~/taskflow_backup

# Backup current data if exists
if [ -f "backend/tasks.db" ]; then
    echo "💾 Backing up your existing data..."
    cp backend/tasks.db ~/taskflow_backup/tasks_original.db
fi

# Make scripts executable
chmod +x start_app.sh stop_app.sh

# Setup virtual environment
echo "🐍 Setting up Python virtual environment..."
cd backend
if [ ! -d "venv" ]; then
    python -m venv venv
fi

echo "📦 Installing Python dependencies..."
venv/bin/pip install -r requirements.txt

cd ..

# Make fish functions available
echo "🐟 Setting up Fish shell commands..."
mkdir -p ~/.config/fish/functions

# The fish functions are already created above

# Reload fish functions
echo "🔄 Reloading Fish shell functions..."
fish -c "source ~/.config/fish/functions/todaytask.fish"
fish -c "source ~/.config/fish/functions/stoptask.fish"

echo ""
echo "✅ TaskFlow setup complete!"
echo ""
echo "🚀 Usage:"
echo "  • Type 'todaytask' to start TaskFlow"
echo "  • Type 'stoptask' to stop TaskFlow"
echo ""
echo "🌐 TaskFlow will run on: http://127.0.0.1:8080"
echo "🔧 API available on: http://127.0.0.1:5000/api"
echo ""
echo "📚 Read README.md for detailed instructions"
echo ""
echo "🎯 Happy task balancing!"
