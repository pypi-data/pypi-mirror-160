
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pytest_addoption(parser):
  """Register argparse-style options and ini-style config values, called once at the beginning of a test run.
  """
  # print(f"running addoption: {__file__}")

  parser.addini(
    'vdisplay_width',
    'Width of the virtual display',
    default='800')

  parser.addini(
    'vdisplay_height',
    'Height of the virtual display',
    default='600')

  parser.addini(
    'vdisplay_colordepth',
    'Color depth of the virtual display',
    default='16')
