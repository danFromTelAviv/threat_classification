In this repo you can find the code used to analyze and cluster scam data.

The general flow is:
analyze.ipynb - incluides basic data analysis and some minor examples of data normalization. 
create_embeddings.py - used to call openai's embedding model 
cluster.ipynb - uses classical clustering methods and presents the data on a 2d dimentionally reduced map.
exctract_chacteristics.py - used for turning the scam description into structured data. 
define_cluster_characteristics.py - uses a contrastive prompt to generate the defintion of each cluster. 


comments:
It is recommended to run everything within the docker defined by the dockerfile, requirements.txt and devcontainer.json (on vs code)

Notice that embeddings and structured data is saved to the folders: embeddings, embeddings 

The code will generate a cluster mapping saved as a csv. 

The code will create a cluster_charactersitics.csv which gives a few examples and the cluster's description - as an alternative to a UI for now. 
*some additonal extensions/installs for jupyter may be required

the code assumes the enviroment variable "OPENAI_API_KEY" is set. 

example launch.json:
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "OPENAI_API_KEY": "xxxxxxx",
            },
            "justMyCode": true
        }
    ]
}
