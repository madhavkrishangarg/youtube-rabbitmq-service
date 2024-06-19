import pika
import sys

def publishVideo(youtuber, videoName):
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('34.126.223.241', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='youtuber_requests')

    message = f'{youtuber} uploaded {videoName}'
    channel.basic_publish(exchange='', routing_key='youtuber_requests', body=message)
    print(f"(+) {youtuber} uploaded {videoName}")
    connection.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python Youtuber.py <YouTuberName> <VideoName>')
        sys.exit(1)
    
    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])
    publishVideo(youtuber_name, video_name)
