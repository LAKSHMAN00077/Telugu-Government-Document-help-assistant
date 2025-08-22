# సర్కారీ సహాయకుడు (Government Helper AI Assistant)

This is an AI-powered web application designed to assist Telugu-speaking users with information about government documents, schemes, and procedures in India. The application leverages Google's Gemini 1.5 Flash model to provide accurate, step-by-step guidance in both Telugu and English.

## ✨ Key Features

- **Bilingual Support**: Responds in Telugu if the question is in Telugu, otherwise defaults to English.
- **Specialized Knowledge**: Trained to answer questions on Aadhaar, property registration, income certificates, pensions, and more.
- **User-Friendly Interface**: A simple web page for users to ask questions and receive instant answers.
- **Easy to Deploy**: Built with Flask, making it straightforward to set up and run.
- **Error Handling**: Includes robust error handling for API and server issues.

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **AI Model**: Google Gemini 1.5 Flash
- **Dependencies**: `google-generativeai`, `python-dotenv`, `Flask`

## 🚀 Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

- Python 3.7+
- A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clone the Repository

First, get the code onto your local machine. If you are starting from scratch, save all the project files in a new directory.

### 3. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
```

### 4. Install Dependencies

Install all the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a file named `.env` in the root directory of your project and add your Gemini API key:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
DEBUG=True
```

### 6. Run the Application

Start the Flask server with the following command:

```bash
python run.py
```

The application will be available at **http://localhost:5000**.

## 📂 Project Structure

Here is an overview of the key files in the project:

-   `app.py`: The main Flask application file containing all routes (`/`, `/chat`, `/health`).
-   `ai_client.py`: A client to handle all interactions with the Gemini API.
-   `response_handler.py`: Manages the logic for generating a response based on user input.
-   `prompts.py`: Contains the core system prompts that define the AI's persona and expertise.
-   `config.py`: Manages configuration from environment variables (API keys, server settings).
-   `requirements.txt`: A list of all Python dependencies for the project.
-   `run.py`: The main entry point to start the application.
-   `.env`: (You create this) Stores secret keys and configuration variables.

## Endpoints

The application exposes the following API endpoints:
- **`/`**: Serves the main HTML interface.
- **`/chat`**: (POST) Handles user messages and returns AI-generated responses.
- **`/health`**: A simple health check endpoint.
- **`/status`**: Provides a detailed status of the application and AI client.
