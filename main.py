"""This is the main module of the project."""

import model.controller
import sys
from ui.ui import main, ft

if __name__ == "__main__":
    ux = input("Do you want to run the GUI? (y/n) ").lower()
    if ux == "y":
        ft.app(target=main)
    elif ux == "n":
        model.controller.main()
    else:
        print("Input invalid. Please enter 'y/n'. Exiting now...")
        sys.exit(1)
