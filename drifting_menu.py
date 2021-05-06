# -*- coding: utf-8 -*-
"""
menu input screen for drifting.py
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import sys

def menu():
    #I don't know if I'll ever understand classes but this works so :shrug:
    class GetEntry():
    
        def __init__(self, master):
    
            self.master=master
            self.master.title('Drifting launcher by Zachary Picker')
            self.entry_contents=None
                       
            #title labels
            self.title = ttk.Label(text='\'Drifting\' launcher')
            self.title['font'] = font.Font(size=14)
            self.title.grid(row=0,column=0,sticky='w')
            self.name = ttk.Label(text = 'by Zachary Picker')
            self.name.grid(row=0,column=1,sticky='w')
            self.name['font']=font.Font(size=11)
            self.website = ttk.Label(text = 'zacpicker.com')
            self.website.grid(row=0,column=2,sticky='w')
            self.website['font'] = font.Font(size=11)
            ttk.Label(text='').grid(row=1,column=0)
            
            #performance mode or random mode:
            ttk.Label(text='Mode:').grid(row=2,column=0,sticky='w')
            self.modevar = tk.IntVar()
            self.modevar.set(0)
            self.modein0 = ttk.Radiobutton(master,text='Performance',variable=self.modevar,value=0)
            self.modein0.grid(row=2,column=1,sticky='w')  
            self.modein1 = ttk.Radiobutton(master,text='Random',variable=self.modevar,value=1)
            self.modein1.grid(row=2,column=2,sticky='w')  
            
            
            #performance time input
            ttk.Label(text='Performance time, minutes:').grid(row=5,column=0,sticky='w')
            self.ptimein = ttk.Entry(master)
            self.ptimein.insert(0,10)
            self.ptimein.grid(row=5,column=1,sticky='w')  

            #at performence end input
            ttk.Label(text='At performance end:',anchor = 'e').grid(row=6,column=0,sticky='w')
            self.endinvar = tk.IntVar()
            self.endinvar.set(0)
            self.endin0 = ttk.Radiobutton(master,text='loop performance',variable=self.endinvar,value=0)
            self.endin0.grid(row=6,column=1,sticky='w')  
            self.endin1 = ttk.Radiobutton(master,text='exit',variable=self.endinvar,value=1)
            self.endin1.grid(row=6,column=2,sticky='w')  
            self.endin2 = ttk.Radiobutton(master,text='continue last effect',variable=self.endinvar,value=2)
            self.endin2.grid(row=6,column=3,sticky='w')  
            
            #changing effect type
            ttk.Label(text='Effect-type changes:').grid(row=7,column=0,sticky='w')
            ttk.Label(text='(back: \'f\', forward:\'j\')').grid(row=7,column=3,sticky='w')
            self.effchvar = tk.IntVar()
            self.effchvar.set(0)
            self.effchin0 = ttk.Radiobutton(master,text='automatically',variable=self.effchvar,value=0)
            self.effchin0.grid(row=7,column=1,sticky='w')  
            self.effchin1 = ttk.Radiobutton(master,text='only on user input',variable=self.effchvar,value=1)
            self.effchin1.grid(row=7,column=2,sticky='w')  
            
            #daytime lengths
            ttk.Label(text='Relative time-of-day lengths:').grid(row=8,column=0,sticky='w')
            ttk.Label(text='Day').grid(row=8,column=1,sticky='w')
            ttk.Label(text='Sunset').grid(row=8,column=2,sticky='w')
            ttk.Label(text='Night').grid(row=8,column=3,sticky='w')
            ttk.Label(text='Sunrise').grid(row=8,column=4,sticky='w')
            ttk.Label(text='Day').grid(row=8,column=5,sticky='w')
            self.pdaytimein0 = ttk.Entry(master)
            self.pdaytimein0.insert(0,1)
            self.pdaytimein0.grid(row=9,column=1,sticky='w')  
            self.pdaytimein1 = ttk.Entry(master)
            self.pdaytimein1.insert(0,2)
            self.pdaytimein1.grid(row=9,column=2,sticky='w')  
            self.pdaytimein2 = ttk.Entry(master)
            self.pdaytimein2.insert(0,4)
            self.pdaytimein2.grid(row=9,column=3,sticky='w')  
            self.pdaytimein3 = ttk.Entry(master)
            self.pdaytimein3.insert(0,2)
            self.pdaytimein3.grid(row=9,column=4,sticky='w')  
            self.pdaytimein4 = ttk.Entry(master)
            self.pdaytimein4.insert(0,1)
            self.pdaytimein4.grid(row=9,column=5,sticky='w')  
            
            #effect-type lengths
            ttk.Label(text='Relative effect-type lengths:').grid(row=10,column=0,sticky='w')
            ttk.Label(text='Effect 1').grid(row=10,column=1,sticky='w')
            ttk.Label(text='Effect 2').grid(row=10,column=2,sticky='w')
            ttk.Label(text='Effect 3').grid(row=10,column=3,sticky='w')
            ttk.Label(text='Effect 4').grid(row=10,column=4,sticky='w')
            self.effecttypein0 = ttk.Entry(master)
            self.effecttypein0.insert(0,1)
            self.effecttypein0.grid(row=11,column=1,sticky='w')  
            self.effecttypein1 = ttk.Entry(master)
            self.effecttypein1.insert(0,1)
            self.effecttypein1.grid(row=11,column=2,sticky='w')  
            self.effecttypein2 = ttk.Entry(master)
            self.effecttypein2.insert(0,1)
            self.effecttypein2.grid(row=11,column=3,sticky='w')  
            self.effecttypein3 = ttk.Entry(master)
            self.effecttypein3.insert(0,2)
            self.effecttypein3.grid(row=11,column=4,sticky='w')
            
            #effect-order. yes I know this isn't actually a good way to do this...
            ttk.Label(text='Effect-type selection:').grid(row=12,column=0,sticky='w')
            ttk.Label(text='Effect 1:').grid(row=13,column=0,sticky='w')
            ttk.Label(text='Effect 2:').grid(row=14,column=0,sticky='w')
            ttk.Label(text='Effect 3:').grid(row=15,column=0,sticky='w')
            ttk.Label(text='Effect 4:').grid(row=16,column=0,sticky='w')
            self.eff1type = tk.IntVar()
            self.eff1type.set(0)
            self.eff2type = tk.IntVar()
            self.eff2type.set(1)
            self.eff3type = tk.IntVar()
            self.eff3type.set(3)
            self.eff4type = tk.IntVar()
            self.eff4type.set(2)
            self.efforin00 = ttk.Radiobutton(master,text='Bars',variable=self.eff1type,value=0)
            self.efforin00.grid(row=13,column=1,sticky='w')  
            self.efforin01 = ttk.Radiobutton(master,text='Mirrors',variable=self.eff1type,value=1)
            self.efforin01.grid(row=13,column=2,sticky='w')  
            self.efforin02 = ttk.Radiobutton(master,text='Outlines',variable=self.eff1type,value=3)
            self.efforin02.grid(row=13,column=3,sticky='w')  
            self.efforin03 = ttk.Radiobutton(master,text='All effects',variable=self.eff1type,value=2)
            self.efforin03.grid(row=13,column=4,sticky='w')
            self.efforin10 = ttk.Radiobutton(master,text='Bars',variable=self.eff2type,value=0)
            self.efforin10.grid(row=14,column=1,sticky='w')  
            self.efforin11 = ttk.Radiobutton(master,text='Mirrors',variable=self.eff2type,value=1)
            self.efforin11.grid(row=14,column=2,sticky='w')  
            self.efforin12 = ttk.Radiobutton(master,text='Outlines',variable=self.eff2type,value=3)
            self.efforin12.grid(row=14,column=3,sticky='w')  
            self.efforin13 = ttk.Radiobutton(master,text='All effects',variable=self.eff2type,value=2)
            self.efforin13.grid(row=14,column=4,sticky='w')     
            self.efforin20 = ttk.Radiobutton(master,text='Bars',variable=self.eff3type,value=0)
            self.efforin20.grid(row=15,column=1,sticky='w')  
            self.efforin21 = ttk.Radiobutton(master,text='Mirrors',variable=self.eff3type,value=1)
            self.efforin21.grid(row=15,column=2,sticky='w')  
            self.efforin22 = ttk.Radiobutton(master,text='Outlines',variable=self.eff3type,value=3)
            self.efforin22.grid(row=15,column=3,sticky='w')  
            self.efforin23 = ttk.Radiobutton(master,text='All effects',variable=self.eff3type,value=2)
            self.efforin23.grid(row=15,column=4,sticky='w')     
            self.efforin30 = ttk.Radiobutton(master,text='Bars',variable=self.eff4type,value=0)
            self.efforin30.grid(row=16,column=1,sticky='w')  
            self.efforin31 = ttk.Radiobutton(master,text='Mirrors',variable=self.eff4type,value=1)
            self.efforin31.grid(row=16,column=2,sticky='w')  
            self.efforin32 = ttk.Radiobutton(master,text='Outlines',variable=self.eff4type,value=3)
            self.efforin32.grid(row=16,column=3,sticky='w')  
            self.efforin33 = ttk.Radiobutton(master,text='All effects',variable=self.eff4type,value=2)
            self.efforin33.grid(row=16,column=4,sticky='w')        
                 
            #launch to black screen:
            ttk.Label(text='Launch to black screen:').grid(row=17,column=0,sticky='w')
            self.blackvar = tk.IntVar()
            self.blackvar.set(1)
            self.blackin0 = ttk.Radiobutton(master,text='No',variable=self.blackvar,value=0)
            self.blackin0.grid(row=17,column=1,sticky='w')  
            self.blackin1 = ttk.Radiobutton(master,text='Yes',variable=self.blackvar,value=1)
            ttk.Label(text=' (hit space/enter/j)').grid(row=18,column=2,sticky='w')
            self.blackin1.grid(row=17,column=2,sticky='w')  
            
            #launch button
            ttk.Label(text='').grid(row=29,column=0)
            ttk.Button(master,text="Launch",command=self.callback).grid(row=30,column=0,sticky='w')
            ttk.Style().configure('red.TLabel', foreground='red')
            self.badvalue = ttk.Label(text='',style = 'red.TLabel')
            self.badvalue.grid(row=30,column=1,sticky='w')
            
            #quit code on exit press
            self.master.protocol("WM_DELETE_WINDOW",self.on_closing)
            
        def on_closing(self):
            self.master.destroy()
            sys.exit()
            
        #either gets the input values to pass out of this function, or asks for sensible input   
        def callback(self):
            """ get the contents of the Entries and exit the prompt"""
            self.entry_contents=[self.ptimein.get(),
                                 self.endinvar.get(),
                                 self.effchvar.get(),
                                 self.pdaytimein0.get(),self.pdaytimein1.get(),self.pdaytimein2.get(),self.pdaytimein3.get(),self.pdaytimein4.get(),
                                 self.effecttypein0.get(),self.effecttypein1.get(),self.effecttypein2.get(),self.effecttypein3.get(),
                                 self.eff1type.get(),self.eff2type.get(),self.eff3type.get(),self.eff4type.get(),
                                 self.modevar.get(),
                                 self.blackvar.get()]
            for i in range(len(self.entry_contents)):
                try:
                    self.entry_contents[i] = float(self.entry_contents[i])
                    self.master.destroy()
                except Exception:
                    self.badvalue['text'] = 'Please enter only numbers'
    
    master = tk.Tk()
    outs=GetEntry(master)
    master.mainloop()
    output=outs.entry_contents
    return output
