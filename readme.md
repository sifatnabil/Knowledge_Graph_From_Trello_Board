# Given a Trello board ID, create a graph from the board's cards

Install the packages using `pip install -r requirements.txt`. Also, create a file named `env.py` and store your Trello API key and token in it. The file should look like this:

```text
key = "YOUR_API_KEY"
token = "YOUR_TOKEN"
board_id = "YOUR_BOARD_ID"

neo4j_url = ""
neo4j_username = ""
neo4j_password = ""
```

To see how to setup a **Neo4j** graph database locally using docker, read the `readme.md` file from [This Repo](https://github.com/sifatnabil/Knowledge_Graph_With_Neo4j).

Feed the graph using the command `python main.py`.
