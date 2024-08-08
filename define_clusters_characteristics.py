import pandas as pd
from openai import OpenAI
import os
from tqdm import tqdm


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def run_query(messages, max_tokens=4_000) -> str:
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
        max_tokens=max_tokens,
    )
    res = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            res.append(chunk.choices[0].delta.content)
    
    return "".join(res)

def create_messages(content):
    return [
        {
            "role": "user",
            "content": content,
        },
    ]



def generate_prompt(positives, negatives):
    return f'''
    given positive and negative examples of different fraud examples describe in words what makes the positives unique and different from the negative example.
    the description should generalize and not stick to any specific piece of information that is found in the positive examples.
    the description should describe the overarching characteristics of the positives that are not present in the negatives.
    the result should be 1 sentence long and should be very to the point.

    positives: [{"][".join(positives)}]
    negatives: [{"][".join(negatives)}]
    '''


def get_cluster_unique_selling_points(cluster_id, df):
    positives = df[df["cluster"] == cluster_id]['description'].tolist()
    negatives = df[df["cluster"] != cluster_id]['description'].tolist()
    prompt = generate_prompt(positives, negatives)
    return run_query(create_messages(prompt))


if __name__ == "__main__":
    df = pd.read_csv("/workspaces/threat_classification/scam_reports_sample_10000_embeddings.csv").groupby("cluster").sample(5).reset_index()

    for cluster_idx in tqdm(df.cluster.unique()):
        df.loc[df.cluster == cluster_idx, "unique_selling_points"] = get_cluster_unique_selling_points(cluster_idx, df)

    df[['cluster', 'description', 'unique_selling_points']].to_csv("cluster_characteristics.csv", index=False)