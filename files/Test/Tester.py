import random
import csv

class Tester(object):

    def __init__(self, filepath:str, delimitter:str = "\t", debug:bool = False):
        """Main tester class"""
        
        #Save the variables
        self.filepath = filepath
        self.delimiter = delimitter if delimitter else "\t"
        self.debug = debug

        #Initialise data structures
        self.data = {}
        self.correct = 0
        self.total = 0

        #Load the file from the filepath
        self._load_data(filepath)
        self.create_set()

    def _load_data(self, filename) -> None:
        """Loads the data into the tester"""
        if self.debug:
            print("Loading File...")

        #Open the file and read the data
        with open(filename,mode = 'r',encoding = 'utf-8') as f:
            data = list(csv.reader(f,delimiter = self.delimiter))

        #Load the data into the dictionary
        for key,val in data[1:]:
            self.data[key] = val

        if self.debug:
            print("File loaded :D")

    def create_set(self) -> None:
        """Creates a set for the tester to test"""
        self.test_set = set(self.data.keys())

    def get_accuracy(self) -> int:
        """Get the % correct for the current user"""
        return self.correct * 100 // self.total

    def generate_test(self) -> tuple:
        """Generate the test"""

        #Pick a random item from the set
        key = random.sample(self.test_set, 1)[0]
        ans = self.data[key]

        #Add to the total tests generated
        self.total += 1
        
        #Return the tuple of the answer
        return key,ans

    def remove(self, key:str) -> None:
        """Remove a particular entry from the test"""
        return self.test_set.remove(key)

    def get_total(self) -> int:
        """Get the total number of test cases generated"""
        return self.total
    
    def get_correct(self) -> int:
        """Get the total number of correct answers"""
        return self.correct

    def get_incorrect(self) -> int:
        """Get the total number of incorrect answers"""
        return self.total - self.correct

    def add_correct(self) -> None:
        """Add 1 to the counter of correct answers"""
        self.correct += 1

    def test_cli(self) -> str:
        """Generate 1 test"""

        #If set does not exist
        if(not self.test_set):
            inp = input(f"You have completed the exercise\nDo you want to go again [y/n]: ")

            #If he does not want to continue
            if inp == 'n':
                return False

            #Create a new set
            self.create_set()

        #Generate the answer
        key,ans = self.generate_test()
        
        #Print out the English meaning and wait for key stroke
        inp = input(f"Write down '{key}' in correct language\nPress 'q' to quit or anything to continue: ")

        #Print the answer
        print(f"Answer: {ans}\n")

        #If the user wants to quit
        if inp == 'q':
            return False

        #Ask user if they got it right
        inp = input("Did you get it right [y/n]: ")

        #Check if the inputs are valid
        while inp.lower() != 'y' and inp.lower() != 'n':
            inp = input("Please choose a valid option: ")

        #If it was right remove from the pool
        if inp.lower() == 'y':
            self.remove(key)

            #Increment total correct number
            self.add_correct()
        
        #Return the input 
        return True


    def testloop(self)->None:
        """Loops the test in CLI"""

        #While the user does not want to quit
        while self.test_cli(): pass

        #When the user ends
        print(f"Accuracy: {self.get_accuracy()}%\nGoodbye")