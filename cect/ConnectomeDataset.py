from cect import print_

from cect.ConnectomeReader import ConnectionInfo
from cect.ConnectomeReader import DEFAULT_COLORMAP
from cect.ConnectomeReader import POS_NEG_COLORMAP
from cect.Cells import get_short_description
from cect.Cells import get_standard_color
from cect.Cells import is_bilateral_left
from cect.Cells import is_bilateral_right
from cect.Cells import are_bilateral_pair
from cect.ConnectomeReader import is_neuron
from cect.ConnectomeReader import is_muscle

import numpy as np
import math
import sys
import networkx as nx
import pprint

from cect.Cells import get_SIM_class


class ConnectomeDataset:
    DEFAULT_DTYPE = np.float64

    verbose = False

    def __init__(self):
        self.nodes = []
        self.connections = {}
        self.connection_infos = []

        self.view = None

    def _expand_conn_arrays(self):
        for c in self.connections:
            conn_array = self.connections[c]

            dim = conn_array.shape[0]
            new_conn_array = np.zeros([dim + 1, dim + 1], dtype=self.DEFAULT_DTYPE)
            new_conn_array[: conn_array.shape[0], : conn_array.shape[1]] = conn_array

            self.connections[c] = new_conn_array

    def to_networkx_graph(self, synclass):
        import networkx as nx

        conn_array = self.connections[synclass]

        G = nx.DiGraph(conn_array)
        mapping = {}

        for n_id in range(len(self.nodes)):
            mapping[n_id] = self.nodes[n_id]

        Gn = nx.relabel_nodes(G, mapping)

        for nn_id in Gn.nodes:
            nn = Gn.nodes[nn_id]
            nn["SIM_class"] = get_SIM_class(nn_id)

        return Gn

    def add_connection_info(self, conn: ConnectionInfo):
        if self.verbose:
            print_("----   Adding: %s" % conn)

        self.connection_infos.append(conn)

        if conn.synclass not in self.connections:
            if len(self.connections) == 0:
                self.connections[conn.synclass] = np.zeros(
                    [0, 0], dtype=self.DEFAULT_DTYPE
                )
            else:
                existing = list(self.connections.values())[0]
                self.connections[conn.synclass] = np.zeros(
                    existing.shape, dtype=self.DEFAULT_DTYPE
                )

        if conn.pre_cell not in self.nodes:
            self.nodes.append(conn.pre_cell)
            self._expand_conn_arrays()

        if conn.post_cell not in self.nodes:
            self.nodes.append(conn.post_cell)
            self._expand_conn_arrays()

        conn_array = self.connections[conn.synclass]

        pre_index = self.nodes.index(conn.pre_cell)
        post_index = self.nodes.index(conn.post_cell)

        conn_array[pre_index, post_index] = conn.number

        if self.verbose:
            print_(
                "Updated (%i,%i), nodes %s: \n%s"
                % (pre_index, post_index, self.nodes, conn_array)
            )

    def read_data(self):
        return self.get_neuron_to_neuron_conns()

    def get_neuron_to_neuron_conns(self):
        neurons = set([])
        neuron_conns = []
        for conn_info in self.connection_infos:
            if is_neuron(conn_info.pre_cell) and is_neuron(conn_info.post_cell):
                neurons.add(conn_info.pre_cell)
                neurons.add(conn_info.post_cell)
                neuron_conns.append(conn_info)
        return list(neurons), neuron_conns

    def read_muscle_data(self):
        return self.get_neuron_to_muscle_conns()

    def get_neuron_to_muscle_conns(self):
        neurons = set([])
        muscles = set([])
        conns = []

        for conn_info in self.connection_infos:
            if is_neuron(conn_info.pre_cell) and is_muscle(conn_info.post_cell):
                neurons.add(conn_info.pre_cell)
                muscles.add(conn_info.post_cell)
                conns.append(conn_info)

        return list(neurons), list(muscles), conns

    def get_connections_from(self, node, synclass, ordered_by_weight=False):
        if synclass not in self.connections:
            return {}
        conn_array = self.connections[synclass]
        if node not in self.nodes:
            return {}
        index = self.nodes.index(node)
        slice = conn_array[index]
        conns = {}
        for idn, n in enumerate(self.nodes):
            weight = slice[idn]
            if weight != 0:
                conns[n] = weight
        if ordered_by_weight:
            conns = dict(sorted(conns.items(), key=lambda item: item[1], reverse=True))
        return conns

    def get_connections_summary(self, node, synclass, direction, bold_cells=False):
        if direction == "from":
            conns = self.get_connections_from(node, synclass)
        elif direction == "to":
            conns = self.get_connections_to(node, synclass)

        ordered = dict(
            sorted(conns.items(), key=lambda key_val: key_val[1], reverse=True)
        )
        vals = [
            "%s: %s"
            % (
                k if not bold_cells else "<b>%s</b>" % k,
                int(v) if v == int(v) else v,
            )
            for k, v in ordered.items()
        ]
        info = ""
        for v in vals:
            if len(info.split("<br>")[-1]) > 80:
                info += "<br>"
            info += v + ", "

        return info[:-2]

    def get_connections_to(self, node, synclass, ordered_by_weight=False):
        if synclass not in self.connections:
            return {}
        conn_array = self.connections[synclass]
        if node not in self.nodes:
            return {}
        index = self.nodes.index(node)
        slice = conn_array.T[index]
        conns = {}
        for idn, n in enumerate(self.nodes):
            weight = slice[idn]
            if weight != 0:
                conns[n] = weight
        if ordered_by_weight:
            conns = dict(sorted(conns.items(), key=lambda item: item[1], reverse=True))
        return conns

    def get_connectome_view(self, view):
        self.view = view

        cv = ConnectomeDataset()

        for n in view.node_sets:
            if view.only_show_existing_nodes:
                if n.name in self.nodes:
                    cv.nodes.append(n.name)
            else:
                cv.nodes.append(n.name)

        if self.verbose:
            print_(
                "-- Creating view (%s, only_show_existing_nodes=%s) with %i nodes: %s\n  My %i nodes: %s"
                % (
                    view.name,
                    view.only_show_existing_nodes,
                    len(cv.nodes),
                    sorted(cv.nodes),
                    len(self.nodes),
                    sorted(self.nodes),
                )
            )

        for synclass_set in view.synclass_sets:
            cv.connections[synclass_set] = np.zeros(
                [len(cv.nodes)] * 2, dtype=self.DEFAULT_DTYPE
            )

            for synclass in view.synclass_sets[synclass_set]:
                if synclass in self.connections:
                    conn_array = self.connections[synclass]
                    for pre in self.nodes:
                        pre_index = (
                            cv.nodes.index(pre)
                            if view.only_show_existing_nodes
                            else view.get_index_of_cell(pre)
                        )
                        for post in self.nodes:
                            post_index = (
                                cv.nodes.index(post)
                                if view.only_show_existing_nodes
                                else view.get_index_of_cell(post)
                            )

                            if self.verbose and False:
                                print_(
                                    "-- Testing if %s (%i), %s (%s) in my %i node sets %s..."
                                    % (
                                        pre,
                                        pre_index,
                                        post,
                                        post_index,
                                        len(view.node_sets),
                                        view.node_sets[:5],
                                    )
                                )

                            if pre_index >= 0 and post_index >= 0:
                                cv.connections[synclass_set][pre_index, post_index] += (
                                    conn_array[
                                        self.nodes.index(pre), self.nodes.index(post)
                                    ]
                                )

        return cv

    def summary(self):
        info = "Nodes present: %s\n" % self.nodes
        for c in self.connections:
            conn_array = self.connections[c]
            info += (
                "- Connection type - %s: %s, %i non-zero entries, %i total\n%s\n"
                % (
                    c,
                    conn_array.shape,
                    np.count_nonzero(conn_array),
                    np.sum(conn_array),
                    conn_array,
                )
            )
        return info

    def to_plotly_matrix_fig(self, synclass, view, color_continuous_scale=None):
        import plotly.express as px

        conn_array = self.connections[synclass]

        zmin = np.min(conn_array)
        zmax = np.max(conn_array)
        color_continuous_scale = DEFAULT_COLORMAP

        if synclass == "Functional":
            color_continuous_scale = POS_NEG_COLORMAP
            largest = max(abs(zmin), abs(zmax))
            zmin = -1 * largest
            zmax = largest

        def get_color_html(color, node):
            return f'<span style="color:{color};">{node}</span>'

        node_colors = [
            (
                view.get_node_set(node).color
                if view.has_color()
                else get_standard_color(node)
            )
            for node in self.nodes
        ]

        x_ticktext = [
            get_color_html(color, node) for node, color in zip(self.nodes, node_colors)
        ]
        y_ticktext = [
            get_color_html(color, node) for node, color in zip(self.nodes, node_colors)
        ]

        fig = px.imshow(
            conn_array,
            labels=dict(x="Postsynaptic", y="Presynaptic", color="Weight"),
            x=x_ticktext,
            y=y_ticktext,
            color_continuous_scale=color_continuous_scale,
            zmin=zmin,
            zmax=zmax,
        )

        fig.update(
            data=[
                {
                    "hovertemplate": "<b>%{y}</b> -> <b>%{x}</b>: <b>%{z}</b><extra></extra> "
                }
            ]
        )
        fig.update_layout(
            margin=dict(l=2, r=2, t=2, b=2),
        )

        return fig

    def to_plotly_graph_fig(self, synclass, view):
        conn_array = self.connections[synclass]

        verbose = False

        print_("==============")
        print_(
            f"Generating: {synclass} for {view.name}, {view.synclass_sets[synclass]}"
        )

        DEFAULT_NODE_SIZE = 15

        def get_node_size(node_set):
            if node_set.size is not None:
                return node_set.size
            return DEFAULT_NODE_SIZE * math.sqrt(len(node_set.cells))

        import plotly.graph_objects as go
        import networkx as nx

        gap_junction = synclass == "Electrical" or "All" in synclass

        G = nx.Graph(conn_array)
        pos = nx.spring_layout(G, seed=1)

        for i, node_value in enumerate(self.nodes):
            node_set = view.get_node_set(node_value)
            if node_set.position is not None:
                pos[i] = node_set.position

        node_x = [float("{:.6f}".format(pos[i][0])) for i in G.nodes()]
        node_y = [float("{:.6f}".format(pos[i][1])) for i in G.nodes()]

        edge_traces = []

        for edge in G.edges():
            dirs = [[edge[0], edge[1]], [edge[1], edge[0]]]
            for dir_ in dirs:
                edge_x = []
                edge_y = []
                from_node_set = view.get_node_set(self.nodes[dir_[0]])

                conn_weight = conn_array[dir_[0], dir_[1]]
                weight = min(10, math.sqrt(abs(conn_weight)))
                opposite_dir_weight = math.sqrt(abs(conn_array[dir_[1], dir_[0]]))

                straight = edge[0] != edge[1] and (
                    gap_junction or opposite_dir_weight == 0
                )  # i.e. connections in both dirs, so add a curve...

                if weight > 0:
                    x0, y0 = (float("{:.6f}".format(a)) for a in pos[dir_[0]])
                    x1, y1 = (float("{:.6f}".format(a)) for a in pos[dir_[1]])

                    edge_x.append(x0)
                    edge_y.append(y0)

                    if x0 != x1 or y0 != y1:
                        if verbose:
                            print_(f" - Different points ({x0},{y0}) -> ({x1},{y1})")
                        if not straight:
                            if verbose:
                                print_(" - 2 way connections")
                            # L = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)  # length
                            offset = 0.2
                            edge_x.append(((x0 + x1) / 2) + offset * (y0 - y1))
                            edge_y.append(((y0 + y1) / 2) + offset * (x1 - x0))
                    else:
                        if verbose:
                            print_(
                                f" - Same point ({x0},{y0}) -> ({x1},{y1})   {x0 != x1} and {y0 != y1}"
                            )
                        circle_offset_a = get_node_size(from_node_set) / 100

                        edge_x.append(x0 - circle_offset_a)
                        edge_y.append(y0 + circle_offset_a / 3)
                        edge_x.append(x0 - circle_offset_a / 3)
                        edge_y.append(y0 + circle_offset_a)

                    edge_x.append(x1)
                    edge_y.append(y1)
                    # edge_x.append(None)
                    # edge_y.append(None)

                    if verbose:
                        print_(
                            f"Node {dir_[0]} ({x0},{y0}) -> node {dir_[1]} ({x1},{y1}), weight: {weight} (from {conn_weight}), opp weight: {opposite_dir_weight}, gj: {gap_junction}, xs: {edge_x}, ys: {edge_y}"
                        )
                    line_color = "grey"
                    if gap_junction:
                        line_color = "#ff6f6f "
                    elif from_node_set.color is not None:
                        line_color = from_node_set.color

                    # Add edges to the figure
                    edge_trace = go.Scatter(
                        x=edge_x,
                        y=edge_y,
                        mode="lines",
                        # marker=dict(symbol="arrow",size=weight * 3,angleref="previous",     ),
                        line=dict(
                            color=line_color,
                            width=weight,
                        ),
                        hoverinfo="none",
                        line_shape="spline" if not straight else "linear",
                    )
                    edge_traces.append(edge_trace)

        node_adjacencies = []
        node_colours = []
        node_font_colors = {}
        node_text = []
        node_sizes = []
        node_shapes = []

        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            if not view.has_color():
                node_colours.append(len(adjacencies[1]))

        add_text = False

        for i, node_value in enumerate(self.nodes):
            # num_connections = node_adjacencies[i]

            node_set = view.get_node_set(node_value)

            if view.has_color():
                node_colours.append(node_set.color)

                if "#" in node_set.color:
                    h = node_set.color[1:]
                    rgb = tuple((int(h[i : i + 2], 16) / 256) for i in (0, 2, 4))
                else:
                    import webcolors

                    rgb = webcolors.name_to_rgb(node_set.color)

                # https://stackoverflow.com/questions/3942878
                if (
                    float(rgb[0]) * 0.299 + float(rgb[1]) * 0.587 + float(rgb[2]) * 0.2
                ) > 0.35:
                    fcolor = "#000000"
                else:
                    fcolor = "#ffffff"
                node_font_colors[node_value] = fcolor
                if verbose:
                    print_(
                        f"For node {node_value}, with color {node_set.color} ({rgb}), using color {fcolor} for optional text"
                    )

            node_sizes.append(get_node_size(node_set))

            if node_set.shape is not None:
                node_shapes.append(node_set.shape)
                add_text = True
            else:
                node_shapes.append("circle")

            if node_set.is_one_cell():
                desc = get_short_description(node_set.name)
            else:
                desc = "Cells: "
                cc = 0
                for c in node_set.cells:
                    if cc % 10 == 9:
                        desc += c + "<br>"
                    desc += c + ", "
                    cc += 1
                desc = desc[:-2]

            text = f"<b>{node_value}</b>"
            text += "<br>%s" % desc

            into = self.get_connections_summary(
                node_value, synclass, "to", bold_cells=True
            )
            if len(into) > 0:
                text += f"<br>Conns in: {into}"

            out_of = self.get_connections_summary(
                node_value, synclass, "from", bold_cells=True
            )
            if len(out_of) > 0:
                text += f"<br>Conns out: {out_of}"

            node_text.append(text)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text" if add_text else "markers",
            text=[
                '<span style="color:%s;font-size:1.0em"><b>%s</b></span>'
                % (node_font_colors[n] if n in node_font_colors else "black", n)
                for n in self.nodes
            ],
            marker=dict(
                showscale=not view.has_color(),
                colorscale="YlGnBu",
                reversescale=True,
                color=[],
                size=DEFAULT_NODE_SIZE,
                colorbar=dict(
                    thickness=15,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right",
                ),
                line_width=1,
            ),
            opacity=1,
            hoverinfo="text",
        )

        node_trace.marker.size = node_sizes
        node_trace.marker.symbol = node_shapes
        node_trace.marker.color = node_colours
        node_trace.hovertext = node_text

        fig = go.Figure(
            data=edge_traces + [node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False),
                width=800,
                height=800,
            ),
        )
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        fig.update_traces(textposition="middle center")

        fig.update_layout(
            template="plotly_white",
        )

        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)

        return fig

    def to_plotly_hive_plot_fig(self, synclass, view):
        from hiveplotlib import hive_plot_n_axes
        from hiveplotlib.converters import networkx_to_nodes_edges
        from hiveplotlib.node import split_nodes_on_variable
        from hiveplotlib.viz.plotly import hive_plot_viz as plotly_hive_plot_viz

        print_("==============")
        print_(f"Generating: {synclass} for {view}")

        verbose = False
        # print(self.summary())
        cv = self

        G = cv.to_networkx_graph(synclass)

        nids = [n for n in G.nodes]

        for n_id in nids:
            node = G.nodes[n_id]
            if node["SIM_class"] == "Other":
                G.remove_node(n_id)

        if len(G.nodes) == 0:
            return None

        nodes, edges = networkx_to_nodes_edges(G)

        blocks_dict_unordered = split_nodes_on_variable(
            nodes, variable_name="SIM_class"
        )

        if verbose:
            print_(nodes)
            print_(edges)
            print_(pprint.pprint(nx.node_link_data(G)))

            print_(
                "Unordered: %s (%s)"
                % (blocks_dict_unordered, type(blocks_dict_unordered))
            )

        INTERNEURON = "Interneuron"
        MOTORNEURON = "Motorneuron"
        SENSORY = "Sensory"

        blocks_dict = {}
        for k in [INTERNEURON, MOTORNEURON, SENSORY]:
            if k not in blocks_dict_unordered:
                blocks_dict[k] = []
            else:
                blocks_dict[k] = blocks_dict_unordered[k]

        splits = list(blocks_dict.values())

        # pull out degree information from nodes
        degrees = dict(G.degree)
        in_degrees = dict(G.in_degree)
        out_degrees = dict(G.out_degree)

        # add degree information to Node instances
        for node in nodes:
            deg = degrees[node.unique_id]
            block = node.data["SIM_class"]
            node.add_data(data={"degree": deg})

            if verbose:
                print_(
                    f" - Node {node.unique_id}, block {block} has degree {deg}; {node.data}"
                )

        num_steps_for_edge_curves = 25

        hp = hive_plot_n_axes(
            node_list=nodes,
            edges=edges,
            axes_assignments=splits,
            sorting_variables=["degree"] * 3,
            repeat_axes=[True, True, True],
            repeat_edge_kwargs={
                "color": "grey",
                "num_steps": num_steps_for_edge_curves,
            },
            cw_edge_kwargs={"num_steps": num_steps_for_edge_curves},
            ccw_edge_kwargs={"num_steps": num_steps_for_edge_curves},
            vmins=[0] * 3,
            vmaxes=[max(degrees.values())] * 3,
        )

        for ax in hp.axes:
            if "1" in ax:
                hp.axes[ax].long_name = INTERNEURON
            if "2" in ax:
                hp.axes[ax].long_name = MOTORNEURON
            if "3" in ax:
                hp.axes[ax].long_name = SENSORY

        for ax_name in hp.axes:
            ax = hp.axes[ax_name]
            if verbose:
                print_(f" - Axis {ax.long_name}, {ax.start}->{ax.end}...")

        from cect.WormAtlasInfo import WA_COLORS

        INTERNEURON_COLOR = WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["interneuron"]
        SENSORY_COLOR = WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["sensory neuron"]
        MOTORNEURON_COLOR = WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["motor neuron"]

        hp.add_edge_kwargs(
            axis_id_1="Group 1_repeat",
            axis_id_2="Group 2",
            a2_to_a1=False,
            color=INTERNEURON_COLOR,
        )

        hp.add_edge_kwargs(
            axis_id_1="Group 2",
            axis_id_2="Group 1_repeat",
            a2_to_a1=False,
            color=MOTORNEURON_COLOR,
        )
        hp.add_edge_kwargs(
            axis_id_1="Group 1",
            axis_id_2="Group 3_repeat",
            a2_to_a1=False,
            color=INTERNEURON_COLOR,
        )
        hp.add_edge_kwargs(
            axis_id_1="Group 3_repeat",
            axis_id_2="Group 1",
            a2_to_a1=False,
            color=SENSORY_COLOR,
        )
        hp.add_edge_kwargs(
            axis_id_1="Group 3",
            axis_id_2="Group 2_repeat",
            a2_to_a1=False,
            color=SENSORY_COLOR,
        )
        hp.add_edge_kwargs(
            axis_id_1="Group 2_repeat",
            axis_id_2="Group 3",
            a2_to_a1=False,
            color=MOTORNEURON_COLOR,
        )

        fig = plotly_hive_plot_viz(
            hp,
            width=800,
            height=800,
        )
        # ax.set_title("Stochastic Block Model, Base Hive Plot Visualization", y=1.05, size=20)
        # fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="closest")

        fig.update_layout(
            template="plotly_white",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
        )

        fig.update_layout(
            margin=dict(l=2, r=2, t=2, b=2),
        )

        fig.update(data=[{"hoverinfo": "skip"}])

        # print(dir(fig))
        count = 0
        for d in fig.data:
            if d["mode"] == "text":
                if d["text"] == "Sensory" and d["textposition"] == "top center":
                    d["y"] = [-5.4]
                if d["text"] == "Motorneuron" and d["textposition"] == "bottom center":
                    d["y"] = [5.4]
                if d["text"] == "Interneuron":
                    if d["y"][0] > 0:
                        d["y"] = [2.6]
                    if d["y"][0] < 0:
                        d["y"] = [-2.6]
                # print("Moving text %s" % d)
            if d["mode"] == "markers":
                nrn_num = len(d["x"])
                d["hovertemplate"] = "%{text}<extra></extra>"
                d.pop("hoverinfo", None)

                if count == 0 or count == 1:
                    d["marker"]["color"] = [INTERNEURON_COLOR] * nrn_num
                    type_ = "Interneuron"
                if count == 2 or count == 3:
                    d["marker"]["color"] = [MOTORNEURON_COLOR] * nrn_num
                    type_ = "Motorneuron"
                if count == 4 or count == 5:
                    d["marker"]["color"] = [SENSORY_COLOR] * nrn_num
                    type_ = "Sensory"

                text_at_point = {}

                for n_index in range(len(blocks_dict[type_])):
                    n = blocks_dict[type_][n_index]
                    x = d["x"][n_index]
                    n_text = "%s (in: %s, out: %s)" % (n, in_degrees[n], out_degrees[n])
                    if x in text_at_point:
                        text_at_point[x] += "<br>%s" % n_text
                    else:
                        text_at_point[x] = n_text

                d["text"] = [text_at_point[x] for x in d["x"]]

                # print(d)
                count += 1

        return fig

    def connection_number_plot(self, synclass):  # Todo: get better name
        from cect.Cells import COOK_GROUPING_1
        from cect.Cells import get_standard_color
        from matplotlib import pyplot as plt

        for group in COOK_GROUPING_1:
            print_(" = Adding plot for %s" % group)
            xs = []
            ys = []
            labels = []
            colors = []
            markers = []
            fill_styles = []
            pre_cells = sorted(COOK_GROUPING_1[group])

            for pre_cell_index in range(len(pre_cells)):
                pre_cell = pre_cells[pre_cell_index]
                conns = self.get_connections_from(
                    pre_cell, synclass, ordered_by_weight=True
                )
                for post_cell in conns:
                    weight = conns[post_cell]
                    colors.append(get_standard_color(post_cell))
                    xs.append(pre_cell_index)
                    ys.append(weight)
                    labels.append(pre_cell)
                    if weight < 0:
                        fill_styles.append("none")
                    else:
                        fill_styles.append("full")

                    if are_bilateral_pair(pre_cell, post_cell):
                        markers.append("D")
                    elif is_bilateral_left(pre_cell):
                        markers.append(">")
                    elif is_bilateral_right(pre_cell):
                        markers.append("<")
                    else:
                        markers.append("o")

                    print_(
                        f"  Adding {pre_cell}->{post_cell} with weight {weight} ({markers[-1]})"
                    )

            if len(xs) > 0:
                fig, ax = plt.subplots()
                plt.title("Conns of type: %s from cells in: %s" % (synclass, group))

                for i in zip(labels, ys, colors, markers, fill_styles):
                    plt.plot(
                        i[0], i[1], linewidth=0, color=i[2], marker=i[3], fillstyle=i[4]
                    )

                plt.setp(
                    ax.get_xticklabels(),
                    rotation=90,
                    ha="center",
                    rotation_mode="default",
                )

                # ax.set_xticks(ticks=range(len(pre_cells)), labels=pre_cells)

        plt.show()


