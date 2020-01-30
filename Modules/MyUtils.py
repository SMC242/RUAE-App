'''Utility functions that don't don't belong in any classes
and classes that don't really belong to the Optimisation project'''
from tkinter import *
from typing import Union, Callable , Any, Tuple, List

def bubbleSort(varList: list)-> list:
    '''Sorts a list of numbers ascending
    varList: a list of items to be sorted'''
    upper=len(varList)
    for i in range(0,upper):
        for index in range(0, (upper-1)):
            if varList[index]>varList[index+1]:
                varList[index+1], varList[index]=varList[index], varList[index+1]

    return varList


def binarySearch(search: str, returnBool: bool, file: str=None, varList: list=None)->Union[int, bool]:
    '''Binary searches the input file path or list for search.
    Outputs either the index or a boolean value.
    returnBool: 
    file: the string file path to be searched. Defaults to None
    varList: the list to be searched. Defaults to None'''

    #ensuring that a file or list is passed in
    fail=False

    isFile=file is None
    if isFile is True:
        fail=varList is None
        if fail:
            raise Exception("Internal error: no file or list passed into binarySearch")

    if not isFile:
        with open(file) as f:
            fileText=f.readlines()
            lines=[]
            for item in fileText:
                newItem=item.strip("\n")
                lines.append(newItem)

    else:
        lines=varList

    #standard binary search algorithm
    lower=0
    upper=len(lines)-1
    found=False
    while lower<=upper and not found:
        mid=(lower+upper)//2
        if lines[mid]==search:
            found=True

        elif search<lines[mid]:
            upper=mid-1

        else:
            lower=mid+1

    if returnBool:#returns boolean
        return found
    else:#returns index
        return mid


def fileLength(f: str)->int:
    '''Opens the file and returns the number of lines. File path must be passed in.'''
    index=0
    with open(f) as f:
        for index, l in enumerate(f):
            pass
    return index+1


def validateInput(input: str)->bool:
    '''Validates the input string, float, or integer. input is the input to be validated.
    Returns boolean'''
    isString=isinstance(input,str)

    #strings
    if isString==True:
        if len(input)==0 or input== ' ':
            return True #use this boolean to know whether to re-ask the question
    else:
        return False
    
    #numbers
    if isString==False:
        if input==0 or input<0 or len(input)==0:
            return True
        else:
            return False


def fillListFromFile(file: str, floatVal: bool, varList: list=[])-> list:
    '''Takes in a file path and fills the input array with the contents of the file.
    varList: the list to fill. It will create itself if no list is passed in
    file: the file object
    floatVal: boolean value to indicate whether the file contents are numbers'''

    try:
        with open(file) as f:
            for line in f:
                newLine=line.strip("\n")
                newLine=newLine.lower()
                if floatVal:
                    newLine=float(newLine)
                varList.append(newLine)

        return varList

    except:
        raise Exception(f"{file} not found")


def removeFromDict(original: dict, toRemove: Union[Tuple, List])-> Tuple[dict, dict]:
    '''Removes the keys of toRemove from the original dictionary.
    Returns the edited dict.
    Pure function as it does not edit the original dict.

    original: the dict to be edited
    toRemove: list or tuple of keys to remove from original
    labelParams=kwargsDict'''

    editedDict={}
            
    for key, value in original.items():
        try:
            if key not in toRemove:
                editedDict[key]=value

        except KeyError:
            #debugging information to remove upon release
            print(f"Key ({key}) not in original")

    return editedDict


