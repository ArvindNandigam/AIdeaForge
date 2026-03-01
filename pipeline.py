from hf_client import query_text_model, generate_image
import json


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

If a field is missing, intelligently infer it.
Do not include explanations.
Only return JSON.
"""

    structured_output = query_text_model(structured_prompt)

    try:
        structured_json = json.loads(structured_output)
    except:
        structured_json = {
            "event_name": "AI Campus Initiative",
            "date": "To Be Decided",
            "location": "College Campus",
            "objectives": user_input,
            "target_audience": "Students"
        }

    # ---------- Event Plan Generation ----------
    plan_prompt = f"""
Create a detailed campus event plan based on:

{structured_json}

Include:
- Overview
- Activities
- Timeline
- Required Resources
- Expected Impact
"""

    event_plan = query_text_model(plan_prompt)

    # ---------- Poster Generation ----------
    image_url = generate_image(structured_json.get("event_name", "Campus Event"))

    return {
        "structured": structured_json,
        "plan": event_plan,
        "image": image_url
    }