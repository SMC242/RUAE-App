'''This module contains all of the custom Widget/window classes'''

from tkinter import Tk, Button, IntVar, StringVar, DoubleVar, BooleanVar, Entry, Label, Widget, Toplevel, Frame, Message
from typing import Tuple, Callable, Union, List
from Modules.MyUtils import WidgetFactory
from sys import exc_info
import traceback

class Popup:
    '''Popup class intended to be used for errors,
   but flexible enough to be used for any popup
   
   ATTRIBUTES
   instances: dict of the currently alive instances.

   _population: integer for tracking current number of instances and auto-triggering culling.
   Popups are culled every 2 open popups. If modified: the user must clean up the instances attr accordingly.
   _name: string to describe the purpose of the popup. Composite key of name+population.
   _window: the root window of the popup.
   _errorBackground: all widgets are placed on this. Destroy it to clear the popup.
   _message: Message widget that contains the input text.
   _dieButton: Button to close the widget.
   '''

    #attributes
    _population=0
    instances={}

    def __init__(self, text: str="Something went wrong",\
       title: str="Error!", name: str=None):
        '''Builds a custom popup

        ARGUMENTS:
        factory: used to build the widgets

        text: (optional) the text for the message.
        Defaults to 'Something went wrong.'

        title: (optional) the window title. 
        Defaults to 'Error'

        name: the name of the instance. Used to reference the instance
        from the instances attribute and should describe the instance of the popup.
        The current population will be appended to the attribute to ensure it's unique.
        Defaults to the title plus the current population.
        '''

        #culling the population if too many popups are active
        if self._population>=2:
            for name, instance in reversed(list(self.instances.items())):
                instance._window.destroy()
                del Popup.instances[name]
                Popup._population-=1

        #create window
        self._window=Tk()
        self._window.protocol("WM_DELETE_WINDOW", self.close)  #close is called when the window is closed by user
        self._window.title(title)

        #create background
        self._errorBackground=Frame(self._window, height=200, width=200)
        self._errorBackground.grid(row=0, column=0)

        #create message
        self._message=Message(text=text, master=self._window, fg="red", width=120)
        self._message.place(x =100, y=75, anchor="center")

        #create dismiss button
        self._dieButton=Button(text="OK", command=self.close, master=self._window)
        self._dieButton.place(x=100, y=125, anchor="center")

        #update population
        Popup._population+=1
        if name is not None:
            self._name=f"{name}{self._population}"  #population appended to ensure it's unique

        else:
            self._name=f"{title}{self._population}"

        Popup.instances[self._name]=self


    def close(self):
        '''Kills the window and cleans up the class data'''

        try:
            del Popup.instances[self._name]

        except KeyError:
            #KeyError would mean that __init__ failed before the end
            #perhaps add a status attribute
            #and log death circumstances instead of silencing this
            pass
            
        try:
            self._window.destroy()

        except:
            #will result in an infinite loop if this is caused by a code error
            Popup(text="Unable to kill popup", title="Popup error!", name="Popup Error")


class ToolTip(Toplevel):
    '''Class to create tool tips when hovering over a widget.
    Supports grouping widgets under one ToolTip instance.

    ATTRIBUTES
    _widgets: list of parent widgets of the tooltip.
    label: the widget that displays the text.
    text: the string text of the label. Does not change.
    getText: the function that returns the text for the label on each hover.
    Allows for dynamic text such as displaying current state.
    '''

    def __init__(self, widget: List[Widget], text: str=None, getText: Callable=None):
        '''ARGUMENTS
        widget: the parent widget(s) of the ToolTip. The tooltip will show when the widget(s) is hovered.
        
        One of the following must be included:
        text: static text to be displayed in the tooltip
        getText: function to execute to return the text of the tooltip.

        RAISES
        ValueError: Either text or getText must be given.
            One of the two arguments is required.

        ValueError: One or more widgets' masters are unequal.
            Every widget must have the same master.
        '''

        if text is None and getText is None:
            raise ValueError("Either text or getText must be given")

        self._widgets=widget
        self._master=self._widgets[0].master

        #verifying that all masters are the same
        if len(self._widgets)!=0:
            for widget in self._widgets:
                if widget.master is not self._master:
                    raise ValueError("One or more widgets' masters are unequal")

        #self becomes an instance of Toplevel
        Toplevel.__init__(self, master=self._master)
        
        #hide the toplevel immediately and remove its border + exit buttons
        self.withdraw()
        self.overrideredirect(True)

        if text is not None:
            self.label=Label(master=self, text=text)
            self.label.pack()
            self.getText=None

        else:
            self.label=Label(master=self, text="")
            self.label.pack()
            self.getText=getText

        for widget in self._widgets:
            widget.bind("<Enter>", self.display)
            widget.bind("<Motion>", self.goToWidget)
            widget.bind("<Leave>", self.die)
        

    def display(self, event=None):  #the context is taken in to silence it
        '''Wrapper for Toplevel.deiconify to show the popup when needed.
        Necessary because events pass a context object into the callback so
        deiconify gets unexpected arguments'''

        if self.getText is not None:
            self.label.config(text=self.getText())

        self.deiconify()


    def die(self, event=None):  #again the context must be silenced
        '''Wrapper for Toplevel.withdraw to make the popup disappear.
        Necessary due to the event object passed to an event's callback'''

        self.withdraw()


    def goToWidget(self, event=None):
        '''Moves the tip to where the cursor is instead of the top left corner'''

        self.geometry(f"+{event.x_root+10}+{event.y_root+10}")  #not exactly placed on cursor to avoid interferance
        self.display()


