# Scam Data Analysis and Clustering

This repository contains the code for analyzing and clustering scam data.

## Workflow Overview

1. **`analyze.ipynb`**  
   - Performs basic data analysis.
   - Includes minor examples of data normalization.

2. **`create_embeddings.py`**  
   - Calls OpenAI's embedding model to generate embeddings for the data.

3. **`cluster.ipynb`**  
   - Applies classical clustering methods.
   - Presents the data on a 2D dimensionally reduced map.

4. **`extract_characteristics.py`**  
   - Converts scam descriptions into structured data.

5. **`define_cluster_characteristics.py`**  
   - Uses a contrastive prompt to define the characteristics of each cluster.

## Setup and Usage

- It is recommended to run the code within a Docker environment defined by the `Dockerfile`, `requirements.txt`, and `devcontainer.json` (if using VS Code).
- Ensure that the environment variable `OPENAI_API_KEY` is set before running the code.

### Output

- Embeddings and structured data will be saved in the `embeddings/` directory.
- A cluster mapping will be generated and saved as a CSV file.
- A `cluster_characteristics.csv` file will be created, providing examples and descriptions of each cluster as an alternative to a UI for now.

### Additional Notes

- Some additional extensions or installs for Jupyter may be required.
- The code assumes the environment variable `OPENAI_API_KEY` is set.

## Example `launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "env": {
        "OPENAI_API_KEY": "xxxxxxx"
      },
      "justMyCode": true
    }
  ]
}
