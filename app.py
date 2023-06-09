import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# AI model code
HF_API_KEY = os.getenv("HF_API_KEY")

# API_URL_ED = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base" #alternate ED model(slow loading on first run)
API_URL_ED = "https://api-inference.huggingface.co/models/bhadresh-savani/bert-base-go-emotion"
API_URL_HS = "https://api-inference.huggingface.co/models/IMSyPP/hate_speech_en"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

st.set_page_config(
    page_title="GoEmotions Dashboard",
    layout="wide"
)

# Set page title
st.title("GoEmotions Dashboard - Analyzing Emotions in Text")

def query(payload):
    response_ED = requests.request("POST", API_URL_ED, headers=headers, json=payload)
    response_HS = requests.request("POST", API_URL_HS, headers=headers, json=payload)
    return (json.loads(response_ED.content.decode("utf-8")),json.loads(response_HS.content.decode("utf-8")))

# Define color map for each emotion category
color_map = {
    'admiration': ['#1f77b4', '#98df8a', '#2ca02c', '#d62728'],
    'amusement': ['#ff7f0e', '#98df8a', '#2ca02c', '#d62728'],
    'anger': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'annoyance': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'approval': ['#1f77b4', '#98df8a', '#2ca02c', '#d62728'],
    'caring': ['#98df8a', '#2ca02c', '#FF69B4', '#d62728'],
    'confusion': ['#ffbb78', '#ff7f0e', '#9467bd', '#d62728'],
    'curiosity': ['#ffbb78', '#ff7f0e', '#9467bd', '#d62728'],
    'desire': ['#2ca02c', '#ff7f0e', '#98df8a', '#d62728'],
    'disappointment': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'disapproval': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'disgust': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'embarrassment': ['#ffbb78', '#ff7f0e', '#9467bd', '#d62728'],
    'excitement': ['#ff7f0e', '#2ca02c', '#98df8a', '#d62728'],
    'fear': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'gratitude': ['#98df8a', '#2ca02c', '#1f77b4', '#d62728'],
    'grief': ['#ffbb78', '#d62728', '#bcbd22', '#ff7f0e'],
    'joy': ['#ff7f0e', '#98df8a', '#2ca02c', '#d62728'],
    'love': ['#FF69B4', '#98df8a', '#2ca02c', '#d62728'],
    'nervousness': ['#ffbb78', '#ff7f0e', '#9467bd', '#d62728'],
    'optimism': ['#98df8a', '#2ca02c', '#1f77b4', '#d62728'],
    'pride': ['#98df8a', '#ff7f0e', '#1f77b4', '#d62728'],
    'realization': ['#9467bd', '#ff7f0e', '#ffbb78', '#d62728'],
    'relief': ['#1f77b4', '#98df8a', '#2ca02c', '#d62728'],
    'remorse': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'sadness': ['#ffbb78', '#ff7f0e', '#d62728', '#bcbd22'],
    'surprise': ['#ff7f0e', '#ffbb78', '#9467bd', '#d62728'],
    'neutral': ['#2ca02c', '#98df8a', '#1f77b4', '#d62728']
}


# Labels for Hate Speech Classification
label_hs = {"LABEL_0": "Acceptable", "LABEL_1": "Inappropriate", "LABEL_2": "Offensive", "LABEL_3": "Violent"}

# Define default options

default_options = [
    "I'm so excited for my vacation next week!",
    "I'm feeling so stressed about work.",
    "I just received great news from my doctor!",
    "I can't wait to see my best friend tomorrow.",
    "I'm feeling so lonely and sad today."
    "I'm so angry at my neighbor for being so rude.",
    "You are so annoying!",
    "You people from small towns are so dumb.",
    "If you don't agree with me, you are a moron.",
    "I hate you so much!",
    "If you don't listen to me, I'll beat you up!",
]

with st.sidebar:

    # Add page description
    description = "The GoEmotions Dashboard is a web-based user interface for analyzing emotions in text. The dashboard is powered by a pre-trained natural language processing model that can detect emotions in text input. Users can input any text and the dashboard will display the detected emotions in a set of gauges, with each gauge representing the intensity of a specific emotion category. The gauge colors are based on a predefined color map for each emotion category. This dashboard is useful for anyone who wants to understand the emotional content of a text, including content creators, marketers, and researchers."
    #st.markdown(description)

    # Create dropdown with default options
    selected_option = st.selectbox("Select a default option or enter your own text:", default_options)

    # Display text input with selected option as default value
    text_input = st.text_area("Enter text to analyze emotions:", value = selected_option, height=100)

    # Add submit button
    submit = st.button("Submit")

# If submit button is clicked
if submit:

    # Call API and get predicted probabilities for each emotion category and hate speech classification
    payload = {"inputs": text_input, "options": {"wait_for_model": True, "use_cache": True}}
    response_ED, response_HS = query(payload)
    predicted_probabilities_ED = response_ED[0]
    predicted_probabilities_HS = response_HS[0]

    ED, _, HS = st.columns([5,2,3])

    with ED:
        # Sort the predicted probabilities in descending order
        sorted_probs_ED = sorted(predicted_probabilities_ED, key=lambda x: x['score'], reverse=True)

        # Get the top 4 emotion categories and their scores
        top_emotions = sorted_probs_ED[:4]
        top_scores = [e['score'] for e in top_emotions]

        # Normalize the scores so that they add up to 100%
        total = sum(top_scores)
        normalized_scores = [score/total * 100 for score in top_scores]

        # Create the gauge charts for the top 4 emotion categories using the normalized scores
        fig = make_subplots(rows=2, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                                                    [{'type': 'indicator'}, {'type': 'indicator'}]],
                            vertical_spacing=0.4)

        for i, emotion in enumerate(top_emotions):
            category = emotion['label']
            color = color_map[category]
            value = normalized_scores[i]
            row = i // 2 + 1
            col = i % 2 + 1
            fig.add_trace(go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=value,
                mode="gauge+number",
                title={'text': category.capitalize()},
                gauge={'axis': {'range': [None, 100]},
                    'bar': {'color': color[3]},
                    'bgcolor': 'white',
                    'borderwidth': 2,
                    'bordercolor': color[1],
                    'steps': [{'range': [0, 33], 'color': color[0]},
                                {'range': [33, 66], 'color': color[1]},
                                {'range': [66, 100], 'color': color[2]}],
                    'threshold': {'line': {'color': "black", 'width': 4},
                                    'thickness': 0.5,
                                    'value': 50}}), row=row, col=col)


        # Update layout
        fig.update_layout(height=400, margin=dict(t=50, b=5, l=0, r=0))

        # Display gauge charts
        st.text("")
        st.text("")
        st.text("")
        st.subheader("Emotion Detection")
        st.text("")
        st.plotly_chart(fig, use_container_width=True)
    
    with _:
        st.text("")

    with HS:
        # Display Hate Speech Classification
        hate_detection = label_hs[predicted_probabilities_HS[0]['label']]
        st.text("")
        st.text("")
        st.text("")
        st.subheader("Hate Speech Analysis")
        st.text("")
        st.image(f"assets/{hate_detection}.jpg", width=200)
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.markdown(f"#### The given text is {hate_detection}")

 


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)