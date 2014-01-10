
from chai import Chai
from pluto.output import output
from pluto.output import Output

class OutputTest(Chai):

  def setUp(self):
    super(OutputTest, self).setUp()
    self.start_types = output.__output_types__.copy()

  def tearDown(self):
    super(OutputTest, self).tearDown()
    output.__output_types__ = self.start_types

  def test_outputs_register(self):
    class TestOutput(Output):
      pass

    assert_true( 'TestOutput' in output.__output_types__.keys() )
    assert_true( TestOutput is output.__output_types__['TestOutput'] )
    assert_true( isinstance(Output({'type':'TestOutput'}), TestOutput) )

  def test_output_base_class_doesnt_register(self):
    assert_false( 'Output' in output.__output_types__ )

  def test_cant_init_unknown_output_type(self):
    with assert_raises( ImportError ):
      Output({'type':'nomysql'})

