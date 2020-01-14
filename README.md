Creates reaction graph for NeuroRD tool:
https://github.com/neurord/stochdiff

# Features

Creating reaction graph in the web browser.
* square - represents molecule
* diamond - represents reaction
* arrow direction - represents the forward direction
* arrow thickness - represents value of the reaction that represents its color

Edge colors:
* green - represents domination of the forward rate
* red - represents domination of the reverse rate

Square colors:
* blue - regular particle
* yellow - (if selected) key particles from reactants 

# Prerequisites
```bash
pip install -r requiremets.txt
```

# Run
```bash
python create_reaction_graph.py --reaction_file [FILE] 
```

* reaction_file - is the XML reaction file created for NeuroRD tool
* By default all results are created inside reaction_visualizations/ volder

# Example graph

![CK_GRAPH](examples/graph.gif)
This is the example graph of all reactions of CaMKII kinase from the dendritic spine in the CA1 hippocampal cell 

In the examples folder/ :
* graph.html - interactive graph to play, shows all reactions of CaMKII (denoted as CK)
* graph.gif - gif shows the same graph

