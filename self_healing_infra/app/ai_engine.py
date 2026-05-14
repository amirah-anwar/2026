from openai import OpenAI

client = OpenAI()


class AIRootCauseAnalyzer:

    def build_prompt(self, alerts):

        alert_text = "\n".join([
            f"- SERVICE={alert.service} ALERT={alert.message}"
            for alert in alerts
        ])

        prompt = f"""
You are an expert infrastructure incident commander.

Analyze the following infrastructure alerts.

Alerts:
{alert_text}

Tasks:
1. Summarize the incident.
2. Identify the most likely root cause.
3. Explain cascading impact.
4. Recommend remediation steps.
5. Mention which service should be prioritized first.

Be concise but technically detailed.
"""

        return prompt

    def analyze_alerts(self, alerts):

        if not alerts:
            return {
                "summary": "No active incidents detected.",
                "root_cause": "None",
                "recommended_action": "No action required."
            }

        prompt = self.build_prompt(alerts)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior site reliability engineer."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        return {
            "analysis": content
        }