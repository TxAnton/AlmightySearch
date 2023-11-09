import openai
#%%
# _api_key = "API KEY"
#%%
def init_api_key(_api_key):
    openai.api_key = _api_key

#%%
paraphrased_phrases = []
def paraphrase_with_comment(input_text, comment = "Хочу получить перефразированное предложение",num_phrases=5):
    # num_phrases = 5
    response = openai.completions.create(
        model='text-davinci-003',
        prompt=f"{input_text} {comment} {num_phrases} штук каждое на новой строке без нумерации",
        max_tokens=500,
        temperature=0.7,
        n=1,
        stop=None,
        logprobs=0
    )
    paraphrased_text = response.choices[0].text.strip()
    paraphrased_phrases.append(paraphrased_text)
    return response.choices[0].text.strip()

# input_text = "Какая хорошая погода на улице"
# comment = "Хочу получить перефразированное предложение"

# paraphrased_text = paraphrase_with_comment(input_text, comment)

# print("Оригинальный текст:", input_text)
# print("Комментарий:", comment)
# print("Перефразированный текст:")
# print(*paraphrased_phrases)

