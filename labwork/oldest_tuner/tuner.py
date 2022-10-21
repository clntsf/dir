import musicosity; import wx; import os

def openFile(filename):
    os.system("open " + filename)

class ListCtrl(wx.ListCtrl):

    def __init__(self, *args, **kw):
        super(ListCtrl, self).__init__(*args, **kw, style=wx.LC_REPORT)
        self.EnableCheckBoxes()

class CheckboxComboPopup(wx.ComboPopup):
    
    def Init(self):
        self.sampleList = [item for item in musicosity.notes_dict]
        self.CheckList = None

    def AddItem(self, item):
        self.CheckList.InsertItem(0,item)
        
    def Create(self, parent):
        self.CheckList = ListCtrl(parent)
        self.CheckList.InsertColumn(0,'')
        {self.AddItem(item) for item in self.sampleList[::-1]}
        return True
    
    def GetControl(self):
        return self.CheckList
    
    def OnPopup(self):
        pass

    def GetAdjustedSize(self,minWidth,prefHeight,maxHeight):
        num_of_items = len(self.sampleList)
        pref_height = (num_of_items * 21)
        return wx.Size(minWidth, min(pref_height, maxHeight))

class FormFrame(wx.Frame):
    
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(FormFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        self.panel = wx.Panel(self)

        self.ButtonPressed = 0 # Set a variable to lock the button to one use to prevent spamming
        self.ActiveTuner = 'scale'

        # put some text with a larger bold font on it
        st = wx.StaticText(self.panel, label="Sinewave Speech Musicalizer")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        sub_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        
        main_sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 15))  # Make the title sizer
        
        scale_descriptor = wx.StaticText(self.panel, label="Select Tuning: ") # Format the input prompts
        self.scale_type_chooser = wx.RadioBox(self.panel,choices=['By Scale','By Notes'],style = wx.RA_SPECIFY_COLS)
        self.scale_type_chooser.Bind(wx.EVT_RADIOBOX, self.TunerChange)
        
        interval_descriptor = wx.StaticText(self.panel, label="Select Sampling Interval (x10 ms): ")
        input_descriptor = wx.StaticText(self.panel, label="Select Input Spreadsheet: ")
        
        self.scale_selector = wx.ComboBox(self.panel,value= '', choices=[item for item in musicosity.scales_dict], style= wx.CB_READONLY) # Format the actual input mediums
        self.scale_selector.Bind(wx.EVT_COMBOBOX, self.DataChange) # Binds change of scale to refresh submit button
        self.note_selector = wx.ComboCtrl(self,value='Select Notes',size=(150,-1),style=wx.CB_READONLY)
        self.ComboPopup = CheckboxComboPopup()
        self.note_selector.SetPopupControl(self.ComboPopup)
        self.notes = self.ComboPopup.CheckList
        
        self.interval_input = wx.TextCtrl(self.panel,value= '')
        self.interval_input.Bind(wx.EVT_TEXT,self.DataChange)
        
        self.input_spreadsheet_selector = wx.FilePickerCtrl(self.panel, path = '', wildcard="XLSX files (*.xlsx)|*.xlsx", style = wx.FLP_DEFAULT_STYLE)
        self.input_spreadsheet_selector.Bind(wx.EVT_FILEPICKER_CHANGED,self.DataChange)
        
        self.interval_input.SetMaxLength(3)
        
        submit_button = wx.Button(self.panel,label="Submit Input Data")  # Add and functionalize the submit button
        submit_button.Bind(wx.EVT_BUTTON,self.OnButton)

        sub_sizer0.Add(scale_descriptor,wx.SizerFlags().Border(wx.TOP,10)) # Scale descriptor
        sub_sizer0.Add(self.scale_type_chooser,wx.SizerFlags().Border()) # Radios
        sub_sizer0.Add(self.scale_selector,wx.SizerFlags().Border(wx.TOP|wx.LEFT,8)) # Combobox
        sub_sizer0.Add(self.note_selector,wx.SizerFlags().Border()) # ComboCtrl
        
        sub_sizer1.Add(interval_descriptor,wx.SizerFlags().Border()) # Interval descriptor
        sub_sizer1.Add(self.interval_input,wx.SizerFlags().Border()) # Interval entering box
        
        sub_sizer2.Add(input_descriptor,wx.SizerFlags().Border()) # Input sheet descriptor
        sub_sizer2.Add(self.input_spreadsheet_selector,wx.SizerFlags().Border()) # Input Selector

        sub_sizer3.Add(submit_button,wx.SizerFlags().Border())
        
        main_sizer.Add(sub_sizer0,wx.SizerFlags().Border(wx.LEFT,15))
        main_sizer.Add(sub_sizer1,wx.SizerFlags().Border(wx.LEFT,15))   # Add all sizers to the main sizer, and set it as the sizer for our panel
        main_sizer.Add(sub_sizer2,wx.SizerFlags().Border(wx.LEFT,15))
        main_sizer.Add(sub_sizer3,wx.SizerFlags().Border(wx.LEFT|wx.BOTTOM,15))
        self.panel.SetSizer(main_sizer)


        self.makeMenuBar()

    def makeMenuBar(self):

        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(-1, "&Exit...\tCtrl-W")
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit,exitItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def DataChange(self, event):
        self.ButtonPressed = 0

    def OnButton(self, event):
        if self.ButtonPressed != 1:
            if self.interval_input.GetValue() != '' and self.input_spreadsheet_selector.GetPath() != '':
                if self.ActiveTuner == 'scale' and self.scale_selector.GetValue() != '': self.scale = self.scale_selector.GetValue()
                elif self.ActiveTuner == 'notes':
                    self.notes_checked = [musicosity.notes_dict[note] for note in self.ComboPopup.sampleList if self.ComboPopup.CheckList.IsItemChecked(self.ComboPopup.sampleList.index(note))]
                    if len(self.notes_checked) != 0: self.scale = self.notes_checked
                self.input_sheet = self.input_spreadsheet_selector.GetPath()
                try:
                    self.interval = int(self.interval_input.GetValue())
                except ValueError:
                    print("Invalid interval input. Please input an integer"); return
                musicosity.main(self.input_sheet,self.scale,self.interval)
                openFile("output_sheet.xlsx")
            self.ButtonPressed = 1

    def TunerChange(self, event):
        self.ActiveTuner = ['scale','notes'][self.scale_type_chooser.GetSelection()]
        if self.ActiveTuner == 'notes':
            self.scale_selector.Hide(); self.panel.Fit()
            self.note_selector.Show(); self.panel.Fit()
        else:
            self.note_selector.Hide(); self.panel.Fit()
            self.scale_selector.Show(); self.panel.Fit()

    def NoteIsChecked(self, event):
        print('hello',self.note_selector.GetPopupControl().GetControl().GetCheckedItems())

if __name__ == '__main__':
    app = wx.App()
    frm = FormFrame(None, title="CSF's Sinewave Speech Musicalizer",size=(550,250))
    frm.Show()
    frm.note_selector.Hide()
    frm.panel.Fit()
    app.MainLoop()
