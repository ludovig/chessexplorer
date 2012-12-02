import networkx as nx
import re

label_re = re.compile("r/label/")
dot_graph = open("graph.txt");
sorted_dot_graph = open("sorted_graph.txt", 'w');
move_lines = []
edge_lines = []
count = 0
for line in dot_graph:
    count = count + 1
    if (count <= 2) :
        sorted_dot_graph.write(line)
    else:
        #line = line.strip()
        if re.match(r'.*label.*', line) is not None:
            move_lines.append(line)
        else:
            edge_lines.append(line)

def getlabel(line):
    splited = line.split("=");
    label = splited[1]
    label = re.sub(r'[\W]', '', label)
    return label

move_lines.sort(key= lambda line : getlabel(line))
for line in move_lines:
    sorted_dot_graph.write(line)
    #print getlabel(line)
for line in edge_lines:
    sorted_dot_graph.write(line)

sorted_dot_graph.close()
graph = nx.read_dot('sorted_graph.txt')
#print nx.graphviz_layout(graph)
# Draw a nice graph
A = nx.to_agraph(graph)
A.graph_attr.update(rankdir='LR')
A.layout(prog='dot')
A.draw('test.png')
#A.draw('test2.png')
