'''Command line version of the app'''

from json import load, decoder
from typing import Tuple, Dict
from sys import exit
from Modules.Widgets import Popup

def getJson()-> Dict[Tuple[str,], str]:
    #get file
    with open("skills.json") as f:
        try:
            json = load(f)
            #convert keys back to list
            return {tuple(key.split(", ")) : value for key, value in dict(json).items()}

        except decoder.JSONDecodeError:
            error = Popup(title = "Skills Error", text = "Skills file is in the wrong format")
            error._dieButton.config( command = lambda: exit(0))
            error._window.mainloop()


def searchKey(target: str, json: Dict[Tuple[str,], str]) -> str:
    '''Return a search's result from the JSON
    
    RAISES
    ValueError: key not in JSON'''

    for key, value in json.items():
        if target in key:
            return value

    raise ValueError("Target not found")


# show help
help = '''Commands:
help: display this.
edit: displays how to edit the question info/add info.

GET QUESTION INFORMATION COMMANDS
"u" or "understanding"
"a" or "analysis"
"e" or "evalutation"

'''

edit = r'''Step 1: Go into the folder of this script.
Step 2: Select "skills.json" and open it in a text editor
Step 3: either use a JSON editor online or edit it manually.
If editing manually: the format is "alias, alias" : "info". "\n" represents a new line.

Alternatively if you have Python, you can open "dumpToSkills.py" with a text editor,
and edit the information enclosed in {}.
Then run "dumpToSkills.py" from CMD by copying its file path,
and add "dumpToSkills.py" to the end.
E.G: C:/desktop/RUAE/dumpToSkills.py
This will ensure that the format is correct.

'''

if __name__ == "__main__":
    print(help)

    #get search
    while True:
        search = input("Input command.\n")

        try:
            print(searchKey(search))

        except ValueError:
            if "help" in search:
                print(help)

            elif "edit" in search:
                print(edit)

            else:
                print("Invalid command.\n")
