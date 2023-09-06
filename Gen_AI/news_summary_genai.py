import vertexai
from vertexai.language_models import CodeGenerationModel
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import streamlit as st


# Run first time only
#import nltk
#nltk.download('punkt')

# def get_article_text():
import nltk
#nltk.download('punkt')

st.header("News Summary Generator")
st.markdown("Please click on the news title to get summary")

rss_feed_url = 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms'

vertexai.init(project="sadaindia-tvm-poc-de", location="us-central1")
parameters = {
    # "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2
}
print("intializing")
model = CodeGenerationModel.from_pretrained("code-bison@001")
dict1 = {}

# Send GET request
url_response = requests.get(rss_feed_url)
i = 0

if url_response.status_code == 200:

    try:

        # Parsing the XML
        soup = BeautifulSoup(url_response.content, "xml")
        channel = soup.find('channel')

        for item in channel.find_all('item'):
            for link in item.find("link"):
                if i < 6:
                    # parsing through each link
                    article_url = link.text
                    toi_article = Article(article_url)

                    # To download the article
                    toi_article.download()

                    # To parse the article
                    toi_article.parse()

                    # To perform natural language processing
                    # toi_article.nlp()


                    dict1[toi_article.title] = toi_article.text

                    i = i + 1

    except Exception as e:
        print(f"Error while fetching data: {e}")

for i in dict1:
    if st.button(i):
        with st.spinner('Wait for it...'):
            response = model.predict(
                prefix=f"Provide a brief summary for the following article: "
                       f"{dict1.get(i)}", **parameters
            )
            # print(dict1.get(i))

            st.write(f"{response.text}")

