from hf_client import query_text_model, generate_image


def extract_structured_info(raw_text):

    prompt = f"""
    Extract the following information from the text below.
    Return ONLY valid JSON.

    Required fields:
    - event_name
    - date
    - location
    - objectives
    - target_audience

    Text:
    {raw_text}
    """

    return query_text_model(prompt)


def generate_event_plan(structured_json):

    prompt = f"""
    Using the structured data below, generate a detailed and professional campus event execution plan.

    Structured Data:
    {structured_json}
    """

    return query_text_model(prompt)


def run_pipeline(raw_text):

    structured = extract_structured_info(raw_text)

    plan = generate_event_plan(structured)

    image = generate_image("Professional campus event poster")

    return {
        "structured": structured,
        "plan": plan,
        "image": image
    }