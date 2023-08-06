# :snake: neo4jvis
<div align="center">
    <img src="./docs/example.png" width="400">
</div>

## Installation

Neo4jvis requires [Neo4j driver](https://neo4j.com/developer/python/#python-driver).
You can install neo4jvis with:
```sh
pip install neo4jvis
```

## Usage

Here's how you can use it:
First import libraries, initialise the driver and create the graph container:

###  1. Import and init

```python
from neo4j import GraphDatabase
from neo4jvis.model.styled_graph import StyledGraph

driver = GraphDatabase.driver(uri="bolt://url:port", auth=("my user", "my pass"))
graph = StyledGraph(driver)
```
###  2. Retrieve graph from neo4j

#### 2.1 Retrieve whole graph

Here's how you can generate an html file with all the nodes and relationships of the database:
```python
graph.generate_whole_graph()
graph.draw("output.html")
```

#### 2.2 Generate graph from a query

Here's is how you can generate a graph from a given query provided by the developer:
```python
QUERY = "MATCH p=()-[]->() RETURN p"

graph.add_from_query(QUERY)
graph.draw("output.html")
```

### 3. Style graph

#### 3.1 Change nodes color
```python
RED = "#ff0000"
WHITE = "#FFFFFF"

for node in list(graph.nodes.values()):
    node["color"] = {
        "border": WHITE,
        "background": RED
    }
graph.draw("output.html")
```
<div align="center">
    <img src="./docs/color.png" width="400">
</div>

#### 3.2 Change nodes size
```python
for node in list(graph.nodes.values()):
    node["value"] = randrange(1, 10)
graph.draw("output.html")
```
<div align="center">
    <img src="./docs/size.png" width="400">
</div>

#### 3.3. Change other node properties supported by vis.js

Neo4jvis supports all the [options for nodes of vis.js](https://visjs.github.io/vis-network/docs/network/nodes.html).

Example usage:
```python
node["shape"] = "triangle"
node["borderWidth"] = 10
node["label"] = "EXAMPLE"
node["font"] = {
    "color": "#e8c2b0",
    "size": 20,
}
graph.draw("output.html")
```
<div align="center">
    <img src="./docs/node_example.png" width="400">
</div>

#### 3.4. Change edge properties
```python
for edge in graph.edges:
    edge["value"] = random.randrange(1, 10)
    edge["color"] = {
        "color": "#e8c2b0"
    }
graph.draw("output.html")
```
<div align="center">
    <img src="./docs/edges.png" width="400">
</div>

#### 3.5. Change other edge properties
Similarly, as with nodes, neo4jvis supports all the [options for edges of vis.js](https://visjs.github.io/vis-network/docs/network/edges.html).

#### 4. Change graph options
Graphs come with a default set of options defined in ```options``` property:

```python
>>> print(graph.options)
{
    'nodes': ...
    'edges': ...
    'interaction': ...
    'physics': ...
}
```

See the available [options for graphs supported by vis.js](https://visjs.github.io/vis-network/docs/network/#options).

Example usage:
```python
graph.options["directed"] = "false"
```

## Advanced usage

#### Generate graph from neomodel StructuredRel

[Neomodel](https://neomodel.readthedocs.io) is a Object Graph Mapper for Neo4j database. Neo4jvis allows the retrieval of the network from a list of neomodel [StructuredRel objects](https://neomodel.readthedocs.io/en/latest/relationships.html). 
Here's an example of the usage:
```python
class Connected(StructuredRel):
    pass
    
class Usuarios(StructuredNode):
    id = StringProperty()
    connected = RelationshipTo("Usuarios", "CONNECTED", model = Connected)
    
QUERY = """ 
    MATCH (n1:Usuarios)-[r:CONNECTED]->() 
    RETURN r
"""

Z = neomodel.db.cypher_query(
    QUERY, 
    resolve_objects=True)
relationships_list = [rel[0] for rel in Z[0]]    
graph.add_from_neomodel_relationships(relationships_list)
graph.draw("output.html")
```