import os
import re
from pyvis.network import Network
import networkx as nx
import urllib.parse


class MDG:
    def get_all_files_from(self, path: str, type: str = '.md'):
        """
        Traverses through all subfolders of path and returns a list of all files, together with their paths and links to other sites
        :param path: The base path (root directory)
        :param type: File extenstion. E.g. '.md'
        :return: List of alle files, together with their paths and links
        """
        files = []
        for root, directories, file in os.walk(path):
            for file in file:
                if (file.endswith(type)):
                    files.append(
                        ({
                            "path": root,
                            "filename": file,
                            "links": self._extract_links_from(file, root)
                        })
                    )
        return files

    def _extract_links_from(self, file: str, path: str, delim: str = "/") -> list[dict]:
        """Returns dict of wiki-style links in markdown file"""
        f = open(path + "/" + file)
        lines = f.read()
        WIKISTYLE_LINK = re.compile(r'\[\[(.*)\]\]')
        links = list(WIKISTYLE_LINK.findall(lines))
        link_list = []
        for link in links:
            parts = link.split(delim)
            path = ''
            if len(parts) > 1:
                path = delim.join(parts[:-1])
                file_name = parts[-1]
                link_list.append({"path": path, "filename": file_name})
        return link_list

    def create_graph_from_directory(self, dir: str):
        G = nx.DiGraph()
        all_files_with_links = self.get_all_files_from(dir)
        for file in all_files_with_links:
            file_name = os.path.splitext(file["filename"])[0]
            # file_path = file["path"]
            index_of_first_delim = file["path"].find("/")
            file_path = file["path"][index_of_first_delim + 1:]
            node_id = file_path + "/" + file_name
            links = file["links"]
            G.add_node(node_id, label=file_name)
            print("Node: " + node_id)
            for link in links:
                target_node_id = link["path"] + "/" + link["filename"]
                G.add_node(target_node_id, label=link['filename'])
                G.add_edge(node_id, target_node_id)
                print("Link:" + target_node_id)
        return G

#   def run():
#      dir = "Vault/👨🏻‍🏫 Unterricht"
#     G = create_graph_from_directory(dir)

#  G.add_nodes_from(links)

# äG.add_weighted_edges_from(edges)

#    nt = Network('1000px', '1000px', directed=True)
# populates the nodes and edges data structures
#   nt.from_nx(G)
#  nt.show_buttons(filter_=['physics'])
# nt.show('nx.html')
