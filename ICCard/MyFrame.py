import wx

class MyFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(
            self,
            parent,
            title=title,
            size=(300,200)
        )
        self.control = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE
        )