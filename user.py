import pika
import sys

def updateSubscription(username, action, youtuber):
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('34.126.223.241', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='user_requests')

    message = f'{username} {action} to {youtuber}'
    channel.basic_publish(exchange='', routing_key='user_requests', body=message)
    print(f"(+) {username} {action} to {youtuber}")
    connection.close()


def receiveNotifications(username):
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('34.126.223.241', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=username)

    def callback(ch, method, properties, body):
        print(f'New Notification: {body.decode()}')

    channel.basic_consume(queue=username, on_message_callback=callback, auto_ack=True)
    print('Waiting for notifications...')
    channel.start_consuming()
    #close when all notifications are received
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python User.py <Username> [s/u YouTuberName]')
        sys.exit(1)

    username = sys.argv[1]

    if len(sys.argv) == 4:
        action = "subscribe" if sys.argv[2]=="s" else "unsubscribe"
        youtuber = sys.argv[3]
        updateSubscription(username, action, youtuber)
    elif len(sys.argv) == 2:
        receiveNotifications(username)
