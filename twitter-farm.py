

#NLP Sentiment Analysis 
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import bigtable

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#JSON parsing
import json

#UUID
import uuid


#Variables that contains the user credentials to access Twitter API 


# URI scheme for Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'


instance_id = 'crypto-farm-datastore'
project_id = 'crypto-sent-analysis'
column_family_id = 'twitter_farm'

client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)




def analyze(content):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Write results to GCS 
    return annotations.document_sentiment.score

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        parsed_data = json.loads(data)
        text = parsed_data['text'].replace("\r","")
        text = text.replace("\n","")
        # score = analyze(text)
        name = parsed_data['user']['name']
        screen_name = parsed_data['user']['screen_name']
        retweet_count = parsed_data['retweet_count']
        fav_count = parsed_data['favorite_count']
        followers_count = parsed_data['user']['followers_count']
        timestamp_ms = parsed_data['timestamp_ms']
        lang = parsed_data['lang']

        row_key = uuid.uuid4()
        row.set_cell(
            column_family_id,
            'name'.encode('utf-8'),
            name.encode('utf-8'))
        row.set_cell(
            column_family_id,
            'screen_name'.encode('utf-8'),
            screen_name.encode('utf-8'))
        row.set_cell(
            column_family_id,
            'retweet_count'.encode('utf-8'),
            retweet_count.encode('utf-8'))
        row.set_cell(
            column_family_id,
            'fav_count'.encode('utf-8'),
            fav_count.encode('utf-8'))
        row.set_cell(
            column_family_id,
            'followers_count'.encode('utf-8'),
            followers_count.encode('utf-8'))
        row.set_cell(
            column_family_id,
            'timestamp_ms'.encode('utf-8'),
            timestamp_ms.encode('utf-8'))
        row.set_cell(
            column_family_id,
            'lang'.encode('utf-8'),
            lang.encode('utf-8'))
        row.commit()
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['xrp', 'lumens', 'xlm'])

