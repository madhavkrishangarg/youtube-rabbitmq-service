install rabbitmq
sudo apt install rabbitmq-server

add /etc/rabbitmq/rabbitmq.conf

add line loopback_users=none

restart the server at instance having server.py

Change the ip adress in user.py and server.py to the external address of server instance