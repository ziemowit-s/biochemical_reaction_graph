import os
import argparse

from utils import neurord_parse_reaction_file, reaction_filter, create_graph

description = """
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
"""
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--reaction_file", help="Xml file containing reactions.", required=True)

    ap.add_argument("--result_folder",
                    help="Path to folder where to put HTML result files, default: reaction_visualizations/",
                    default='reaction_visualizations')

    ap.add_argument("--left_edges", help="Left only the percent value of the biggest edges from 0 to 100, default: 100",
                    default=100, type=float)

    ap.add_argument("--node_distance", help="Distance between nodes on the graph, default: 140.", default=140)

    ap.add_argument("--reactants", nargs='+',
                    help="Reduce graph particles only to those denifed here, default: None, "
                         "meaning - left edges of all nodes selected.",
                    default=None)

    args = ap.parse_args()

    species_kdiff, reactions = neurord_parse_reaction_file(filename=args.reaction_file)

    reactions = reaction_filter(reactions, reactants_left=args.reactants, percent_biggest_edges_to_left=args.left_edges)
    graph = create_graph(reactions=reactions, reactants=args.reactants)

    graph.show_buttons(filter_=['physics'])
    graph.hrepulsion(node_distance=args.node_distance, spring_strength=0.001)

    name = '_'.join(args.reactants) if args.reactants else 'all_reactions'
    os.makedirs(args.result_folder, exist_ok=True)
    graph.show('%s/%s_%s_percent.html' % (args.result_folder, name, args.left_edges))
