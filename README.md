# FastAPI Sample App

## Compile TS components

```bash
tsc frontend/components/input.ts --outDir frontend/static/
```

## Run the App

```bash
python -m app
```

or

```bash
uvicorn app.__main__:app --reload --host 0.0.0.0 --port 8000
```