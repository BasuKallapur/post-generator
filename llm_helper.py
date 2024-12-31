from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192"
)

def invoke_model(prompt, max_tokens=1000):
    """
    Invokes the language model with a given prompt.

    Args:
        prompt (str): The input prompt for the model.
        max_tokens (int): Maximum number of tokens to generate.

    Returns:
        str: The response content from the model.
    """
    try:
        response = llm.invoke(prompt, max_tokens=max_tokens)
        return response.content
    except Exception as e:
        raise RuntimeError(f"Failed to generate content: {e}")

if __name__ == "__main__":
    # Test example
    test_prompt = "Generate a LinkedIn post about the benefits of mindfulness at work."
    try:
        response = invoke_model(test_prompt)
        print(response)
    except RuntimeError as e:
        print(e)
