from pathlib import Path

import pyautolab_Loadcell

loadcell_path = Path(pyautolab_Loadcell.__file__).parent

datas = []
datas += [(str(loadcell_path), "pyautolab_Loadcell")]
