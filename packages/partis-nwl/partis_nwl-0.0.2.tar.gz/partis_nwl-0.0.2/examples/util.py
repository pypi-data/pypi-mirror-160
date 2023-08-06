
import numpy as np

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def relative_error( x, y ):

  scale = 0.5 * ( np.linalg.norm(x) + np.linalg.norm(y) )

  return float( np.where( scale > 0.0,
    np.linalg.norm( x - y ) / scale,
    0.0 ) )
