# -*- coding: utf-8 -*-
import sys
import wx
from MyFrame import MyFrame

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None,'wxNotepad')
    frame.Show(True)
    app.MainLoop()