# Step 1: Create the basic project structure
mkdir -p my_task_manager/frontend
mkdir -p my_task_manager/backend

# Step 2: Initialize a new Vue.js project for the frontend
cd my_task_manager/frontend
vue create .

# Choose default settings in case you need automated selections

# Step 3: Add Tailwind CSS and Bootstrap to the Vue.js project
# Install Tailwind CSS
npm install tailwindcss @tailwindcss/postcss7-compat @tailwindcss/forms @tailwindcss/typography postcss@^7 autoprefixer@^9

# Add Bootstrap
npm install bootstrap

# Configure Tailwind
npx tailwindcss init

# Step 4: Create base files for the Flask backend
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install flask

# Optionally install SQLite support
pip install sqlite

# Step 5: Create a basic main.py file for the Flask backend
cat <<EOL > app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Task Manager"

if __name__ == '__main__':
    app.run(debug=True)
EOL

# Finalize setup
cd ../..
echo "Project setup complete. Proceed with development!"
