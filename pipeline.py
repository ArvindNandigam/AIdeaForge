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

    json_match = re.search(r"\{.*\}", structured_output, re.DOTALL)

    if json_match:
        try:
            structured_json = json.loads(json_match.group())
        except:
            structured_json = None
    else:
        structured_json = None

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
Create a detailed campus event plan.

Structured Data:
{json.dumps(structured_json, indent=2)}

Include:
- Overview
- Activities
- Timeline
- Required Resources
- Expected Impact
"""

    event_plan = query_text_model(plan_prompt)

    # ---------- Poster ----------
    image_url = generate_image(structured_json["event_name"])

    return {
        "structured": structured_json,
        "plan": event_plan,
        "image": image_url
    }