class ToggleButton():
    '''Button subclass that toggles its state when clicked'''

    #attributes
    __state=False
    colours=("red", "green")

    def __init__(self, factory, coords: Tuple[int, int], command: Callable=None,\
       fgColours: Tuple[str, str]=None, popouts: Tuple[Widget,] = [], **kwargs):
        '''Wraps the widget factory to create a button that can toggle its state
        
        ARGUMENTS
        factory: an instance of Modules.MyUtils.WidgetFactory.
        Used to build the widgets.
        coords: tuple of float coordinates to place the button at
        command: the function to be called upon state toggle as well as toggling the state.
        Must be anonymous.
        fgColours: tuple of strings of the colours to toggle between.
        Format= ({state=off colour}, {state=on colour})
        Defaults to (red, green)
        popouts: placed widgets to popout upon state change.
        **kwargs: dict of extra settings for the button. Do not include the command
        '''

        def validatePopoutType(var):
            '''Checks if var is a tkinter variable type'''
            #type enforcing is not a good practice
            #this should be patched if it becomes a problem
            validTypes=[StringVar, IntVar, DoubleVar, BooleanVar]
            
            #checks against every type
            for type in validTypes:
                if isinstance(var, type):
                    return True

            #if list of type is exhausted, it must be of the wrong type
            raise TypeError("Popout var is not a tkinter type")


        self.factory=factory


        #set commands
        self.commands=[self.stateChange] #list of anonymous functions to call upon button press

        if command is not None:
            self.commands.append(command)

        #create button
        self.button=factory.generalBuilder(Button, (coords[0], coords[1]),\
            relief="raised", **kwargs)


        #set colours
        if fgColours is not None:
            self.colours=fgColours

        self.button.config(fg=self.colours[0])

        #handling popouts
        self.popouts = []
        for popout in popouts:
            info = popout.place_info()

            relx = float(info["relx"])
            rely = float(info["rely"])
            x = int(info["x"])
            y = int(info["y"])
            anchor = info["anchor"]

            #check if relative. If relative is deliberately 0, it doesn't matter if changed to absolute
            if (any((relx, rely)) > 0) and (x == 0 and y == 0):
                self.popouts.append((popout, (info["relx"], info["rely"]), True, anchor))

            else:
                self.popouts.append( (popout, (info["x"], info["y"]) , False, anchor))

            popout.place_forget()

        self.commands.append(self.popOutTextBox)

        #allowing tooltips to appear to show state
        #for accessibility I don't want to rely on colours only to show state
        self._tooltip=ToolTip([self.button], getText=lambda: f"State: {self.state}")

        self.button.config(command= self.callCommands)


    def callCommands(self):
        '''Wrapper to call each function in funcs with their arguments

        funcs: list of functions to be called
        args: list of tuples of arguments to be passed into funcs. 
        Must be in order. Pad with (None) where there are no arguments.'''

        for command in self.commands:
            try:
                command()

            #debugging tool. can be removed later
            except Exception:
                traceback.print_exc()


    def stateChange(self):
        '''Toggles the state of the button'''

        #changing the state
        self.__state=not self.__state

        #choosing the colour to change the fg attribute to
        #0=off, 1=on
        if self.__state:
            index=1
            self.button.config(relief="sunken")

        else:
            index=0
            self.button.config(relief="raised")

        self.button.config(fg=self.colours[index])


    def popOutTextBox(self):
        if self.state:
            for popout, coords, relative, anchor in self.popouts:
                if relative:
                    popout.place(relx = coords[0], rely = coords[1], anchor = anchor)

                else:
                    popout.place(x = coords[0], y = coords[1], anchor = anchor)

        else:
            for widget, *_ in self.popouts:
                widget.place_forget()

    #getters
    @property
    def state(self):
        '''Getter for self.state'''
        return self.__state

class DimensionGetter():
    '''Prints the dimensions of the master on click. Developer tool'''

    def __init__(self, master: Union[Tk, Widget]):
        '''Adds a button to master to track its dimensions
        '''
        self.master = master
        Button(master, text = "Print Dimensions", command = lambda: print(f"{self.master.winfo_width()}, {self.master.winfo_height()}")).pack()