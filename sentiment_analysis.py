import streamlit as st
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Azure Text Analytics credentials
API_KEY = "49b5229135a44cd58c00b70d36a3d14f"
ENDPOINT = "https://sentimenttt.cognitiveservices.azure.com/"


# Authenticate the Azure Text Analytics client
def authenticate_client():
    ta_credential = AzureKeyCredential(API_KEY)
    text_analytics_client = TextAnalyticsClient(
        endpoint=ENDPOINT, credential=ta_credential)
    return text_analytics_client


# Sentiment Analysis function using Azure Text Analytics
def analyze_sentiment(client, text):
    response = client.analyze_sentiment(documents=[text])[0]
    return response


# Streamlit Frontend
def main():
    st.title("Sentiment Analysis with Azure AI")

    # Add a sidebar for navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Choose a section", ("Text Input", "Upload File",))

    if option == "Text Input":
        user_input = st.text_area("Enter text to analyze", "")

        if st.button("Analyze Sentiment"):
            if user_input.strip():
                client = authenticate_client()
                result = analyze_sentiment(client, user_input)

                # Display sentiment analysis results
                st.subheader("Sentiment Analysis Result:")
                st.write(f"**Overall Sentiment:** {result.sentiment.capitalize()}")
                st.write(f"**Confidence Scores:**")
                st.write(f"Positive: {result.confidence_scores.positive:.2f}")
                st.write(f"Neutral: {result.confidence_scores.neutral:.2f}")
                st.write(f"Negative: {result.confidence_scores.negative:.2f}")

                # Display sentiment per sentence
                st.subheader("Detailed Sentence-Level Analysis:")
                for i, sentence in enumerate(result.sentences):
                    st.write(f"Sentence {i + 1}: '{sentence.text}'")
                    st.write(f"  Sentiment: {sentence.sentiment.capitalize()}")
                    st.write(f"  Positive: {sentence.confidence_scores.positive:.2f}")
                    st.write(f"  Neutral: {sentence.confidence_scores.neutral:.2f}")
                    st.write(f"  Negative: {sentence.confidence_scores.negative:.2f}")

                    # Bar chart visualization of confidence scores
                    scores = {
                        'Sentiment': ['Positive', 'Neutral', 'Negative'],
                        'Confidence': [
                            result.confidence_scores.positive,
                            result.confidence_scores.neutral,
                            result.confidence_scores.negative
                        ]
                    }
                    df = pd.DataFrame(scores)
                    st.bar_chart(df.set_index('Sentiment'))

            else:
                st.error("Please enter some text for analysis.")

        st.title("Compare Sentiment Across Multiple Inputs")

        # Input text area to accept multiple sentences (one per line)
        user_input = st.text_area("Enter multiple texts (one per line)",
                                  "I love Azure!\nThis service is terrible.\nThe product is okay.")

        # Process the input into individual texts
        texts = user_input.split("\n")  # Split the input by new lines

        if st.button("Compare Sentiment"):
            if len(texts) > 0:
                client = authenticate_client()
                sentiments = []

                # Analyze sentiment for each text
                for text in texts:
                    if text.strip():  # Only process non-empty lines
                        result = analyze_sentiment(client, text)
                        sentiments.append({
                            'Text': text,
                            'Overall Sentiment': result.sentiment.capitalize(),
                            'Positive': result.confidence_scores.positive,
                            'Neutral': result.confidence_scores.neutral,
                            'Negative': result.confidence_scores.negative
                        })

                # Display the results in a table
                if sentiments:
                    df = pd.DataFrame(sentiments)
                    st.subheader("Sentiment Comparison Results")
                    st.dataframe(df)  # You can also use st.table(df) for a static table view
                else:
                    st.error("No valid text entries for analysis.")
            else:
                st.error("Please enter at least one text.")

    elif option == "Upload File":
        uploaded_file = st.file_uploader("Choose a text file", type="txt")
        if uploaded_file is not None:
            user_input = uploaded_file.read().decode("utf-8")
            st.write(user_input)

        if st.button("Analyze Sentiment"):
            if user_input.strip():
                client = authenticate_client()
                result = analyze_sentiment(client, user_input)

                # Display sentiment analysis results
                st.subheader("Sentiment Analysis Result:")
                st.write(f"**Overall Sentiment:** {result.sentiment.capitalize()}")
                st.write(f"**Confidence Scores:**")
                st.write(f"Positive: {result.confidence_scores.positive:.2f}")
                st.write(f"Neutral: {result.confidence_scores.neutral:.2f}")
                st.write(f"Negative: {result.confidence_scores.negative:.2f}")

                # Display sentiment per sentence
                st.subheader("Detailed Sentence-Level Analysis:")
                for i, sentence in enumerate(result.sentences):
                    st.write(f"Sentence {i + 1}: '{sentence.text}'")
                    st.write(f"  Sentiment: {sentence.sentiment.capitalize()}")
                    st.write(f"  Positive: {sentence.confidence_scores.positive:.2f}")
                    st.write(f"  Neutral: {sentence.confidence_scores.neutral:.2f}")
                    st.write(f"  Negative: {sentence.confidence_scores.negative:.2f}")

                    # Bar chart visualization of confidence scores
                    scores = {
                        'Sentiment': ['Positive', 'Neutral', 'Negative'],
                        'Confidence': [
                            result.confidence_scores.positive,
                            result.confidence_scores.neutral,
                            result.confidence_scores.negative
                        ]
                    }
                    df = pd.DataFrame(scores)
                    st.bar_chart(df.set_index('Sentiment'))

            else:
                st.error("Please enter some text for analysis.")













if __name__ == "__main__":
    main()
