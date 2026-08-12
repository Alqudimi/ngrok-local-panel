# Project documentation

## Overview

ngrok-local-panel is a Python application with `main.py`, an `app/` package, local data, tests, and a requirements file. It is intended to provide a local panel for managing or viewing ngrok-related state.

## Development

Create a virtual environment, install `requirements.txt`, configure any required ngrok credentials through environment variables, and run `python main.py`. Use the tests directory to verify behavior after configuration changes.

## Security

Treat tunnel URLs and auth tokens as sensitive. Restrict the panel to localhost or an authenticated network, never commit tokens, and close tunnels that are no longer needed.
