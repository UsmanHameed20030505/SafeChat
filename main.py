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
        # Generate a random code consisting of uppercase letters
        code = "".join(random.choice(ascii_uppercase) for _ in range(length))
        # Ensure the generated code is unique (not already in use)
        if code not in rooms:
            break
    return code
@app.route("/", methods=["POST", "GET"])
def home():
    # Clear session data on loading the home page
    session.clear()
    if request.method == "POST":
        # Get the name from the form input
        name = request.form.get("name")
        # Get the room code from the form input
        code = request.form.get("code")
        # Check if the join button was pressed
        join = request.form.get("join", False)
        # Check if the create button was pressed
        create = request.form.get("create", False)

        # Validate the form input
        if not name:
            # If the name is not provided, display an error message
            return render_template("home.html", error="Please Enter Your Name.", code=code, name=name)
        if join != False and not code:
            # If joining a room and no code is provided, display an error message
            return render_template("home.html", error="Please Enter Your Room Code.", code=code, name=name)

        room = code  # Use the provided room code
        if create != False:
            # If creating a new room, generate a unique room code
            room = generate_unique_code(4)
            # Create a new room with initial member count and message list
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            # If the room code does not exist, display an error message
            return render_template("home.html", error="Room Does Not Exist.", code=code, name=name)
        # Save the room and name in the session
        session["room"] = room
        session["name"] = name
        # Redirect to the room page
        return redirect(url_for("room"))
    # Render the home page template
    return render_template("home.html")
@app.route("/room")
def room():
    # Get the room and name from the session
    room = session.get("room")
    name = session.get("name")
    # Redirect to the home page if the room or name is not in the session or the room does not exist
    if room is None or name is None or room not in rooms:
        return redirect(url_for("home"))
    # Render the room page template with the room code and messages
    return render_template("room.html", code=room, messages=rooms[room]["messages"])
@socketio.on("message")
def message(data):
    """Handle incoming messages and broadcast to the room."""
    room = session.get("room")
    # Ensure the room exists
    if room not in rooms:
        return 
    # Create the content to send
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    # Broadcast the message to the room
    send(content, to=room)
    # Add the message to the room's message list
    rooms[room]["messages"].append(content)
    # Print the message for debugging purposes
    print(f"{session.get('name')} said: {data['data']}")
        
@socketio.on("connect")
def connect(auth):
    """Handle a new connection to the chat room."""
    room = session.get("room")
    name = session.get("name")
    # Ensure the room and name are valid
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    # Join the room
    join_room(room)
    # Notify the room that a new user has joined
    send({"name": name, "message": "has entered the room"}, to=room)
    # Increment the member count
    rooms[room]["members"] += 1
    # Print a message for debugging purposes
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    """Handle disconnection from the chat room."""
    room = session.get("room")
    name = session.get("name")
    # Leave the room
    leave_room(room)
