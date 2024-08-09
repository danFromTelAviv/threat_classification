import pandas as pd
from openai import OpenAI
import os
from tqdm.contrib.concurrent import process_map
from pathlib import Path
import numpy as np
import json
Path("scammer_identities").mkdir(parents=True, exist_ok=True)
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def run_query(messages, max_tokens=4_000) -> str:
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
        stream=True,
        max_tokens=max_tokens,
    )
    res = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            res.append(chunk.choices[0].delta.content)
    
    return json.loads("".join(res))

def create_messages(row):
    return [
        {
            "role": "user",
            "content": f'''generate a structured JSON containing detailed information about the scam based on the description. 
            The JSON should include the following fields with the specified options for consistency:

            name: Name of the scam if mentioned.
            email: Email address used by the scammer if mentioned.
            phone_number: Phone number used by the scammer if mentioned.
            target_state: The state targeted by the scam if mentioned.
            target_zip: The zip code targeted by the scam if mentioned.
            target_country: The country targeted by the scam if mentioned.
            from_state: The state from where the scam originates if mentioned.
            from_zip: The zip code from where the scam originates if mentioned.
            from_country: The country from where the scam originates if mentioned.
            channel: The medium used for the scam. Options: ["email", "phone", "SMS", "social media", "postal mail", "in-person"].
            company_or_entity_name: Name of the company or entity the scammer claims to represent if mentioned.
            age_of_victim: Age of the victim if mentioned.
            type_of_scam: The type of scam based on common characteristics. Options: ["phishing", "advance fee fraud", "tech support scam", "lottery/sweepstakes scam", "charity scam", "employment scam", "investment scam"].
            scammer_tactics: Tactics used by the scammer. Options: ["urgency", "authority", "emotional appeal", "incentives", "threats"].
            payment_methods: Payment methods requested by the scammer if mentioned. Options: ["gift cards", "wire transfers", "cryptocurrency", "prepaid debit cards"].
            content_characteristics: Notable characteristics of the content. Options: ["poor grammar", "spelling errors", "non-native language patterns", "unusual formatting", "excessive use of capitalization", "urgent tone"].
            entities_involved: Entities involved in the scam if mentioned.
            entities_types: Types of entities involved in the scam if mentioned. Options: ["individual", "organization", "government"].
            
            scam description: {row['description']}''',
        },
    ]


def process_row(row):
    try:
        row['structured'] = run_query(create_messages(row))
        Path(f"scammer_identities/{row['index']}.json").write_text(json.dumps(row['structured']))
    except:
        pass
    return row




if __name__ == "__main__":
    df = pd.read_csv("/workspaces/threat_classification/scam_reports_sample_10000.csv").reset_index()
    mapping_df = pd.read_csv("/workspaces/threat_classification/clusters_mapping.csv")
    df = df.merge(mapping_df, on="index", how="left")

    rows = process_map(process_row, df.reset_index().to_dict('records'), max_workers=20, chunksize=10)