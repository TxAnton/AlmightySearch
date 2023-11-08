import openai

openai.api_key = "<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>"

response = openai.completions.create(
    model="text-davinci-003",
    prompt="Напиши 7 животных ",
    max_tokens=70
)

print(response.choices[0].text)
