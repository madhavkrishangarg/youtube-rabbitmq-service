This repository contains a simplified YouTube-like application using RabbitMQ for asynchronous communication between different components. The system consists of three main components: YouTubeServer, Youtuber, and User.

Prerequisites

Python 3.x
RabbitMQ
Setup

Install RabbitMQ: https://www.rabbitmq.com/download.html

Install Python dependencies:

bash
Copy code
pip install pika
Running the Application

1. Start the YouTube Server
The YouTube server handles messages from both YouTubers and Users. It maintains a list of YouTubers, their videos, and all users and their subscriptions.

bash
Copy code
python youtubeServer.py
2. Run the Youtuber Service
The Youtuber service allows YouTubers to publish videos.

bash
Copy code
# Example: Run the Youtuber service to publish a video
python Youtuber.py TomScott "After ten years, it's time to stop weekly videos."
3. Run the User Service
The User service allows users to subscribe or unsubscribe to YouTubers and receive notifications of new videos.

bash
Copy code
# Example: Run the User service to log in and subscribe to a YouTuber
python User.py username s TomScott

# Example: Run the User service to log in and unsubscribe from a YouTuber
python User.py username u TomScott

# Example: Run the User service to log in and receive notifications
python User.py username
Project Structure

youtubeServer.py: Sets up and runs the YouTube server. It handles user logins, subscription requests, and video uploads.
Youtuber.py: Represents the Youtuber service. It allows YouTubers to publish videos.
User.py: Represents the User service. It allows users to log in, subscribe or unsubscribe to YouTubers, and receive notifications.


On GCP VM:
sudo apt install rabbitmq-server

add /etc/rabbitmq/rabbitmq.conf

add line loopback_users=none

restart the server at instance having server.py

Change the ip adress in user.py and server.py to the external address of server instance
