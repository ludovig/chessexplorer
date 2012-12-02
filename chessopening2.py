from chess import *
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
file_pgn = file("./../openings/white")

# Retrieve games
games = GamesLines()
games.import_pgn(file_pgn)

# Build tree
graph = nx.DiGraph()
for game in games.games:
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

for fen in graph.nodes():
    del graph.node[fen]["games"]
nx.write_dot(graph, 'graph.txt')
