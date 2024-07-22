# SerenityAI
Your AI Friend for Mental Health and Wellness


SerenityAI is a medical healthcare chatbot designed to assist users with mental health assessments and provide initial support and guidance. The chatbot uses natural language processing (NLP) techniques to understand and respond to users' inputs, offering assessments and resources based on their responses.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Description

SerenityAI aims to provide users with a supportive and interactive platform to assess their mental health. By leveraging machine learning models and NLP techniques, the chatbot can understand user inputs, perform sentiment analysis, and suggest relevant resources or actions.

## Features

- Interactive mental health assessment quiz.
- Sentiment analysis of user inputs.
- Provides resources and helpline information based on assessment results.
- Uses logistic regression for prediction and TF-IDF for text vectorization.

## Installation

To set up SerenityAI on your local machine, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Abhishek-vardhanapu/SerenityAI.git
    cd SerenityAI
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download the datasets and place them in the project directory:**
    - `train.csv`
    - `test.csv`

## Usage

To run SerenityAI, execute the main script:

```bash
python serenityai.py
