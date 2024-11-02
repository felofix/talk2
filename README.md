# Chat with Historical figures

This is a simple web application that allows users to chat with historical fivgures, starting with Friedrich Nietzsche. The backend is powered by FastAPI, and the frontend is a basic HTML/CSS/JavaScript setup. Queries are processed with the help of OpenAI's GPT model, and relevant text chunks are retrieved from a Qdrant vector database.

## Project Structure

```plaintext
/talk2
│
├── main.py                # FastAPI application
├── .env                   # Environment file for API keys
└── static                 # Directory for static files
    ├── index.html         # Frontend HTML file
    ├── styles.css         # CSS for styling
    └── script.js          # JavaScript for frontend interactivity

Requirements

Python 3.8+
Qdrant account (for cloud database access)
OpenAI API key
Dependencies
The following packages are required for the application:

FastAPI: Web framework for building the API backend.
Uvicorn: ASGI server to serve the FastAPI application.
Qdrant Client: Interface to connect to Qdrant’s vector database.
OpenAI API: Used to generate responses based on the retrieved context.
Python Dotenv: For loading environment variables from the .env file.
