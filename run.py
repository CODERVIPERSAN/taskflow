#!/usr/bin/env python3
"""
TASKFLOW - Self-Balancing Task Manager
Run: python run.py | Access: http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import sqlite3, os, webbrowser, json
from threading import Timer
from datetime import date, datetime, timedelta

app = Flask(__name__)
CORS(app)
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'taskflow.db')

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT DEFAULT '',
        score INTEGER DEFAULT 0, daily_increment INTEGER DEFAULT 1, category TEXT DEFAULT 'General',
        priority TEXT DEFAULT 'medium', created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        completion_count INTEGER DEFAULT 0, streak INTEGER DEFAULT 0, best_streak INTEGER DEFAULT 0,
        last_completed DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, action TEXT, details TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, description TEXT,
        icon TEXT, unlocked_at DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE UNIQUE, 
        completions INTEGER DEFAULT 0, score INTEGER DEFAULT 0)''')
    c.execute('SELECT COUNT(*) FROM tasks')
    if c.fetchone()[0] == 0:
        tasks = [('Learn Programming', 'Daily coding practice', 5, 2, 'Learning', 'high'),
                 ('Exercise', '30 min physical activity', 3, 3, 'Health', 'high'),
                 ('Read Books', 'Read 20 pages daily', -1, 1, 'Learning', 'medium'),
                 ('Meditation', '10 min mindfulness', 0, 1, 'Health', 'medium'),
                 ('Side Project', 'Work on projects', 8, 2, 'Work', 'high')]
        c.executemany('INSERT INTO tasks (name,description,score,daily_increment,category,priority) VALUES (?,?,?,?,?,?)', tasks)
        c.execute('INSERT INTO logs (action,details) VALUES (?,?)', ('system', 'TaskFlow initialized'))
    # Add columns if they don't exist (for existing databases)
    try: c.execute('ALTER TABLE tasks ADD COLUMN streak INTEGER DEFAULT 0')
    except: pass
    try: c.execute('ALTER TABLE tasks ADD COLUMN best_streak INTEGER DEFAULT 0')
    except: pass
    try: c.execute('ALTER TABLE tasks ADD COLUMN last_completed DATE')
    except: pass
    conn.commit()
    conn.close()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY score DESC').fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    d = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO tasks (name,description,score,daily_increment,category,priority) VALUES (?,?,?,?,?,?)',
              (d.get('name','Task'), d.get('description',''), d.get('score',0), d.get('daily_increment',1), d.get('category','General'), d.get('priority','medium')))
    c.execute('INSERT INTO logs (task_name,action,details) VALUES (?,?,?)', (d.get('name'), 'created', 'New task'))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    d = request.json
    conn = get_db()
    conn.execute('UPDATE tasks SET name=?,description=?,daily_increment=?,category=?,priority=? WHERE id=?',
                 (d.get('name'), d.get('description'), d.get('daily_increment'), d.get('category'), d.get('priority'), id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/tasks/<int:id>/complete', methods=['POST'])
def complete_task(id):
    conn = get_db()
    c = conn.cursor()
    t = c.execute('SELECT name,score,streak,best_streak,last_completed FROM tasks WHERE id=?', (id,)).fetchone()
    if t:
        today = str(date.today())
        yesterday = str(date.today() - timedelta(days=1))
        last = t['last_completed']
        streak = t['streak'] or 0
        best = t['best_streak'] or 0
        
        # Update streak
        if last == today:
            pass  # Already completed today, just increment count
        elif last == yesterday:
            streak += 1  # Continue streak
        else:
            streak = 1  # Start new streak
        
        if streak > best:
            best = streak
            check_achievements(c, 'streak', best)
        
        c.execute('UPDATE tasks SET score=score-1, completion_count=completion_count+1, streak=?, best_streak=?, last_completed=? WHERE id=?', 
                  (streak, best, today, id))
        c.execute('INSERT INTO logs (task_name,action,details) VALUES (?,?,?)', 
                  (t['name'], 'completed', f"Score: {t['score']} → {t['score']-1} | Streak: {streak}🔥"))
        
        # Update daily stats
        c.execute('INSERT OR REPLACE INTO daily_stats (date, completions, score) VALUES (?, COALESCE((SELECT completions FROM daily_stats WHERE date=?),0)+1, ?)',
                  (today, today, t['score']-1))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'streak': streak if t else 0})

def check_achievements(cursor, type, value):
    achievements = []
    if type == 'streak':
        if value >= 3: achievements.append(('streak_3', '3 Day Streak', 'Completed a task 3 days in a row', '🔥'))
        if value >= 7: achievements.append(('streak_7', 'Week Warrior', 'Completed a task 7 days in a row', '⚡'))
        if value >= 30: achievements.append(('streak_30', 'Monthly Master', 'Completed a task 30 days in a row', '👑'))
    for a in achievements:
        try: cursor.execute('INSERT INTO achievements (name, description, icon, unlocked_at) VALUES (?,?,?,?)', (a[0], a[1], a[3], datetime.now()))
        except: pass

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db()
    c = conn.cursor()
    t = c.execute('SELECT name FROM tasks WHERE id=?', (id,)).fetchone()
    if t:
        c.execute('DELETE FROM tasks WHERE id=?', (id,))
        c.execute('INSERT INTO logs (task_name,action,details) VALUES (?,?,?)', (t['name'], 'deleted', 'Task removed'))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/daily-increment', methods=['POST'])
def daily_increment():
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE tasks SET score = score + daily_increment')
    c.execute('INSERT INTO logs (action,details) VALUES (?,?)', ('daily_increment', 'Applied to all tasks'))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = get_db()
    logs = conn.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50').fetchall()
    conn.close()
    return jsonify([dict(l) for l in logs])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    c = conn.cursor()
    return jsonify({
        'total_score': c.execute('SELECT COALESCE(SUM(score),0) FROM tasks').fetchone()[0],
        'task_count': c.execute('SELECT COUNT(*) FROM tasks').fetchone()[0],
        'critical': c.execute('SELECT COUNT(*) FROM tasks WHERE score > 5').fetchone()[0],
        'attention': c.execute('SELECT COUNT(*) FROM tasks WHERE score > 0 AND score <= 5').fetchone()[0],
        'balanced': c.execute('SELECT COUNT(*) FROM tasks WHERE score = 0').fetchone()[0],
        'ahead': c.execute('SELECT COUNT(*) FROM tasks WHERE score < 0').fetchone()[0],
        'completions': c.execute('SELECT COALESCE(SUM(completion_count),0) FROM tasks').fetchone()[0],
        'best_streak': c.execute('SELECT COALESCE(MAX(best_streak),0) FROM tasks').fetchone()[0],
        'active_streaks': c.execute('SELECT COUNT(*) FROM tasks WHERE streak > 0').fetchone()[0]
    })

# Feature 1: Achievements
@app.route('/api/achievements', methods=['GET'])
def get_achievements():
    conn = get_db()
    achievements = conn.execute('SELECT * FROM achievements ORDER BY unlocked_at DESC').fetchall()
    conn.close()
    all_achievements = [
        {'id': 'streak_3', 'name': '3 Day Streak', 'desc': 'Complete a task 3 days in a row', 'icon': '🔥'},
        {'id': 'streak_7', 'name': 'Week Warrior', 'desc': 'Complete a task 7 days in a row', 'icon': '⚡'},
        {'id': 'streak_30', 'name': 'Monthly Master', 'desc': 'Complete a task 30 days in a row', 'icon': '👑'},
        {'id': 'first_task', 'name': 'Getting Started', 'desc': 'Complete your first task', 'icon': '🎯'},
        {'id': 'ten_completions', 'name': 'On a Roll', 'desc': 'Complete 10 tasks total', 'icon': '🚀'},
        {'id': 'balanced', 'name': 'Perfect Balance', 'desc': 'Reach a total score of 0', 'icon': '⚖️'},
    ]
    unlocked = {a['name'] for a in [dict(x) for x in achievements]}
    for a in all_achievements:
        a['unlocked'] = a['name'] in unlocked
    return jsonify(all_achievements)

# Feature 2: Weekly Progress
@app.route('/api/weekly-progress', methods=['GET'])
def weekly_progress():
    conn = get_db()
    c = conn.cursor()
    days = []
    for i in range(6, -1, -1):
        d = str(date.today() - timedelta(days=i))
        row = c.execute('SELECT completions FROM daily_stats WHERE date=?', (d,)).fetchone()
        completions = row[0] if row else 0
        # Also count from logs as fallback
        if completions == 0:
            completions = c.execute("SELECT COUNT(*) FROM logs WHERE action='completed' AND DATE(timestamp)=?", (d,)).fetchone()[0]
        days.append({'date': d, 'day': (date.today() - timedelta(days=i)).strftime('%a'), 'completions': completions})
    conn.close()
    return jsonify(days)

# Feature 3: Search & Filter (handled in frontend, but add categories endpoint)
@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    cats = conn.execute('SELECT DISTINCT category FROM tasks').fetchall()
    conn.close()
    return jsonify([c['category'] for c in cats])

# Feature 4: Export Data
@app.route('/api/export', methods=['GET'])
def export_data():
    conn = get_db()
    data = {
        'tasks': [dict(t) for t in conn.execute('SELECT * FROM tasks').fetchall()],
        'logs': [dict(l) for l in conn.execute('SELECT * FROM logs').fetchall()],
        'achievements': [dict(a) for a in conn.execute('SELECT * FROM achievements').fetchall()],
        'exported_at': datetime.now().isoformat()
    }
    conn.close()
    return jsonify(data)

# Feature 4: Import Data
@app.route('/api/import', methods=['POST'])
def import_data():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    if 'tasks' in data:
        c.execute('DELETE FROM tasks')
        for t in data['tasks']:
            c.execute('INSERT INTO tasks (name,description,score,daily_increment,category,priority,completion_count,streak,best_streak) VALUES (?,?,?,?,?,?,?,?,?)',
                      (t.get('name'), t.get('description',''), t.get('score',0), t.get('daily_increment',1), 
                       t.get('category','General'), t.get('priority','medium'), t.get('completion_count',0),
                       t.get('streak',0), t.get('best_streak',0)))
    c.execute('INSERT INTO logs (action,details) VALUES (?,?)', ('import', f"Imported {len(data.get('tasks',[]))} tasks"))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Feature 5: Get Critical Tasks for Notifications
@app.route('/api/critical', methods=['GET'])
def get_critical():
    conn = get_db()
    tasks = conn.execute('SELECT id,name,score,category FROM tasks WHERE score > 5 ORDER BY score DESC LIMIT 5').fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route('/')
def index():
    return Response(open(os.path.join(os.path.dirname(__file__), 'index.html')).read(), mimetype='text/html')

if __name__ == '__main__':
    print('\n🎯 TaskFlow - http://127.0.0.1:5000\n')
    init_db()
    Timer(1.5, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
