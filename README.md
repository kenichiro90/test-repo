# Kanban Todo Application

A simple, web-based Kanban-style Todo application built with Flask.

## Features

- Create, move, and delete tasks.
- Tasks can be categorized into "Todo", "In Progress", and "Done".
- Add, update, and delete checklist items for each task.
- Data is persistently stored in a SQLite database (`todos.db`).

## Requirements

- Python 3.x
- Flask

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone YOUR_REPOSITORY_URL
    cd YOUR_REPOSITORY_DIRECTORY
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    The application will automatically create and initialize the `todos.db` database file on the first run.
    ```bash
    python app.py
    ```

4.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000`.