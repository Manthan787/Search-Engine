from HW4.config import GRAPH_PATH
graph = {}


def GraphFromFile():
    global graph
    g = parse_file()
    for node in g:
        outlinks = list(set(g[node][0]))
        inlinks = list(set(g[node][1]))
        g[node] = (outlinks, inlinks)

    return g


def parse_file():
    with open(GRAPH_PATH, 'r') as f:
        lines = f.readlines()

        for line in lines:
            nodes = line.split()
            node = nodes[0].strip()
            inlinks = nodes[1:]
            graph.setdefault(node, [[],[]])

            for inlink in inlinks:
                graph[node][1].append(inlink)
                graph.setdefault(inlink, [[], []])
                graph[inlink][0].append(node)

        return graph