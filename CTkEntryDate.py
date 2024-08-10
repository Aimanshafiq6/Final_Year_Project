import customtkinter
from typing import Any
import calendar as cr
from tkinter import END


class EntryDate(customtkinter.CTkEntry):
    def __init__(self,
                 master: Any,
                 placeholder_text: str = 'DD / MM / YY',
                 *args, **kwargs):
        super().__init__(master=master, placeholder_text=placeholder_text, *args, **kwargs)
        self.__super_get = super().get
        self.__super_delete = super().delete
        self.__super_insert = super().insert
        self.letter_input = False
        self.temp = ""
        self.bind("<KeyRelease>", self.__check_entry)

    def get(self):
        date_int_list = []
        for i in self.__super_get().split(' / '):
            if not i.isdigit() or len(i) != 2:
                return False
            date_int_list += [int(i)]
        if date_int_list[1] > 12 or (cr.monthrange(2000 + date_int_list[2], date_int_list[1])[1]) < date_int_list[0]:
            return False
        return tuple(date_int_list)

    def delete(self, first_index, last_index=None):
        self.__super_delete(0, END)
        self.__super_insert(0, self.temp)
        self.__super_delete(first_index, last_index)
        self.temp = self.__super_get()
        self.__insert_fix()

        if not self._is_focused and self._entry.get() == "":
            self._activate_placeholder()

    def insert(self, index, string=None, date=None):
        if date is not None and type(date) == tuple and len(date) == 3:
            string = ''
            for i in date:
                if type(i) == int and i < 100:
                    string += str(i)
                else:   raise TypeError('The format of a "date" is (DD, MM, YY) where DD, MM, YY is an integer!')
            if date[1] > 12 or (cr.monthrange(2000 + date[2], date[1])[1]) < date[0]:
                raise ValueError('The "date" is invalid!')
            self.temp = string
            return self.__insert_fix()
        if string is not None:
            if type(string) != str:   raise TypeError('The type "string" likes to be "str".'
                                                      '\nThe format of a "string" is "DDMMYY"')
            if string.isdigit():
                self.__super_delete(0, END)
                self.__super_insert(0, self.temp)
                self.__super_insert(index, string)
                self.temp = self.__super_get()
                return self.__insert_fix()
            raise ValueError('The "string" can only contain numbers!')

    def __insert_fix(self):
        if len(self.temp) > 6:  self.temp = self.temp[-6:]
        insert_str = ''
        for i in range(len(self.temp)):
            insert_str += self.temp[i]
            if i % 2 == 1 and i < 5:  insert_str += ' / '
        self.__super_delete(0, END)
        self.__super_insert(0, insert_str)

    def __check_entry(self, evt):
        if evt.char.isdigit():
            self.temp += evt.char
        elif evt.keysym != 'BackSpace':
            self.delete(0, END)
            self.letter_input = True
        else:
            self.temp = self.temp[:-1]
        if len(self.__super_get()) == 2:
            self.__super_insert(END, ' / ')
        if len(self.__super_get()) == 7:
            self.__super_insert(END, ' / ')

        if len(self.__super_get()) > 12 or evt.keysym == 'BackSpace' or self.letter_input:
            self.__insert_fix()
            self.letter_input = False


if __name__ == '__main__':

    def get_date():
        date_entry_list = [date_entry1, date_entry2, date_entry3]
        for i in range(3):
            print(f'The date on date_entry{i+1} is: {date_entry_list[i].get()}')

    def insert_date():
        date_entry1.insert(0)
        date_entry2.insert(0, date=(12, 12, 12))
        date_entry3.insert(0, string="121212")


    app = customtkinter.CTk()
    date_entry1 = EntryDate(master=app, width=98)
    date_entry1.pack()

    date_entry2 = EntryDate(master=app, placeholder_text='Date')
    date_entry2.pack()

    date_entry3 = EntryDate(master=app)
    date_entry3.pack()

    button1 = customtkinter.CTkButton(master=app, command=get_date, text='get date')
    button1.pack()

    button2 = customtkinter.CTkButton(master=app, command=insert_date, text='insert date')
    button2.pack()

    app.mainloop()