# FastAPI Sample App

A sample project demonstrating a FastAPI backend with TypeScript-based web components for the frontend.

## 🚀 Getting Started

### 1. Compile TypeScript Components

Compile the TypeScript components for the frontend:

```bash
tsc -p ./frontend/
```

Or, in Visual Studio Code, press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd> to build.

### 2. Run the FastAPI App

You can start the FastAPI server in several ways:

- Using Python:

```bash
python -m app
```

- Using Uvicorn:

```bash
uvicorn app.__main__:app --reload --host 0.0.0.0 --port 8000
```

- In Visual Studio Code:

    - Press <kbd>Ctrl</kbd>+<kbd>F5</kbd> to start without debugging.
    - Press <kbd>F5</kbd> to start in debug mode.
