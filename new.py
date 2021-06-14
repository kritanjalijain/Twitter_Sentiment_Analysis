# from keras.models import load_model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
model = load_model('best_model.h5')
import pickle
max_words = 5000
max_len=50
tokenizer = Tokenizer(num_words=max_words, lower=True, split=' ')
with open('preprocess.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
# tokenizer.fit_on_texts(text)
# tokenizer = Tokenizer(num_words=max_words, lower=True, split=' ')
def predict_class(text):
    '''Function to predict sentiment class of the passed text'''
    
    sentiment_classes = ['Negative', 'Neutral', 'Positive']
    max_len=50
    # print(text)
    # Transforms text to a sequence of integers using a tokenizer object
    # tokenizer = Tokenizer()
    
    xt = tokenizer.texts_to_sequences(text)
    print(xt)
    # Pad sequences to the same length
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    print(xt)
    # Do the prediction using the loaded model
    yt = model.predict(xt).argmax(axis=1)
    print(model.predict(xt))
    # Print the predicted sentiment
    k= sentiment_classes[yt[0]]
    # print(k)
    return k

#predict_class(['"I hate when I have to call and wake people up'])
