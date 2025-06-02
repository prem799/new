from flask import Flask, render_template_string, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for session handling

# Mock user database
users = {
    "admin": "password123"
}

# In-memory employee record store
employee_records = []

# HTML templates (as strings for single-file simplicity)
login_template = '''
<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
  <style>
    body { font-family: sans-serif; background: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; }
    .container { background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 300px; }
    input, button { width: 100%; padding: 10px; margin-top: 10px; }
    .error { color: red; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Login</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <p class="error">{{ messages[0] }}</p>
      {% endif %}
    {% endwith %}
    <form method="POST">
      <input type="text" name="username" placeholder="Username" required>
      <input type="password" name="password" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
  </div>
</body>
</html>
'''

form_template = '''
<!DOCTYPE html>
<html>
<head>
  <title>Publish Employee</title>
  <style>
    body { font-family: sans-serif; background: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; }
    .container { background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 400px; }
    input, button { width: 100%; padding: 10px; margin-top: 10px; }
    label { font-weight: bold; margin-top: 10px; display: block; }
    .logout { text-align: right; margin-bottom: 10px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="logout">
      <a href="{{ url_for('logout') }}">Logout</a>
    </div>
    <h2>Publish Employee Details</h2>
    <form action="/submit" method="POST">
      <label>Employee Name</label>
      <input type="text" name="empName" required>
      <label>Employee ID</label>
      <input type="text" name="empId" required>
      <label>Department</label>
      <input type="text" name="department" required>
      <label>Designation</label>
      <input type="text" name="designation" required>
      <label>Email</label>
      <input type="email" name="email" required>
      <label>Joining Date</label>
      <input type="date" name="joinDate" required>
      <button type="submit">Publish</button>
    </form>
  </div>
</body>
</html>
'''

success_template = '''
<!DOCTYPE html>
<html>
<head>
  <title>Success</title>
  <style>
    body { font-family: sans-serif; background: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; }
    .container { background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 400px; }
    ul { padding-left: 0; list-style: none; }
    li { margin-bottom: 8px; }
    .back { margin-top: 20px; display: block; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Employee Details Published</h2>
    <ul>
      <li><strong>Name:</strong> {{ emp.name }}</li>
      <li><strong>ID:</strong> {{ emp.id }}</li>
      <li><strong>Department:</strong> {{ emp.department }}</li>
      <li><strong>Designation:</strong> {{ emp.designation }}</li>
      <li><strong>Email:</strong> {{ emp.email }}</li>
      <li><strong>Joining Date:</strong> {{ emp.join_date }}</li>
    </ul>
    <a class="back" href="{{ url_for('index') }}">Back to Form</a>
  </div>
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['username'] = uname
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template_string(login_template)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template_string(form_template)

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('login'))

    emp_details = {
        "name": request.form['empName'],
        "id": request.form['empId'],
        "department": request.form['department'],
        "designation": request.form['designation'],
        "email": request.form['email'],
        "join_date": request.form['joinDate']
    }
    employee_records.append(emp_details)
    return render_template_string(success_template, emp=emp_details)

if __name__ == '__main__':
    app.run(debug=True)
