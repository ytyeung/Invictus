#!/usr/bin/env python
import os
import wx
import re
import time
from threading import *
import subprocess
# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()
# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

#START recognition service
SERVER_ID=subprocess.Popen('julius -input adinnet -quiet -C /home/pi/julius4/Invictus.jconf',shell=True,stdout=subprocess.PIPE)

#
def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data=data
        
        

# Thread class that executes processing
class WorkerThread(Thread):
    """Worker Thread Class."""
    REC_ID=None
    RECOG_ID=None

    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0

        self.start()
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        
        CD_ID=subprocess.Popen('cd /home/pi/julius4',shell=True)
        
        
    def run(self):	
       
        # This is the code executing in the new thread. Simulation of
        # a long process (well, 10s here) as a simple loop - you will
        # need to structure your processing so that you periodically
        # peek at the abort variable
        
        
            if self._want_abort == 0:
                wx.PostEvent(self._notify_window,ResultEvent('Recording...Please place your order.'))
                global REC_ID
                #REC_ID=subprocess.Popen('arecord -D plughw:0 -c 1 -r 16000 -f S16_LE -d 5 /home/pi/julius4/rec.wav',shell=True)
                REC_ID=subprocess.Popen('adinrec -48 -input alsa  /home/pi/julius4/rec.wav',shell=True)

                REC_ID.wait()

            if self._want_abort == 0:
                wx.PostEvent(self._notify_window,ResultEvent('Reading your order...Please Wait.'))
                global RECOG_ID
                #RECOG_ID=subprocess.Popen('julius -input rawfile -filelist /home/pi/julius4/recfile -quiet -C /home/pi/julius4/Invictus.jconf -outfile',shell=True)
                #RECOG_ID.wait()
                RECOG_ID=subprocess.Popen('echo /home/pi/julius4/rec.wav | adintool -in file -out adinnet -server localhost',shell=True)
                RECOG_ID.wait()

            if self._want_abort == 0:
                #input=open ("/home/pi/julius4/rec.out",'r')
                #S = input.readline()
                #input.close()

                #m = re.search('<s>\s+(.+?)\s+<\/s>', S)
                #if m:
                #    found = m.group(1)
                #    print (found) 
                #    wx.PostEvent(self._notify_window,ResultEvent(found))
                #    self._notify_window.ResetButton()
                #else:
                #    wx.PostEvent(self._notify_window,ResultEvent('No result'))
                #    self._notify_window.ResetButton()
                time.sleep(1)
                found = 'No result'
                while True:
                    line=SERVER_ID.stdout.readline()
                    #connected 
                    starthint = re.search('Stat: adin_tcpip: connected', line)

                    if starthint:
                        break


                while True:
                    line=SERVER_ID.stdout.readline()
                    # now search for result
                    m = re.search('sentence1: <s>\s+(.+?)\s+<\/s>', line)

                    if m:
                        found = m.group(1)
                        
                    notfound = re.search('Stat: adin_tcpip: connection end', line)
                    
                    if notfound:
                        break
                
                wx.PostEvent(self._notify_window,ResultEvent(found))
                self._notify_window.ResetButton()

    def abort(self):
        self._want_abort = 1
        print('Trying to abort computation')
        if REC_ID.returncode is None:
            print('Killing ARecord: PID:',REC_ID.pid)
            os.system('pkill arecord')
            
            
        elif RECOG_ID.returncode is None:
            print('Killing Julius: PID: ',RECOG_ID.pid)
            os.system('pkill arecord')       
            
        print('Computation Aborted')
        wx.PostEvent(self._notify_window,ResultEvent('Hello! Please order by pressing start~'))
        

   
        
        
class MyFrame(wx.Frame):
    def __init__(self ,parent ,id ,title):
        ###
        ###
        wx.Frame.__init__(self , parent,id ,title,wx.DefaultPosition, size=(700,350))
        self.CreateStatusBar() # A StatusBar in the bottom of the window
        hbox = wx.BoxSizer(wx.VERTICAL)
        
                
               
        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        panel = wx.Panel(self, -0)
        panel.SetBackgroundColour((255,222,173))

        # pick a button image file you have (.bmp .jpg .gif or .png)
        # Button Start
        imageFile= "/home/pi/bluemicrophone.png"
        self.image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.button1 = wx.BitmapButton(panel, id=-1, bitmap=self.image1, pos=(200,300), size=(128,128))
    
       
   
        # Button Close
        imageFile3= "/home/pi/childish_Cross.png"
        self.image3 = wx.Image(imageFile3, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.button3 = wx.BitmapButton(panel, id=-3, bitmap=image3,pos=(300,100), size=(128,128))
        

        #Font
        font1 = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.NORMAL,False,u'Comic Sans MS')
        font2 = wx.Font(14, wx.DEFAULT, wx.NORMAL,wx.NORMAL, False, faceName="Century Schoolbook L")
        font3 = wx.Font(14, wx.TELETYPE, wx.NORMAL, wx.NORMAL)

        
        
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_BUTTON, self.OnButton1, id=-1)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        #self.Bind(wx.EVT_BUTTON, self.OnButton3, id=-3)
     
        EVT_RESULT(self,self.OnUpdate)

        # And indicate we don't have a worker thread yet
        self.worker = None
        self.WorkerRunning = False
       

        self.textLabel=wx.StaticText(panel, -4, 'Hello! Please order by pressing start~', (80, 0),size=(400,128),style=wx.ALIGN_CENTRE)
        self.textLabel.SetForegroundColour((106,90,205))
        self.textLabel.SetFont(font1)

        hbox.Add(self.textLabel,0,wx.ALIGN_CENTER)
        hbox.Add(self.button1,0,wx.ALIGN_CENTER)
        panel.SetSizer(hbox)
        self.Centre()
        
    
    def OnExit (self,e):
        os.system('pkill julius')
        self.Destroy()  # Close the frame.
        
    
        
        

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        font2 = wx.Font(14, wx.DEFAULT, wx.NORMAL,wx.NORMAL, False, faceName="Century Schoolbook L")
        dlg = wx.MessageDialog( self, "Invictus is a sound-recognition POS application programme project conducted in CUHK", "About", wx.OK )
        dlg.SetFont(font2)
        dlg.ShowModal()# Show it
        dlg.Destroy() # finally destroy it when finished.
        
    def ResetButton(self):
        self.button1.SetBitmapLabel(self.image1)
        self.Refresh()
        self.WorkerRunning = False
        self.worker = None
        
    def OnButton1(self,event):
                   
                   
        if self.WorkerRunning is False:
            self.button1.SetBitmapLabel(self.image3)
            self.Refresh()
            print('Invictus System')
            self.worker = WorkerThread(self)
            self.WorkerRunning = True
            
            
            
        else:
            print ("Trying to stop")
            self.worker.abort()
            self.WorkerRunning = False
            self.worker = None
            self.button1.SetBitmapLabel(self.image1)
            self.Refresh()
            
                        
        
   
              
    #def OnButton3(self,event):
        #self.Close(True)  # Close the frame.

    def OnUpdate(self, event):
        self.textLabel.SetLabel(event.data)
        self.Update()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Invictus System") 
        frame.Show(True)
        frame.Centre()
        return True
        

        
app = MyApp(0)
app.MainLoop()


