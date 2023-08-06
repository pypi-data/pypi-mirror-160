from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import Bytecode
from gremlin_python.process.graph_traversal import __ as AnonymousTraversal
from gremlin_python.process.graph_traversal import GraphTraversal
from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.process.strategies import *


def get_db_endpoint():
    """Provide the local connection URL"""
    return "ws://localhost:8182/gremlin"


class SocialTraversal(GraphTraversal):
    """
    Adds the domain level methods for the social graph.

    The goal here is to move from Gremlin language to a vocabulary
    with domain concepts.
    """

    def knows(self, person_name):
        return self.out("knows").has_label("person").has("name", person_name)

    def youngest_friends_age(self):
        return self.out("knows").has_label("person").values("age").min()

    def created_at_least(self, number):
        return self.out_e("created").count().is_(P.gte(number))


class __(AnonymousTraversal):
    """This class is simply necessary for getting anonymous traversals to work."""

    graph_traversal = SocialTraversal

    # Class methods only have access to the class, not class instance
    @classmethod
    def knows(cls, *args):
        # Simply passes what is recieves to the social traversal
        # Args here are graph, traversal strategy, and the bytecode
        return cls.graph_traversal(None, None, Bytecode()).knows(*args)

    @classmethod
    def youngest_friends_age(cls, *args):
        return cls.graph_traversal(None, None, Bytecode()).youngest_friends_age(*args)

    @classmethod
    def created_at_least(cls, *args):
        return cls.graph_traversal(None, None, Bytecode()).created_at_least(*args)


class SocialTraversalSource(GraphTraversalSource):
    """
    Extend graph source for the social graph.

    Uses to the main graph source constructor,
    and then as a place to add functions for retrieving
    basic properties like people in the graph.
    """

    def __init__(self, *args, **kwargs):
        super(SocialTraversalSource, self).__init__(*args, **kwargs)
        self.graph_traversal = SocialTraversal

    def persons(self, *args):
        traversal = self.get_graph_traversal()
        traversal.bytecode.add_step("V")
        traversal.bytecode.add_step("hasLabel", "person")

        if len(args) > 0:
            traversal.bytecode.add_step("has", "name", P.within(args))

        return traversal
