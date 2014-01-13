
from chai import Chai
from pluto.node import Node

class ScheduleTest(Node):
  def run(self):
    print 'run schedule test'

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

  def test_find_loads_the_right_class(self):
    class ClassLoadTest(Node): pass

    node = Node({'type':'ClassLoadTest', 'foo':'bar'}).save()
    res = list(Node.find())
    assert_equals( 1, len(res) )
    assert_equals( node.id, res[0].id )
    assert_true( isinstance(res[0], ClassLoadTest) )

    node = ClassLoadTest().save()
    res = list(Node.find())
    assert_equals( 2, len(res) )
    assert_equals( node.id, res[1].id )
    assert_true( isinstance(res[1], ClassLoadTest) )

  def test_schedule(self):
    node = ScheduleTest().save()
    node.schedule()
