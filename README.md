The backend for our 2024 MHacks x Google Hackathon submission, GeminAAC. Built in Flask, you can see both our application in app.py, our api handler in helper.py, as well as a handful of our testing scripts and notebooks.

## Getting Started

Provide your own API key by setting the APIKEY variable.

Run the backend by simply calling `python3 app.py`. The API is ran on [http://localhost:5000](http://localhost:5000/test). The application needs access to the user's microphone and camera. The backend is expected to be ran alongside the frontend, on the same machine.