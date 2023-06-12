---
license: apache-2.0
title: GoEmotions Dashboard
sdk: streamlit
sdk_version: "1.22.0"
app_file: app.py
---
# GoEmotions Dashboard - Analyzing Emotions in Text

This is a Python script that uses Streamlit, Plotly, and the Hugging Face API to create a web-based dashboard for analyzing emotions in text.

## Requirements:

Python 3.7 or higher
Hugging Face API

## Installation

- Clone this repository to your local machine.
- Install the required packages using pip:

```bash
pip install -r requirements.txt
```

- Create a free account on the Hugging Face website to get an API key.

- Create a `.env` file in the root directory of the project and add your
- Hugging Face API key like this: `HF_API_KEY=<your_api_key_here>`

## Usage

- Navigate to the root directory of the project.
- Run the Streamlit app by typing `streamlit run app.py` or `python -m streamlit run app.py` in the command line.
- For GitHub Codespaces, Run: `python -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false`

- A web-based dashboard will open in your default browser.
- Type or paste a text input in the text box provided.
- The dashboard will display the detected emotions in a set of gauges, with each gauge representing the intensity of a specific emotion category.
- The gauge colors are based on a predefined color map for each emotion category.
