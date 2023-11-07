#!/usr/bin/env python
# coding: utf-8

# # Examples
# 
# Connects to IPFS and instantiate configured indices for searching
# It will take a time depending on your IPFS performance

#%% [1]:


from stc_geck.client import StcGeck
geck = StcGeck(
    ipfs_http_base_url='http://127.0.0.1:8080',
    timeout=300,
)
await geck.start()


# GECK encapsulates Python client to Summa. It can be either external stand-alone server or embed server, but details are hidden behind `SummaClient` interface.

#%% [2]:


summa_client = geck.get_summa_client()


# Match search returns top-5 documents which contain `additive manufacturing` in their title, abstract or content.

#%% [3]:


from stc_geck.advices import format_document
#%%
async def geck_search(prompt = "additive manufacturing"):
    documents = await summa_client.search_documents({
        "index_alias": "nexus_science",
        "query": {
            "match": {
                "value": prompt,
                "query_parser_config": {"default_fields": ["abstract", "title", "content"]}
            }
        },
        "collectors": [{"top_docs": {"limit": 5}}],
        "is_fieldnorms_scoring_enabled": False,
    })
    return documents
#%%
documents = await geck_search()


#%%
# for document in documents:
#     print(format_document(document) + '\n')


# Let's download PDFs. Helper function `download_document` stores files in the current directory.

#%% [4]:

type(documents)

#%%
for document in documents:
    await geck.download_document(document,file_name=f'files/{document["title"]}')


# Below we have several more examples of search queries. More documentation on how to do queries to Summa can be found at https://izihawa.github.io/summa/core/query-dsl/

#%%