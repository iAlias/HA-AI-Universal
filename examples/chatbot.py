"""Simple chatbot example using universal-ai."""

from uai import ai

# Switch provider if needed
# ai.use("gemini")

response = ai.ask("Hello! Tell me a fun fact about programming.")
print(response)
