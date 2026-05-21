import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def explain_recommendation(workload_name, recommendation, ranked_clusters, rejected_clusters):
    prompt = f"""
Explain this infrastructure placement recommendation in clear, concise language.

Workload:
{workload_name}

Recommendation:
{recommendation}

Ranked valid clusters:
{ranked_clusters}

Rejected clusters:
{rejected_clusters}

Explain:
1. Why the selected cluster was chosen
2. Why rejected clusters were not chosen
3. Any production infrastructure tradeoffs
"""

    response = client.responses.create(
        model="gpt-5.2",
        input=prompt
    )

    return response.output_text