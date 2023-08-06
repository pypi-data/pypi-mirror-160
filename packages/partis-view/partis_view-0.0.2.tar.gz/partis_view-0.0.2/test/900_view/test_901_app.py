import os
import pytest
import tempfile
import logging


from partis.view import (
  MainWindow,
  Manager )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ErrorLogHandler( logging.Handler ):
  """Collects log error records in local list of hints

  Parameters
  ----------
  level : int
    The level enabled for the handler
  **kwargs :
    Keyword arguments passed to the ModelHint when casting
  """
  #-----------------------------------------------------------------------------
  def __init__(self, level = logging.NOTSET ):
    super().__init__( level )

    self._errors = list()

  #-----------------------------------------------------------------------------
  def emit( self, record ):

    if record.levelno >= logging.ERROR:
      self._errors.append( record )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.mark.with_gui
def test_app():

  error_handler = ErrorLogHandler()
  logger = logging.getLogger(__name__)
  logger.addHandler( error_handler )

  with tempfile.TemporaryDirectory() as tmpdir:
    os.chdir( tmpdir )

    app_manager = Manager(
      main_window_class = MainWindow,
      theme = 'light',
      init_file = tmpdir,
      testing = True,
      logger = logger )

    if len(error_handler._errors) > 0:
      assert( False )

    assert( app_manager.run() == 0 )
