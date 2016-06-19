from Tkinter import Tk
import tkFileDialog


class InputHelper:
    def __init__(self):
        pass

    def get_file(self):
        root = Tk()
        root.withdraw()
        root.update()
        input_file = tkFileDialog.askopenfilename(parent=root)
        root.destroy()
        return input_file

    # Prompt for index of a field, display the first value, loop until user confirms input
    def get_value(self, question):
        return raw_input(question)

    # Prompt user for a Y/N answer; 'Y' and 'y' = True, everything else = False
    def yes_no(self, question):
        response = raw_input(question + " (Y/N) ")
        if response in ('Y', 'y'):
            return True
        else:
            return False

    def confirm_column(self, preview_line, entities):
        while True:
            column_index = int(self.get_value("What is the index of the column containing the " + entities + "? "))
            print "This is the first value in the column you specified: " + preview_line[column_index]
            if self.yes_no("Is that the correct column?"):
                return column_index
