'''The command line app but with a GUI'''

from typing import *
from Modules.MyUtils import WidgetFactory
from Modules.Widgets import Popup, ToggleButton, ToolTip, DimensionGetter
from RUAE_Revision import *
from tkinter import Tk, Button, Label, Frame, OptionMenu, BooleanVar, Radiobutton
from json import dump, load, decoder
from sys import exit
import asyncio

WINDOW = Tk()
WINDOW.minsize(645, 269)

class InfoButton(ToggleButton):
    brothers = []

    def __init__(self, info: str, factory: WidgetFactory, coords: Tuple[float, float], **kwargs):
        self.info = info
        ToggleButton.__init__(self, factory, coords, **kwargs)
        self.commands.append(self.loadInfo)

    def loadInfo(self):
        '''Search for the first Label popout and change its text to self.info'''

        for brother in InfoButton.brothers:
            if brother is self:
                continue

            brother.button.config(fg = brother.colours[0])

        for popout in self.popouts:
            if type(popout[0]) is Label:
                return popout[0].config(text = self.info)


class Page:
    '''Manages proper displaying of pages'''

    lightColours = {"bg" : "#ffffff", "fg" : "#1316e8"}

    darkColours = {"bg" : "#000000", "fg" : "#ffffff"}

    dark = None

    infoButtons = []  #must be cleaned up

    def __init__(self):
        # get theme
        if self.dark is None:
            Page.dark = BooleanVar()
            with open("settings.json") as f:
                try:
                    self.dark.set(load(f)["dark"])

                except decoder.JSONDecodeError:
                    error = Popup(title = "Settings Error", text = "Settings file is in the wrong format")
                    error._dieButton.config( command = lambda: exit(0))

            self.dark.trace("w", self.changeTheme)

        if self.dark.get():
            self.colours = self.darkColours
            backgroundColour = "#0d0d0d"

        else:
            self.colours = self.lightColours
            backgroundColour = "#d9d9d9"

        # create factory
        self.factory = WidgetFactory(master = WINDOW, **self.colours, relative = True, width = 18)

        # create background for clearing the screeen
        self.background = Frame(WINDOW, bg = backgroundColour)
        self.background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        # draw movement buttons
        # home button
        self.factory.generalBuilder(Button, (0, 0), relative = True, text ="HOME", command = lambda: self.movePage(InfoPage))

        # tools button
        self.factory.generalBuilder(Button, (0.25, 0), relative = True, text = "TOOLS", command = lambda: self.movePage(ToolsPage))


    def movePage(self, target):
        '''Move to target page'''

        InfoButton.brothers = []

        self.background.destroy()

        target()

    def changeTheme(self, *args):  #absorb context
        Popup(text = "Switch pages to apply the theme", title = "Theme Changed!")

        with open("settings.json", "r+") as f:
            # get current settings and replace only the theme
            json = dict(load(f))
            json["dark"] = self.dark.get()

            # go back to the start and overwrite
            f.seek(0)
            dump(json, f)
            f.truncate()  #prevent error if file is smaller


class InfoPage(Page):
    '''The page for UAE skills info'''

    def __init__(self):
        super().__init__()

        # info buttons
        info  = getJson()

        # create containers for buttons and info
        mainContainer = Frame(self.background, bg = self.colours["bg"])
        mainContainer.place(relwidth = 0.8, relheight = 0.4, relx = 0.5, rely = 0.35, anchor = "center")

        bottomContainer = Frame(self.background, bg = self.colours["bg"])
        bottomContainer.place(relwidth = 0.8, relheight = 0.4, relx = 0.5, rely = 0.8, anchor = "center")

        #create info buttons
        x = 2
        contents = self.factory.generalBuilder(Label, (0.5, 0.5), master = bottomContainer, anchor = "center", width = 100)  #where the info goes
        Frame(mainContainer, width = 20, height = 20, bg = self.colours["bg"]).grid(column = 0, row = 0, columnspan = 2)  #push the buttons into the right column

        for names, text in info.items():
            contents.place(relx = 0.5, rely = 0.5, anchor = "center")
            button = InfoButton(text, self.factory, (x, 0.33), text = f"{names[1].upper()}", popouts = (contents, ),
                fgColours = ("red", self.colours["fg"]), master = mainContainer)

            button.button.place_forget()
            button.button.grid(column = x, row = 2)

            x += 1


class ToolsPage(Page):
    '''Settings and guides on using the app'''

    def __init__(self):
        super().__init__()

        # change theme choice
        if self.dark.get():
            selectcolor = "black"

        else:
            selectcolor = "white"

        self.factory.generalBuilder(Label, (0.0, 0.3), text = "Use Dark Theme?", relative = True)
        darkChoiceYes = Radiobutton(self.background, variable = Page.dark, text = "Yes", value = True, **self.colours,
            borderwidth =0, selectcolor = selectcolor).place(relx = 0, rely = 0.4)

        darkChoiceNo = Radiobutton(self.background, variable = Page.dark, text = "No", value = False, **self.colours,
            borderwidth =0, selectcolor = selectcolor).place(relx = 0, rely = 0.5)

        # edit info
        self.factory.generalBuilder(Label, (0.6, 0.3), relative = True, text = f"HOW TO EDIT INFO\n{edit}", width = 65, anchor = "n")


InfoPage()
WINDOW.mainloop()
