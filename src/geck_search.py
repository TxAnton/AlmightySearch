#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%

import argparse
import asyncio

#%%
from datetime import datetime
import pandas as pd

#%%
from stc_geck.advices import format_document
from stc_geck.client import StcGeck
#%%

# DEFAULT_LIMIT = 5

#%%

async def _geck_search(prompt: str, limit: int=10, ipfs_url='http://127.0.0.1:8080'):
    geck = StcGeck(
        ipfs_http_base_url=ipfs_url,
        timeout=300,
    )

    # Connects to IPFS and instantiate configured indices for searching
    # It will take a time depending on your IPFS performance
    await geck.start()

    # GECK encapsulates Python client to Summa.
    # It can be either external stand-alone server or embed server,
    # but details are hidden behind `SummaClient` interface.
    summa_client = geck.get_summa_client()

    # Match search returns top-5 documents which contain `additive manufacturing` in their title, abstract or content.
    documents = await summa_client.search_documents({
        "index_alias": "nexus_science",
        "query": {
            "match": {
                "value": prompt,
                "query_parser_config": {"default_fields": ["abstract", "title", "content"]}
            }
        },
        "collectors": [{"top_docs": {"limit": limit}}],
        "is_fieldnorms_scoring_enabled": False,
    })

    await geck.stop()

    return documents
    # for document in documents:
    #     print(format_document(document) + '\n')

    
    
#%%
def geck_search(prompt: str ="additive manufacturing", limit: int=5, ipfs_url='http://127.0.0.1:8080'):
    res = asyncio.run(_geck_search(prompt, limit, ipfs_url))
    # ['abstract',
    #  'authors',
    #  'content',
    #  'ctr',
    #  'custom_score',
    #  'id',
    #  'issued_at',
    #  'languages',
    #  'links',
    #  'metadata',
    #  'page_rank',
    #  'referenced_by_count',
    #  'title',
    #  'type',
    #  'updated_at']

    obs = []
    for doc in res: # doc = res[0]
        abstract = doc["abstract"] # clean from xml
        authors = []
        for author in doc['authors']: # author = doc['authors'][0]

            given = author.get("given")
            if type(given) == list:
                given = given[0]
            given = str(given)
            family = author.get("family")
            if type(family) == list:
                family = family[0]
            family = str(family)

            authors.append(str(given+" "+family))  # authors.append(f"{author["given"]} {author["family"]}")

        content = doc["content"] # clean xml
        # doc["ctr"] # drop
        # doc["custom_score"] # drop
        dois = doc["id"].get("dois")
        doi = dois[0] if dois else None
        issued_at = datetime.fromtimestamp(doc["issued_at"])
        language = doc["languages"][0] if doc.get("languages") else None
        links = doc.get("links")
        publisher = doc["metadata"].get("publisher")
        # doc["page_rank"] # drop
        references = doc.get("referenced_by_count")
        title = doc.get("title")
        _type = doc.get("type")
        # updated_at = doc["updated_at"] #drop
        issued_at = datetime.fromtimestamp(doc["issued_at"])
        
        # updated_at = doc["updated_at"] #drop
        ob = [abstract, authors, content, doi, issued_at,language, links, publisher, references, title, _type]
        obs.append(ob)

    cols = ["abstract", "authors", "content", "doi", "issued_at", "language", "links", "publisher", "references", "title", "type"]
    df = pd.DataFrame(obs, columns=cols)
    return df
#%%
df = geck_search(prompt = "Ontology learning")

#%%

df


#%%