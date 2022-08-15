import time
import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import messagebox, ttk

from bs4 import BeautifulSoup

from download_attach import *
from excel_to_pandas import *
from ftp_connect import *
from html_download_idLink import *
from login_website import uwaga_post
from main import *

attach_name = []
attach_name_pdf = []

user_log = []
user_pass = []

user_server_ftp = []
user_login_ftp = []
user_pass_ftp = []

name_selected = []

options = {'padx': 10, 'pady': 20}
size = {'ipadx': 20}

def windows_msg(typ, msg):
    if typ == 'info':
        messagebox.showinfo(title='INFO', message=msg)
    elif typ == 'error':
        messagebox.showerror(title='ERROR!', message=msg)
    elif typ == 'warning':
        messagebox.showwarning(title='WARNING', message=msg)

def dane_sharepoint(selected):
    clear_path_pdf()
    title.set(selected)
    name_selected.append(selected)
    data = list_excel_items(selected)
    location.set(data[3])
    dateOD.set(data[1])
    dateDO.set(data[2])
    login_computer.get()
    haslo_computer.get()
    
def get_pdf_strona():
    #   download attachment from sharepoint
    download_pdf(sharepoint_attachment_link(name_selected[0])[2],
                                            user_log[1], 
                                            user_pass[1]
                                            )
    windows_msg('info', 'PDF download')

    #   unlock button Public
    button_dodaj['state'] = 'normal'

def clear_path_pdf():
    attach_name_pdf.clear()
    attach_name.clear()
    attach_name_label.set('')
    location.set('')
    name_selected.clear()

def post_login_passw(user, password):
    #   user and password add to array
    user_log.append(user)
    user_pass.append(password)

def post_login_passw_ftp(server, user, password):
    #   user and password add to array
    user_server_ftp.append(server)
    user_login_ftp.append(user)
    user_pass_ftp.append(password)

def komunikat_post():
    title_ogl = title.get()
    lokalizacja = location.get()
    data_start = dateOD.get()
    data_end = dateDO.get()
    date_time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    date_now = time.strftime("%Y-%m-%d")
    option_link = location.get()

    attach_html = 'data/zalacznik.html'
    with open(attach_html, 'r', encoding='UTF-8') as response:
        soup = BeautifulSoup(response, 'html.parser')
        for i in soup.select('tr[id]'):
            link = i.find('a', href=True)
            if link is None:
                continue
            pdf_name = link.get_text()
            
    if option_link == 'Option1':
        ftp_folder = 'ftpfolder1'
                
    if option_link == 'Option2':
        ftp_folder =  'ftpfolder2'
                
    if option_link == 'Option3':
        ftp_folder =  'ftpfolder3'

    #   create url 
    pdf = f"url + {ftp_folder} + {pdf_name}"
    if len(pdf) >= 40:
        connect_ftp(user_server_ftp[0], user_login_ftp[0],
                    user_pass_ftp[0], option_link, pdf_name
                    )
        uwaga_post(user_log[0], user_pass[0], lokalizacja, title_ogl,
                   pdf, data_start, data_end,
                   date_time_now, date_now, option_link)
        #   open website with pdf 
        webbrowser.open(pdf)
        windows_msg('info', 'Post Publish')

    else:
        windows_msg('error', 'File no available')

def okno_dane(self): 
    #   Nazwy Labels
    title_label = Label(self, text='Name:', font='arial 9 bold')
    title_label.grid(column=0, row=0, sticky=tk.NW, **options)

    location_label = Label(self, text='Option:', font='arial 9 bold')
    location_label.grid(column=0, row=1, sticky=tk.NW, **options)

    dateOD_label_rmd = Label(self, text='YYYY-MM-DD', font='4')
    dateOD_label_rmd.grid(column=1, row=2, padx=140, pady=20, sticky=tk.NW)

    dateOD_label = Label(self, text='Date Start:', font='arial 10 bold')
    dateOD_label.grid(column=0, row=2, sticky=tk.NW, **options)

    dateDO_label = Label(self, text='Date Expired:', font='arial 9 bold')
    dateDO_label.grid(column=0, row=3,sticky=tk.NW, **options)

    uwagi_label = Label(self, text='Note:', font='arial 9 bold')
    uwagi_label.grid(column=0, row=4, sticky=tk.NW, **options)

    workflow_label = Label(self, text='Workflow*:', font='arial 9 bold')
    workflow_label.grid(column=0, row=5,sticky=tk.NW, **options)

    attachment_label = Label(self, text='Attachment:', font='arial 9 bold')
    attachment_label.grid(column=0, row=7, sticky=tk.NW, **options)

    global attach_name_label
    attach_name_label = StringVar()
    attachment_name = Label(self,
                            textvariable='test',
                            font='arial 8 bold')
    attachment_name.grid(column=1, row=7, padx=170, pady=25, sticky=tk.NW)

    #   Kontenery
    global title
    title = StringVar()

    global location
    location = StringVar()

    global dateOD
    dateOD = StringVar()

    global dateDO
    dateDO = StringVar()

    global uwagi
    uwagi = StringVar()

    global workflow
    workflow = StringVar()

    global login_computer
    login_computer = tk.StringVar()

    global haslo_computer
    haslo_computer = tk.StringVar()
            
    title_entry = Entry(self, textvariable=title)

    title_entry.grid(column=1, row=0, sticky=tk.W, ipadx=140, **options)

    location_entry = Entry(self, textvariable=location)
    location_entry.grid(column=1, row=1, sticky=tk.W, **size, **options)

    dateOD_entry = Entry(self, textvariable=dateOD)
    dateOD_entry.grid(column=1, row=2, sticky=tk.W, **options)

    dateDO_entry = Entry(self, textvariable=dateDO)
    dateDO_entry.grid(column=1, row=3, sticky=tk.W, **options)

    global uwagi_entry
    uwagi_entry = Text(self, height=3, width=18,)
    uwagi_entry.grid(column=1, row=4, sticky=tk.NW, rowspan=2, ipadx=50, **options)

    workflow_entry = Entry(self, textvariable=workflow, state='disabled')
    workflow.set('Yes')
    workflow_entry.grid(column=1, row=5, sticky=tk.W, **options)

    #   Button
    button_generuj = Button(self, text='Get PDF', command=get_pdf_strona)
    button_generuj.grid(column=1, row=7, sticky=tk.W, **options)

    global button_dodaj
    button_dodaj = Button(self, text='Public', command=lambda: [
                                                            komunikat_post()
                                                            ])
    button_dodaj['state'] = 'disabled'
    button_dodaj.grid(column=1, row=8, pady=30, sticky=tk.W)

    button_cancel = Button(self, text='Cancel', command=lambda: [
                                                        self.destroy(),
                                                        clear_path_pdf(),
                                                        ])
    button_cancel.grid(column=1, padx=150, row=8, sticky=tk.W)


if __name__ == '__main__':
    okno_dane()
