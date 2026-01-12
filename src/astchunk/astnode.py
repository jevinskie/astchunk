import tree_sitter as ts

from astchunk.preprocessing import ByteRange
from rich.repr import RichReprResult
from rich.syntax import Syntax
from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text


class ASTNode():
    """
    A wrapper class for tree-sitter node.

    This class provides additional information for each node, including:
        - node_size: size of the node (in non-whitespace characters)
        - ancestors: ancestors of the node (list of tree-sitter nodes)

    Attributes:
        - node: tree-sitter node
        - node_size: size of the node (in non-whitespace characters)
        - ancestors: ancestors of the node (list of tree-sitter nodes)
    """
    def __init__(self, ts_node: ts.Node, node_size: int, ancestors: list[ts.Node] = []):
        self.node = ts_node
        self.node_size = node_size
        self.ancestors = ancestors

    @property
    def bcode(self):
        return self.node.text
    
    @property
    def strcode(self):
        assert self.bcode is not None
        return self.bcode.decode("utf8")
    
    @property
    def brange(self):
        return ByteRange(self.node.start_byte, self.node.end_byte)
    
    @property
    def start_line(self):
        return self.node.start_point.row
    
    @property
    def end_line(self):
        return self.node.end_point.row
    
    @property
    def start_col(self):
        return self.node.start_point.column
    
    @property
    def end_col(self):
        return self.node.end_point.column
    
    @property
    def size(self):
        """
        Define size as the number of non-whitespace characters
        """
        return self.node_size

    @property
    def length(self):
        """
        Define length as the number of lines covered by the node
        """
        return self.end_line - self.start_line + 1

    # def __rich_repr__(self) -> RichReprResult:
    #     yield "Node", self.node
    #     syntax = Syntax(self.strcode, "c").highlight(self.strcode)
    #     yield "Code", syntax.markup
    #     yield "NodeSize", self.node_size
    #     yield "Ancestors", self.ancestors

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Node:[/b] #{self.node}"
        syntax = Syntax(self.strcode, "c", background_color="default").highlight(self.strcode)
        yield syntax
        yield f"[b]NodeSize:[/b] #{self.node_size}"
        yield f"[b]Ancestors:[/b] #{self.ancestors}"