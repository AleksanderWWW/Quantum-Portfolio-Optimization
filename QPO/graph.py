import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from QPO.assets import PreparedData


class GraphBuilder(PreparedData):

    def __init__(self, in_data_frame: pd.DataFrame):
        super().__init__(in_data_frame)
        self.G = nx.Graph()
        self.chosen_sub_graph = None
        self.not_chosen_sub_graph = None
        self.considered = set()
        self.not_considered = set()  # tickers that don't have above-threshold corr with any of other assets

    def check_for_not_considered(self):
        asset_set = set(asset for asset in self.df.columns)
        self.not_considered = asset_set - self.considered
        return self.not_considered

    def build_nodes(self, corr_threshold):
        assets = self.df.columns
        nodes = []
        for i in assets:
            for j in assets:
                if i != j:
                    corr = self.corr_matrix.loc[i, j]
                    if corr >= corr_threshold:  # łączymy węzły, jeśli ich korelacja przekracza próg
                        pair = (i, j)
                        self.considered.add(i)
                        self.considered.add(j)
                        if (j, i) not in nodes:
                            nodes.append(pair)
        return nodes

    def build_graph(self, nodes):
        self.G.add_edges_from(nodes)
        return self

    def color_graph(self, chosen):
        not_chosen = list(set(self.G.nodes()) - set(chosen))
        self.not_chosen_sub_graph = self.G.subgraph(not_chosen)
        self.chosen_sub_graph = self.G.subgraph(chosen)

        return self

    def show_graph(self):
        pos = nx.spring_layout(self.G)
        plt.figure()
        nx.draw(self.G, pos=pos)
        nx.draw(self.chosen_sub_graph, pos=pos, node_color="yellow")
        nx.draw(self.not_chosen_sub_graph, pos=pos, node_color="black")
        plt.show()


