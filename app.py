from flask import Flask, render_template, request, redirect, url_for
from models import db, Reminder, Task, Note, Mood, HealthLog
from gradio_client import Client
from datetime import datetime, time, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Gradio Hugging Face AI client
client = Client("huggingface-projects/gemma-3n-E4B-it")

# Create the database tables
with app.app_context():
    db.create_all()

# ---------- Routes ----------

@app.route('/', methods=['GET', 'POST'])
def home():
    ai_response = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        try:
            ai_response = client.predict(
                message={"text": user_input},
                system_prompt="You are a helpful assistant.",
                max_new_tokens=300,
                api_name="/chat"
            )
        except Exception as e:
            ai_response = "Error: " + str(e)
    return render_template('base.html', ai_response=ai_response)

# ---------------- Reminders ----------------
@app.route('/reminders')
def reminders():
    reminders = Reminder.query.order_by(Reminder.time).all()
    return render_template('reminders.html', reminders=reminders)

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    title = request.form['title']
    time_str = request.form['time']
    new_reminder = Reminder(title=title, time=time_str)
    db.session.add(new_reminder)
    db.session.commit()
    return redirect(url_for('reminders'))

@app.route('/delete_reminder/<int:id>')
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()
    return redirect(url_for('reminders'))

@app.route('/add_default_reminders')
def add_default_reminders():
    # Drinking Water: Every 1 hour from 7 AM to 10 PM
    start_time = datetime.strptime("07:00", "%H:%M")
    for i in range(8):  # 8 reminders = every ~2 hours for 3 liters
        drink_time = (start_time + timedelta(hours=i * 2)).time()
        db.session.add(Reminder(title="Drink Water 💧", time=drink_time.strftime("%H:%M")))

    # Food Reminders
    db.session.add(Reminder(title="🍽️ Breakfast Time", time="08:30"))
    db.session.add(Reminder(title="🍛 Lunch Time", time="13:00"))
    db.session.add(Reminder(title="🍲 Dinner Time", time="20:00"))

    db.session.commit()
    return redirect(url_for('reminders'))

# ---------------- Tasks ----------------
@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    due_date = request.form['due_date']
    new_task = Task(title=title, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))

# ---------------- Notes ----------------
@app.route('/notes')
def notes():
    notes = Note.query.all()
    return render_template('notes.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    content = request.form['content']
    new_note = Note(content=content)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/delete_note/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes'))

# ---------------- Mood Tracker ----------------
@app.route('/mood')
def view_mood():
    moods = Mood.query.all()
    return render_template('mood.html', moods=moods)

@app.route('/add_mood', methods=['GET', 'POST'])
def add_mood():
    if request.method == 'POST':
        feeling = request.form['feeling']
        note = request.form.get('note')
        new_mood = Mood(feeling=feeling, note=note)
        db.session.add(new_mood)
        db.session.commit()
        return redirect(url_for('view_mood'))
    return render_template('add_mood.html')

@app.route('/delete_mood/<int:id>')
def delete_mood(id):
    mood = Mood.query.get_or_404(id)
    db.session.delete(mood)
    db.session.commit()
    return redirect(url_for('view_mood'))

# ---------------- Health Tracker ----------------
@app.route('/health')
def health():
    logs = HealthLog.query.all()
    return render_template('health.html', logs=logs)

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
