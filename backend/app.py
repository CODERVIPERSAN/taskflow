from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import datetime
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Vue.js frontend

# Database initialization
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            daily_increment INTEGER DEFAULT 3,
            last_updated DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Create task_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    ''')
    
    # Insert sample data if not exists
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        sample_tasks = [
            ('Learn Python', 8, 3),
            ('Daily Exercise', 15, 5),
            ('Read Books', -2, 2),
            ('Language Practice', -8, 3),
            ('Side Project', 12, 4),
            ('Meditation', -1, 2),
            ('Cooking Skills', 6, 3),
            ('Network Building', 9, 3)
        ]
        cursor.executemany('INSERT INTO tasks (name, score, daily_increment) VALUES (?, ?, ?)', sample_tasks)
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Self-Balancing Task Manager API"})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, score, daily_increment FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task[0],
            'name': task[1],
            'score': task[2],
            'daily_increment': task[3]
        })
    
    return jsonify(task_list)

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    # Decrease task score by 1
    cursor.execute('UPDATE tasks SET score = score - 1 WHERE id = ?', (task_id,))
    
    # Log the completion
    cursor.execute('INSERT INTO task_logs (task_id, action) VALUES (?, ?)', (task_id, 'completed'))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Task completed successfully"})

@app.route('/api/tasks/add', methods=['POST'])
def add_task():
    data = request.json
    name = data.get('name')
    score = data.get('score', 0)
    daily_increment = data.get('daily_increment', 3)
    
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (name, score, daily_increment) VALUES (?, ?, ?)', 
                   (name, score, daily_increment))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Task added successfully"})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Task deleted successfully"})

@app.route('/api/daily-increment', methods=['POST'])
def daily_increment():
    """Manually trigger daily increment for all tasks"""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    # Update all tasks with their daily increment
    cursor.execute('UPDATE tasks SET score = score + daily_increment')
    
    # Log the daily increment
    cursor.execute('INSERT INTO task_logs (task_id, action) VALUES (NULL, ?)', ('daily_increment',))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Daily increment applied successfully"})

@app.route('/api/total-score', methods=['GET'])
def get_total_score():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(score) FROM tasks')
    total = cursor.fetchone()[0] or 0
    conn.close()
    
    return jsonify({"total_score": total})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tl.id, t.name, tl.action, tl.timestamp
        FROM task_logs tl
        LEFT JOIN tasks t ON tl.task_id = t.id
        ORDER BY tl.timestamp DESC
        LIMIT 50
    ''')
    logs = cursor.fetchall()
    conn.close()
    
    log_list = []
    for log in logs:
        log_list.append({
            'id': log[0],
            'task_name': log[1] or 'System',
            'action': log[2],
            'timestamp': log[3]
        })
    
    return jsonify(log_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
