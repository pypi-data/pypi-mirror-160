import time
author="Hansheng Wang"
version="2022-07-24 15:09:20"

from IPython import get_ipython

try:
    _config = get_ipython().config
    if _config:
        print("Welcome to clubear! A subsample-based massive data analysis and research toolkit (",version,").")
except:
    pass

from .dm import manager
from .pm import pump
from .pm import tank
from .pm import save
from .ck import check
from .pt import plot
from .md import model
from .sf import shuffle
from .sim import simulator
from .fun import demo
from .fun import ispump
from .da import datasets