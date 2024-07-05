from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management
app.config["SECRET_KEY"] = "hjhjsdahhds"
# Initialize Flask-SocketIO for real-time communication
socketio = SocketIO(app)
# Dictionary to store room information (members and messages)
rooms = {}
def generate_unique_code(length):
    """Generate a unique room code of given length."""
    while True:

