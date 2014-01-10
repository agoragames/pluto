
from chai import Chai
from pluto.input import input
from pluto.input import Input

class InputTest(Chai):

  def setUp(self):
    super(InputTest, self).setUp()
    self.start_types = input.__input_types__.copy()

  def tearDown(self):
    super(InputTest, self).tearDown()
    input.__input_types__ = self.start_types

  def test_inputs_register(self):
    class TestInput(Input):
      pass

    assert_true( 'TestInput' in input.__input_types__.keys() )
    assert_true( TestInput is input.__input_types__['TestInput'] )
    assert_true( isinstance(Input({'type':'TestInput'}), TestInput) )

  def test_input_base_class_doesnt_register(self):
    assert_false( 'Input' in input.__input_types__ )

  def test_cant_init_unknown_input_type(self):
    with assert_raises( ImportError ):
      Input({'type':'nomysql'})
