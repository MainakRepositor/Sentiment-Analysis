import streamlit as st  
from textblob import TextBlob
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Fxn
def convert_to_df(sentiment):
	sentiment_dict = {'polarity':sentiment.polarity,'subjectivity':sentiment.subjectivity}
	sentiment_df = pd.DataFrame(sentiment_dict.items(),columns=['metric','value'])
	return sentiment_df

def analyze_token_sentiment(docx):
	analyzer = SentimentIntensityAnalyzer()
	pos_list = []
	neg_list = []
	neu_list = []
	for i in docx.split():
		res = analyzer.polarity_scores(i)['compound']
		if res > 0.1:
			pos_list.append(i)
			pos_list.append(res)

		elif res <= -0.1:
			neg_list.append(i)
			neg_list.append(res)
		else:
			neu_list.append(i)

	result = {'positives':pos_list,'negatives':neg_list,'neutral':neu_list}
	return result 




		






def main():
	st.title("ππππ‘πππππ‘ π΄ππππ¦π ππ  π΄ππ ππ")
	st.subheader("ππ ππππππ€πππππ π¦ππ’π ππππ‘ππππ  πβ")

	menu = ["Home","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("πΈππ‘ππ π¦ππ’π π‘ππ₯π‘ πππ π€π π€πππ βπππ ππππππππ§π π¦ππ’π π πππ‘πππππ‘π ")
		with st.form(key='nlpForm'):
			raw_text = st.text_area("πΈππ‘ππ πππ’π πππ₯π‘ π»πππππ")
			submit_button = st.form_submit_button(label='π΄ππππ¦π§π π')

		# layout
		col1,col2 = st.columns(2)
		if submit_button:

			with col1:
				st.info("Results")
				sentiment = TextBlob(raw_text).sentiment
				st.write(sentiment)

				# Emoji
				
				if sentiment.polarity > 0:
					st.markdown("Sentiment:: Positive :smiley: π ")
					st.balloons()
				elif sentiment.polarity < 0:
					st.markdown("Sentiment:: Negative :angry: π ")
					st.snow()
				else:
					st.markdown("Sentiment:: Neutral π ")

				# Dataframe
				result_df = convert_to_df(sentiment)
				st.dataframe(result_df)

				# Visualization
				c = alt.Chart(result_df).mark_bar().encode(
					x='metric',
					y='value',
					color='metric')
				st.altair_chart(c,use_container_width=True)



			with col2:
				st.info("Token Sentiment")

				token_sentiments = analyze_token_sentiment(raw_text)
				st.write(token_sentiments)


		
			



	elif choice == "About":
		st.subheader("About")
		st.text("Analysis of sentiments of the farmers of the cultivators can be analysed\n alongwith the objectivity and subjectivity of the sentence\n along with the sentiment distribution.")


if __name__ == '__main__':
	main()