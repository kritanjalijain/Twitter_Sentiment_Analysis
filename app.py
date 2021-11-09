from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from new import predict_class
import streamlit as st
import tweepy as tw
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
from dotenv import load_dotenv

import os

load_dotenv()

consumerKey = os.getenv("consumer_key")
consumerSecret = os.getenv("consumer_key_secret")
accessToken = os.getenv("access_token")
accessTokenSecret = os.getenv("access_token_secret")
#Create the authentication object
authenticate = tw.OAuthHandler(consumerKey, consumerSecret) 
    
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret) 
    
# Creating the API object while passing in auth information
api = tw.API(authenticate, wait_on_rate_limit = True)


def app():
	def process_stauses(sta):
		print(sta.text)

	st.title("Twitter Sentiment Analyzer")

	def load_lottieurl(url: str):
		r = requests.get(url)
		if r.status_code != 200:
			return None
		return r.json()

	lottie_twitter = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_ayl5c9tf.json')
	st_lottie(lottie_twitter, speed=1, height=180, key="initial")

	st.subheader("Analyze Sentiments on Twitter in Real Time!")
	
	st.markdown("Hey there! Welcome to Twitter Sentiment Analysis App. This app scrapes (and never keeps or stores!) the tweets you want to classfiy and analyzes the sentiments as positive, negative or neutral and visualises their distribution.")
	st.markdown("**To begin, please enter the number of tweets you want to analyse.** 👇")

	
	notweet = st.slider('Select a number between 1-100')
	st.write(notweet, 'tweets are being fetched.')
	st.write("__________________________________________________________________________________")

		# Radio Buttons
	st.markdown(" Great! Now, let's select the type of search you want to conduct. You can either search a twitter handle (e.g. @elonmusk) which will analyse the recent tweets of that user or search a trending hashtag (e.g. #WorkFromHome) to classify sentiments of the tweets regarding it. ")
	st.write("")

	stauses = st.radio('Select the mode of fetching',("Fetch the most recent tweets from the given twitter handle","Fetch the most recent tweets from the given twitter hashtag"))

	if stauses == 'Fetch the most recent tweets from the given twitter handle':
		st.success("Enter User Handle")
	elif stauses == 'Fetch the most recent tweets from the given twitter hashtag':
    		st.success("Enter Hashtag")
	else:
		st.warning("Choose an option")

		
	raw_text = st.text_input("Enter the twitter handle of the personality (without @) or enter the hashtag (without #)")
	need_help = st.expander('Need help? 👉')
	with need_help:
		st.markdown("Having trouble finding the Twitter profile or Hashtag? Head to the [Twitter website](https://twitter.com/home) and click on the search bar in the top right corner.")

	st.markdown(" ### Almost done! Finally, let's choose what we want to do with the tweets ")
	Analyzer_choice = st.selectbox("Choose the action to be performed 👇",  ["Show Recent Tweets","Classify Sentiment"])


	if st.button("Analyze"):

			
		if Analyzer_choice == "Show Recent Tweets":

			st.success("Fetching latest Tweets")

				
			def Show_Recent_Tweets(raw_text):
					

				if stauses == 'Fetch the most recent tweets from the given twitter handle': 
						posts = [status for status in tw.Cursor(api.user_timeline, screen_name=raw_text).items(notweet)]

						
				else :
    					posts = [status for status in tw.Cursor(api.search, q=raw_text).items(100)]
    						


					
				def get_tweets():

					l=[]
					i=1
					for tweet in posts[:notweet]:
						l.append(tweet.text)
						i= i+1
					return l

				recent_tweets=get_tweets()		
				return recent_tweets

			recent_tweets=Show_Recent_Tweets(raw_text)

			st.write(recent_tweets)
		else:
			st.success("Analysing latest tweets")
			m=[]
			def Analyse_Recent_Tweets(raw_text):
    					
				if stauses == 'Fetch the most recent tweets from the given twitter handle': 
						posts = [status for status in tw.Cursor(api.user_timeline, screen_name=raw_text).items(notweet)]

						
				else:
					posts=[status for status in tw.Cursor(api.search, q=raw_text).items(100)]

				
				def fetch_tweets():

					l2=[]
					# i=1
					for tweet in posts[:notweet]:
						l2.append(tweet.text)
						# i= i+1
					for j in range(0,notweet):
						#m=[]
						m.append(predict_class([l2[j]]))
						st.write(l2[j])
						st.write("The predicted sentiment is",predict_class([l2[j]]))
						st.write("")
						st.write("__________________________________________________________________________________")
						#st.write(m)

				rec_tweets=fetch_tweets()		
				return rec_tweets

			rece_tweets= Analyse_Recent_Tweets(raw_text)

			df = pd.DataFrame(m, columns = ['Sentiment'])
			#st.write(df)
				#df=pandas.DataFrame(m)
			st.markdown("**Whoa! Those are some strong opinions alright. Outta the {0} tweets that we analysed, the positive, negative and neutral sentiment distribution is summed up in the followed visualisation and table.**".format(notweet))
			st.write("")
			fig = px.pie(df,names=df['Sentiment'], title ='Pie chart of different sentiments of tweets')
			st.plotly_chart(fig)
			pos = df[df['Sentiment'] == 'Positive']
				#st.write(pos)
			neg = df[df['Sentiment'] == 'Negative']
				#st.write(neg)
			neu = df[df['Sentiment'] == 'Neutral']
				#st.write(neu)
			total_rows = df.count()
			rowsp = pos.count()
			rowsn = neg.count()
			rowsne = neu.count()
			
				#st.write(total_rows)
			result = pd.concat([rowsp, rowsn, rowsne], axis=1)
			result.columns = ['Positive', 'Negative', 'Neutral' ]
			result.index = ['No. of Tweets']
			st.subheader('Sentiment Distribution')
			st.write(result)
			st.markdown('***')
			st.markdown("Thanks for going through this mini-analysis with us. Cheers!")
				


if __name__ == "__main__":
	app()
