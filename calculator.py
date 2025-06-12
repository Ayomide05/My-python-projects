from tkinter import *
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator App")
        self.root.geometry('376x600')
        self.root.resizable(0,0)
        
        self.total_expression = ""
        self.current_expression = ""

        self.digit_positions = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            0:(4,2), '.':(4,1)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+":"+"}
     
    # To create frame. one frame for the display section and the other one for the buttons
        self.display_frame = Frame(self.root, height="220", bg="#F5F5F5")
        self.display_frame.pack(expand=True, fill="both")

        self.button_frame = Frame(self.root)
        self.button_frame.pack(expand=True, fill="both")
        
        #The display frame consist of two lables, one which displays the current expression the user is currently entering, while the total expression displays the total calculation including the previous calculations
        self.total_expression_label = Label(self.display_frame, text=self.total_expression, font=("Arial", 12, "normal"), bg="#F5F5F5", fg="#25265E",anchor=E, padx=24)
        self.total_expression_label.pack(expand=True, fill="both")

        self.current_expression_label = Label(self.display_frame, text=self.current_expression, font=("Arial", 16, "bold"),bg="#F5F5F5", fg="#25265E", anchor=E, padx=24)
        self.current_expression_label.pack(expand=True, fill="both")

        # Create digit and operator buttons
        self.create_digit_button()
        self.create_operator_button()
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
    #Method Add_to_expression that add a given value to the current expression
    def add_to_expr(self,value):
       self.current_expression += str(value)
       self.update_current_label() 

    def create_digit_button(self):
        for digit, grid_value in self.digit_positions.items():
            button = Button(self.button_frame, text=str(digit), bg="white", fg="#25265E", font=("Arial", 24, "bold"), borderwidth=0, command=lambda x=digit: self.add_to_expr(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=NSEW)

    #Method append_operator that gices functionality to our operator button   
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_current_label()
   
    def create_operator_button(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = Button(self.button_frame, text=symbol, bg="#FAFAFF", fg="#25265E", font=("Arial", 20), borderwidth=0, command=lambda x=operator: self.append_operator(x))         
            button.grid(row=i, column=4, sticky=NSEW)
            i +=1
    #Method that add functionality to the clear button
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_current_label()
        self.update_total_label()    

    def create_clear_button(self):
        button = Button(self.button_frame, text="C", bg="#FAFAFF", fg="#25265E", font=("Arial", 20), borderwidth=0, command=self.clear)         
        button.grid(row=0, column=1, sticky=NSEW)
    #Method to add functionality to the square button
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_current_label()
    #Function to add the square button
    def create_square_button(self):
        button = Button(self.button_frame, text="x\u00b2", bg="#FAFAFF", fg="#25265E", font=("Arial", 20), borderwidth=0, command=self.square)         
        button.grid(row=0, column=2, sticky=NSEW)    
    
    #Method to add functionality to the square root button
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_current_label()
    #Function to add the square root button
    def create_sqrt_button(self):
        button = Button(self.button_frame, text="\u221Ax", bg="#FAFAFF", fg="#25265E", font=("Arial", 20), borderwidth=0, command=self.sqrt)         
        button.grid(row=0, column=3, sticky=NSEW) 
    #Method to evaluates our operations which returns the value of a valid python expression using eval function
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        #To handle Exception error
        try:
            self.current_expression = str(eval(self.total_expression)) 

            self.total_expression = ""
        except:
            self.current_expression = "Error"
        finally:
            self.update_current_label()    
        

    def create_equals_button(self):
        button = Button(self.button_frame, text="=", bg="#CCEDFF", fg="#25265E", font=("Arial", 20), borderwidth=0, command=self.evaluate)         
        button.grid(row=4, column=3, columnspan=2, sticky=NSEW) 

    #To expand our buttons to fill up the whole button frame
        self.button_frame.rowconfigure(0, weight=1)
        for x in range(1,5):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)  
    #Function that help to update or current_label and total_label
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_expression_label.config(text=expression)

    def update_current_label(self):
        self.current_expression_label.config(text=self.current_expression) 
   
                      

def main():
    root = Tk()     #Create a special window
    my_calc = Calculator(root)    # Make a calculator application in that window
    root.mainloop()        # Show the window on the computer screen when you run the program

if __name__ == "__main__":   #This means that when the name that is specified when you want to run the program is the same as the name that this particular file is saved with then it should run the main function
    main()            