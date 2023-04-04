import snscrape.modules.twitter as sntwitter
from tensorflow import keras
from keras.utils import pad_sequences
from keras.preprocessing.text import tokenizer_from_json
from twittes_preprocessing import normalize_text
import json

def get_twittes(user: str, amount: int):
  tweets = []
  for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"from:{user}").get_items()):
    if i >= amount:
      break
    tweets.append(tweet)

  content_tweets = [tweet.rawContent for tweet in tweets]
  return content_tweets

def load_model():
  model = keras.models.load_model('./data/exported/twitter_toxicity_model')
  with open('./data/exported/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

  return model, tokenizer

def run(user: str, twittes_amount: int):
  user = user.replace('@', '')
  twittes = get_twittes(user, twittes_amount)

  model, tokenizer = load_model()

  # cálculo de toxicidade 
  tweets_normalized = [normalize_text(tweet) for tweet in twittes]
  tweets_tokens = pad_sequences(tokenizer.texts_to_sequences(tweets_normalized), maxlen = 30)  

  y = model(tweets_tokens, training=False)
  output = []
  for i, twitte_y in enumerate(y):
    output.append((twittes[i], round(float(twitte_y)*100), 2))
  
  return output
