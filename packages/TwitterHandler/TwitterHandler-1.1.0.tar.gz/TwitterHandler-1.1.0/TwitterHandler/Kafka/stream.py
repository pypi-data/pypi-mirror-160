import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from tweepy import StreamingClient, StreamRule
from kafka import KafkaProducer

BEARER_TOKEN = os.environ['BEARER_TOKEN']
KAFKA_HOST = os.environ['KAFKA_HOST']
KAFKA_PORT = os.environ['KAFKA_PORT']
KAFKA_TOPIC = os.environ['KAFKA_TOPIC']


class TweetsStreamer(StreamingClient):
    def __init__(self, producer, **kwargs):
        super().__init__(**kwargs)
        self.producer = producer

    def on_data(self, raw_data):
        try:
            self.producer.send(
                KAFKA_TOPIC, raw_data)
        except BaseException as e:
            print(e)
        return True

    def on_disconnect(self):
        # self.thread.join()
        pass

    def on_error(self, status_code):
        print(status_code)

class Streamer:
    def __init__(self, ):
        producer = KafkaProducer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}")
        self.streamer = TweetsStreamer(producer, bearer_token=BEARER_TOKEN)
        self.thread = None

    def delete_rules(self):
        rules = self.streamer.get_rules().data
        rules_list = []
        for rule in rules:
            rules_list.append(rule.id)
        self.streamer.delete_rules(rules_list)

    def start_stream(self, query):
        rule = query + " lang:en" 
        self.streamer.add_rules([StreamRule(rule), ], dry_run=False)
        self.thread = self.streamer.filter(threaded=True, tweet_fields=['text', 'author_id', ])

    def stop_stream(self):
        self.streamer.disconnect()
        self.thread.join()
        self.delete_rules()


