import re 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('floresta')
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from data.abbreviations_synonyms import abbreviations_synonyms_dict
import joblib

tagger = joblib.load('./data/POS_tagger_bigram.pkl') # https://github.com/inoueMashuu/POS-tagger-portuguese-nltk/tree/master/trained_POS_taggers

def clean_text(text):
  text = ' '.join([ word for word in text.split(' ') if not word.startswith('@') ])
  # replace punctuations with ' '
  # text = text.translate(str.maketrans(' ', ' ', string.punctuation))
  text = re.sub(r"[^A-Za-z ]+", '', text) # keep only letters and spaces
  text = text.strip()
  return text

def replace_synonyms_abbreviations(text):
  for abbr_or_syn, full_text in abbreviations_synonyms_dict.items():
    text = text.replace(f' {abbr_or_syn} ', f' {full_text} ')
  return text

def remove_stop_words(text):
  stopwords_pt = stopwords.words('portuguese')
  
  text_without_sw = [word for word in text.split(' ') if not word in stopwords_pt]
  return (" ").join(text_without_sw)

def lemmatization_nltk(text):
  lemmatizer = WordNetLemmatizer()
  palavras = nltk.word_tokenize(text, language='portuguese')
  lemmas = [lemmatizer.lemmatize(p).lower() for p in palavras]
  return (" ").join(lemmas)

def remove_proper_nouns(text):
  words = []
  for word,tag in tagger.tag(word_tokenize(text)):
    if tag != 'NPROP':
      words.append(word)
  return ' '.join(words)

def normalize_text(text):
  text = clean_text(text)
  text = remove_proper_nouns(text)
  text = text.lower() # outside clean_text because capitalization influences remove_proper_nouns function 
  text = replace_synonyms_abbreviations(text)
  text = remove_stop_words(text)
  text = lemmatization_nltk(text)
  return text