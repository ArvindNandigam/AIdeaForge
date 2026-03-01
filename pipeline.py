from hf_client import query_text_model, generate_image
import json
import re

def run_pipeline(user_input):
    # ---------- Structured Extraction ----------
    structured_prompt = f"""
Extract structured information from the following campus idea.

Return ONLY valid JSON in this exact format:

{{
  "event_name": "",
  "date": "",
  "location": "",
  "objectives": "",
  "target_audience": ""
}}

Campus Idea:
{user_input}

Only return JSON.
"""
    structured_output = query_text_model(structured_prompt)

    # Extract JSON safely
    json_match = re.search(r"\{.*\}", structured_output, re.DOTALL)
    try:
        structured_json = json.loads(json_match.group()) if json_match else None
    except:
        structured_json = None

    # Default fallback if extraction fails
    if not structured_json:
        structured_json = {
            "event_name": "AI Campus Initiative",
            "date": "To Be Decided",
            "location": "College Campus",
            "objectives": user_input,
            "target_audience": "Students"
        }

    # ---------- Event Plan ----------
    plan_prompt = f"""
Using the following structured data, create a complete campus event plan.

Structured Data:
{json.dumps(structured_json, indent=2)}

Include:
- Overview
- Detailed Activities (at least 5)
- Timeline (day-wise or hour-wise)
- Required Resources
- Expected Impact

Return in clear, human-readable text. Ensure no truncation and include all activities.
"""
    event_plan = query_text_model(plan_prompt)

    # ---------- Poster / Image ----------
    # Use more context to generate a richer poster
    poster_prompt = f"""
Create a visually appealing poster for the following campus event:

Event Name: {structured_json['event_name']}
Date: {structured_json['date']}
Location: {structured_json['location']}
Highlights/Objectives: {structured_json['objectives']}

Style: vibrant, modern, cinematic lighting, detailed illustration, eye-catching
"""
    image_url = generate_image(poster_prompt)

    return {
        "structured": structured_json,
        "plan": event_plan,
        "image": image_url
    }