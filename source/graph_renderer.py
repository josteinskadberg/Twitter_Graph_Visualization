from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, ColumnDataSource, LabelSet
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Category20c
from bokeh.plotting import figure, from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from bokeh.embed import components
from networkx.algorithms import community
import networkx as nx


def render_graph(G=None):
    if G is None:
        G = nx.read_graphml("test.graphml")
    degrees = dict(nx.degree(G))

    # set degree for each node
    nx.set_node_attributes(G, name='degree', values=degrees)

    # Detect communities
    communities = community.greedy_modularity_communities(G)

    # adjust node size to degree
    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, degree+number_to_adjust_by)
                               for node, degree in nx.degree(G)])
    nx.set_node_attributes(G, name='adjusted_node_size',
                           values=adjusted_node_size)
    # Create empty dictionaries
    modularity_class = {}
    modularity_color = {}

    # Loop through each community in the network
    n_comm = len(communities)
    if n_comm <= 3:
        n_comm = 3
    for community_number, comm in enumerate(communities):
        # For each member of the community, add their community number and a distinct color
        for name in comm:
            modularity_class[name] = community_number
            modularity_color[name] = Category20c[n_comm][community_number]

    # Add modularity class and color as attributes from the network above
    nx.set_node_attributes(G, modularity_class, 'modularity_class')
    nx.set_node_attributes(G, modularity_color, 'modularity_color')

    # colors for nodes and edge highlighting
    node_hightlight_color = "white"
    edge_highlight_color = "black"

    HOVER_TOOLTIPS = [
        ("Tag", "@index"),
        ("Degree", "@degree"),
        ("Modulerity Class", "@modularity_class"),
        ("Modularity Color", "$color[swatch]:modularity_color")
    ]

    plot = figure(tooltips=HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom')

    # remove background grid
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.axis.visible = False

    # generate bokeh graph from network x graph
    network_graph = from_networkx(
        G, nx.spring_layout, scale=10, center=(0, 0))

    node_size_by = "adjusted_node_size"
    node_color_by = "modularity_color"
    # Set size from degree attribute and color from modularity_color attribute
    network_graph.node_renderer.glyph = Circle(
        size=node_size_by, fill_color=node_color_by)

    # set node hover and selection properties
    network_graph.node_renderer.hover_glyph = Circle(
        size=node_size_by, fill_color=node_color_by, line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(
        size=node_size_by, fill_color=node_color_by, line_width=2)

    # Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    # Set edge highlight colors
    network_graph.edge_renderer.selection_glyph = MultiLine(
        line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(
        line_color=edge_highlight_color, line_width=2)

    # Highlight nodes and edges
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()

    # Add Labels
    x, y = zip(*network_graph.layout_provider.graph_layout.values())
    nodes = list(G.nodes())
    source = ColumnDataSource(
        {'x': x, 'y': y, 'name': [nodes[i] if G.nodes[nodes[i]]["degree"] > 2 else "" for i in range(len(x))]})
    labels = LabelSet(x='x', y='y', text='name', source=source,
                      background_fill_color='white', text_font_size='10px', background_fill_alpha=.7)
    plot.renderers.append(labels)

    plot.renderers.append(network_graph)
    return components(plot)+(G,)


if __name__ == "__main__":
    render_graph()