class WidgetFactory:
    '''Class to define the default settings for the factories.
    
    ATTRIBUTES
    defaultAttrs: dict of the default settings that are overridden at instantiation.
    These are applied unless overridden by the builders'''

    #attributes
    defaultAttrs={
        'labelText': None,
        'command': None,
        'borderwidth': 0,
        'master': None,
        'fg': "white",
        'bg': "black",
        'text': None,
        'anchor': None,
        'relative': None,
        'sticky': None
        }

    def __init__(self, **kwargs):
        '''Pass in any settings that should be applied by default by the builders'''

        #override the default attrs
        for attr in list(kwargs.keys()):
            self.defaultAttrs[attr]=kwargs[attr]


    def setToDefaults(self, kwargsDict):
        '''Checks if the defaults have been overridden, 
        if not then sets them to default and returns as a
        dict of variable name : value

        kwargsDict: dictionary of keyword arguments.'''

        #will store all  pairs
        arguments={}

        #create list of names of variables where variable=None
        #append input dict to arguments
        isNone=[]
        for key in kwargsDict:
            if kwargsDict[key] is None:
                isNone.append(key)
                
            else:
                arguments[key]=kwargsDict[key]

        #check if a default value for it is stored
        for key in isNone:
            try:
                arguments[key]=self.defaultAttrs[key]

            except KeyError:  #ignore unknown keys
                pass

        #append all default values to dict if not already given a value
        for key, value in self.defaultAttrs.items():
            if key not in arguments.keys():
                arguments[key]=value

        return arguments


    def generalBuilder(self, type: Widget, coords: tuple, *args: tuple, **kwargs) -> Tuple:

        '''Factory to create most widgets with common arguments. 

        Use .config() on the results of this method to add extra attributes.
        Returns Widgets as a tuple as either (widget) or (label, widget)
        Not compatible with OptionMenu and Frame.

        Widget Attribute Arguments:
        type: tkinter widget class.
        co-ords: tuple of floats (x, y) to place the widget at.

        KWARGS:
        labelText: text for a label to be placed at co-ords(x, y-20).
        command: anonymous function to activate upon click of widget.
        create an anonymous function inline like this:
        command=lambda: func(args)
        borderwidth: float for the border size.
        master: Tk object to place the widget in.
        height: float height of the widget.
        width: float width of the widget.
        fg: string foreground colour.
        bg: string background colour.
        
        Placement Arguments:
        anchor: string anchor point.
        relative: boolean to define whether co-ords are relative.
        sticky: string sticky cardinal direction. These are inverted.
        
        THROWS
        KeyError: if a default setting has been removed from WidgetFactory.defaultAttrs
        '''

        #this function assumes that no elements will be removed from
        #WidgetFactory.defaultAttrs

        #set any NoneType kwargs to their defaults
        kwargsDict=self.setToDefaults(kwargs)

        #if labelText has a value, place a label at x, y-20
        if kwargsDict["labelText"]:
            #getting rid of incompatible kwargs
            labelParams=removeFromDict(kwargsDict, ["command", "text", "relative", "sticky"])

            #retrieving label text which is not compatible with label
            labelText=labelParams.pop("labelText")

            newLabel = Label(text =labelText, **labelParams)

            #if relative, place at y - 20% of y
            if kwargsDict["relative"]:
                newLabel.place(relx = coords[0], rely = coords[1] -(coords[1]*0.2), \
                    anchor = kwargsDict["anchor"], sticky = kwargsDict["sticky"])
            else:
                newLabel.place(x = coords[0], y = (coords[1]-20), \
                    anchor = kwargsDict["anchor"], sticky = kwargsDict["sticky"])


        #removing inconpatible params
        widgetParams=removeFromDict(kwargsDict, ["anchor", "sticky", "relative", "labelText"])

        #expands the dictionary into kwargs again (key = value)
        newWidget=type(**widgetParams)

        #placing the widget
        if kwargsDict["relative"]:
            newWidget.place(relx = coords[0], rely = coords[1],\
                anchor = kwargsDict["anchor"], sticky = kwargsDict["sticky"])

        else:
            newWidget.place(x = coords[0], y = coords[1],\
                anchor = kwargsDict["anchor"], sticky= kwargsDict["sticky"])

        if kwargsDict["labelText"]:
            return (newLabel, newWidget)

        else:
            return (newWidget)

