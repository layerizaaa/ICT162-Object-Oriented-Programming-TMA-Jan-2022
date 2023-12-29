# after importing tkinter we will call it tk
import tkinter as tk
# import themed tk package
from tkinter import ttk
from tkinter import scrolledtext

from datetime import datetime
from question1 import Course


class GolfScheduleGUI_Grid:
    def __init__(self):
        self._win = tk.Tk()
        self._win.title('Golf Schedule - done by Leariza Vinteres') 
        self._win.geometry('510x600') 
        self._win.resizable(True, True)

        #create widgets
        self.create_widgets()

        # run the application infinitely, wait for event to occur
        self._win.mainloop()

    def create_widgets(self):
        #top level frame
        dataFrame = ttk.Frame(self._win)
        dataFrame.grid(column=0, row=0)

        #teeTime Label
        teeTime_lbl = ttk.Label(dataFrame, text="Tee Time: (HH:MM)")
        teeTime_lbl.grid(column=0, row=0, pady=8, sticky='E')

        #teeTime Entry
        self._teeTime = tk.StringVar()
        self._teeTime_Ety = ttk.Entry(dataFrame,
                                      width=15,
                                      textvariable=self._teeTime)
        self._teeTime_Ety.grid(column=1, row=0)

        #course Label
        course_lbl = ttk.Label(dataFrame, text="Course: ")
        course_lbl.grid(column=0, row=1, sticky='NE')

        #radio button frame
        radioFrame = ttk.Frame(dataFrame)
        radioFrame.grid(column=1, row=1)

        #radio button Value
        self._radValue = tk.IntVar()
        self._radValue.set(0)

        #create course radio buttons
        self._courseAugusta_rdbtn = ttk.Radiobutton(radioFrame,
                                                    text='Augusta',
                                                    variable=self._radValue,
                                                    value=0)
        self._courseLaguna_rdbtn = ttk.Radiobutton(radioFrame,
                                                   text='Laguna',
                                                   variable=self._radValue,
                                                   value=1)
        self._coursePebbleBay_rdbtn = ttk.Radiobutton(radioFrame,
                                                      text='Pebble Bay',
                                                      variable=self._radValue,
                                                      value=2)

        self._courseAugusta_rdbtn.grid(column=0, row=0, sticky='W')
        self._courseLaguna_rdbtn.grid(column=0, row=1, sticky='W')
        self._coursePebbleBay_rdbtn.grid(column=0, row=2, sticky='W')

        #button frame
        buttonFrame = ttk.Frame(dataFrame)
        buttonFrame.grid(column=1, row=4, pady=8)

        #button "Show Schedule" in button Frame
        self._showSched_btn = ttk.Button(buttonFrame,
                                         text='Show Schedule',
                                         command=self.getSchedule)
        self._showSched_btn.grid(column=0, row=0, padx=4, sticky= 'E')

        #button "Clear" in button Frame
        self._clear_btn = ttk.Button(buttonFrame,
                                     text='Clear',
                                     command=self.clear)
        self._clear_btn.grid(column=1, row=0, padx=4, sticky='E')
        self._clear_btn.config(state=tk.DISABLED)

        #bottom level frame
        outputFrame = ttk.Frame(self._win)
        outputFrame.grid(column=0, row=1, padx=8, pady=4, columnspan=3)

        # create mulit-line output 50 chars x 5 lines, word wrap
        self._scroll_txt = scrolledtext.ScrolledText(outputFrame,
                                                     width=60,
                                                     height=25,
                                                     wrap=tk.WORD)
        # place into GRID(0,0) of outputFrame
        self._scroll_txt.grid(column=0, row=0, sticky='NSWE')
        # no editing of this ScrolledText
        self._scroll_txt.config(state=tk.DISABLED)

        # indicate where the cursor should FOCUS at the start
        self._teeTime_Ety.focus()

    def getSchedule(self):
        self._scroll_txt.config(state=tk.NORMAL)

        try:
            #retrieve user teeTime input
            teeTime = self._teeTime.get()
            datetime.strptime(teeTime, "%H:%M")

            #check which radioButton is selected and call the class methods
            if self._radValue.get() == 0:
                course1 = Course('Augusta')
            elif self._radValue.get() == 1:
                course2 = Course('Laguna')
            else:
                course3 = Course('Pebble Bay')

        except Exception:
            self._scroll_txt.insert('end', '\nInvalid time input. Please enter time in HH:MM format. \n')

        else:
            if self._radValue.get() == 0:
                self._scroll_txt.insert('end', course1.getPlaySchedule(teeTime))

            elif self._radValue.get() == 1:
                self._scroll_txt.insert('end', course2.getPlaySchedule(teeTime))

            else:
                self._scroll_txt.insert('end', course3.getPlaySchedule(teeTime))

            self._teeTime.set("")

        finally:
            # turn OFF the mutli-line output
            self._scroll_txt.config(state=tk.DISABLED)
            # making sure the last line is visiable (can SEE)
            self._scroll_txt.see('end')
            self._teeTime_Ety.focus()
            self._clear_btn.config(state=tk.NORMAL)

    def clear(self):
        # enable the scrolledText, clear it, and disable
        self._scroll_txt.config(state=tk.NORMAL)
        self._scroll_txt.delete(1.0, tk.END)
        self._scroll_txt.config(state=tk.DISABLED)

        self._teeTime.set("")
        self._radValue.set(0)

        # reset the FOCUS to weight input, disable CLEAR button
        self._teeTime_Ety.focus()
        self._clear_btn.config(state=tk.DISABLED)

def main():
    GolfScheduleGUI_Grid()

main()