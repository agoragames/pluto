
from chai import Chai
from pluto import node
from pluto.node import Node

class NodeTest(Chai):

  def setUp(self):
    super(NodeTest, self).setUp()
    self.start_types = node.__node_types__.copy()

  def tearDown(self):
    super(NodeTest, self).tearDown()
    node.__node_types__ = self.start_types

  def test_nodes_register(self):
    class TestNode(Node):
      pass

    assert_true( 'TestNode' in node.__node_types__.keys() )
    assert_true( TestNode is node.__node_types__['TestNode'] )
    assert_true( isinstance(Node({'type':'TestNode'}), TestNode) )

  def test_node_base_class_doesnt_register(self):
    assert_false( 'Node' in node.__node_types__ )

  def test_cant_init_unknown_input_type(self):
    with assert_raises( ImportError ):
      Node({'type':'whyunonode'})
