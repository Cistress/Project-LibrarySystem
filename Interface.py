import customtkinter as ctk
import pandas as pd
import random


# Top level class
class Toplevel_win(ctk.CTkToplevel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x200")
        self.title("Registration")
        self.wm_attributes("-topmost", True)

        self.password = []
        # generating password
        def generating_password():
            while len(self.password) < 6:
                _ = random.randint(0,9)
                self.password.append(_)
            self.password = "".join(str(x) for x in self.password)
        # making sure no same passwords
        def double_check():
            generating_password()

            same_combi = True

            with open("user_id.csv", "r") as user_file:
                user_df = pd.read_csv(user_file)
                for row in user_df["ID"]:
                    while same_combi:
                        if self.password == row:
                            generating_password()
                        else:
                            user_df.loc[len(user_df.index)] = [self.name_entry.get().upper(), self.password]
                            user_df.to_csv("user_id.csv", index=False)
                            same_combi = False
                            print("Account created successfully")
        # username prompting
        self.name_label = ctk.CTkLabel(self,text= "What would you like your username to be? :")
        self.name_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
        # confirm button?
        self.confirm_button = ctk.CTkButton(self, text= "Confirm", command = double_check)
        self.confirm_button.grid(row = 1, column = 0, padx = 10, pady = 10)
#--------------------------------------------------------------------------------------
# Ctk frame
class CtkEntryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # borrow function
        def borrow():
            # inquiries
            book_inquiry = self.option_menu.get()
            ID_inquiry = int(self.id_entry.get())

            borrow_successful = False

            with open("user_id.csv", "r") as file:
                user_df = pd.read_csv(file)
                for row in user_df['ID']:
                    if ID_inquiry == row:
                        borrow_successful = True

            with open("borrowing_record.csv", "r") as csv_file:
                borrowing_record_df = pd.read_csv(csv_file)
                # add new line
                if borrow_successful:
                    borrowing_record_df.loc[len(borrowing_record_df.index)] = [book_inquiry, ID_inquiry]
                    #borrowing_record_df.reset_index(drop=True, inplace=True)
                    borrowing_record_df.to_csv("borrowing_record.csv", index = False)
                    print(f"You have borrowed {book_inquiry} successfully!")
                else:
                    print("Sorry, the user ID is not registered, please become a member first.")

        # return function
        def returning():
            book_inquiry = self.option_menu.get()
            ID_inquiry = int(self.id_entry.get())

            with open("borrowing_record.csv", "r") as file:
                borrowing_record_df = pd.read_csv(file)
                for index, row in borrowing_record_df.iterrows():
                    if ID_inquiry == row["ID"] and book_inquiry == row ["title"]:
                        # open the file again since we left the indented block
                        book_recording_df = pd.read_csv("borrowing_record.csv")
                        # drop the returned line
                        book_recording_df.drop(index, inplace = True)
                        book_recording_df.to_csv("borrowing_record.csv", index = False)
                        print(f"You have returned {book_inquiry} successfully!")
                    else:
                        print(f"Sorry, are you sure you borrowed the {book_inquiry} at the first place?")


        #ID
        self.id_label = ctk.CTkLabel(self, text= "ID-number: ")
        self.id_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.id_entry = ctk.CTkEntry(self)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)
        # option menu
        self.option_label = ctk.CTkLabel(self, text = "Title of the book: ")
        self.option_label.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.option_menu = ctk.CTkOptionMenu(
            self,
            values = ["Pride and Prejudice","It","Frankenstein","Running the light","rising man"]
        )
        self.option_menu.grid(row = 1, column = 1, padx = 10, pady = 10)
        # Borrow button
        self.borrow_button = ctk.CTkButton(self, text = "Borrow", command = borrow)
        self.borrow_button.grid(row = 2, column = 0, padx = 10, pady = 10)
        # Return button
        self.return_button = ctk.CTkButton(self, text = "Return",command = returning)
        self.return_button.grid(row = 2, column = 1, padx = 10, pady = 10)
    # -------------------------------------------------------------------
        # Top level
        self.toplevel_window = None

        self.sign_in_button = ctk.CTkButton(self, text="Registration", command= self.open_toplevel)
        self.sign_in_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")
    # you dont need to put the function inside "super init" because it has no inheritance from it
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Toplevel_win(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
#--------------------------------------------------------------------

class app(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("borrow & return system")
        self.geometry("510x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # calling Entry frame class
        entryframe = CtkEntryFrame(master= self)
        entryframe.grid(row = 0, column = 0, sticky = "new", padx = 10, pady = 10)


app = app()
app.mainloop()