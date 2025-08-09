import sqlite3

def get_db_connection():
    """データベース接続を取得します。接続は辞書のように振る舞うRowオブジェクトを返します。"""
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """データベースを初期化し、テーブルを作成します。"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Todosテーブルの作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('todo', 'inprogress', 'done'))
    )
    ''')

    # Checklist Itemsテーブルの作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS checklist_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        checked INTEGER NOT NULL DEFAULT 0,
        todo_id INTEGER NOT NULL,
        FOREIGN KEY (todo_id) REFERENCES todos (id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("データベースを初期化しています...")
    init_db()
    print("データベースの初期化が完了しました。")
