
# ---------------------------------------------------------------------------- #

from app.services import get_configuration

# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    """
    Main entry point for the application. Loads the configuration and starts
    the application server.
    """
    import uvicorn

    config = get_configuration()
    host = config.backend.host
    port = int(config.backend.port)

    uvicorn.run(app="app:create_app", host=host,
                port=port, reload=True, factory=True)

# ---------------------------------------------------------------------------- #
