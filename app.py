from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data store
app.todos = []
app.next_id = 1

@app.route('/')
def index():
    todos_todo = [t for t in app.todos if t['status'] == 'todo']
    todos_inprogress = [t for t in app.todos if t['status'] == 'inprogress']
    todos_done = [t for t in app.todos if t['status'] == 'done']
    return render_template('index.html', todos_todo=todos_todo, todos_inprogress=todos_inprogress, todos_done=todos_done)

@app.route('/move/<int:todo_id>', methods=['POST'])
def move_todo(todo_id):
    todo = find_todo_by_id(todo_id)
    if todo:
        if todo['status'] == 'todo':
            todo['status'] = 'inprogress'
        elif todo['status'] == 'inprogress':
            todo['status'] = 'done'
    return redirect(url_for('index'))

@app.route('/move_back/<int:todo_id>', methods=['POST'])
def move_todo_back(todo_id):
    todo = find_todo_by_id(todo_id)
    if todo:
        if todo['status'] == 'done':
            todo['status'] = 'inprogress'
        elif todo['status'] == 'inprogress':
            todo['status'] = 'todo'
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        app.todos.append({'id': app.next_id, 'task': task, 'status': 'todo', 'checklist': []})
        app.next_id += 1
    return redirect(url_for('index'))

def find_todo_by_id(todo_id):
    for todo in app.todos:
        if todo['id'] == todo_id:
            return todo
    return None

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    app.todos = [todo for todo in app.todos if todo['id'] != todo_id]
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
