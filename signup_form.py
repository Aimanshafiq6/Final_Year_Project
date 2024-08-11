from customtkinter import *
import tkinter
from PIL import Image
from CTkEntryDate import EntryDate
from tkinter import messagebox
import json
import datetime

class SignUpForm:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("856x645")
        self.app.resizable(0, 0)

        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

        self.create_sidebar()
        self.create_main_view()

    def create_sidebar(self):
        sidebar_frame = CTkFrame(master=self.app, fg_color="#601E88", width=210, height=650, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")
        image_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"images")

        logo_img_data = Image.open(os.path.join(image_dir_path,"rocket_signup.png"))
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="s")
        CTkLabel(master=sidebar_frame, text="Welcome!\nThanks for choosing vibe vision."
                 ,font=("Arial Bold",13), text_color="#fff").pack(pady=(40,0), anchor='center')
        person_img_data = Image.open(os.path.join(image_dir_path,"person_icon.png"))
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        #CTkButton(master=sidebar_frame, image=person_img, text="Account", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(160, 0))

    def create_main_view(self):
        main_view = CTkFrame(master=self.app, fg_color="#fff", width=680, height=650, corner_radius=0)
        main_view.pack_propagate(0)
        main_view.pack(side="left")

        CTkLabel(master=main_view, text="Lets Get you Started!\nPlease Enter your personal details", justify="left", font=("Arial Bold", 24), text_color="#601E88").pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=main_view, text="Name:", font=("Arial Bold", 17), text_color="#601e88",anchor="w",justify="left").pack(anchor="w", pady=(21,0), padx=27)

        self.username_entry = CTkEntry(master=main_view,width=226, fg_color="#EEEEEE", border_width=1 ,justify="left", border_color="#601E88", text_color="#000")
        self.username_entry.pack(pady=(6,0),ipady=5,padx=27,anchor="w")
        
        CTkLabel(master=main_view, text="Date of Birth:", font=("Arial Bold", 17), text_color="#601e88",anchor="w",justify="left").pack(anchor="w", pady=(21,0), padx=27)
        self.dob_entry = EntryDate(master=main_view, width=226, fg_color="#EEEEEE", border_width=1 ,justify="left", border_color="#601E88", text_color="#000")
        self.dob_entry.pack(pady=(6,0),ipady=5,padx=27,anchor="w")
        
        # gender
        CTkLabel(master=main_view, text="Gender:", font=("Arial Bold", 17), text_color="#601e88",anchor="w",justify="left").pack(anchor="w", pady=(21,0), padx=27)
        self.gender_entry = CTkOptionMenu(master=main_view, button_color="#601E88" ,values=["Male","Female","Other"],width=226, fg_color="#c76fff", text_color="#000")
        self.gender_entry.pack(pady=(6,0),ipady=5,padx=27,anchor="w")

        # pass
        self.create_grid(main_view)
        self.create_actions(main_view)

    def create_grid(self, main_view):
        grid = CTkFrame(master=main_view, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))

        CTkLabel(master=grid, text="Password:", font=("Arial Bold", 17), text_color="#601e88", justify="left", ).grid(row=0, column=0, sticky="w")
        self.password_entry = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=1, width=270,show="*",justify="left", border_color="#601E88", text_color="#000")
        self.password_entry.grid(row=1, column=0, ipady=10)

        CTkLabel(master=grid, text="Confirm password", font=("Arial Bold", 17), text_color="#601e88", justify="left").grid(row=0, column=1, sticky="w", padx=(25,0))
        self.confirm_password_entry = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=1, width=270,show="*",justify="left", border_color="#601E88", text_color="#000")
        self.confirm_password_entry.grid(row=1, column=1, ipady=10, padx=(24,0))

        '''
        CTkLabel(master=grid, text="Status", font=("Arial Bold", 17), text_color="#601e88", justify="left").grid(row=2, column=0, sticky="w", pady=(38, 0))

        self.status_var = tkinter.IntVar(value=0)

        CTkRadioButton(master=grid, variable=self.status_var, value=0, text="Confirmed", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=3, column=0, sticky="w", pady=(16,0))
        CTkRadioButton(master=grid, variable=self.status_var, value=1, text="Pending", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=4, column=0, sticky="w", pady=(16,0))
        CTkRadioButton(master=grid, variable=self.status_var, value=2, text="Cancelled", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=5, column=0, sticky="w", pady=(16,0))

        CTkLabel(master=grid, text="Quantity", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=6, column=0, sticky="w", pady=(42, 0))

        quantity_frame = CTkFrame(master=grid, fg_color="transparent")
        quantity_frame.grid(row=7, column=0, pady=(21,0), sticky="w")
        CTkButton(master=quantity_frame, text="-", width=25, fg_color="#2A8C55", hover_color="#207244", font=("Arial Black", 16)).pack(side="left", anchor="w")
        CTkLabel(master=quantity_frame, text="01", text_color="#2A8C55", font=("Arial Black", 16)).pack(side="left", anchor="w", padx=10)
        CTkButton(master=quantity_frame, text="+", width=25, fg_color="#2A8C55", hover_color="#207244", font=("Arial Black", 16)).pack(side="left", anchor="w")

        CTkLabel(master=grid, text="Description", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=2, column=1, sticky="w", pady=(42, 0), padx=(25,0))

        CTkTextbox(master=grid, fg_color="#F0F0F0", width=300, corner_radius=8).grid(row=3, column=1, rowspan=5, sticky="w", pady=(16, 0), padx=(25,0), ipady=10)
        '''

    def create_actions(self, main_view):
        actions = CTkFrame(master=main_view, fg_color="transparent")
        actions.pack(fill="both")

        CTkButton(master=actions, text="Back", width=270, fg_color="transparent", font=("Arial Bold", 17), border_color="#2A8C55", hover_color="#eee", border_width=2, text_color="#2A8C55",command=self.app.destroy).pack(side="left", anchor="sw", pady=(30,0), padx=(27,24))
        CTkButton(master=actions, text="Create", width=270, font=("Arial Bold", 17), hover_color="#207244", fg_color="#2A8C55", text_color="#fff",command=self.submit_form).pack(side="left", anchor="se", pady=(30,0), padx=(0,27))
    
    def submit_form(self):
        name = self.username_entry.get()
        dob = self.dob_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        gender = self.gender_entry.get()

        print(dob)
        print(gender)
        factor = dob[2]
        if factor > 0 and factor < 24:
            age = datetime.datetime.now().year - (factor + 2000)
        else:
            age = datetime.datetime.now().year -  (1900 + factor)
        
        print(age)
        if not all([name, dob, password, age ,confirm_password, gender]):
            messagebox.showerror("Error", "All fields are required!")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            new_user = {"username": name, "password": password, "DOB":dob, "age":age, "gender":gender}
            self.save_user(new_user)
            messagebox.showinfo("Success", "Sign Up Successful!")
            self.app.destroy()
        
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

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    order_form = SignUpForm()
    order_form.run()