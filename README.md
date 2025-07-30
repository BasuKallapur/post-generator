# LinkedIn Post Generator with Image and Video Support

This project is a Streamlit application that generates professional LinkedIn posts with support for images and videos. It uses a Large Language Model (LLM) from Groq to generate content based on user prompts, desired length, and language. The application also allows users to upload media files and post the generated content directly to their LinkedIn profile.

## Features

- Generate LinkedIn posts from a user-provided topic.
- Customize post length (Short, Medium, Long).
- Select post language (English, Hinglish, Kannada).
- Upload images and videos to accompany the post.
- Copy the generated post to the clipboard.
- Post directly to LinkedIn.

## Technologies Used

- Streamlit
- LangChain
- Groq API
- Pandas
- python-dotenv
- requests
- pyperclip
- LinkedIn API

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd linkedin-post-generator-with-image-post
```

### 2. Install Dependencies

Create a virtual environment and install the required dependencies.

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add the following:

```
GROQ_API_KEY="your_groq_api_key"
LINKEDIN_ACCESS_TOKEN="your_linkedin_access_token"
LINKEDIN_COMPANY_ID="your_linkedin_company_id"
```

## How to Run

### 1. Pre-process the data (optional)

If you have raw post data in `data/raw_posts.json`, you can pre-process it to generate `data/processed_posts.json`.

```bash
python preprocess.py
```

### 2. Run the Streamlit app

```bash
streamlit run main.py
```

## Project Structure

```
.
├── .env
├── data
│   ├── processed_posts.json
│   └── raw_posts.json
├── few_shot.py
├── llm_helper.py
├── main.py
├── post_generator.py
├── preprocess.py
├── README.md
├── requirements.txt
└── testfile.py
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
