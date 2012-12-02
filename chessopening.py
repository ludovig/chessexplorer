from chess import *
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
file_pgn = file("./chess_com_games_(4106370)-2012_09_18_9_21_am.pgn")
#file_pgn = file("./testpgn.pgn")

# Retrieve games
games = Games()
games.import_pgn(file_pgn)

# Build tree
graph = nx.DiGraph()
for game in games.games:
    print game.tags["White"]
    if not "Variant" in game.tags:
        if game.tags["White"] != "WhiteDragoon":
        #if game.tags["White"] == "WhiteDragoon":
            game.setup()
            fen = None
            for i in range(min(len(game.moves), 20)):
                move=game.moves[i]
                label=move.san(game.board)
                game.board.do_move(move);
                previous_fen = fen
                fen = game.board.fen()
                if not graph.has_node(fen):
                    graph.add_node(fen, games=[game], label=label)
                    if (i > 0):
                        graph.add_edge(previous_fen, fen)
                else:
                    graph.node[fen]['games'].append(game)
                    if (i > 0):
                        graph.add_edge(previous_fen, fen)

# Remove single branches
last_branches = []
def get_last_branches(nodes):
    end = False
    for fen in nodes:
        nb_games = len(graph.node[fen]['games'])
        if nb_games > 1:
            #if len(last_branches) > 0:
            #    last_branches.pop()
            end = True
            continue
        else:
            end = get_last_branches(graph.predecessors(fen))
            if not end:
                last_branches.append(fen)
            end = False

    return end

leaves=[n for n, d in graph.out_degree_iter() if 0==d]
get_last_branches(leaves)
for fen in last_branches:
    graph.remove_node(fen)

for fen in graph.nodes():
    del graph.node[fen]["games"]
nx.write_dot(graph, 'graph.txt')
#print nx.graphviz_layout(graph)
# Draw a nice graph
#A = nx.to_agraph(graph)
#A.graph_attr.update(rankdir='LR')
#A.layout(prog='dot')
#A.draw('test.png')
#A.draw('test2.png')
