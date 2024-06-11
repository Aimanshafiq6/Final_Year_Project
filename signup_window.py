import customtkinter as ctk
from tkinter import messagebox
import json
import os

# Initialize the main window
ctk.set_appearance_mode("dark")  # Modes: "system" (default), "dark", "light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class SignupWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sign Up Form")
        self.geometry("360x430")
        # Configure grid layout to be centered
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)
        # Create and place the widgets
        self.create_widgets()

    def create_widgets(self):
         # Heading Label
        self.heading_label = ctk.CTkLabel(self, text="Sign Up", font=("Helvetica", 24, "bold"))
        self.heading_label.grid(row=1, column=0, columnspan=2, pady=20)

        # Name Entry
        self.name_label = ctk.CTkLabel(self, text="Name:")
        self.name_label.grid(row=2, column=0, padx=10, pady=10)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row=2, column=1, padx=10, pady=10)

        # DOB Entry
        self.dob_label = ctk.CTkLabel(self, text="DOB (YYYY-MM-DD):")
        self.dob_label.grid(row=3, column=0, padx=10, pady=10)
        self.dob_entry = ctk.CTkEntry(self)
        self.dob_entry.grid(row=3, column=1, padx=10, pady=10)

        # Password Entry
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=4, column=0, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=10)

        # Confirm Password Entry
        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm Password:")
        self.confirm_password_label.grid(row=5, column=0, padx=10, pady=10)
        self.confirm_password_entry = ctk.CTkEntry(self, show="*")
        self.confirm_password_entry.grid(row=5, column=1, padx=10, pady=10)

        # Age Entry
        self.age_label = ctk.CTkLabel(self, text="Age:")
        self.age_label.grid(row=6, column=0, padx=10, pady=10)
        self.age_entry = ctk.CTkEntry(self)
        self.age_entry.grid(row=6, column=1, padx=10, pady=10)

        # Gender Options
        self.gender_label = ctk.CTkLabel(self, text="Gender:")
        self.gender_label.grid(row=7, column=0, padx=10, pady=10)
        self.gender_option = ctk.CTkOptionMenu(self, values=["Male", "Female", "Other"])
        self.gender_option.grid(row=7, column=1, padx=10, pady=10)

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=8, column=0, columnspan=2, pady=20)

    def submit_form(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        age = self.age_entry.get()
        gender = self.gender_option.get()

        if not all([name, dob, password, confirm_password, age, gender]):
            messagebox.showerror("Error", "All fields are required!")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            new_user = {"username": name, "password": password, "DOB":dob, "age":age, "gender":gender}
            self.save_user(new_user)
            messagebox.showinfo("Success", "Sign Up Successful!")

    def save_user(self, user):
        file_path = "users.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                users = json.load(file)
        else:
            users = []

        users.append(user)

        with open(file_path, "w") as file:
            json.dump(users, file, indent=4)

# Run the application
if __name__ == "__main__":
    app = SignupWindow()
    app.mainloop()
