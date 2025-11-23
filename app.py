from mediaserver import create_app
import os

app = create_app()


if __name__ == "__main__":
    # read port from the centralized config (no environment variables required)
    port = int(app.config.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
