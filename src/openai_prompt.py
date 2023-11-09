import openai

#%%
# _api_key = "API KEY"
#%%
def init_api_key(_api_key):
    openai.api_key = _api_key
#%%

def openai_prompt(prompt:str="Привет, OpenAI!",max_tokens):
    max_tokens = max_tokens or 4096-len(prompt)
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=4096-len(prompt)*10
    )
    return response.choices[0].text

# print(response.choices[0].text)
#%%

# res = openai_prompt("Перечисли ресурсы для поиска статей. Напиши какие из них бесплатны")
#%%
# res.choices


#%%
