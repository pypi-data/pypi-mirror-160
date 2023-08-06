# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

import re
import numpy as np
from copy import copy, deepcopy



from pygments.lexers import (
  get_lexer_by_name,
  PythonLexer,
  CheetahLexer )

from partis.utils import (
  indent_lines )

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  blocked,
  rgba )

# syntax highlighting
from pygments import (
  lexers )

from partis.view.highlight import (
  PygmentsHighlighter )

# linting python source
import ast
from pyflakes import (
  checker )

from pyflakes.messages import (
  UndefinedName,
  ReturnOutsideFunction )

# linting cheetah templates
from Cheetah.Template import (
  Template )

from Cheetah.Parser import (
  ParseError )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ExternalName:

  #-----------------------------------------------------------------------------
  def __init__( self, name, doc = None, children = None ):

    if doc is None:
      doc = ""

    if children is None:
      children = dict()

    self._name = name
    self._doc = doc
    self._children = children

  #-----------------------------------------------------------------------------
  @property
  def name( self ):
    return self._name

  #-----------------------------------------------------------------------------
  @property
  def doc( self ):
    return self._doc

  #-----------------------------------------------------------------------------
  @property
  def children( self ):
    return self._children

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return self._name

  #-----------------------------------------------------------------------------
  def __hash__( self ):
    return hash(self._name)

  #-----------------------------------------------------------------------------
  def __eq__( self, other ):

    return self._name == str(other)

  #-----------------------------------------------------------------------------
  def __ne__( self, other ):

    return self._name != str(other)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def join_docs( docs ):

  docs = [ d for d in docs if d ]

  return "\n\n".join(docs)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def flatten_xname( xname, docs = None ):
  if docs is None:
    docs = list()
  else:
    docs = list(docs)

  if isinstance( xname, dict ):
    flat = list()
    doc = list()
    _xname = dict()

    for k, v in xname.items():
      _v, _flat, _doc = flatten_xname(v, docs = docs)

      flat.extend( _flat )
      doc.extend( _doc )

      _xname[k] = _v

    return _xname, flat, doc

  if not isinstance( xname, ExternalName ):
    xname = ExternalName(xname)


  docs = docs + [xname.doc]
  sum_doc = join_docs( docs )

  flat = [ xname ]

  doc = [ sum_doc ]
  children = dict()

  for k, v in xname.children.items():

    _v, _flat, _doc = flatten_xname(v, docs = docs)

    flat.extend( _flat )
    doc.extend( _doc )

    children[k] = _v

  _xname = ExternalName(
    name = xname.name,
    doc = sum_doc,
    children = children )

  return _xname, flat, doc

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hover_segment( text, sep, hover_col ):

  # finds contiguous sequence of characters at the position that would be the cursor
  # under the hovering mouse position
  segs = re.split( sep, text )
  ncols = np.array([len(s) for s in segs])
  ncols += 1
  ends = np.cumsum(ncols)
  starts = ends - ncols

  m = (hover_col >= starts) & (hover_col < ends)

  hover_i = np.argmax(m)

  hover_val = segs[ hover_i ]

  return hover_i, hover_val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class InsertData:
  """Data to be inserted at a given cursor location
  """

  #-----------------------------------------------------------------------------
  def __init__( self, cursor, data ):
    self._cursor = cursor
    self._data = data

  #-----------------------------------------------------------------------------
  def __call__( self, *args ):
    self._cursor.insertText( str(self._data) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _build_insert_menu( cursor, menu, k, xname ):
  if len(xname.children) > 0:

    _menu = menu.addMenu( k )
    _menu.setToolTipsVisible(True)

    add_act = _menu.addAction( "*" )
    add_act.setToolTip( xname.doc )

    tmp = InsertData( cursor, xname )

    add_act.triggered.connect( tmp )

    build_insert_menu( cursor, _menu, xname )

  else:
    add_act = menu.addAction( k )
    add_act.setToolTip( xname.doc )

    tmp = InsertData( cursor, xname )

    add_act.triggered.connect( tmp )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def build_insert_menu( cursor, menu, xname ):
  """Constructs a menu tree to select something to be inserted.

  Parameters
  ----------
  cursor : QTextCursor
    Cursor location to insert if triggered
  menu : QMenu
    menu to add actions / sub-menus
  xname : ExternalName

  """
  if isinstance( xname, dict ):
    for k, v in xname.items():
      _build_insert_menu( cursor, menu, k, v )

    return

  for k, v in xname.children.items():
    _build_insert_menu( cursor, menu, k, v )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LineNumberArea(QtWidgets.QWidget):
  #-----------------------------------------------------------------------------
  def __init__(self, editor):
    super().__init__(editor)
    self.editor = editor

  #-----------------------------------------------------------------------------
  def sizeHint(self):
    return QtCore.Qsize(self.editor.line_numbers_width(), 0)

  #-----------------------------------------------------------------------------
  def paintEvent(self, event):
    # defers to the editor to paint this area with numbers

    self.editor.verticalScrollBar().setSliderPosition(
      self.editor.verticalScrollBar().sliderPosition() )

    # get colors for widget palette
    palette = self.palette()

    cur_color = palette.color( QtGui.QPalette.WindowText )
    cur_bg = palette.color( QtGui.QPalette.AlternateBase )

    other_color = palette.color( QtGui.QPalette.PlaceholderText )
    other_bg = palette.color( QtGui.QPalette.Window )

    painter = QtGui.QPainter(self)

    # fill the line numbers area
    painter.fillRect( event.rect(), other_bg )


    height = self.editor.fontMetrics().height()
    width = self.width()
    cursor = self.editor.textCursor()
    cur_block_num = cursor.blockNumber()

    block_num = 0
    block = self.editor.document().begin()

    # Draw the numbers (displaying the current line number in green)
    while block.isValid():
      blockCursor = QtGui.QTextCursor( block )
      blockCursorRect = self.editor.cursorRect( blockCursor )

      top = blockCursorRect.y()
      bottom = top + height

      if top > event.rect().bottom():
        break

      if block.isVisible() and (bottom >= event.rect().top()):

        if cur_block_num == block_num:
          # lighter background at current line
          painter.fillRect(
            QtCore.QRect(
              0,
              top,
              width,
              height ),
            cur_bg )

          painter.setPen( cur_color )

        else:
          painter.setPen( other_color )

        painter.drawText(
          -5,
          top,
          width,
          height,
          QtCore.Qt.AlignRight,
          str(block_num + 1) )

      block = block.next()

      block_num += 1

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CodeEdit( QtWidgets.QTextEdit ):
  #-----------------------------------------------------------------------------
  def __init__(self,
    manager,
    lang = None,
    expanding = False,
    *args,
    **kwargs):

    super().__init__(*args, **kwargs)
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self._expanding = expanding

    if self._expanding:
      self.setSizePolicy(
        QtWidgets.QSizePolicy.Preferred,
        QtWidgets.QSizePolicy.Minimum )


      self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    self._manager = manager
    self._validator = None

    self.line_numbers = LineNumberArea(self)

    # TODO: figure out how to set color of white-space characters,
    # and to only display for leading white-space
    # option = QtGui.QTextOption()
    # option.setFlags(QtGui.QTextOption.ShowTabsAndSpaces | QtGui.QTextOption.ShowLineAndParagraphSeparators)
    # self.document().setDefaultTextOption(option)

    self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
    self.verticalScrollBar().valueChanged.connect(self.updateLineNumberArea)

    self.updateLineNumberAreaWidth(0)

    self._colors_computed = False
    self._cur_cursor_line = 0

    self._highlight_line_bg = QtGui.QColor()
    self._hi_selections = list()

    self._lint_error_bg = QtGui.QColor()
    self._linted = False
    self._lint_selections = list()
    self._lint_msg = dict()
    self._cur_linted_line = 0
    self._embed_func = False

    self._external_names = dict()
    self._external_names_flat = dict()
    self._external_names_doc = dict()

    self._lexer = None
    self._highlighter = PygmentsHighlighter(
      self.document(),
      style = self._manager.theme_module.PygmentsStyle )


    self.textChanged.connect( self.text_changed )
    self.cursorPositionChanged.connect( self.cursor_changed )

    self.setMouseTracking( True )

    # self.setCurrentFont( QtGui.QFont("RobotoMono") )
    # self.setFontPointSize(10)

    if lang is not None:
      self.set_lang( lang )

  #-----------------------------------------------------------------------------
  @property
  def embed_func(self):
    return self._embed_func

  #-----------------------------------------------------------------------------
  @embed_func.setter
  def embed_func(self, val):
    self._embed_func = val

  #-----------------------------------------------------------------------------
  def paintEvent(self, event):
    if not self._colors_computed:
      # NOTE: this is noticeably hacky. However, there is no guarantee that the
      # current pallete colors are correct until the first paintEvent.
      # Since these values depend on the theme, they cannot be determined until the
      # widget is actually painted.
      self.compute_colors()

    return super().paintEvent(event)

  #-----------------------------------------------------------------------------
  def compute_colors( self ):
    self._colors_computed = True

    bg_color = self.palette().base().color()

    bg_color_hsl = bg_color.getHslF()
    hi_color_hsl = list(bg_color_hsl)
    err_color_hsl = list(hi_color_hsl)
    err_color_hsl[0] = 0.02


    if hi_color_hsl[2] > 0.5:
      # light theme
      hi_color_hsl[2] -= 0.05

      err_color_hsl[1] = 0.5
      err_color_hsl[2] -= 0.1

    else:
      # dark theme
      hi_color_hsl[2] += 0.05

      err_color_hsl[1] = 0.25
      err_color_hsl[2] += 0.05


    self._highlight_line_bg.setHslF(*hi_color_hsl)

    self._lint_error_bg.setHslF(*err_color_hsl)

  #-----------------------------------------------------------------------------
  def sizeHint(self):
    if self._expanding:
      size = self.document().size().toSize()
      return size

    else:
      return super().sizeHint()

  #-----------------------------------------------------------------------------
  def update_selections( self ):
    self.setExtraSelections(self._hi_selections + self._lint_selections)

  #-----------------------------------------------------------------------------
  def set_lang( self, lang ):

    if isinstance( lang, str ):
      lang = get_lexer_by_name(lang)

    self._lexer = lang
    self._highlighter.lexer = lang

    with blocked( self ):
      self.setPlainText( self.toPlainText() )

  #-----------------------------------------------------------------------------
  def setValidator( self, validator ):
    self._validator = validator

  #-----------------------------------------------------------------------------
  def set_external_names( self, names ):
    """Sets a hierarchy of names

    Parameters
    ----------
    names : dict[ str, ExternalName ]
      List of the recognized variable names.
      If a dictionary, the keys are the displayd branch/variable names, the leaf
      values are the name values to be highlighted/inserted into text document.
    """

    names, flat, doc = flatten_xname( names )

    self._external_names = names

    self._external_names_flat = { str(v) : v for v in flat }

    self._external_names_doc = { str(k) : v for k, v in zip(flat, doc) }

    self._highlighter.external_names = list(self._external_names_flat.keys())

  #-----------------------------------------------------------------------------
  def text_changed( self ):

    self.updateLineNumberArea()

    self._highlighter.rehighlight()
    self._linted = False

    self.lint()

    self.update_selections()

  #-----------------------------------------------------------------------------
  def cursor_changed( self ):
    self.updateLineNumberArea()
    self.highlightCurrentLine()

    self._cur_cursor_line = self.textCursor().block().blockNumber()

    self.lint()

    self.update_selections()

  #-----------------------------------------------------------------------------
  def validate( self ):
    if self._validator is None:
      return

    # TODO: implement validation

  #-----------------------------------------------------------------------------
  def lint( self ):
    if self._linted or self._cur_linted_line == self._cur_cursor_line:
      # only lint when cursor moved to another line
      return

    self._lint_selections = list()

    self._linted = True
    self._lint_msg = dict()
    self._cur_linted_line = self._cur_cursor_line

    if isinstance( self._lexer, PythonLexer ):
      self.lint_python()

    elif isinstance( self._lexer, CheetahLexer ):
      self.lint_cheetah()

  #-----------------------------------------------------------------------------
  def lint_python( self ):
    src = self.toPlainText()
    src_lines = src.splitlines()

    if self._embed_func:
      fsrc = "def func():\n  __noop__ = 0\n{}".format(indent_lines(2, src))
      ix = 2
      iy = 2
    else:
      fsrc = src
      ix = 0
      iy = 0

    filename = ''

    try:

      tree = ast.parse(fsrc, filename = filename)

    except SyntaxError as e:

      lineno = e.lineno - iy
      col = e.offset - ix

      msg = f"line: {lineno}, col: {col}\n{e.msg}"

      offset = col - 1
      idx = lineno - 1

      if e.text:
        text = e.text[ix:]
        msg += f"\n{indent_lines(2, text)}\n"
        msg += '  ' + ' '*offset + '^'

      if idx in self._lint_msg:
        self._lint_msg[idx] += '\n\n' + msg
      else:
        self._lint_msg[idx] = msg

      self._lint_selections.extend( self.highlightLine(
        lineno = idx,
        qcolor = self._lint_error_bg,
        underline_offset = offset ) )

    else:

      file_tokens = checker.make_tokens(fsrc)
      w = checker.Checker(tree, file_tokens=file_tokens, filename=filename)
      w.messages.sort(key=lambda m: m.lineno)

      for m in w.messages:
        if m.lineno - iy <= 0:
          continue

        message_args = m.message_args

        lineno = m.lineno - iy
        col = m.col - ix

        idx = lineno - 1
        offset = col

        if isinstance( m, UndefinedName ):

          name = m.message_args[0]

          if name in self._external_names_flat:
            # This is an external name.
            # Since many of the names are actually attributes of a root name,
            # pyflakes will only catch the root, but now can check the
            # remainder of the attributes to see if it is known

            # extract full qualified name from the source

            _, _name = hover_segment(
              text = src_lines[idx],
              sep = r"[^a-zA-Z0-9_\.]",
              hover_col = offset )

            if _name in self._external_names_flat:
              # ignore known external names
              continue

            partial = _name

            while partial and partial not in self._external_names_flat:
              # finds most full match based on 'parent' attributes
              partial, _, _ = partial.rpartition('.')

            if partial:
              # ignore if a partial match has a wildcard attribute
              if '*' in self._external_names_flat[ partial ].children:
                continue

            message_args = (_name,)

        # elif isinstance( m, ReturnOutsideFunction ) and m.col == 0:
        #   # ignore returns at zero indentation
        #   continue

        msg = m.message % message_args

        msg = f"line: {lineno}, col: {col+1}\n{msg}"

        if idx in self._lint_msg:
          self._lint_msg[idx] += '\n\n' + msg
        else:
          self._lint_msg[idx] = msg

        self._lint_selections.extend( self.highlightLine(
          lineno = idx,
          qcolor = self._lint_error_bg,
          underline_offset = offset ) )

  #-----------------------------------------------------------------------------
  def lint_cheetah( self ):

    src = self.toPlainText()

    try:

      tmpl = Template(src)

    except ParseError as e:
      if e.lineno:
        lineno = e.lineno
        col = e.col or 1
        line = e.stream.splitlines()[lineno-1]

      else:
        lineno, col, line = e.stream.getRowColLine()


      msg = f"line: {lineno}, col: {col}\n{e.msg}"

      offset = col - 1
      idx = lineno - 1

      if line:
        msg += f"\n{indent_lines(2, line)}\n"
        msg += '  ' + ' '*offset + '^'

      self._lint_msg[idx] = msg

      self._lint_selections.extend( self.highlightLine(
        lineno = idx,
        qcolor = self._lint_error_bg,
        underline_offset = offset ) )

  #-----------------------------------------------------------------------------
  def keyPressEvent( self, event ):
    # override tabs to use space delimeter
    if event.key() == QtCore.Qt.Key_Tab:
      tc = self.textCursor()
      tc.insertText("  ")
      return

    return QtWidgets.QTextEdit.keyPressEvent(self,event)

  #-----------------------------------------------------------------------------
  def line_numbers_width(self):
    # compute width based on how many digits the largest line number has
    digits = 1 + np.floor( np.log10( max(1, self.document().blockCount()) ) )

    width = 13 + self.line_numbers.fontMetrics().width('9') * digits

    return width

  #-----------------------------------------------------------------------------
  def highlightCurrentLine(self):
    self._hi_selections = []

    if not self.isReadOnly():
      selection = QtWidgets.QTextEdit.ExtraSelection()

      selection.format.setBackground( self._highlight_line_bg )
      selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
      selection.cursor = self.textCursor()
      selection.cursor.clearSelection()
      self._hi_selections.append(selection)

  #-----------------------------------------------------------------------------
  def highlightLine( self, lineno, qcolor, underline_offset = None ):
    extraSelections = []

    selection = QtWidgets.QTextEdit.ExtraSelection()

    selection.format.setBackground( QtGui.QBrush(qcolor) )
    selection.format.setProperty( QtGui.QTextFormat.FullWidthSelection, True )

    block = self.document().findBlockByNumber(lineno)
    cursor = QtGui.QTextCursor( block )
    rect = self.cursorRect( cursor )

    selection.cursor = cursor

    # selection.cursor = self.cursorForPosition( QtCore.QPoint(lineno, 0) )
    selection.cursor.clearSelection()

    extraSelections.append(selection)

    if underline_offset is not None:

      selection = QtWidgets.QTextEdit.ExtraSelection()

      selection.format.setUnderlineStyle( QtGui.QTextCharFormat.SpellCheckUnderline )
      selection.format.setUnderlineColor( rgba(173, 44, 44, 1) )

      cursor = QtGui.QTextCursor( block )
      cursor.clearSelection()

      if underline_offset >= block.length()-1:
        # ensure offset starts before newline character, if possible
        underline_offset = max(0, block.length() - 2 )

      cursor.movePosition(
        QtGui.QTextCursor.NextCharacter,
        QtGui.QTextCursor.MoveAnchor,
        underline_offset )

      cursor.movePosition(
        QtGui.QTextCursor.NextCharacter,
        QtGui.QTextCursor.KeepAnchor,
        block.length() - 1 - underline_offset )

      selection.cursor = cursor

      extraSelections.append(selection)

    return extraSelections

  #-----------------------------------------------------------------------------
  def updateLineNumberAreaWidth( self, _ ):
    if self._expanding:
      # self.setMinimumSize( self.document().size().toSize() )

      if self.document().blockCount() > 1:
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

      else:
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

      self.updateGeometry()

    self.setViewportMargins( self.line_numbers_width(), 0, 0, 0 )

  #-----------------------------------------------------------------------------
  def updateLineNumberArea(self):

    rect = self.contentsRect()
    self.line_numbers.update(0, rect.y(), self.line_numbers.width(), rect.height())
    self.updateLineNumberAreaWidth(0)
    dy = self.verticalScrollBar().sliderPosition()
    if dy:
      self.line_numbers.scroll(0, dy)

    first_block_id = self.getFirstVisibleBlockId()
    if first_block_id == 0 or self.textCursor().block().blockNumber() == first_block_id - 1:
      self.verticalScrollBar().setSliderPosition(dy - self.document().documentMargin())

  #-----------------------------------------------------------------------------
  def resizeEvent(self, event):

    if self._expanding:
      self.updateGeometry()

    cr = self.contentsRect()

    self.line_numbers.setGeometry(QtCore.QRect(
      cr.left(),
      cr.top(),
      self.line_numbers_width(),
      cr.height() ))

    super().resizeEvent(event)

  #-----------------------------------------------------------------------------
  def getFirstVisibleBlockId(self):
    cursor = QtGui.QTextCursor(self.document())
    cursor.movePosition(QtGui.QTextCursor.Start)

    for block_idx in range(self.document().blockCount()):
      block = cursor.block()
      r1 = self.viewport().geometry()
      r2 = self.document().documentLayout().blockBoundingRect(block).translated(r1.x(), r1.y() - self.verticalScrollBar().sliderPosition()).toRect()

      if r1.contains(r2, True):
          return block_idx

      cursor.movePosition(QtGui.QTextCursor.NextBlock)

    return 0


  #-----------------------------------------------------------------------------
  def mouseMoveEvent( self, event ):

    r1 = self.viewport().geometry()

    vpos = self.viewport().mapFromGlobal( event.globalPos() )
    # vpos = QtCore.QPoint( vpos.x() - r1.x(), vpos.y() )

    hover_cursor = self.cursorForPosition( vpos )
    hover_block = hover_cursor.block()

    if hover_block is not None:
      cursor_rect = self.document().documentLayout().blockBoundingRect(hover_block)

      cursor_rect = cursor_rect.translated(0.0*r1.x(), r1.y() - self.verticalScrollBar().sliderPosition()).toRect()

      if cursor_rect.contains( vpos, True ):

        hover_block_text = hover_block.text()

        hover_line = hover_cursor.blockNumber()
        hover_col = hover_cursor.positionInBlock()

        if hover_line in self._lint_msg:
          self.setToolTip(self._lint_msg[hover_line])
        else:

          hover_i, hover_val = hover_segment(
            text = hover_block_text,
            sep = r"[^a-zA-Z0-9_\.]",
            hover_col = hover_col )

          while hover_val and hover_val not in self._external_names_flat:
            # finds most full match based on 'parent' attributes
            hover_val, _, _ = hover_val.rpartition('.')

          if hover_val in self._external_names_flat:
            self.setToolTip( self._external_names_doc[ hover_val ] )
          else:
            self.setToolTip("")

      else:
        self.setToolTip("")

    else:
      self.setToolTip("")



    super().mouseMoveEvent( event )

    event.accept()

  #-----------------------------------------------------------------------------
  def contextMenuEvent( self, event ):
    event.accept()

    menu = self.createStandardContextMenu()

    # get the current cursor, regardless of where the mouse is hovering
    cur_cursor = self.textCursor()
    cur_block = cur_cursor.block()
    selection = cur_cursor.selection().toPlainText()

    vpos = self.viewport().mapFromGlobal( event.globalPos() )
    hover_cursor = self.cursorForPosition( vpos )
    hover_block = hover_cursor.block()
    hover_block_text = hover_block.text()

    hover_col = hover_cursor.positionInBlock()

    # finds contiguous sequence of characters at the position that would be the cursor
    # under the hovering mouse position
    segs = hover_block_text.split(" ")
    ncols = np.array([len(s) for s in segs])
    ncols += 1
    ends = np.cumsum(ncols)
    starts = ends - ncols

    m = (hover_col >= starts) & (hover_col < ends)

    hover_i = np.argmax(m)

    hover_segment = segs[ hover_i ]

    if self._external_names is not None and len(self._external_names) > 0:

      var_name_menu = QtWidgets.QMenu( "Insert Variable", menu )
      var_name_menu.setToolTipsVisible(True)

      build_insert_menu( cur_cursor, var_name_menu, self._external_names )

      menu.insertMenu( menu.actions()[0], var_name_menu )


    menu.exec_( event.globalPos() )
