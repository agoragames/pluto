
from chai import Chai
from pluto.node import Node

class NodeTest(Chai):

  def setUp(self):
    super(NodeTest,self).setUp()
    Node.backend = {}
    Node.backend.drop()

  def test_node_can_save(self):
    n = Node()
    n.save()

  def test_node_can_be_found(self):
    assert_equals( [], list(Node.find()) )
    n = Node()
    n.save()
    assert_equals( 1, len(list(n.find())) )

  def test_node_loads_the_right_class(self):
    class ClassLoadTest(Node): pass

    Node({'type':'ClassLoadTest'}).save()
    print list(n.find())
