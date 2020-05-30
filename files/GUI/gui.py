import tkinter
from tkinter import filedialog
from tkinter import messagebox as msg
from .. import Tester

class Window(tkinter.Frame):
    def __init__(self, master = None, debug:bool = True):
        """Constructor for the main gui window"""
        #Call the super class
        super().__init__(master)

        #Store variables
        self.master = master

        #Create dictionary to store buttons and labels
        self.buttons = {}
        self.labels = {}
        self.answer_var = tkinter.StringVar()
        self.filename = None
        self.debug = debug

        #Create the widgets
        self.create_widgets()
        

    def create_widgets(self) -> None:
        """Create the widgets on the GUI"""

        #Create the main label
        self.labels['main'] = tkinter.Label(text = "Language Tester")
        #Grid the main label
        self.labels['main'].grid(row = 0, column = 5, columnspan = 10)

        #Create an entry box for the person to key in the answer
        self.entry = tkinter.Entry(textvariable = self.answer_var)
        #Grid the entry box
        self.entry.grid(row = 5, column = 2, padx = 10, pady = 10, columnspan = 7)

        #Create a browse button for the user to browse files
        self.browse = tkinter.Button(text = "Browse", command = self.browse_file)
        #Grid the browse button
        self.browse.grid(row = 1, column = 10)

        #Generate a question label
        self.labels['question'] = tkinter.Label(text = "Please Load a CSV file")
        self.labels['question'].grid(row = 1, column = 0, columnspan = 10)

        #Next question button
        self.buttons['next'] = tkinter.Button(text = "Next Question", command = self.generate_question)
        self.buttons['next'].grid(row = 5, column = 10)

        #Create the submit buttonm
        self.buttons['submit'] = tkinter.Button(text = "Submit", command = self.handle)
        self.buttons['submit'].grid(row = 5, column = 9)

        #Create the check label
        self.labels['check'] = tkinter.Label(text = "")
        self.labels['check'].grid(row = 2, column = 0, columnspan = 5)

        #Create the accuracy label
        self.labels['accuracy'] = tkinter.Label(text = "Accuracy: 0.0%")
        self.labels['accuracy'].grid(row = 2, column = 5, columnspan = 5)

    def browse_file(self) -> str:
        """Allows the user to browse a file and return the filepath"""

        #Get the name of the file chosen
        self.filename = filedialog.askopenfilename(title = "Select A File", filetype = (("CSV files","*.csv"),))

        #If the user did not choose a file
        if self.filename == '':

            #Do nothing
            return

        #Check if there are any errors
        try:
            #Create an instance of the tester
            self.tester = Tester(self.filename, debug = self.debug)

            #Generate the next question
            self.generate_question()

        except Exception as exp:
            
            #Print an error message
            if self.debug:
                print(f"Error: {exp}")

            #Set it onto the screen
            self.labels['question']['text'] = f"Error: {exp}"

    def file_loaded(self) -> bool:
        """Checks whether the file is loaded properly"""
        return self.filename

    def handle(self) -> None:
        """Handle the question checking"""
        if not self.file_loaded():
            self.show_filenotloaded()
            return

        #If the answer is correct
        if self.check_answer():

            #Add the number of correct tests
            self.tester.add_correct()

            #Add a Label to show the user is correct
            self.labels['check']['text'] = f"You are correct"

        else:
            if self.debug:
                print(f"Answer is incorrect")

            #Add a Label to show the user is correct
            self.labels['check']['text'] = f"You are incorrect"

        #Update accuracy
        self.labels['accuracy']['text'] = f"Accuracy: {self.tester.get_accuracy()}"

        #Generates next question
        self.generate_question()
            
    def clear_entry(self):
        """Clear the entry"""
        self.entry.delete(0, tkinter.END)

    def generate_question(self) -> None:
        """Check the submission of the user"""
        if self.file_loaded():

            #Check the submission
            self.key,self.answer = self.tester.generate_test()

            #Load the key into the label
            self.labels['question']['text'] = f"What is the translation for: {self.key}"

            #Clear the entry:
            self.clear_entry()

        else:
            #Create warning box to ask user to browse for a valid data file
            self.show_filenotloaded()

    def check_answer(self) -> bool:
        """Check if the answer that is keyed is correct"""
        #Get the answer from the text variable
        ans = self.answer_var.get()

        if self.debug:
                print(f"Answer {self.answer}, User answer {ans}")

        #Compare it with the answer from the database and return
        return ans.strip().lower() in self.answer.strip().lower().split()

    def show_filenotloaded(self) -> None:
        msg.showwarning("Please Select a valid file", "Please select a valid csv file for the database\n")
        
