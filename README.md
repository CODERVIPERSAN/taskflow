# 🎯 TaskFlow - Self-Balancing Task Manager

**A smart, numerical approach to task management that helps you maintain perfect work-life balance.**

TaskFlow uses a unique scoring system where tasks accumulate points daily and decrease when completed. Your goal is to keep your total score at zero or below - achieving perfect balance!

![TaskFlow Dashboard](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Vue.js](https://img.shields.io/badge/Vue.js-3.0-green) ![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey)

## 🌟 Features

### 🎮 Core Concept
- **Self-Balancing System**: Tasks auto-increment daily, decrease when completed
- **Numerical Feedback**: Visual scoring system with color-coded indicators
- **Goal-Oriented**: Aim for zero or negative total score for perfect balance

### 🎨 User Interface
- **Modern Glass-morphism Design** with gradient backgrounds
- **Responsive Navigation** with 4 main sections
- **Real-time Updates** every 30 seconds
- **Interactive Animations** and hover effects

### 📊 Dashboard Features
- **Neutrality Score**: Live total score with motivational messages
- **Quick Stats**: Total tasks, attention needed, ahead, balanced
- **Task Cards**: Individual task management with completion tracking
- **Activity Log**: Track all actions with timestamps

### ⚙️ Management Tools
- **Add Tasks**: Custom names, initial scores, daily increments
- **Complete Tasks**: One-click completion (-1 score)
- **Daily Increment**: Bulk apply daily increases
- **Delete Tasks**: Remove unwanted tasks
- **Data Persistence**: SQLite database with logging

## 🚀 Quick Start

### One-Command Setup
```bash
git clone https://github.com/yourusername/taskflow.git
cd taskflow
./setup_taskflow.sh
```

### Daily Usage
```bash
# Start TaskFlow
todaytask

# Stop TaskFlow  
stoptask
```

### Manual Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/taskflow.git
   cd taskflow
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # From the project root
   chmod +x start_app.sh
   ./start_app.sh
   ```

4. **Access the app**
   - Open your browser and go to `http://127.0.0.1:8080`
   - Backend API available at `http://127.0.0.1:5000/api`

## 📱 How to Use TaskFlow

### 🎯 Understanding the Scoring System

**The Goal**: Keep your total neutrality score at **0 or below**

- **Positive scores** (Red) = Tasks need attention
- **Negative scores** (Green) = You're ahead of schedule  
- **Zero scores** (Gray) = Perfect balance

### 📝 Managing Tasks

1. **Adding Tasks**
   - Click "Add New Task" button
   - Enter task name, initial score, and daily increment
   - Higher daily increments = more important tasks

2. **Completing Tasks**
   - Click the green "Complete Task" button
   - Each completion reduces the task score by 1
   - Watch your neutrality score improve!

3. **Daily Increments**
   - Click "Apply Daily Increment" to simulate daily accumulation
   - Each task increases by its daily increment value
   - Represents the natural buildup of pending work

### 🧭 Navigation Sections

- **🏠 Dashboard**: Overview, stats, and main controls
- **📋 Tasks**: Full task management interface
- **📊 Analytics**: Performance insights and trends
- **❓ Help**: User guidance and tips

## 🛠️ Technical Stack

### Backend
- **Flask**: Python web framework
- **SQLite**: Lightweight database
- **Flask-CORS**: Cross-origin resource sharing

### Frontend  
- **Vue.js 3**: Progressive JavaScript framework
- **Bootstrap 5**: CSS framework
- **Tailwind CSS**: Utility-first CSS
- **Font Awesome**: Icon library
- **Axios**: HTTP client

### Deployment
- **Simple HTTP Server**: Frontend serving
- **Shell Scripts**: Easy startup/shutdown

## 📁 Project Structure

```
taskflow/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── tasks.db              # SQLite database
│   └── venv/                 # Python virtual environment
├── frontend/
│   ├── index.html            # Main Vue.js application
│   └── public/               # Static assets
├── start_app.sh              # Startup script
├── stop_app.sh               # Shutdown script
├── setup_taskflow.sh         # Complete setup script
├── daily_task_manager.sh     # Enhanced daily startup
└── README.md                 # This file
```

## 🔧 Command Line Tools

### Available Commands
- `todaytask` - Start TaskFlow with enhanced daily management
- `stoptask` - Stop TaskFlow and backup data
- `./daily_task_manager.sh` - Enhanced startup with motivational messages
- `./start_app.sh` - Basic startup
- `./stop_app.sh` - Basic shutdown

### Smart Features
- **Automatic daily increments** on new days
- **Data backup and restore** functionality
- **Time-based motivational messages**
- **Browser auto-opening**
- **Personal data preservation**

## 🔧 API Endpoints

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks/add` - Add new task
- `POST /api/tasks/{id}/complete` - Complete task
- `DELETE /api/tasks/{id}` - Delete task

### System
- `GET /api/total-score` - Get neutrality score
- `POST /api/daily-increment` - Apply daily increments
- `GET /api/logs` - Get activity logs

## 🎨 Customization

### Adding New Task Categories
Edit the sample tasks in `backend/app.py`:
```python
sample_tasks = [
    ('Your Task Name', initial_score, daily_increment),
    # Add more tasks here
]
```

### Styling
Modify the CSS in `frontend/index.html` to customize:
- Colors and gradients
- Glass-morphism effects
- Animations and transitions

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   ./stop_app.sh
   ./start_app.sh
   ```

2. **Database not found**
   - Delete `backend/tasks.db` and restart
   - Fresh database will be created with sample data

3. **Frontend not loading**
   - Check if port 8080 is available
   - Try `python -m http.server 8081` in frontend folder

4. **API errors**
   - Ensure Flask backend is running on port 5000
   - Check `backend/app.log` for error details

### Resetting Data
```bash
rm backend/tasks.db
./start_app.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Roadmap

- [ ] User authentication and profiles
- [ ] Task categories and tags
- [ ] Weekly/monthly analytics
- [ ] Mobile app version
- [ ] Calendar integration
- [ ] Team collaboration features
- [ ] Smart notifications
- [ ] Data export/import

## 🙏 Acknowledgments

- Vue.js community for excellent documentation
- Flask team for the lightweight framework
- Bootstrap and Tailwind CSS for beautiful styling
- All contributors and testers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for better productivity and work-life balance**

*Start your journey to perfect task balance today!* 🎯

## 🚀 Ready to Push to GitHub?

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed instructions on how to push this project to your GitHub repository.
