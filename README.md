# かんばんTodoアプリケーション

Flaskで構築された、シンプルなWebベースのかんばん風Todoアプリケーションです。

## 主な機能

- タスクの作成、移動、削除
- タスクを「Todo」、「In Progress」（作業中）、「Done」（完了）のカテゴリに分類
- 各タスクにチェックリスト項目を追加、更新、削除
- データはSQLiteデータベース（`todos.db`）に永続的に保存されます

## 必要なもの

- Python 3.x
- Flask

## セットアップと使い方

1.  **リポジトリをクローンする:**
    ```bash
    git clone あなたのリポジトリURL
    cd あなたのリポジトリのディレクトリ
    ```

2.  **依存関係をインストールする:**
    仮想環境の使用を推奨します。
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate` を使用
    pip install -r requirements.txt
    ```

3.  **アプリケーションを実行する:**
    初回実行時に、`todos.db`というデータベースファイルが自動的に作成・初期化されます。
    ```bash
    python app.py
    ```

4.  **アプリケーションにアクセスする:**
    Webブラウザを開き、`http://127.0.0.1:5000`にアクセスしてください。