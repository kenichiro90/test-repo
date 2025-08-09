import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g
from database import init_db

app = Flask(__name__)
DATABASE = 'todos.db'

def get_db():
    """リクエストごとに一意のデータベース接続を取得し、再利用します。"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """リクエストの最後にデータベース接続を閉じます。"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# アプリケーションコンテキスト内でデータベースを初期化
with app.app_context():
    init_db()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM todos ORDER BY id DESC")
    all_todos_raw = cursor.fetchall()

    todos_by_status = {'todo': [], 'inprogress': [], 'done': []}

    for todo_raw in all_todos_raw:
        todo = dict(todo_raw)
        cursor.execute("SELECT * FROM checklist_items WHERE todo_id = ? ORDER BY id", (todo['id'],))
        checklist_items_raw = cursor.fetchall()
        todo['checklist'] = [dict(item) for item in checklist_items_raw]

        if todo['status'] in todos_by_status:
            todos_by_status[todo['status']].append(todo)

    return render_template('index.html',
                           todos_todo=todos_by_status['todo'],
                           todos_inprogress=todos_by_status['inprogress'],
                           todos_done=todos_by_status['done'])

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        db = get_db()
        db.execute("INSERT INTO todos (task, status) VALUES (?, ?)", (task, 'todo'))
        db.commit()
    return redirect(url_for('index'))

@app.route('/move/<int:todo_id>', methods=['POST'])
def move_todo(todo_id):
    db = get_db()
    todo = db.execute("SELECT status FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if todo:
        new_status = ''
        if todo['status'] == 'todo':
            new_status = 'inprogress'
        elif todo['status'] == 'inprogress':
            new_status = 'done'

        if new_status:
            db.execute("UPDATE todos SET status = ? WHERE id = ?", (new_status, todo_id))
            db.commit()

    return redirect(url_for('index'))

@app.route('/move_back/<int:todo_id>', methods=['POST'])
def move_todo_back(todo_id):
    db = get_db()
    todo = db.execute("SELECT status FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if todo:
        new_status = ''
        if todo['status'] == 'done':
            new_status = 'inprogress'
        elif todo['status'] == 'inprogress':
            new_status = 'todo'

        if new_status:
            db.execute("UPDATE todos SET status = ? WHERE id = ?", (new_status, todo_id))
            db.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/todo/<int:todo_id>/checklist/add', methods=['POST'])
def add_checklist_item(todo_id):
    item_text = request.form.get('item')
    if item_text:
        db = get_db()
        db.execute("INSERT INTO checklist_items (item, todo_id) VALUES (?, ?)", (item_text, todo_id))
        db.commit()
    return redirect(url_for('index'))

@app.route('/todo/<int:todo_id>/checklist/update/<int:item_id>', methods=['POST'])
def update_checklist_item(todo_id, item_id):
    db = get_db()
    item = db.execute("SELECT checked FROM checklist_items WHERE id = ?", (item_id,)).fetchone()
    if item:
        new_checked_status = 1 - item['checked']
        db.execute("UPDATE checklist_items SET checked = ? WHERE id = ?", (new_checked_status, item_id))
        db.commit()
    return redirect(url_for('index'))

@app.route('/todo/<int:todo_id>/checklist/delete/<int:item_id>', methods=['POST'])
def delete_checklist_item(todo_id, item_id):
    db = get_db()
    db.execute("DELETE FROM checklist_items WHERE id = ?", (item_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
