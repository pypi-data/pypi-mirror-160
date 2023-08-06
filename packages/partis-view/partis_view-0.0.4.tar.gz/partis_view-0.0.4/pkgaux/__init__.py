import os
import os.path as osp

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def bdist_prep( self, logger, rcc_runs ):

  if len(rcc_runs) > 0:

    from .build_qrc import build_qrc

    for i, rcc_run in enumerate(rcc_runs):
      rcc_name = f'rcc_run[{i}]'

      # valid_keys(
      #   obj = rcc_run,
      #   keys = [
      #     'src',
      #     'prefix' ] )

      src = rcc_run.get( 'src', None )

      if not src:
        raise ValueError(
          f"{rcc_name} must specify 'src'" )

      if not osp.exists(src) or not osp.isdir(src):
        raise ValueError(
          f"{rcc_name}.src must be an existing directory: {src}" )

      self.logger.info(f"{rcc_name}: {src}")

      build_qrc(
        src = src,
        dst = src,
        prefix = rcc_run.get( 'prefix', '_res' ) )
