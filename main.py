import json
import logging
import os
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk

import requests
from requests_ntlm3 import HttpNtlmAuth

from baza_xml import *
from download_xml import *
from excel_to_pandas import *
from gui_post_window2 import *

logging.basicConfig(filename='error_message.txt',
                    filemode='a+',
                    level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s"
                    )


class GuiPost(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.label_title = Label(self, text='Login panel', font='arial 17 bold')
        self.label_title.grid(ipady=10)
        
        #   Login&Hasło
        self.label_title_ftp = Label(self, text='Login:', font='arial 10 bold')
        
        self.label_login = Label(self, text='Login:', font='arial 10 bold')
        self.label_login.grid(column=0, row=2, padx=10, sticky=tk.NW)

        self.label_password = Label(self, text='Passw:', font='arial 10 bold')
        self.label_password.grid(column=0, row=3, padx=10, sticky=tk.NW)

        self.login = StringVar()
        self.password = StringVar()
        
        self.login_entry = Entry(self, textvariable=self.login)
        self.login_entry.grid(column=0, row=2, padx=60, sticky=tk.N)
        self.login_entry.bind('<Return>', self.login_password_sp)
        
        self.password_entry = Entry(self, textvariable=self.password, show='*')
        self.password_entry.grid(column=0, row=3, padx=60, sticky=tk.N)


        self.password_entry.bind('<Return>', self.login_password_sp)
                
        self.refresh_button = Button(self, text='Refresh', 
                                     font='arial 10 bold', 
                                     bg='red', 
                                     command=self.lista_cala
                                     )
        
        self.select_button_true = Button(self, text='True',
                                         font='arial 10 bold',
                                         bg='green',
                                         command=self.update_tree
                                         )

        self.grid()
        
    def login_password_sp(self, event):
        
        post_login_passw(self.login.get(), self.password.get())
        self.login_entry.grid_remove()
        self.password_entry.grid_remove()
        self.label_title['text'] = 'Login To SharePoint'

        self.login_sp = StringVar()
        self.entry_login_sp = Entry(self, textvariable=self.login_sp)
        self.entry_login_sp.grid(column=0, row=2, sticky=tk.N)
        self.entry_login_sp.bind('<Return>', self.login_ftp)
        self.entry_login_sp.focus()

        self.password_sp = StringVar()
        self.entry_password_sp = Entry(self, textvariable=self.password_sp, show='*')
        self.entry_password_sp.grid(column=0, row=3, sticky=tk.N)
        self.entry_password_sp.bind('<Return>', self.login_ftp)

    def login_ftp(self, event):
        
        post_login_passw(self.login_sp.get(), self.password_sp.get())
        self.entry_login_sp.grid_remove()
        self.entry_password_sp.grid_remove()
        
        self.label_title_ftp['text'] = 'Server:'
        self.label_title_ftp.grid(column=0, row=1, padx=10, sticky=tk.NW)
        self.label_title['text'] = 'Login To FTP'

        self.server_ftp = StringVar()
        self.entry_server_ftp = Entry(self, textvariable=self.server_ftp)
        self.entry_server_ftp.grid(column=0, row=1, padx=100, sticky=tk.N)
        self.entry_server_ftp.bind('<Return>', self.login_password_ftp_disabled)
        self.entry_server_ftp.focus()

        self.login_ftp = StringVar()
        self.entry_login_ftp = Entry(self, textvariable=self.login_ftp)
        self.entry_login_ftp.grid(column=0, row=2, padx=100, sticky=tk.N)
        self.entry_login_ftp.bind('<Return>', self.login_password_ftp_disabled)

        self.password_ftp = StringVar()
        self.entry_password_ftp = Entry(self, textvariable=self.password_ftp)
        self.entry_password_ftp.grid(column=0, row=3, padx=100, sticky=tk.N)
        self.entry_password_ftp.bind('<Return>', self.login_password_ftp_disabled)

    def login_password_ftp_disabled(self, event):
        post_login_passw_ftp(self.server_ftp.get(),
                             self.login_ftp.get(),
                             self.password_ftp.get()
                             )
        self.lista_cala()

    def lista_cala(self):
        try:
            #   comment for open GUI
            #dow_excel(self.login_sp.get(), self.password_sp.get())
            #get_data_xml()
            #self.download_html()
        
            self.entry_server_ftp['show'] = '*'
            self.entry_login_ftp['show'] = '*'
            self.entry_password_ftp['show'] = '*'

            self.refresh_button.grid(column=2, row=0, sticky=tk.S)
            
            self.list_all = ttk.Treeview(self, show='headings', height=10)

            self.scroll_bar = ttk.Scrollbar(self, orient='vertical', command=self.list_all)
            self.scroll_bar.grid(column=0, row=5, ipady=112, sticky=tk.NE)

            self.list_all.configure(yscrollcommand=self.scroll_bar.set)
            
            #   scrollbar
            self.scroll_bar.config(command=self.list_all.yview)
            
            self.list_all['columns'] = ('Nr', 'Name', 'Status')
            self.list_all.column('#0', anchor=CENTER, stretch=YES)
            self.list_all.column('#1', anchor=CENTER, stretch=YES, width=30)
            self.list_all.column('#2', anchor='w', stretch=YES, width=200)
            self.list_all.column('#3', anchor='w', stretch=YES, width=80)
            
            self.list_all.heading('#0', text='')
            self.list_all.heading('Nr', text='Nr', anchor=CENTER)
            self.list_all.heading('Name', text='Name', anchor=CENTER)
            self.list_all.heading('Status', text='Status', anchor='w')
            self.list_all.grid(column=0, row=5, ipady=20, sticky=tk.S)
            
            self.list_sharepoint()
            self.list_all.focus()
            
            self.entry_server_ftp['state'] = 'disabled'
            self.entry_login_ftp['state'] = 'disabled'
            self.entry_password_ftp['state'] = 'disabled'

            self.select_button = Button(self, text='Choose', command=self.select_record)
            self.list_all.bind("<Double-1>", self.treeview_react_select)
            self.list_all.grid()

            self.select_button.grid(column=2, row=5, sticky=tk.N)
            self.select_button_true.grid(column=2, row=5)
            
        except Exception as exc:
            logging.error(f"ERROR: {exc}")
            
    def dane(self):
        self.final = {}
        #for i, k in enumerate(list_excel()):
        #    self.final[i+1] = k
        test = ['Test', 'False']
        for i, k in enumerate(test):
            self.final[i+1] = test
    
    def list_sharepoint(self):
        self.dane()
        for k, v in self.final.items():
            try:
                self.list_all.insert(parent='', index=k, iid=k, text='',
                                     values=(f"{k}", f"{v[0]}{k}", f"{v[1]}"))
            except:
                windows_msg(self, 'error', 'Something wrong with data')
                sys.exit()

    def login_status(self, event):
        self.login_password_sp()

    def update_tree(self):
        selected = self.list_all.focus()
        self.list_all.item(selected, text='',
                                             values=(self.selected_record()[0], 
                                                    self.selected_record()[1], 
                                                    'True'
                                                    )
                           )

    def treeview_react_select(self, event):
        self.select_record()

    def selected_record(self):
        selected = self.list_all.focus()
        values = self.list_all.item(selected, 'values')
        
        return values[0], values[1]

    def select_record(self):
        #   otwórz nowe okno z danymi obw
        self.exit_new_window()
        self.new_window = Toplevel(self)
        self.new_window.resizable(False, False)
        nw_width, nw_height = 600, 600
        window_position(self.new_window, nw_width, nw_height, divisor=5)

        #   clear path_pdf when click X
        self.new_window.protocol('WM_DELETE_WINDOW', attach_name.clear())
        
        #   new_window
        okno_dane(self.new_window)
        #   window with select name
        dane_sharepoint(self.selected_record()[1])

             
    def exit_new_window(self):
        try:
            self.new_window.destroy()
            self.new_window.update()
        except:
            pass

    def download_html(self):
        #   update list/button refresh
        user = self.login_sp.get()
        x = json.load(open('data/config.json'))
        username = 'SERWER_SP + {user}'
        password = self.password_sp.get()
        url = x.get('URL')
        
        with requests.Session() as session: 
            response = session.get(
                           url,
                           auth=HttpNtlmAuth(username, password)
                           )
            with open('data/sp.html', 'w', encoding="UTF-8") as f:
                f.write(response.text)

def windows_msg(self, typ, msg):
    if typ == 'info':
        messagebox.showinfo(title='INFO', message=msg)
    elif typ == 'error':
        messagebox.showerror(title='ERROR!', message=msg)
    elif typ == 'warning':
        messagebox.showwarning(title='WARNING', message=msg)
        
def window_position(self, width, height, /, divisor=2):
    
    scrwdth = self.winfo_screenwidth()
    scrhgt = self.winfo_screenheight()

    xLeft = int(scrwdth/divisor) - int(width/divisor)
    yTop = int(scrhgt/divisor) - int(height/divisor)

    return self.geometry(f"{str(width)}x{str(height)}+{str(xLeft)}+{str(yTop)}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Adding Posts')

        mywidth = 400
        myheight = 500

        window_position(self, mywidth, myheight, divisor=2)
        self.resizable(False, False)


if __name__ == '__main__':
    app = App()
    GuiPost(app)
    app.mainloop()
    
