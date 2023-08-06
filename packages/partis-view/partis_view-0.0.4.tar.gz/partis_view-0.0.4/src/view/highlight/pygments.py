# -*- coding: utf-8 -*-
import sys
import re
from PySide2 import QtCore, QtGui, QtWidgets

from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.lexer import (
  RegexLexer,
  words,
  default,
  do_insertions )

from pygments.token import (
  Keyword,
  Name,
  Punctuation,
  Comment,
  String,
  Literal,
  Text,
  Error,
  Number,
  Operator,
  Generic,
  Other )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def make_external_name_lexer( lexer, names, token = Name.External ):
  """Combines a given lexer with one to highlight special names
  """

  class CustomNameLexer( RegexLexer ):

    name = None
    aliases = []
    filenames = []

    keywords = words( names, suffix = r'\b' )

    tokens = {
      'root': [
        ( keywords, token )
      ] }

    #---------------------------------------------------------------------------
    def get_tokens_unprocessed( self, text ):
      buffered = ''
      insertions = []
      lng_buffer = []

      # first process using lexer for special words
      for i, t, v in super().get_tokens_unprocessed(text):
        if t is token:

          lng_buffer.append((i, t, v))

        else:
          if lng_buffer:
            insertions.append((len(buffered), lng_buffer))
            lng_buffer = []

          buffered += v


      if lng_buffer:
        insertions.append((len(buffered), lng_buffer))

      # anything else now lexed using given lexer
      return do_insertions(
        insertions,
        lexer.get_tokens_unprocessed(buffered) )

  return CustomNameLexer

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PygmentsBlockUserData( QtGui.QTextBlockUserData ):
  #-----------------------------------------------------------------------------
  def __init__( self, text, formats ):
    super().__init__()
    self.text = text
    self.formats = formats

    self.applied = False


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PygmentsHighlighter( QtGui.QSyntaxHighlighter ):
  """Syntax highligher using Pygments
  """

  #-----------------------------------------------------------------------------
  def __init__(self,
    parent,
    lexer = None,
    style = None,
    external_names = None ):

    super().__init__(parent)

    self._base_lexer = None
    self._lexer = None
    self._style = None
    self._external_names = None
    self._formats = dict()
    self._do_rehighlight = False

    self.lexer = lexer

    if style is not None:
      self.style = style

    else:
      self.style = 'default'

    self.external_names = external_names

  #-----------------------------------------------------------------------------
  @property
  def external_names( self ):
    return self._external_names

  #-----------------------------------------------------------------------------
  @external_names.setter
  def external_names( self, names ):

    if names is not None and len(names) == 0:
      names = None

    self._external_names = names

    if self._external_names is None:
      self._lexer = self._base_lexer

    elif self._base_lexer is not None:
      self._lexer = make_external_name_lexer( self._base_lexer, self._external_names )()

  #-----------------------------------------------------------------------------
  @property
  def lexer( self ):
    return self._lexer

  #-----------------------------------------------------------------------------
  @lexer.setter
  def lexer( self, lexer ):

    if isinstance( lexer, str ):
      lexer = get_lexer_by_name( lexer )

    self._base_lexer = lexer

    if lexer is not None and self._external_names is not None:
      lexer = make_external_name_lexer( lexer, self._external_names )()

    self._lexer = lexer

  #-----------------------------------------------------------------------------
  @property
  def style( self ):
    return self._style

  #-----------------------------------------------------------------------------
  @style.setter
  def style( self, style ):

    if isinstance(style, str):
      style = get_style_by_name( style )

    self._style = style
    self._formats = dict()

    if self._style is not None:

      for token, _style in self._style:

        fmt = QtGui.QTextCharFormat()

        for key, value in _style.items():
          if value:
            if key == 'color':
              fmt.setForeground(self._get_brush(value))

            elif key == 'bgcolor':
              fmt.setBackground(self._get_brush(value))

            elif key == 'bold':
              fmt.setFontWeight(QtGui.QFont.Bold)

            elif key == 'italic':
              fmt.setFontItalic(True)

            elif key == 'underline':
              fmt.setUnderlineStyle(
                  QtGui.QTextCharFormat.SingleUnderline)

            elif key == 'sans':
              fmt.setFontStyleHint(QtGui.QFont.SansSerif)

            elif key == 'roman':
              fmt.setFontStyleHint(QtGui.QFont.Times)

            elif key == 'mono':
              fmt.setFontStyleHint(QtGui.QFont.TypeWriter)

        self._formats[token] = fmt


  #-----------------------------------------------------------------------------
  def _get_brush(self, color):

    qcolor = self._get_color(color)
    brush = QtGui.QBrush(qcolor)

    return brush

  #-----------------------------------------------------------------------------
  def _get_color(self, color):

    qcolor = QtGui.QColor()

    qcolor.setRgb(
      int(color[:2], base = 16),
      int(color[2:4], base = 16),
      int(color[4:6], base = 16) )

    return qcolor

  #-----------------------------------------------------------------------------
  def _get_format( self, token ):

    fmt = self._formats.get( token, None )

    if fmt is None:
      # use parent tokens to resolve format.
      # By default this will find the root style format
      missing = list()

      while token not in self._formats:
        missing.append(token)

        token = token.parent

      fmt = self._formats[token]

      # add the tokens using the found format
      for token in missing:
        self._formats[token] = fmt

    return fmt

  #-----------------------------------------------------------------------------
  def rehighlight( self ):
    if self._do_rehighlight:
      # update rendering of all blocks that have not been applied
      self._do_rehighlight = False

      cur_block = self.document().begin()

      for i in range( self.document().blockCount() ):
        data = cur_block.userData()

        if data is None or not data.applied:
          self.rehighlightBlock(cur_block)

        cur_block = cur_block.next()


  #-----------------------------------------------------------------------------
  def highlightBlock( self, text ):
    """ Highlight a block of text.
    """

    if self._lexer is None:
      return

    data = self.currentBlock().userData()

    if data is not None:
      if text != data.text:
        # the text has changed, so remove previously lexed formatting
        self.currentBlock().setUserData(None)

      else:
        # must apply formatting whether or not it has already been applied,
        # because this was called on the block and not setting the format will
        # result in removal of any previous formatting

        # print('highlightBlock applying', self.currentBlock().blockNumber(), text )
        for fmt in data.formats:
          self.setFormat( *fmt )

        # print('highlightBlock applied', self.currentBlock().blockNumber(), text )
        data.applied = True
        return

    text = self.document().toPlainText()

    # recompute highlight formating for all blocks
    self._do_rehighlight = False
    cur_block = self.document().begin()
    index = 0
    tokens = self._lexer.get_tokens(text)
    tokens = list(tokens)

    formats = list()
    _tokens = list()

    num_tokens = len(tokens)

    while len(tokens) > 0:
      token, token_text = tokens.pop(0)

      if ( index == 0
        and len(cur_block.text()) == 0
        and len(token_text) > 0
        and token_text[0] != '\n' ):
        # NOTE: this is to handle leading blocks that are ignored by the lexer
        cur_block = cur_block.next()
        tokens.insert(0, (token, token_text))
        continue

      # print('highlightBlock formats', cur_block.blockNumber(), token_text, token )

      _tokens.append( (token, token_text) )

      length = len(token_text) if isinstance(token_text, str) else token_text.length()
      _length = min( length, cur_block.length() - index )

      if _length < length:
        # print('  span block', token, _length, length )
        tokens.insert(0, ( token, token_text[ _length: ] ) )
        length = _length


      # get formatting for this token
      fmt = (
        index,
        length,
        self._get_format(token) )

      formats.append( fmt )

      index += length

      if index == cur_block.length() or len(tokens) == 0:

        data = cur_block.userData()
        block_text = cur_block.text()

        # print('highlightBlock block ', cur_block.blockNumber(), cur_block.length(), len(block_text), block_text, _tokens )

        if data is None or data.formats != formats or data.text != block_text:
          # update formatting of this block
          data = PygmentsBlockUserData(
            text = block_text,
            formats = formats )

          cur_block.setUserData(data)

          if self.currentBlock() == cur_block:
            # print('highlightBlock inplace', self.currentBlock().blockNumber() )

            for fmt in data.formats:
              self.setFormat( *fmt )

            data.applied = True

          else:
            self._do_rehighlight = True

        cur_block = cur_block.next()

        index = 0
        formats = list()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
