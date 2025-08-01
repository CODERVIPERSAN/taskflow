#!/bin/bash

# Daily Task Manager - Enhanced startup with system integration
# This script provides a complete daily task management experience

clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎯 DAILY TASK MANAGER                     ║"
echo "║                Self-Balancing Productivity System            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if it's a new day and apply daily increments
check_daily_increment() {
    local last_run_file="$HOME/.taskflow_last_run"
    local today=$(date +%Y-%m-%d)
    
    if [ -f "$last_run_file" ]; then
        local last_run=$(cat "$last_run_file")
        if [ "$last_run" != "$today" ]; then
            echo "📅 New day detected! Applying daily increments..."
            # Start the app briefly to apply increments
            cd ~/my_task_managing
            ./start_app.sh > /dev/null 2>&1 &
            sleep 5
            curl -s -X POST http://127.0.0.1:5000/api/daily-increment
            ./stop_app.sh > /dev/null 2>&1
            sleep 2
            echo "✅ Daily increments applied!"
        fi
    fi
    
    # Update last run date
    echo "$today" > "$last_run_file"
}

# Show motivational message based on time
show_time_greeting() {
    local hour=$(date +%H)
    local greeting=""
    local emoji=""
    
    if [ $hour -lt 6 ]; then
        greeting="Early bird"
        emoji="🌅"
    elif [ $hour -lt 12 ]; then
        greeting="Good morning"
        emoji="☀️"
    elif [ $hour -lt 17 ]; then
        greeting="Good afternoon"
        emoji="🌤️"
    elif [ $hour -lt 21 ]; then
        greeting="Good evening"
        emoji="🌆"
    else
        greeting="Night owl"
        emoji="🌙"
    fi
    
    echo "$emoji $greeting! Ready to balance your tasks?"
    echo ""
}

# Show current task summary
show_task_summary() {
    if [ -f ~/taskflow_backup/tasks_original.db ]; then
        echo "📊 Your Task Summary:"
        echo "────────────────────────────────────────"
        echo "💾 Personal data: ✅ Available"
        echo "🎯 Goal: Keep total score ≤ 0"
        echo "🔄 System: Auto-increments daily"
        echo ""
    else
        echo "🆕 Welcome to TaskFlow!"
        echo "────────────────────────────────────"
        echo "📝 This is your first time running TaskFlow"
        echo "🎯 Goal: Balance your tasks using numerical scoring"
        echo "📊 Demo data will be loaded for you to explore"
        echo ""
    fi
}

# Main execution
main() {
    show_time_greeting
    show_task_summary
    check_daily_increment
    
    echo "🚀 Starting TaskFlow..."
    echo "════════════════════════════════════════"
    
    # Use the fish function if available, otherwise use direct script
    if command -v fish > /dev/null && fish -c "functions -q todaytask" 2>/dev/null; then
        fish -c "todaytask"
    else
        # Fallback to direct execution
        cd ~/my_task_managing
        
        # Restore data
        if [ -f ~/taskflow_backup/tasks_original.db ]; then
            cp ~/taskflow_backup/tasks_original.db backend/tasks.db
        fi
        
        ./start_app.sh
        
        # Try to open browser
        sleep 3
        if command -v xdg-open > /dev/null; then
            xdg-open "http://127.0.0.1:8080" 2>/dev/null
        elif command -v open > /dev/null; then
            open "http://127.0.0.1:8080" 2>/dev/null
        else
            echo "🌐 Please open http://127.0.0.1:8080 in your browser"
        fi
    fi
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  TaskFlow is now running! Focus on achieving balance! 🎯   ║"
    echo "║                                                              ║"
    echo "║  💡 Tips:                                                    ║"
    echo "║  • Red scores need attention                                 ║"
    echo "║  • Green scores mean you're ahead                            ║"
    echo "║  • Aim for zero total score                                  ║"
    echo "║                                                              ║"
    echo "║  Type 'stoptask' when done                                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
}

# Run the main function
main
