import argparse
import tkinter
from files import Window

def CLI() -> None:
    """The main function for the Tester"""

    #Create the CLI interface
    parser = argparse.ArgumentParser(description="Language Tester")

    #Add the relevant arguments
    parser.add_argument("Filepath")
    parser.add_argument("Language")
    parser.add_argument("--d",dest = "Delimiter", default = '\t', required=False)
    
    #Parse the arguments
    args = parser.parse_args()
    delimitter = args.Delimiter if args.Delimiter else None
    language = args.Language
    filepath = args.Filepath

    #Creating the tester object
    tester = Tester(filepath, language, delimitter)

    #Running the test loop
    tester.testloop()

def gui():
    """The main function for the file"""
    #Create the tkinter main window
    root = tkinter.Tk()

    #Set the title and the geometry
    root.title("Language Tester")
    root.minsize(600,400)
    root.resizable(width=tkinter.FALSE, height=tkinter.FALSE)

    #Create the application
    app = Window(root)
    app.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    #Run the mainloop for the application
    app.mainloop()

#If the file is run as the main file run the main function
if __name__ == '__main__':
    gui()


