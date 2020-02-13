from pyvis.network import Network
import xml.etree.ElementTree as ET


def neurord_parse_reaction_file(filename, remove_p=False):
    """

    :param filename:
    :param remove_p:
    :return:
    """
    doc = ET.parse(filename)

    species_kdiff = {}
    for s in doc.findall('Specie'):
        name = s.attrib['name']
        if remove_p:
            name = name.replace('p', '')
        species_kdiff[name] = float(s.attrib['kdiff'])

    reactions = {}
    for reaction in doc.findall("Reaction"):
        r = {'reactant': [], 'product': [], 'forward': 0, 'reverse': 0}
        reactions[reaction.attrib['name']] = r

        f = reaction.find("forwardRate")
        if f is not None:
            r['forward'] = float(f.text)

        b = reaction.find("reverseRate")
        if b is not None:
            r['reverse'] = float(b.text)

        for reactant in reaction.findall("Reactant"):
            name = reactant.attrib['specieID']
            r['reactant'].append(name)

        for product in reaction.findall("Product"):
            name = product.attrib['specieID']
            r['product'].append(name)

    return species_kdiff, reactions


def reaction_filter(reactions, reactants_left=None, percent_biggest_edges_to_left=None):
    """

    :param reactions:
    :param reactants_left:
    :param percent_biggest_edges_to_left:
        the percent value of biggest edges to left: 0-100. Default is None, meaning - left edges of all nodes selected.
    :return:
    """

    def is_add(name):
        for r in reactants_left:
            if r in name:
                return True
        return False

    if reactants_left:
        filtered = []
        for k, v in reactions.items():
            for r in v['reactant']:
                for p in v['product']:
                    if is_add(r) or is_add(p):
                        filtered.append((k, v))
        reactions = dict(filtered)

    if percent_biggest_edges_to_left:
        p = percent_biggest_edges_to_left / 100
        sorted_dict = [x for x in sorted(reactions.items(), key=lambda x: -(
            x[1]['forward'] if x[1]['forward'] > x[1]['reverse'] else x[1]['reverse']))]
        max_len = round(len(sorted_dict) * p)
        reactions = dict(sorted_dict[:max_len])

    return reactions


def create_graph(reactions, reactants=None, height="100%", width="100%", bgcolor="#222222", font_color="white",
                 node_distance=140, spring_strength=0.001):
    """

    :param reactions:
    :param reactants:
    :param height:
    :param width:
    :param bgcolor:
    :param font_color:
    :param node_distance:
    :param spring_strength:
    :return:
    """
    g = Network(height=height, width=width, bgcolor=bgcolor, font_color=font_color, directed=True)

    nodes = []
    if reactants is None:
        reactants = []
    for k, v in reactions.items():
        fr = float(v['forward'])
        rr = float(v['reverse'])
        afinity_rate = fr / rr if rr != 0 else fr
        diffusion_rate = rr / fr if fr != 0 else rr
        if afinity_rate > diffusion_rate:
            edge_color = "#91db7b"  # green - domination of forward reaction
            value = afinity_rate
        else:
            edge_color = "#ff9999"  # red - domination of reverse reaction
            value = diffusion_rate

        edge_thick = value
        if edge_thick > 10000:
            edge_thick = 10000

        for r in v['reactant']:
            for p in v['product']:

                if r not in nodes:
                    nodes.append(r)
                    g.add_node(r, color="#f5ce42" if r in reactants else "#80bfff")
                if p not in nodes:
                    nodes.append(p)
                    g.add_node(p, color="#f5ce42" if p in reactants else "#80bfff")
                if k not in nodes:
                    nodes.append(k)
                    g.add_node(n_id=k, shape="diamond", color="#969696", label="R", size=10, title=k)

                g.add_edge(r, k, color=edge_color, value=edge_thick, title=value)
                g.add_edge(k, p, color=edge_color, value=edge_thick, title=value)

    g.show_buttons(filter_=['physics'])
    g.hrepulsion(node_distance=node_distance, spring_strength=spring_strength)

    return g
