import json
from llm_helper import invoke_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)
        enriched_posts = []
        for post in posts:
            metadata = extract_metadata(post["text"])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post["tags"]
        new_tags = {unified_tags[tag] for tag in current_tags}
        post["tags"] = list(new_tags)

    with open(processed_file_path, encoding="utf-8", mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


def extract_metadata(post):
    """
    Extract metadata from a LinkedIn post using an LLM.
    """
    template = '''
    You are given a LinkedIn post. Extract the following metadata in JSON format:
    1. line_count: Number of lines in the post.
    2. language: Language of the post (English, Hinglish, or Kannada).
    3. tags: Array of up to two relevant text tags for the post.
    
    Post: 
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    prompt = pt.format(post=post)
    
    try:
        response_content = invoke_model(prompt)
        json_parser = JsonOutputParser()
        metadata = json_parser.parse(response_content)
    except OutputParserException:
        raise OutputParserException("Unable to parse metadata due to large context or invalid response.")
    except RuntimeError as e:
        raise RuntimeError(f"LLM invocation failed: {e}")
    
    return metadata


def get_unified_tags(posts_with_metadata):
    """
    Generate a unified mapping for tags across multiple posts.
    """
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post["tags"])

    unique_tags_list = ", ".join(unique_tags)
    template = '''
    Unify the following tags into a shorter, consistent list:
    - Merge similar or related tags into one.
    - Follow title case convention for all unified tags.
    
    Original Tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    prompt = pt.format(tags=unique_tags_list)
    
    try:
        response_content = invoke_model(prompt)
        json_parser = JsonOutputParser()
        unified_tags = json_parser.parse(response_content)
    except OutputParserException:
        raise OutputParserException("Unable to parse unified tags due to large context or invalid response.")
    except RuntimeError as e:
        raise RuntimeError(f"LLM invocation failed: {e}")
    
    return unified_tags


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
