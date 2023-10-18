from tkinter import *
from tkinter import messagebox
import pickle

class todo:
    def __init__(self, root):
        self.root = root
        self.root.title("To-do-list")
 #       self.root.geometry('700x450')

        self.label = Label(self.root, text="To-Do-List Application", width=60, font=("ariel", 10, "italic", "bold"), bd=2, bg="#008080", fg="white", )  
        self.label.pack() 

        frame = Frame(self.root)
        frame.pack()

        self.list_box = Listbox(frame, height=10, width=70)
        self.list_box.pack(side='left')

        # A scroll feature which gives us the ability to scroll down or up just incase out tasks is more than the provided geometry for the listbox
        scroller = Scrollbar(frame)
        scroller.pack(side='right', fill=Y)

        self.list_box.config(yscrollcommand=scroller.set)
        scroller.config(command=self.list_box.yview)

        self.text = Entry(self.root, width=75)
        self.text.pack() 

        #To be able to add task
        def add():
            content = self.text.get()
            if content != "":
                self.list_box.insert(END, content)
                self.text.delete(0, END)
            else:
                messagebox.showwarning(title="Attention!!", message="You must enter a task.")  
        #To be able to delete task          
        def delete():
            try:
                content_index = self.list_box.curselection()[0]
                task_to_delete = self.list_box.get(content_index)
                self.list_box.delete(content_index)
            except:
                messagebox.showwarning(title="Attention!!", message="You must enter a task.")  
        # To be able to load task         
        def load():
            try:
                with open("data.txt", "rb") as f:
                    tasks = pickle.load(f)
                    self.list_box.delete(0, END)
                for task in tasks:
                    self.list_box.insert(END, task)
            except:
                messagebox.showwarning(title="Attention!!", message="Cannot find data.txt file.")    
        # To be able to save task             
        def save():
            tasks = self.list_box.get(0, self.list_box.size())
            with open("data.txt", "wb") as f:
                pickle.dump(tasks, f)
        # for hover features on my buttons        
        def on_enter(e):
            self.add_task['background'] = "#00ffff"
           
        def on_leave(e):
            self.add_task['background'] = "#008080" 
            
                      

        self.add_task = Button(self.root, text="Add task", width=60, font=("ariel", 10, "italic", "bold"), bd=2, bg="#008080", fg="white", command=add)
        self.add_task.bind("<Enter>", on_enter)
        self.add_task.bind("<Leave>", on_leave)
        self.add_task.pack()

        self.delete_task = Button(self.root, text="Delete task", font=("ariel", 10, "italic", "bold"), bd=2, bg="#008080", fg="white", width=60, command=delete)
        self.delete_task.pack()

        self.load_task = Button(self.root, text="Load task", width=60, font=("ariel", 10, "italic", "bold"), bd=2, bg="#008080", fg="white", command=load)
        self.load_task.pack()

        self.save_task = Button(self.root, text="Save task", width=60, font=("ariel", 10, "italic", "bold"), bd=2, bg="#008080", fg="white", command=save)
        self.save_task.pack()

def main():
    root = Tk()     #Create a special window
    my_todo = todo(root)    # Make a to-do list in that window
    root.mainloop()         # Show the window on the computer screen when you run the program

if __name__ == "__main__":   #This means that when the name that is specified when you want to run the program is the same as the name that this particular file is saved with then it should run the main function
    main()    