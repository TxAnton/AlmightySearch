#%%
import json
from tqdm import tqdm
from src.rephrasing_a_sentence import paraphrase_with_comment,init_api_key
init_api_key(_api_key)
from src.geck_search import geck_search


#%%
# paraphrase_with_comment
input_text = "Using RNNs in ontology learning"
comment = "Хочу получить перефразированное предложение"
print("Оригинальный текст:", input_text)
print("Комментарий:", comment)

#%%

paraphrased_text = paraphrase_with_comment(input_text, comment,num_phrases = 3)
#%%
print("Полученные промпты")
print(paraphrased_text)
#%%
transformed_prompts = [t for t in paraphrased_text.split("\n") if not("фраз" in t.lower() or "текст" in t.lower()) and t]
transformed_prompts.append(input_text)
_transformed_prompts = []
for t in transformed_prompts:
    if t[1]=='.':
        t = t[2:]
        t = t.strip(". ")
    _transformed_prompts.append(t)
transformed_prompts = _transformed_prompts
#%%
# with open("transformed_prompts1.txt",'w+') as fp:
#     json.dump(transformed_prompts,fp)
with open("transformed_prompts1.txt",'r') as fp:
    transformed_prompts = json.load(fp)
#%%
dfs = []
print("Поиск статей")
for tp in tqdm(transformed_prompts):
    df = geck_search(prompt=tp,limit=5)
    dfs.append(df)
#%%
# for i in range(len(transformed_prompts)):
#     dfs[i].to_csv(f"{transformed_prompts[i]}.csv")
# tmp = []
# for i in range(len(transformed_prompts)):
#     d = pd.read_csv(f"{transformed_prompts[i]}.csv")
#     tmp.append(d)
# dfs = tmp
#%%
#%%
print("Ранжирование найденных статей")
rows = []
for triplet in zip([list(df.iterrows()) for df in dfs]):
    rows.extend(triplet[0])
df = pd.DataFrame([list(i[1]) for i in rows],columns = ["abstract", "authors", "content", "doi", "issued_at", "language", "links", "publisher", "references", "title", "type"])
#%%
for ix,row in df.iterrows():
    print("===================")
    print(ix)
    print("-------------------")
    print(row["title"])
    print("Relaease year:",row["issued_at"].year)
    print("Authors:",end='\n\t')
    print(*row["authors"],sep='\n\t')
    print(row["doi"])
    
    

#%%
# %time
gargantext = ""
i =0
for ix,row in df.iterrows():
    if not i<3: continue
    i+=1
    t = row["abstract"]+row["content"]
    gargantext+=t
    gargantext = df.iloc[n,:]["abstract"]+df.iloc[n,:]["content"]
    # if len(gargantext)100000: break
#%%
!pip install openai_summarize
#%%
import openai_summarize
openai_summarizer = openai_summarize.OpenAISummarize(_api_key)

#%%
# summary = openai_summarizer.summarize_text(gargantext)
# with open("summary.txt","w") as fp:
#     fp.write(summary)
with open("summary.txt","r") as fp:
    summary = fp.read()
#%%
# summary = openai_summarizer.summarize_text(gargantext)
print(summary)



#%%