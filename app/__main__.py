
# ---------------------------------------------------------------------------- #

import os

# ---------------------------------------------------------------------------- #

import app.services as services

# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    """
    Main entry point for the application. Loads the configuration and starts
    the application server.
    """
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(app="app:create_app", host=host,
                port=port, reload=True, factory=True)

# ---------------------------------------------------------------------------- #
