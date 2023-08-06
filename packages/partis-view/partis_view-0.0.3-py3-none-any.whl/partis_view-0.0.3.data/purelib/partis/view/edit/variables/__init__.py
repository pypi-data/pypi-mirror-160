# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from .base import VariableWidget
from .bool_w import BoolWidget
from .int_w import IntWidget
from .float_w import FloatWidget
from .gen_str_w import GenStrWidget
from .multi_str_w import MultilineStrWidget
from .select_w import SelectionWidget
from .tuple_w import ArrayWidget
from .filepath_w import FilepathWidget
from .float_spline_2d import FloatSpline2DWidget
