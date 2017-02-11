from chess import *
from chess.pgn import *
from networkx import *
from networkx.drawing.nx_agraph import *

class CommonPosition():
    """
    Fen of some of the thematic games
    """
    SCHLIEMANN_LABEL = "Schliemann"
    SCHLIEMANN = "r1bqkbnr/pppp2pp/2n5/1B2pp2/4P3/5N2/PPPP1PPP/RNBQK2R"
    ITALIAN_LABEL = "Italian"
    ITALIAN = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R"
    DANISH_LABEL = "Danish gambit"
    DANISH = "rnbqkbnr/pppp1ppp/8/8/3pP3/2P5/PP3PPP/RNBQKBNR"
    E4_LABEL = "e4"
    E4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
    PIRC_LABEL = "Pirc"
    PIRC = "rnbqkb1r/ppp1pppp/3p1n2/8/3PP3/8/PPP2PPP/RNBQKBNR"
    SPANISH_LABEL = "Spanish"
    SPANISH = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R"
    CENTER_LABEL = "Center game"
    CENTER = "rnbqkbnr/pppp1ppp/8/8/3pP3/8/PPP2PPP/RNBQKBNR"
    KINGINDIAN_LABEL = "King Indian"
    KINGINDIAN = "rnbqk2r/ppp1ppbp/3p1np1/8/2PPP3/2N5/PP3PPP/R1BQKBNR"
    EVANS_LABEL = "Evans gambit"
    EVANS = "r1bqk1nr/pppp1ppp/2n5/2b1p3/1PB1P3/5N2/P1PP1PPP/RNBQK2R"
    TWO_KNIGHTS_LABEL = "Two Knights Defence"
    TWO_KNIGHTS = "r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R"
    MAXLANGE_LABEL = "Max Lange"
    MAXLANGE =  "r1bqk2r/pppp1ppp/2n2n2/2b5/2BpP3/5N2/PPP2PPP/RNBQ1RK1"
    GRANDPRIX_LABEL = "Grand Prix"
    GRANDPRIX = "r1bqkbnr/pp1ppppp/2n5/2p5/4PP2/2N5/PPPP2PP/R1BQKBNR"
    SCOTCH_LABEL = "Scotch"
    SCOTCH = "r1bqkbnr/pppp1ppp/2n5/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R"
    TROMPOWSKY_LABEL = "Trompowsky"
    TROMPOWSKY = "rnbqkb1r/pppppppp/5n2/6B1/3P4/8/PPP1PPPP/RN1QKBNR"

class ConvertToGraph(BaseVisitor, CommonPosition):
    """
    Convert pgn to graph
    """

    def __init__(self):
        self.graph = networkx.DiGraph()
        self.game = Game()
        self.previous = None

    def visit_header(self, tagname, tagvalue):
        self.game.headers[tagname] = tagvalue

    def visit_move(self, board, move):
        """
        Called for each move.

        *board* is the board state before the move. The board state must be
        restored before the traversal continues.
        """
        if "Variant" in self.game.headers:
            return
        if len(board.move_stack) < 10:
            fen = board.fen()
            position = fen.split(' ')[0]
            label = "?"
            if (self.previous is not None):
                last_move = board.peek()
                board.pop()
                label = board.san(last_move)
                board.push(last_move)
                self.graph.add_edge(self.previous, position)
            if position == chess.STARTING_FEN.split(' ')[0]:
                label = "Starting position"
            elif position == self.SCHLIEMANN:
                label = self.SCHLIEMANN_LABEL
            elif position == self.ITALIAN:
                label = self.ITALIAN_LABEL
            elif position == self.DANISH:
                label = self.DANISH_LABEL
            elif position == self.E4:
                label = self.E4_LABEL
            elif position == self.PIRC:
                label = self.PIRC_LABEL
            elif position == self.SPANISH:
                label = self.SPANISH_LABEL
            elif position == self.CENTER:
                label = self.CENTER_LABEL
            elif position == self.KINGINDIAN:
                label = self.KINGINDIAN_LABEL
            elif position == self.EVANS:
                label = self.EVANS_LABEL
            elif position == self.TWO_KNIGHTS:
                label = self.TWO_KNIGHTS_LABEL
            elif position == self.MAXLANGE:
                label = self.MAXLANGE_LABEL
            elif position == self.GRANDPRIX:
                label = self.GRANDPRIX_LABEL
            elif position == self.SCOTCH:
                label = self.SCOTCH_LABEL
            elif position == self.TROMPOWSKY:
                label = self.TROMPOWSKY_LABEL

            self.graph.add_node(position, label=label)
            self.previous = position

    def result(self):
        """Called to get the result of the visitor. Defaults to ``True``."""
        return self.graph

pgn = file("./games/extract/white.pgn")
fullGraph = networkx.DiGraph()

while (True):
    gameGraph = chess.pgn.read_game(pgn, Visitor=ConvertToGraph)
    if (gameGraph is None):
        break
    fullGraph = networkx.compose(fullGraph, gameGraph)

A = networkx.drawing.nx_agraph.to_agraph(fullGraph)
A.graph_attr.update(rankdir='LR')
A.layout(prog='dot')
A.draw('test.png')