if __name__ == "__main__":
    cds = ConnectomeDataset()

    cds.add_connection_info(ConnectionInfo("VA6", "VD6", 6, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("VA6", "VD1", 1, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("VA6", "VD5", 5, "Send", "Acetylcholine"))

    cds.add_connection_info(ConnectionInfo("VB6", "DD4", 32, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("VA2", "VA6", 7, "Send", "Acetylcholine"))

    cds.add_connection_info(ConnectionInfo("AVFL", "AVHL", 2, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("AVFR", "AVHL", 3, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("AVFR", "AVHR", -3, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("AVFL", "VA6", 6, "Send", "Acetylcholine"))

    cds.add_connection_info(ConnectionInfo("DVA", "PVCL", 3, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("ASHR", "RMGR", 6, "Send", "Acetylcholine"))
    cds.add_connection_info(ConnectionInfo("AWBR", "ASHR", 2, "Send", "Acetylcholine"))

    cds.add_connection_info(ConnectionInfo("VD6", "VA6", 3, "Send", "GABA"))

    cds.add_connection_info(
        ConnectionInfo("ASHR", "ASKR", 1, "GapJunction", "Generic_GJ")
    )

    print(cds.summary())

    synclass = "Acetylcholine"

    print(cds.get_connections_from("VA6", synclass))
    print("From: %s" % cds.get_connections_summary("VA6", synclass, "from"))
    print("To: %s" % cds.get_connections_summary("VA6", synclass, "to"))
    print(cds.get_connections_to("DD4", synclass))

    """
    if "-nogui" not in sys.argv:
        cds.connection_number_plot("Acetylcholine")"""

    G = cds.to_networkx_graph(synclass)
    import pprint

    print(pprint.pprint(nx.node_link_data(G)))

    from cect.ConnectomeView import RAW_VIEW as view
    # from cect.ConnectomeView import SOCIAL_VIEW as view
    # from cect.ConnectomeView import COOK_FIG3_VIEW as view

    cds2 = cds.get_connectome_view(view)

    print(cds2.summary())

    fig = cds2.to_plotly_hive_plot_fig(list(view.synclass_sets.keys())[0], view)

    # fig = cds2.to_plotly_graph_fig(list(view.synclass_sets.keys())[0], view)
    # fig = cds2.to_plotly_matrix_fig(list(view.synclass_sets.keys())[0], view)

    import plotly.io as pio

    pio.renderers.default = "browser"
    if "-nogui" not in sys.argv:
        fig.show()
