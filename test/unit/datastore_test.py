
from chai import Chai
from pluto.datastore import datastore
from pluto.datastore import Datastore

class DatastoreTest(Chai):

  def setUp(self):
    super(DatastoreTest, self).setUp()
    self.start_types = datastore.__datastore_types__.copy()

  def tearDown(self):
    super(DatastoreTest, self).tearDown()
    datastore.__datastore_types__ = self.start_types

  def test_datastores_register(self):
    class TestDatastore(Datastore):
      pass

    assert_true( 'TestDatastore' in datastore.__datastore_types__.keys() )
    assert_true( TestDatastore is datastore.__datastore_types__['TestDatastore'] )
    assert_true( isinstance(Datastore({'type':'TestDatastore'}), TestDatastore) )

  def test_datastore_base_class_doesnt_register(self):
    assert_false( 'Datastore' in datastore.__datastore_types__ )

  def test_cant_init_unknown_datastore_type(self):
    with assert_raises( ImportError ):
      Datastore({'type':'nomysql'})
