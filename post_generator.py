import requests
import os
from llm_helper import llm
import re  # Import regex module for removing Markdown syntax

def upload_image_to_linkedin(image_file):
    """Uploads an image to LinkedIn and returns the asset ID."""
    linkedin_api_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {os.getenv('LINKEDIN_ACCESS_TOKEN')}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    # Register the upload request
    payload = {
        "registerUploadRequest": {
            "owner": f"urn:li:person:{os.getenv('LINKEDIN_COMPANY_ID')}",
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ],
            "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
        }
    }

    response = requests.post(linkedin_api_url, headers=headers, json=payload)
    if response.status_code == 200:
        upload_data = response.json()
        upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset_id = upload_data['value']['asset']

        # Upload the image
        upload_headers = {"Authorization": headers["Authorization"]}
        upload_response = requests.put(upload_url, headers=upload_headers, data=image_file.getvalue())
        if upload_response.status_code == 201:
            return asset_id
        else:
            raise Exception(f"Image upload failed: {upload_response.status_code}")
    else:
        raise Exception(f"Failed to register image upload: {response.status_code} - {response.json()}")

def post_to_linkedin(content, uploaded_files):
    """Posts content with optional images to LinkedIn."""
    linkedin_api_url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {os.getenv('LINKEDIN_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }

    # Upload images if provided
    media_list = []
    if uploaded_files:
        for file in uploaded_files:
            asset_id = upload_image_to_linkedin(file)
            media_list.append({
                "status": "READY",
                "media": asset_id
            })

    payload = {
        "author": f"urn:li:person:{os.getenv('LINKEDIN_COMPANY_ID')}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "IMAGE" if media_list else "NONE",
                "media": media_list
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(linkedin_api_url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to post on LinkedIn: {response.status_code} - {response.json()}")

def generate_post(prompt, length, language):
    """Generates a LinkedIn post based on user input."""
    refined_prompt = get_prompt(prompt, length, language)
    response = llm.invoke(refined_prompt)
    clean_response = remove_markdown_syntax(response.content)
    return clean_response

def get_prompt(user_prompt, length, language):
    """Creates a prompt for the language model using user input."""
    length_str = {
        "Short": "1 to 10 lines",
        "Medium": "10 to 20 lines",
        "Long": "20 to 35 lines"
    }.get(length, "10 to 20 lines")

    return f"""
    Generate a professional LinkedIn post based on the following details. 
    Please ensure there are no introductory statements such as 'Here is a LinkedIn post on...', 'This is a post about...', or similar preambles. Start directly with the content.

    1) Topic: {user_prompt}
    2) Length: {length_str}
    3) Language: {language}
    - If Language is Hinglish, it means a mix of Hindi and English. However, ensure the script is written in English.
    4) Structure the content into multiple paragraphs, with each paragraph containing 3-4 sentences for better readability.
    5) Add relevant and popular hashtags at the end.
    6) Maintain a professional tone suitable for LinkedIn's audience, making the content engaging and informative.
    7) Use relevant emojis to enhance engagement and readability.
    """


def remove_markdown_syntax(text):
    """Removes Markdown syntax like ** for bold text."""
    # This regex removes bold text (e.g., **bold**)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # You can add more regex replacements here if you need to clean other Markdown syntax
    return text

if __name__ == "__main__":
    content = generate_post("How AI is transforming the workplace", "Medium", "English")
    try:
        print("Post Successful:", post_to_linkedin(content, None))
    except Exception as e:
        print("Error:", str(e))
