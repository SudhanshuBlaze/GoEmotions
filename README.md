---
license: apache-2.0
title: GoEmotions Dashboard
sdk: streamlit
sdk_version: "1.22.0"
app_file: app.py
---

# GoEmotions Dashboard - Analyzing Emotions in Text

This is a Python script that uses Streamlit, Plotly, and the Hugging Face Inference API to create a web-based dashboard for analyzing emotions in text.

## Pre-requisites:

- Python 3.7 or higher

## Project Structure:
```dir
GoEmotions/
├── app.py
├── requirements.txt
├── .env
├── README.md
└── assets/
```

## Installation

`Step 1` - Clone this repository to your local machine.

```bash
git clone https://github.com/SudhanshuBlaze/GoEmotions.git
```

`Step 2` - Install the required packages using pip:

```bash
pip install -r requirements.txt
```

`Step 3`- Create a free account on the [Hugging Face website](https://huggingface.co/) to get an API key.

`Step 4`

- Create a `.env` file in the root directory of the project and add your
- Hugging Face API key like this: `HF_API_KEY=<your_api_key_here>`

`Step 5` - Navigate to the root directory of the project.

```bash
cd GoEmotions
```

`Step 6` - Run the Streamlit app.

```bash
streamlit run app.py
```

- If you want to run this application on GitHub Codespaces, you will need to add the following flags to the `streamlit run` command:

```bash
python -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

## Usage:

- A web-based dashboard will open in your default browser.
- Type or paste a text input in the text box provided.
- The dashboard will display the detected emotions in a set of gauges, with each gauge representing the intensity of a specific emotion category.
- The gauge colors are based on a predefined color map for each emotion category.
