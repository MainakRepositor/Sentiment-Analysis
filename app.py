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
	st.title("𝑆𝑒𝑛𝑡𝑖𝑚𝑒𝑛𝑡 𝐴𝑛𝑎𝑙𝑦𝑠𝑖𝑠 𝐴𝑝𝑝 😊💖")
	st.subheader("𝑊𝑒 𝑎𝑐𝑘𝑛𝑜𝑤𝑙𝑒𝑑𝑔𝑒 𝑦𝑜𝑢𝑟 𝑒𝑚𝑜𝑡𝑖𝑜𝑛𝑠 😉✔")

	menu = ["Home","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("𝐸𝑛𝑡𝑒𝑟 𝑦𝑜𝑢𝑟 𝑡𝑒𝑥𝑡 𝑎𝑛𝑑 𝑤𝑒 𝑤𝑖𝑙𝑙 ℎ𝑒𝑙𝑝 𝑟𝑒𝑐𝑜𝑔𝑛𝑖𝑧𝑒 𝑦𝑜𝑢𝑟 𝑠𝑒𝑛𝑡𝑖𝑚𝑒𝑛𝑡𝑠")
		with st.form(key='nlpForm'):
			raw_text = st.text_area("𝐸𝑛𝑡𝑒𝑟 𝑌𝑜𝑢𝑟 𝑇𝑒𝑥𝑡 𝐻𝑒𝑟𝑒👇😊")
			submit_button = st.form_submit_button(label='𝐴𝑛𝑎𝑙𝑦𝑧𝑒 🔍')

		# layout
		col1,col2 = st.columns(2)
		if submit_button:

			with col1:
				st.info("Results")
				sentiment = TextBlob(raw_text).sentiment
				st.write(sentiment)

				# Emoji
				
				if sentiment.polarity > 0:
					st.markdown("Sentiment:: Positive :smiley: 😊 ")
					st.balloons()
				elif sentiment.polarity < 0:
					st.markdown("Sentiment:: Negative :angry: 😒 ")
					st.snow()
				else:
					st.markdown("Sentiment:: Neutral 😐 ")

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