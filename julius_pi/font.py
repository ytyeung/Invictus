import random
import wx
import wx.lib.scrolledpanel as scrolled

########################################################################
class MyForm(wx.Frame):
    
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Font Tutorial")
 
        # Add a panel so it looks the correct on all platforms
        panel = scrolled.ScrolledPanel(self)
        panel.SetAutoLayout(1)
        panel.SetupScrolling()
        
        fontSizer = wx.BoxSizer(wx.VERTICAL)
        families = {"FONTFAMILY_DECORATIVE":wx.FONTFAMILY_DECORATIVE, # A decorative font
                    "FONTFAMILY_DEFAULT":wx.FONTFAMILY_DEFAULT,
                    "FONTFAMILY_MODERN":wx.FONTFAMILY_MODERN,     # Usually a fixed pitch font
                    "FONTFAMILY_ROMAN":wx.FONTFAMILY_ROMAN,      # A formal, serif font
                    "FONTFAMILY_SCRIPT":wx.FONTFAMILY_SCRIPT,     # A handwriting font
                    "FONTFAMILY_SWISS":wx.FONTFAMILY_SWISS,      # A sans-serif font
                    "FONTFAMILY_TELETYPE":wx.FONTFAMILY_TELETYPE    # A teletype font
                    }
        weights = {"FONTWEIGHT_BOLD":wx.FONTWEIGHT_BOLD,
                   "FONTWEIGHT_LIGHT":wx.FONTWEIGHT_LIGHT,
                   "FONTWEIGHT_NORMAL":wx.FONTWEIGHT_NORMAL
                   }
        
        styles = {"FONTSTYLE_ITALIC":wx.FONTSTYLE_ITALIC,
                  "FONTSTYLE_NORMAL":wx.FONTSTYLE_NORMAL,
                  "FONTSTYLE_SLANT":wx.FONTSTYLE_SLANT
                  }
        sizes = [8, 10, 12, 14]
        for family in families.keys():
            for weight in weights.keys():
                for style in styles.keys():
                    label = "%s    %s    %s" % (family, weight, style)
                    size = random.choice(sizes)
                    font = wx.Font(size, families[family], styles[style], 
                                   weights[weight])
                    txt = wx.StaticText(panel, label=label)
                    txt.SetFont(font)
                    fontSizer.Add(txt, 0, wx.ALL, 5)
        panel.SetSizer(fontSizer)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()
