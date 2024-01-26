import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import pickle


nltk.download('punkt')
nltk.download('stopwords')

#model

model = pickle.load(open('../Data/model.pkl', 'rb'))
#pickled_model.predict(X_test)
#model = './Data/model.pkl'
# Load JSON data
''''json_filename = './material/reviews.json'
with open(json_filename, 'r') as json_file:
    for line in json_file:
        data = json.loads(line)
    #data = json.load(json_file) '''

csv_filename = 'reviews.csv'
df = pd.read_csv(csv_filename)
 
# Create DataFrame from JSON data
#df = pd.DataFrame(data)
# punctuation 

def punctuation_to_features(df, column):
    """Identify punctuation within a column and convert to a text representation.

    Args:
        df (object): Pandas dataframe.
        column (string): Name of column containing text.

    Returns:
        df[column]: Original column with punctuation converted to text,
                    i.e. "Wow! > "Wow exclamation"

    """

    df[column] = df[column].replace('!', ' exclamation ')
    df[column] = df[column].replace('?', ' question ')
    df[column] = df[column].replace('\'', ' quotation ')
    df[column] = df[column].replace('\"', ' quotation ')

    return df[column]

df['Description'] = punctuation_to_features(df, 'Description')

#Tokenirization
def tokenize(column):
    """Tokenizes a Pandas dataframe column and returns a list of tokens.

    Args:
        column: Pandas dataframe column (i.e. df['text']).

    Returns:
        tokens (list): Tokenized list, i.e. [Donald, Trump, tweets]

    """

    tokens = nltk.word_tokenize(column)
    return [w for w in tokens if w.isalpha()]
df['tokenized'] = df.apply(lambda x: tokenize(x['Description']), axis=1)

#Stop words removal

def remove_stopwords(tokenized_column):
    """Return a list of tokens with English stopwords removed.

    Args:
        column: Pandas dataframe column of tokenized data from tokenize()

    Returns:
        tokens (list): Tokenized list with stopwords removed.

    """
    stops = set(stopwords.words("english"))
    return [word for word in tokenized_column if not word in stops]
df['stopwords_removed'] = df.apply(lambda x: remove_stopwords(x['tokenized']), axis=1)

##############################
def apply_stemming(tokenized_column):
    """Return a list of tokens with Porter stemming applied.

    Args:
        column: Pandas dataframe column of tokenized data with stopwords removed.

    Returns:
        tokens (list): Tokenized list with words Porter stemmed.

    """

    stemmer = PorterStemmer()
    return [stemmer.stem(word).lower() for word in tokenized_column]
df['porter_stemmed'] = df.apply(lambda x: apply_stemming(x['stopwords_removed']), axis=1)


def rejoin_words(tokenized_column):
    return ( " ".join(tokenized_column))
df['all_text'] = df.apply(lambda x: rejoin_words(x['porter_stemmed']), axis=1)

result = model.predict(df)

#print(result)
accuracy = accuracy_score(df[:9], result[:9])
print(f'Accuracy: {accuracy}')       