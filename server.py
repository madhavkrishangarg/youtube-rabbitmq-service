import pika
import threading

subscriptions={}
videos={}
user_list=[]

def notify_users(video_name, youtuber):
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            global subscriptions
            print("Notifying users...")
            
            for user in subscriptions:
                if youtuber in subscriptions[user]:
                    channel.queue_declare(queue=user)
                    message = f'{youtuber} uploaded {video_name}'
                    channel.basic_publish(exchange='', routing_key=user, body=message)
                    print(f"Notification sent to {user}")
            
            
                
def consume_user_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='user_requests')

    def callback(ch, method, properties, body):
        print(body.decode())
        l=body.decode().split()
        l.remove('to')

        if(subscriptions.get(l[0])==None):
            subscriptions[l[0]]=[]
        
        if l[1]=='subscribe':
            subscriptions[l[0]].append(l[2])
        else:
            subscriptions[l[0]].remove(l[2])
        print(f"User {l[0]} {l[1]}d to {l[2]}")
        print(subscriptions)

    channel.basic_consume(queue='user_requests', on_message_callback=callback, auto_ack=True)
    print('Waiting for user requests...')
    channel.start_consuming()

def consume_youtuber_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='youtuber_requests')

    def callback(ch, method, properties, body):    
        print(body.decode())
        l=body.decode().split()
        youtuber=l[0]
        video=' '.join(l[2:])
        if(videos.get(youtuber)==None):
            videos[youtuber]=[]
        videos[youtuber].append(video)
        print(videos)
        
        notify_users(video, youtuber)

    channel.basic_consume(queue='youtuber_requests', on_message_callback=callback, auto_ack=True)
    print('Waiting for YouTuber requests...')
    channel.start_consuming()
    

if __name__ == '__main__':
    user_requests_thread = threading.Thread(target=consume_user_requests)
    youtuber_requests_thread = threading.Thread(target=consume_youtuber_requests)
    user_requests_thread.start()
    youtuber_requests_thread.start()
    user_requests_thread.join()
    youtuber_requests_thread.join()
