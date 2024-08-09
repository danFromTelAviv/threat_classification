import pandas as pd
from openai import OpenAI
import os
from tqdm.contrib.concurrent import process_map
from typing import List
from pathlib import Path
import numpy as np
Path("embeddings").mkdir(parents=True, exist_ok=True)


df = pd.read_csv("/workspaces/threat_classification/scam_reports_sample_10000.csv")
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def get_embedding(text: str, model="text-embedding-3-small", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = client.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding


def process_row(row):
    try:
        row['embedding'] = get_embedding(row['description'])
        np.save(f"embeddings/{row['index']}.npy",  np.array(row['embedding']))
    except:
        pass
    return row

rows = process_map(process_row, df.reset_index().to_dict('records'), max_workers=20, chunksize=10)

hi = 5