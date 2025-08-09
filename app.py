from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data store
todos = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    task = request.form.get('task')
    if task:
        todos.append({'id': next_id, 'task': task, 'done': False, 'checklist': []})
        next_id += 1
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = not todo['done']
            break
    return redirect(url_for('index'))

def find_todo_by_id(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    return None

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect(url_for('index'))

@app.route('/todo/<int:todo_id>/checklist/add', methods=['POST'])
def add_checklist_item(todo_id):
    todo = find_todo_by_id(todo_id)
    item_text = request.form.get('item')
    if todo and item_text:
        todo['checklist'].append({'item': item_text, 'checked': False})
    return redirect(url_for('index'))

@app.route('/todo/<int:todo_id>/checklist/update/<int:item_index>', methods=['POST'])
def update_checklist_item(todo_id, item_index):
    todo = find_todo_by_id(todo_id)
    if todo and 0 <= item_index < len(todo['checklist']):
        item = todo['checklist'][item_index]
        item['checked'] = not item['checked']
    return redirect(url_for('index'))

@app.route('/todo/<int:todo_id>/checklist/delete/<int:item_index>', methods=['POST'])
def delete_checklist_item(todo_id, item_index):
    todo = find_todo_by_id(todo_id)
    if todo and 0 <= item_index < len(todo['checklist']):
        todo['checklist'].pop(item_index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
