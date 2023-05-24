from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector
from datetime import date, timedelta
import datetime
import smtplib
import pandas as pd
from fpdf import FPDF
from pathlib import Path


# widget properties' values defined in one place
main_colors = {"bg": "#201f40", "fg": "white"}
btn_colors = {"bg": "green3", "fg": "white"}
mbtn_colors = {"bg": "#1a15ad", "fg": "white", "rlf": RAISED}  # menu buttons
# cbtn_colors = {"main": "light green", "sec": "red", "rlf": RAISED}
normal_font = ["calibri", 14]
bold_font = ["calibri", 14, "bold"]



# create password file
path = Path('./pass.txt')
res2 = path.is_file()

if res2 == False:
    f = open("pass.txt", "a")
    f.write("admin123")
    f.close()


# create id file
idpath = Path('./demo.txt')
res3 = idpath.is_file()

if res3 == False:
    f = open("demo.txt", "a")
    f.write("1\n")
    f.write("1\n")
    f.close()


# create email pass file
epath = Path('./email_pass.txt')
res4 = epath.is_file()

if res4 == False:
    root = Tk()
    f = open("email_pass.txt", "a")
    # email prompt
    t2 = Toplevel(root)
    t2.transient(root)
    t2.geometry("350x200+200+200")
    t2.configure(bg=main_colors["bg"])

    Label(t2, text="Email Id", background=main_colors["bg"], foreground=main_colors["fg"], pady=20, padx=15,
          font=normal_font).place(relx=0.3, rely=0.3)
    e1 = Entry(t2)
    e1.place(relx=0.6, rely=0.3)

    Label(t2, text="Email Password", background=main_colors["bg"], foreground=main_colors["fg"], pady=20, padx=15,
          font=normal_font).place(relx=0.3, rely=0.6)
    e2 = Entry(t2)
    e2.place(relx=0.6, rely=0.6)

    y = Button(t2, text="OK", background="royalblue", command=lambda: (conf(), t2.destroy()), font=normal_font)
    y.place(rely=0.8, relx=0.1)

    def conf():
        passw = e2.get()
        mail_id = e1.get()
        f.write(mail_id + "\n" + passw + "\n")
        f.close()

        if not mail_id.endswith("@gmail.com"):
            print("Please enter a valid Email address")
            return

    root.mainloop()

f = open("email_pass.txt", "r")
mail_det = f.readlines()

# mail info.
mail_id_name = mail_det[0]
mail_id_pass = mail_det[1]



# create database file
dbpath = Path('./dbpass.txt')
res1 = dbpath.is_file()

if res1 == False:
    root = Tk()
    f = open("dbpass.txt", "a")
    t2 = Toplevel(root)
    t2.transient(root)
    t2.geometry("350x200+200+200")
    t2.configure(bg=main_colors["bg"])

    Label(t2, text="Email Password", background=main_colors["bg"], foreground=main_colors["fg"], pady=20, padx=15,
          font=normal_font).place(relx=0.3, rely=0.3)
    e1 = Entry(t2)
    e1.place(relx=0.6, rely=0.3)

    y = Button(t2, text="OK", background="royalblue", command=lambda: (conf(), t2.destroy()), font=normal_font)
    y.place(rely=0.8, relx=0.1)

    def conf():
        db_pass = e1.get()
        f.write(db_pass)
        f.close()

    root.mainloop()

f = open("dbpass.txt", "r")
passw = f.readlines()
password = passw[0]

# db properties
db_config = {"db_password": password, "db_name": "dbssystem", "user": 'root', "host": '127.0.0.1'}



res = ""
act_rel = ""
search_attr = ""


# miscellaneous functions
# for entry fields
def clear_fields(*args):
    for i in args:
        i.delete(0, END)


# for dropdown list
def set_text(e, text):
    e.delete(0, END)
    e.insert(0, text)


# to clear windows
def clear_frame(dispframe):
    if dispframe != NONE:
        for widgets in dispframe.winfo_children():
            widgets.destroy()


# to change colors of buttons
def change_color(btn):
    if btn.cget("bg") == btn_colors["bg"]:
        btn.configure(bg="red")
    elif btn.cget("bg") == "red":
        btn.configure(bg=btn_colors["bg"])


# to create tables
def create_member_table():
    try:
        conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                       database=db_config["db_name"])
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS members(
        member_id VARCHAR(15) PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        contact_no VARCHAR(10) NOT NULL,
        address VARCHAR(80) NOT NULL,
        email VARCHAR(35) NOT NULL,
        academic_year VARCHAR(20),
        division VARCHAR(4),
        batch VARCHAR(2),
        roll_no INT(5),
        course VARCHAR(30) NOT NULL
        )
        """)
        conn.close()
    except (mysql.connector.errors.ProgrammingError):
        print("wrong database pass, please change it in the setting")


def create_books_table():
    try:
        conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                       host='127.0.0.1', database=db_config["db_name"])
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS book(
        book_topic VARCHAR(40) NOT NULL,
        author_name VARCHAR(30) NOT NULL,
        available_quantity INT(11) NOT NULL,
        total_quantity INT(11) NOT NULL,
        publisher VARCHAR(30),
        category VARCHAR(30),
        book_title VARCHAR(30) NOT NULL
        )
        """)
        conn.close()
    except (mysql.connector.errors.ProgrammingError):
        print("wrong database pass, please change it in the setting")


def create_books_list_table():
    try:
        conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                       host='127.0.0.1', database=db_config["db_name"])
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS book_list(
        book_topic VARCHAR(40) NOT NULL,
        author_name VARCHAR(30) NOT NULL,
        description VARCHAR(250),
        edition VARCHAR(20),
        price INT NOT NULL,
        book_title VARCHAR(30) NOT NULL,
        availability VARCHAR(30),
        book_id  VARCHAR(30)
        )
        """)
        conn.close()
    except (mysql.connector.errors.ProgrammingError):
        print("wrong database pass, please change it in the setting")


def create_transaction_table():
    try:
        conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                       database=db_config["db_name"])
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transaction(
        transaction_id INT(10) PRIMARY KEY,
        trans_date DATE,
        trans_time TIME,
        operation VARCHAR(150)
        )
        """)
        conn.commit()
        conn.close()
    except (mysql.connector.errors.ProgrammingError):
        print("wrong database pass, please change it in the setting")


def create_issued():
    try:
        conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                       database=db_config["db_name"])
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS issued(
        member_id VARCHAR(15),
        book_id VARCHAR(20),
        book_title VARCHAR(100) NOT NULL,
        name VARCHAR(20) NOT NULL,
        email VARCHAR(35) NOT NULL,
        academic_year VARCHAR(50),
        course VARCHAR(30) NOT NULL, 
        borro_date DATE,
        borro_time TIME
        )
        """)
        conn.close()
    except (mysql.connector.errors.ProgrammingError):
        print("wrong database pass, please change it in the setting")


def create_defaulter():
    try:
        conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                       host='127.0.0.1', database=db_config["db_name"])
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS defaulter(
        member_id VARCHAR(15),
        book_id VARCHAR(20),
        book_title VARCHAR(100) NOT NULL,
        name VARCHAR(20) NOT NULL,
        email VARCHAR(35) NOT NULL,
        academic_year VARCHAR(50),
        course VARCHAR(30) NOT NULL,
        borro_date DATE,
        borro_time TIME
        )
        """)
        conn.close()
    except (mysql.connector.errors.ProgrammingError):
        print("wrong database pass, please change it in the setting")


def update_id(tab):
    file = open("demo.txt", "r")
    replaced_content = ""
    i = 0
    line_number = 0

    if tab == 1:
        line_number = 1

    for line in file:
        line = line.strip()
        new_val = str(int(line) + 1)
        if i == line_number:
            temp = line
            new_line = line.replace(line, new_val)
        else:
            new_line = line
        replaced_content = replaced_content + new_line + "\n"
        i = i + 1
    file.close()

    write_file = open("demo.txt", "w")
    write_file.write(replaced_content)
    write_file.close()

    return temp


def focuson(nevobj):
    nevobj.focus()


def app_start():
    # main window
    root = Tk()
    root.title('C.H.M. Library')
    root.geometry("1250x730+0+0")
    root.resizable(False, False)

    # db configuration

    # creating database
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password=db_config["db_password"])
        ccur = mydb.cursor()
        ccur.execute("CREATE DATABASE IF NOT EXISTS dbssystem")

        # creating tables if they donot exist
        create_member_table()
        create_books_table()
        create_issued()
        create_defaulter()
        create_transaction_table()
        create_books_list_table()

    except (mysql.connector.errors.ProgrammingError):
        print("wrong database pass, please change it in the setting")

    # for treeview
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", background=main_colors["bg"], fieldbackground=main_colors["bg"],
                    foreground=main_colors["fg"])
    style.configure('Treeview.Heading', background="green3")

    # frames
    main_frame = Frame(root, height=860, width=1280, bg=main_colors["bg"])
    main_frame.pack(expand=YES, fill=BOTH)

    f1 = Frame(main_frame, height=730, width=160, bg=mbtn_colors["bg"])
    f1.pack(side=LEFT, expand=YES, fill=Y)
    f1.pack_propagate(False)

    menu = Frame(main_frame, bg="grey30", height=110, width=1130)
    menu.pack(side=TOP)
    menu.pack_propagate(False)

    status = Frame(menu, bg="grey30", height=110, width=700)
    status.place(relx=0.01, rely=0.01)
    status.pack_propagate(False)

    main_screen = Frame(main_frame, height=620, width=1130, background=main_colors["bg"], relief=SOLID, borderwidth=4)
    main_screen.pack(side=LEFT, expand=YES, fill=BOTH)
    main_screen.pack_propagate(False)

    disp_frame = Frame(main_screen, bg=main_colors["bg"], height=300, width=400)
    disp_frame.pack(side=TOP, anchor=S, expand=YES, fill=BOTH)
    disp_frame.pack_propagate(False)

    Label(disp_frame, text="Welcome User!!!", bg=main_colors["bg"], fg=main_colors["fg"], font=("arial", 20, "bold")) \
        .place(rely=0.55, relx=0.5, anchor=CENTER)

    # settings
    def change_pass_vin():
        clear_frame(disp_frame)
        Label(disp_frame, text="New Password", font=bold_font, fg=main_colors["fg"], bg=main_colors["bg"],
              width=20).place(relx=0.1, rely=0.1, anchor=CENTER)
        e1 = Entry(disp_frame, font=bold_font)
        e1.place(relx=0.27, rely=0.1, anchor=CENTER)

        Label(disp_frame, text="Confirm Password", font=bold_font, fg=main_colors["fg"], bg=main_colors["bg"],
              width=20).place(relx=0.1, rely=0.2, anchor=CENTER)
        e2 = Entry(disp_frame, font=bold_font)
        e2.place(relx=0.27, rely=0.2, anchor=CENTER)
        temp = Frame(disp_frame)
        temp.place(relx=0.5, rely=0.7, anchor=CENTER)

        def commit():
            clear_frame(temp)
            neu = e1.get()
            conf = e2.get()
            if neu != "":
                if neu == conf:
                    file1 = open("pass.txt", "w")
                    file1.write(neu)
                    file1.close()
                    Label(temp, text="Password changed", fg=main_colors["fg"], bg=main_colors["bg"]).pack(side=LEFT)

                    try:
                        conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                                       database=db_config["db_name"])
                        cur = conn.cursor()
                        # record the transaction
                        curtime = datetime.datetime.now()
                        curdate = date.today()
                        tr_id = update_id(0)
                        trans_stmt = f"Password was changed to {neu}"
                        tran = (tr_id, curdate, curtime, trans_stmt)
                        cur.execute('INSERT into transaction values(%s, %s, %s, %s)', tran)
                        conn.close()
                    except (mysql.connector.errors.ProgrammingError):
                        print("wrong database pass, please change it in the setting")

                else:
                    Label(temp, text="Different password in second field", fg=main_colors["fg"],
                          bg=main_colors["bg"]).pack(side=LEFT)
            else:
                Label(temp, text="Password Field is empty. Please Enter valid Password.", fg=main_colors["fg"],
                      bg=main_colors["bg"]).pack(side=LEFT)

        Button(disp_frame, text="Change", command=commit, fg=btn_colors["fg"], bg=btn_colors["bg"],
               font=bold_font).place(relx=0.27, rely=0.3, anchor=CENTER)

    def setting_vin():
        clear_frame(disp_frame)
        Button(disp_frame, text="Change Password", command=change_pass_vin, font=bold_font, bg="red",
               fg=main_colors["fg"]) \
            .place(relx=0.93, rely=0.20, anchor=CENTER)

    b2 = Button(menu, text="settings", font=bold_font, bg=btn_colors["bg"], command=setting_vin, fg=main_colors["fg"])
    b2.place(rely=0.2, relx=0.9, anchor=CENTER)

    def pop(ent):
        popup = Toplevel(root, bg=main_colors["bg"])
        popup.transient(root)
        popup.geometry("300x200+200+200")
        Label(popup, text=ent, fg=main_colors["fg"], bg=main_colors["bg"], font=normal_font).place(rely=0.5, relx=0.5,
                                                                                                   anchor=CENTER)
        Button(popup, text="Ok", bg=btn_colors["bg"], font=normal_font, command=popup.destroy).place(rely=0.7, relx=0.5,
                                                                                                     anchor=CENTER)

    def confirm(conf_str, comm):
        t2 = Toplevel(root)
        t2.transient(root)
        t2.geometry("350x200+200+200")
        t2.configure(bg=main_colors["bg"])
        Label(t2, text=conf_str, background=main_colors["bg"], foreground=main_colors["fg"], pady=20, padx=15,
              font=normal_font).pack(expand=YES, fill=BOTH)
        y = Button(t2, text="OK", background="royalblue", command=lambda: (comm(), t2.destroy()), font=normal_font)
        y.place(rely=0.8, relx=0.1)
        no = Button(t2, text="Cancel", background="red", command=t2.destroy, font=normal_font)
        no.place(rely=0.8, relx=0.7)

    # main functions
    def add_mem_vin():
        clear_frame(status)
        clear_frame(disp_frame)
        Label(disp_frame, text="Name", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.08, relx=0.025)
        n1 = Entry(disp_frame, font=normal_font)
        n1.place(rely=0.08, relx=0.15)
        n1.focus()
        n1.bind('<Return>', lambda event: focuson(n2))

        Label(disp_frame, text="Contact No", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.16, relx=0.025)
        n2 = Entry(disp_frame, font=normal_font)
        n2.place(rely=0.16, relx=0.15)
        n2.bind('<Return>', lambda event: focuson(n3))

        Label(disp_frame, text="Address", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.24, relx=0.025)
        n3 = Entry(disp_frame, font=normal_font)
        n3.place(rely=0.24, relx=0.15)
        n3.bind('<Return>', lambda event: focuson(n4))

        Label(disp_frame, text="Email", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.32, relx=0.025)
        n4 = Entry(disp_frame, font=normal_font)
        n4.place(rely=0.32, relx=0.15)
        n4.bind('<Return>', lambda event: focuson(n5))

        Label(disp_frame, text="Academic Year", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.40, relx=0.025)
        n5 = Entry(disp_frame, font=normal_font)
        n5.place(rely=0.40, relx=0.15)
        n5.bind('<Return>', lambda event: focuson(n6))

        CmdBtn = Menubutton(disp_frame, text='Select Academic Year', bg=btn_colors["bg"], fg=btn_colors["fg"],
                            font=("Calibri", 12, "bold"))
        CmdBtn.place(rely=0.40, relx=0.34)
        CmdBtn.menu = Menu(CmdBtn)
        CmdBtn.menu.add_command(label='(fy) First Year', underline=0, command=lambda: set_text(n5, "first year"))
        CmdBtn.menu.add_command(label='(sy) Second Year', underline=0, command=lambda: set_text(n5, "second year"))
        CmdBtn.menu.add_command(label='(ty) Third Year', underline=0, command=lambda: set_text(n5, "third year"))
        CmdBtn['menu'] = CmdBtn.menu

        Label(disp_frame, text="Batch", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font).place(rely=0.48,
                                                                                                            relx=0.025)
        n6 = Entry(disp_frame, font=normal_font)
        n6.place(rely=0.48, relx=0.15)
        n6.bind('<Return>', lambda event: focuson(n7))

        Label(disp_frame, text="Roll no", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font).place(rely=0.56,
                                                                                                              relx=0.025)
        n7 = Entry(disp_frame, font=normal_font)
        n7.place(rely=0.56, relx=0.15)
        n7.bind('<Return>', lambda event: focuson(n8))

        Label(disp_frame, text="Division", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font).place(
            rely=0.64, relx=0.025)
        n8 = Entry(disp_frame, font=normal_font)
        n8.place(rely=0.64, relx=0.15)
        n8.bind('<Return>', lambda event: focuson(n9))

        Label(disp_frame, text="Course", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font).place(rely=0.72,
                                                                                                             relx=0.025)
        n9 = Entry(disp_frame, font=normal_font)
        n9.place(rely=0.72, relx=0.15)
        n9.bind('<Return>', None)

        CmdBtn = Menubutton(disp_frame, text='Select Course', bg=btn_colors["bg"], fg=btn_colors["fg"],
                            font=("Calibri", 12, "bold"))
        CmdBtn.place(rely=0.72, relx=0.34)
        CmdBtn.menu = Menu(CmdBtn)
        CmdBtn.menu.add_command(label='Bsc. IT', underline=0, command=lambda: set_text(n9, "bscit"))
        CmdBtn.menu.add_command(label='Bsc. ', underline=0, command=lambda: set_text(n9, "bsc"))
        CmdBtn.menu.add_command(label='CS (Computer Science)', underline=0, command=lambda: set_text(n9, "cs"))
        CmdBtn['menu'] = CmdBtn.menu

        def add_member_query():
            mid = update_id(1)
            nam = n1.get()
            num = n2.get()
            addr = n3.get()
            mail = n4.get()
            acad = n5.get()
            bat = n6.get()
            div = n8.get()
            cour = n9.get()

            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                if nam != "" and num != "" and addr != "" and mail != "" and acad != "":
                    cur.execute(f"SELECT name FROM members WHERE name = '{nam}' AND contact_no = '{num}'")
                    arr = cur.fetchall()
                    if len(arr) == 0:

                        if not mail.endswith("@gmail.com"):
                            pop("Please enter a valid Email address")
                            return

                        try:
                            temp = int(num)
                        except ValueError:
                            # popup
                            pop("Please enter a valid contact number")
                            return

                        if len(num) != 10:
                            pop("Please enter a valid contact number")
                            return

                        try:
                            roll = int(n7.get())
                        except ValueError:
                            # popup
                            pop("Please enter valid roll number")
                            return

                        num = str(temp)

                        # add the member
                        tup = (mid, nam, num, addr, mail, acad, div, bat, roll, cour)

                        # record the transaction
                        curtime = datetime.datetime.now()
                        curdate = date.today()
                        tr_id = update_id(0)
                        trans_stmt = f"{nam} with member id {mid} has been added as a member to the library"
                        tran = (tr_id, curdate, curtime, trans_stmt)

                        def process():
                            conn1 = mysql.connector.connect(user='root', password=db_config["db_password"],
                                                            host='127.0.0.1', database=db_config["db_name"])
                            cur1 = conn1.cursor()
                            cur1.execute("INSERT into members values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tup)
                            cur1.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)
                            conn1.commit()
                            conn1.close()
                            pop("Member added successfully")

                        confirm(f"Add '{n1.get()}' to the library?", process)
                    else:
                        # popup
                        pop(f"member {nam} already exists")
                else:
                    # popup
                    pop("Please fill-in all the mandatory fields")
                conn.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Add member", fg=btn_colors["fg"], bg=btn_colors["bg"], font=bold_font, relief=RAISED,
               command=add_member_query).place(rely=0.6, relx=0.6)

        # Button(disp_frame, text="Add member", bg=btn_colors["bg"], font=normal_font, relief=RAISED, command=lambda: confirm(f"Add '{n1.get()}' to the library?", add_member_query)).place(rely=0.6, relx=0.6)
        Button(disp_frame, text="Reset", bg="red", fg=btn_colors["fg"], font=bold_font, relief=RAISED,
               command=lambda: clear_fields(n1, n2, n3, n4, n5, n6, n7, n8, n9)).place(rely=0.05, relx=0.5,
                                                                                       anchor=CENTER)

    # to remove a single member
    def rem_single_mem_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Label(disp_frame, text="Member ID:", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.08, relx=0.025)
        n1 = Entry(disp_frame, font=normal_font)
        n1.place(rely=0.08, relx=0.2)
        n1.focus()

        def rem_member_query():
            mid = n1.get()
            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                               host='127.0.0.1', database=db_config["db_name"])
                cur = conn.cursor()
                cur.execute(f"select name, academic_year, roll_no, course from members WHERE member_id = '{mid}'")
                otpt = cur.fetchall()
                print(len(otpt))
                if len(otpt) > 0:
                    print("vhy is it executing")
                    cur.execute(f"DELETE FROM members WHERE member_id = '{mid}'")
                    curtime = datetime.datetime.now()
                    curdate = date.today()
                    tr_id = update_id(0)
                    trans_stmt = f"{otpt[0]} with has been removed from library"
                    tran = (tr_id, curdate, curtime, trans_stmt)
                    cur.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)
                    conn.commit()
                    pop(f"Member has been removed successfully")
                else:
                    # popup
                    pop("member not registered")
                conn.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Remove member", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_member_query).place(rely=0.24, relx=0.3)

    # remove multiple members
    def rem_mul_mem_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Label(disp_frame, text="Members attribute value:", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.08, relx=0.025)
        n1 = Entry(disp_frame, font=normal_font)
        n1.place(rely=0.08, relx=0.2)
        n1.focus()
        n1.bind('<Return>', lambda event: focuson(CmdBtn))

        n2 = Entry(disp_frame, font=normal_font)

        def set_var(val):
            global search_attr
            search_attr = val
            CmdBtn.configure(text=val)

        CmdBtn = Menubutton(disp_frame, text='Search by', bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font)
        CmdBtn.place(rely=0.16, relx=0.2)
        CmdBtn.menu = Menu(CmdBtn)
        CmdBtn.menu.add_command(label='Academic Year', underline=0, command=lambda: set_var("academic_year"))
        CmdBtn.menu.add_command(label='Division', underline=0, command=lambda: set_var("division"))
        CmdBtn.menu.add_command(label='Course', underline=0, command=lambda: set_var('course'))
        CmdBtn['menu'] = CmdBtn.menu

        def rem_mul_member_query():
            search_key = n1.get()
            search_attr = CmdBtn.cget("text")
            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                               host='127.0.0.1', database=db_config["db_name"])
                cur = conn.cursor()
                cur.execute(
                    f"select name, academic_year, roll_no, course from members WHERE {search_attr} = '{search_key}'")
                res = cur.fetchall()
                print(search_attr)
                print(search_key)
                print(res)
                if len(res) > 0:
                    cur.execute(f"DELETE FROM members WHERE {search_attr} = '{search_key}'")
                    curtime = datetime.datetime.now()
                    curdate = date.today()
                    tr_id = update_id(0)
                    trans_stmt = f"All Members {search_attr}: {search_key} have been removed from library"
                    tran = (tr_id, curdate, curtime, trans_stmt)
                    cur.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)

                    conn.commit()
                    pop(f"Members have been removed successfully")
                else:
                    # popup
                    pop("Member not registered")
                conn.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Remove member", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_mul_member_query).place(rely=0.32, relx=0.4)

    def rem_mem_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Button(disp_frame, text="Remove Single Member", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_single_mem_vin) \
            .place(rely=0.08, relx=0.025)

        Button(disp_frame, text="Remove Multiple Member", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_mul_mem_vin) \
            .place(rely=0.16, relx=0.025)

    def add_book_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Label(disp_frame, text="Book Topic", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.08, relx=0.025)
        n1 = Entry(disp_frame, font=normal_font)
        n1.place(rely=0.08, relx=0.15)
        n1.focus()
        n1.bind('<Return>', lambda event: focuson(n2))

        Label(disp_frame, text="Author name", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.16, relx=0.025)
        n2 = Entry(disp_frame, font=normal_font)
        n2.place(rely=0.16, relx=0.15)
        n2.bind('<Return>', lambda event: focuson(n3))

        Label(disp_frame, text="Edition", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.24, relx=0.025)
        n3 = Entry(disp_frame, font=normal_font)
        n3.place(rely=0.24, relx=0.15)
        n3.bind('<Return>', lambda event: focuson(n4))

        CmdBtn = Menubutton(disp_frame, text='select edition', bg=btn_colors["bg"], fg=btn_colors["fg"],
                            font=("Calibri", 12, "bold"))
        CmdBtn.place(rely=0.24, relx=0.34)
        CmdBtn.menu = Menu(CmdBtn)
        CmdBtn.menu.add_command(label='First Edition', underline=0, command=lambda: set_text(n3, "first edition (1st)"))
        CmdBtn.menu.add_command(label='Second Edition', underline=0,
                                command=lambda: set_text(n3, "second edition (2nd)"))
        CmdBtn.menu.add_command(label='Third Edition', underline=0, command=lambda: set_text(n3, "third edition (3rd)"))
        CmdBtn.menu.add_command(label='Fourth Edition', underline=0,
                                command=lambda: set_text(n3, "fourth edition (4th)"))
        CmdBtn.menu.add_command(label='Fifth Edition', underline=0, command=lambda: set_text(n3, "fifth edition (5th)"))
        CmdBtn.menu.add_command(label='N/A', underline=0, command=lambda: set_text(n3, "N/A"))
        CmdBtn['menu'] = CmdBtn.menu

        Label(disp_frame, text="Book title", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.32, relx=0.025)
        n4 = Entry(disp_frame, font=normal_font)
        n4.place(rely=0.32, relx=0.15)
        n4.bind('<Return>', lambda event: focuson(n5))

        Label(disp_frame, text="Publisher", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.4, relx=0.025)
        n5 = Entry(disp_frame, font=normal_font)
        n5.place(rely=0.4, relx=0.15)
        n5.bind('<Return>', lambda event: focuson(n6))

        CmdBtn = Menubutton(disp_frame, text='select publisher', bg=btn_colors["bg"], fg=btn_colors["fg"],
                            font=("Calibri", 12, "bold"))
        CmdBtn.place(rely=0.4, relx=0.34)
        CmdBtn.menu = Menu(CmdBtn)
        CmdBtn.menu.add_command(label='Manan', underline=0, command=lambda: set_text(n5, "Manan"))
        CmdBtn.menu.add_command(label='Vipul', underline=0, command=lambda: set_text(n5, "Vipul"))
        CmdBtn.menu.add_command(label='Techmax', underline=0, command=lambda: set_text(n5, "Techmax"))
        CmdBtn.menu.add_command(label='Mah. Govt.', underline=0, command=lambda: set_text(n5, "Mah. Govt."))
        CmdBtn.menu.add_command(label='Sheth', underline=0, command=lambda: set_text(n5, "Sheth"))
        CmdBtn['menu'] = CmdBtn.menu

        Label(disp_frame, text="Quantity", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.48, relx=0.025)
        n6 = Entry(disp_frame, font=normal_font)
        n6.place(rely=0.48, relx=0.15)
        n6.bind('<Return>', lambda event: focuson(n7))

        Label(disp_frame, text="Price", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.56, relx=0.025)
        n7 = Entry(disp_frame, font=normal_font)
        n7.place(rely=0.56, relx=0.15)
        n7.bind('<Return>', lambda event: focuson(n8))

        Label(disp_frame, text="Ids for Individual Books", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.64, relx=0.025)

        Label(disp_frame, text="Book code: ", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.72, relx=0.075, anchor=CENTER)
        n8 = Entry(disp_frame, font=normal_font, width=10)
        n8.place(rely=0.72, relx=0.165, anchor=CENTER)
        n8.bind('<Return>', lambda event: focuson(n9))

        Label(disp_frame, text="Starting from: ", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.72, relx=0.35, anchor=CENTER)
        n9 = Entry(disp_frame, font=normal_font, width=10)
        n9.place(rely=0.72, relx=0.46, anchor=CENTER)
        n9.bind('<Return>', lambda event: focuson(n10))

        Label(disp_frame, text="Category", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.80, relx=0.025)
        n10 = Entry(disp_frame, font=normal_font)
        n10.place(rely=0.80, relx=0.15)
        n10.bind('<Return>', None)

        CmdBtn = Menubutton(disp_frame, text='Category', bg=btn_colors["bg"], fg=btn_colors["fg"],
                            font=("calibri", 12, "bold"))
        CmdBtn.place(rely=0.80, relx=0.34)
        CmdBtn.menu = Menu(CmdBtn)
        # f = open("book_cat.txt", "r+")
        # ff = f.readlines()
        # print(ff)
        ff = ["Textbook", "Novel", "Reference book"]
        for i in range(0, len(ff)):
            ff[i] = ff[i].replace('\n', "")
        # print(ff)
        CmdBtn.menu.add_command(label=ff[0], underline=0, command=lambda: set_text(n10, ff[0]))
        CmdBtn.menu.add_command(label=ff[1], underline=0, command=lambda: set_text(n10, ff[1]))
        CmdBtn.menu.add_command(label=ff[2], underline=0, command=lambda: set_text(n10, ff[2]))
        CmdBtn['menu'] = CmdBtn.menu

        def add_book_query():
            bnam = n1.get()
            anam = n2.get()
            edi = n3.get()
            btit = n4.get()
            pub = n5.get()
            cat = n10.get()
            desc = ""
            alp = n8.get()
            num = n9.get()

            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                if bnam != "" and anam != "" and pub != "" and cat != "" and btit != "" and alp != "" and num != "":
                    try:
                        qua = int(n6.get())
                    except ValueError:
                        # popup
                        pop("Please Enter Valid quantity")
                        return
                    try:
                        pri = int(n7.get())
                    except ValueError:
                        # popup
                        pop("Please Enter Valid Price")
                        return
                    try:
                        num = int(n9.get())
                    except ValueError:
                        # popup
                        pop("Please Enter Valid ID number")
                        return

                    temp = list(alp)
                    for ch in range(0, len(temp)):
                        if str.isdigit(temp[ch]) == True:
                            # popup
                            pop("Please Enter Valid Alpha code for Book ID")
                            return

                    already_assigned = []
                    cur.execute(
                        f"SELECT book_topic FROM book WHERE book_title = '{btit}' AND author_name = '{anam}' AND book_topic='{bnam}'")
                    arr = cur.fetchall()
                    conn.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

                if len(arr) == 0:
                    def process():
                        try:
                            qua = int(n6.get())
                            avqu = qua
                            num = n9.get()
                            avail = "yes"
                            conn1 = mysql.connector.connect(user='root', password=db_config["db_password"],
                                                            host='127.0.0.1', database=db_config["db_name"])
                            cur1 = conn1.cursor()
                            # insert into book list
                            print(f"this is quantity{qua}")
                            for i in range(0, qua):
                                ind = alp + num
                                tup1 = (bnam, anam, desc, edi, pri, btit, avail, ind)
                                # book_topic, author_name, description, edition, price, book_title, availability, book_id
                                # check if a book has been assigned this id
                                cur1.execute(f"Select * from book_list where book_id = '{ind}'")
                                check = cur1.fetchall()
                                if len(check) == 0:
                                    print(f"ind {ind}")
                                    cur1.execute("INSERT into book_list values(%s, %s, %s, %s, %s, %s, %s, %s)", tup1)
                                else:
                                    already_assigned.append(ind)
                                    avqu = avqu - 1
                                    qua = qua - 1
                                    print(f"else is executing at{ind}")
                                num = int(num) + 1
                                num = str(num)

                            # add a new book
                            print(f"This is second qua{qua}")
                            if qua > 0:
                                tup = (bnam, anam, avqu, qua, pub, cat, btit)
                                cur1.execute("INSERT into book values(%s, %s, %s, %s, %s, %s, %s)", tup)

                                # transaction
                                curtime = datetime.datetime.now()
                                curdate = date.today()
                                tr_id = update_id(0)
                                trans_stmt = f"{qua} copies of {btit} have been added to library"
                                tran = (tr_id, curdate, curtime, trans_stmt)
                                cur1.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)
                                conn1.commit()
                                conn1.close()
                                # popup
                                pop("Books added successfully")
                        except (mysql.connector.errors.ProgrammingError):
                            print("wrong database pass, please change it in the setting")

                        if len(already_assigned) > 0:
                            pop(f"Ids {already_assigned} has already been assigned therefore these books were not added")

                    confirm(f"Add '{n1.get()}' to the library?", process)
                else:
                    # add to the already existing book (update)
                    def else_upd():
                        try:
                            already_assigned = []
                            qua = int(n6.get())
                            conn2 = mysql.connector.connect(user='root', password=db_config["db_password"],
                                                            host='127.0.0.1', database=db_config["db_name"])
                            cur2 = conn2.cursor()
                            cur2.execute(f"select total_quantity, available_quantity from book WHERE book_title = '{btit}'")
                            arr2 = cur2.fetchall()

                            avail = "yes"
                            num = n9.get()
                            # insert into book list
                            for ii in range(0, qua):
                                ind = alp + num
                                tup1 = (bnam, anam, desc, edi, pri, btit, avail, ind)
                                cur2.execute(f"select * from book_list where book_id = '{ind}'")
                                check = cur2.fetchall()
                                if len(check) == 0:
                                    cur2.execute("INSERT into book_list values(%s, %s, %s, %s, %s, %s, %s, %s)", tup1)
                                else:
                                    already_assigned.append(ind)
                                    qua = qua - 1
                                    print(qua)

                                num = int(num) + 1
                                num = str(num)

                            neu_total = arr2[0][0] + qua
                            neu_avail = arr2[0][1] + qua
                            # update
                            if qua > 0:
                                cur2.execute(
                                    f"UPDATE book SET available_quantity = '{neu_avail}', total_quantity = '{neu_total}' WHERE book_title = '{btit}'")

                                # transaction
                                curtime = datetime.datetime.now()
                                curdate = date.today()
                                tr_id = update_id(0)
                                trans_stmt = f"{qua} copies of {btit} have been added to library"
                                tran = (tr_id, curdate, curtime, trans_stmt)
                                cur2.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)
                                conn2.commit()
                                conn2.close()
                                # popup
                                pop("Books added successfully")
                            if len(already_assigned) > 0:
                                pop(f"Ids {already_assigned} has already been assigned therefore these books were not added")
                        except (mysql.connector.errors.ProgrammingError):
                            print("wrong database pass, please change it in the setting")

                    # popup
                    confirm(f"This book already exists, add new books to it?", else_upd)
            else:
                # popup
                pop("Please fill-in all the mandatory fields")
            conn.close()

        Button(disp_frame, text="Add books", fg=btn_colors["fg"], bg=btn_colors["bg"], font=bold_font,
               command=add_book_query) \
            .place(rely=0.82, relx=0.50)
        Button(disp_frame, text="Reset", bg="red", fg="white", font=normal_font, relief=RAISED,
               command=lambda: clear_fields(n1, n2, n3, n4, n5, n6, n7, n9)).place(rely=0.05, relx=0.5, anchor=CENTER)

    # remove single book
    def rem_single_book_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Label(disp_frame, text="Book ID", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.24, relx=0.025)

        n1 = Entry(disp_frame, font=normal_font)
        n1.place(rely=0.24, relx=0.15)

        def rem_sin_book_query():
            # remove a book
            bid = n1.get()
            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()

                cur.execute(f"select book_title from book_list WHERE book_id = '{bid}'")
                res = cur.fetchall()
                if len(res) > 0:
                    btit = res[0][0]
                    cur.execute(f"select available_quantity, total_quantity from book WHERE book_title = '{btit}'")
                    res2 = cur.fetchall()
                    cur.execute(f"DELETE from book_list WHERE book_id = '{bid}'")
                    neu_avbl_quan = res2[0][0] - 1
                    neu_tot_quan = res2[0][1] - 1
                    cur.execute(
                        f"UPDATE book SET available_quantity = '{neu_avbl_quan}', total_quantity = '{neu_tot_quan}' WHERE book_title = '{btit}'")

                    curtime = datetime.datetime.now()
                    curdate = date.today()
                    tr_id = update_id(0)
                    trans_stmt = f"One Copy of {btit} with ID {bid} has been removed from library"
                    tran = (tr_id, curdate, curtime, trans_stmt)
                    cur.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)
                    pop("Book removed successfully")
                else:
                    pop("This book does not exists")
                conn.commit()
                conn.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Remove", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_sin_book_query).place(relx=0.25, rely=0.32)

    # remove books within a range of id
    def rem_some_book_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Label(disp_frame, text="Alpha code", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.24, relx=0.025)
        n1 = Entry(disp_frame, font=normal_font)
        n1.place(rely=0.32, relx=0.025)

        Label(disp_frame, text="Numeric code", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.24, relx=0.35)

        Label(disp_frame, text="Starting from", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.32, relx=0.35)
        n2 = Entry(disp_frame, font=normal_font)
        n2.place(rely=0.32, relx=0.5)

        Label(disp_frame, text="upto", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.40, relx=0.35)
        n3 = Entry(disp_frame, font=normal_font)
        n3.place(rely=0.40, relx=0.5)

        def rem_some_book_query():
            try:
                # remove some books
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                # bid = n3.get()
                not_av_str = ""
                strt = int(n2.get())
                end = int(n3.get())
                alp_code = n1.get()
                temp = strt
                cur = conn.cursor()

                # if book exists
                book_removed = []
                for i in range(strt, end + 1):

                    alp = alp_code
                    alp = alp + str(temp)
                    temp = temp + 1

                    cur.execute(f"select book_title from book_list WHERE book_id = '{alp}'")
                    res = cur.fetchall()
                    if len(res) > 0:
                        btit = res[0][0]
                        cur.execute(f"select available_quantity, total_quantity from book WHERE book_title = '{btit}'")
                        res2 = cur.fetchall()
                        cur.execute(f"DELETE from book_list WHERE book_id = '{alp}'")

                        book_removed.append(alp)

                        neu_avbl_quan = res2[0][0] - 1
                        neu_tot_quan = res2[0][1] - 1
                        cur.execute(
                            f"UPDATE book SET available_quantity = '{neu_avbl_quan}', total_quantity = '{neu_tot_quan}' WHERE book_title = '{btit}'")
                    else:
                        # popup
                        not_av_str = not_av_str + alp + ", "
                        if i == end:
                            pop(f"book of id {not_av_str} are not available")
                if len(book_removed) > 0:
                    curtime = datetime.datetime.now()
                    curdate = date.today()
                    tr_id = update_id(0)
                    trans_stmt = f"Books with ID {book_removed} have been removed from library"
                    tran = (tr_id, curdate, curtime, trans_stmt)
                    cur.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)
                conn.commit()
                conn.close()
                pop("Books removed successfully")

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Remove", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_some_book_query).place(relx=0.5, rely=0.48)

    # remove all books with certain condition
    def rem_all_book_vin():
        clear_frame(disp_frame)

        Label(disp_frame, text="Book Title", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.16, relx=0.025)
        n2 = Entry(disp_frame, font=normal_font)
        n2.place(rely=0.16, relx=0.15)

        Label(disp_frame, text="Edition", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(rely=0.24, relx=0.025)
        n3 = Entry(disp_frame, font=normal_font)
        n3.place(rely=0.24, relx=0.15)

        # to be continued
        def rem_all_book_query():
            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                edi = n3.get()
                btit = n2.get()
                if btit != "":
                    cur.execute(
                        f"select book_title, available_quantity, total_quantity from book WHERE book_title = '{btit}'")
                    res = cur.fetchall()
                    if len(res) > 0 and edi == "":
                        cur.execute(f"DELETE FROM book WHERE book_title = '{btit}'")
                        cur.execute(f"DELETE FROM book_list WHERE book_title = '{btit}'")
                        curtime = datetime.datetime.now()
                        curdate = date.today()
                        tr_id = update_id(0)
                        trans_stmt = f"All Books with {btit} have been removed from library"
                        tran = (tr_id, curdate, curtime, trans_stmt)
                        cur.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)

                    elif len(res) > 0 and edi != "":
                        cur.execute(f"Select available_quantity, total_quantity from book where book_title = '{btit}'")
                        cnt = cur.fetchall()
                        curtime = datetime.datetime.now()
                        curdate = date.today()
                        tr_id = update_id(0)
                        trans_stmt = f"All Copies of {btit} of {edi} have been removed from library"
                        tran = (tr_id, curdate, curtime, trans_stmt)
                        cur.execute("INSERT INTO transaction VALUES(%s, %s, %s, %s)", tran)

                        print(len(cnt))
                        cur.execute(
                            f"UPDATE book SET available_quantity = '{cnt[0][0] - len(cnt)}', total_quantity = '{cnt[0][1] - len(cnt)}' WHERE book_title = '{btit}'")
                        cur.execute(f"DELETE FROM book_list WHERE book_title = '{btit}' and edition = '{edi}'")
                    else:
                        # popup
                        pop("book not available")
                    conn.commit()
                    conn.close()
                else:
                    # popup
                    pop("please enter book title")

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")


        Button(disp_frame, text="Remove", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_all_book_query).place(relx=0.32, rely=0.4)

    def rem_book_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Button(disp_frame, text="Remove single book", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_single_book_vin) \
            .place(rely=0.16, relx=0.025)
        Button(disp_frame, text="Remove book within a range", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_some_book_vin) \
            .place(rely=0.24, relx=0.025)
        Button(disp_frame, text="Remove all books", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=rem_all_book_vin) \
            .place(rely=0.32, relx=0.025)

    def issue_book_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Label(disp_frame, text="Member ID:", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font).place(
            rely=0.08, relx=0.025)
        n1 = Entry(disp_frame, font=normal_font)
        n1.place(rely=0.08, relx=0.15)
        n1.focus()
        n1.bind('<Return>', lambda event: focuson(n3))

        Label(disp_frame, text="Book ID", bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font).place(rely=0.16,
                                                                                                              relx=0.025)
        n3 = Entry(disp_frame, font=normal_font)
        n3.place(rely=0.16, relx=0.15)
        n3.bind('<Return>', None)

        def issue_book_query():
            try:
                memid = n1.get()
                bid = n3.get()
                curtime = datetime.datetime.now()
                curdate = date.today()
                tr_id = update_id(0)

                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                # search for this member
                cur.execute(
                    f"select member_id, email, name, academic_year, roll_no, course from members where member_id = '{memid}'")
                arr = cur.fetchall()

                # if registered
                if len(arr) > 0:
                    # search for this book
                    cur.execute(f"select book_title, availability from book_list where book_id = '{bid}'")
                    book = cur.fetchall()

                    if len(book) > 0:
                        btit = book[0][0]
                        # search for this book
                        cur.execute(f"select available_quantity from book where book_title = '{btit}'")
                        book_q = cur.fetchall()
                        # check for quantity
                        avbl_qu = book_q[0][0]

                        if book[0][1] == "yes":
                            # reduce book quantity by one in book table
                            upd = (avbl_qu - 1, btit)
                            cur.execute("UPDATE book SET available_quantity = %s WHERE book_title = %s", upd)

                            # change availability from yes to no in book_list
                            temp = "no"
                            cur.execute(f"UPDATE book_list SET availability = '{temp}' WHERE book_id = '{bid}'")

                            # insert into issued books
                            memid = arr[0][0]
                            bookid = bid
                            booktitl = btit
                            memname = arr[0][2]
                            mail = arr[0][1]
                            acad = arr[0][3]
                            cour = arr[0][5]
                            issued = [memid, bookid, booktitl, memname, mail, acad, cour, curdate, curtime]
                            cur.execute('INSERT into issued values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', issued)

                            trans_stmt = f"Book {btit} with ID {bid} has been issued to {memname} with ID {memid} of {cour}"
                            tran = (tr_id, curdate, curtime, trans_stmt)

                            # record this transaction
                            cur.execute('INSERT into transaction values(%s, %s, %s, %s)', tran)
                            conn.commit()
                            pop("Books issued successfully")
                        else:
                            # popup
                            pop(f"This book has already been issued")
                    else:
                        # popup
                        pop(f"No book with id {bid} is available")
                else:
                    # popup
                    pop(f"No Member with id {memid} is registered")
                conn.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Issue Book", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=issue_book_query).place(rely=0.26, relx=0.4)

    def retrieve_book_vin():
        clear_frame(disp_frame)
        clear_frame(status)

        Label(disp_frame, text="Book ID", width=10, bg=main_colors["bg"], fg=main_colors["fg"], font=normal_font) \
            .place(rely=0.08, relx=0.025)
        n3 = Entry(disp_frame, font=normal_font)
        n3.place(rely=0.08, relx=0.15)
        n3.bind('<Return>', None)

        def retrieve_book_query():
            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()

                # to check for availability of book
                bid = n3.get()
                cur.execute(f"select book_title, availability from book_list where book_id = '{bid}'")
                book = cur.fetchall()

                if len(book) > 0:
                    if book[0][1] == "no":
                        btit = book[0][0]
                        cur.execute(f"select available_quantity from book where book_title = '{btit}'")
                        book2 = cur.fetchall()

                        # increase the book quantity by 1 in book table
                        avbl_qua = book2[0][0]
                        upd = (avbl_qua + 1, btit)
                        cur.execute("UPDATE book SET available_quantity = %s WHERE book_title = %s", upd)

                        # change availability from yes to no in book_list
                        temp = "yes"
                        cur.execute(f"UPDATE book_list SET availability = '{temp}' WHERE book_id = '{bid}'")

                        # search the member name and member id from issued table
                        cur.execute(f"SELECT name, member_id, course FROM issued WHERE book_id = '{bid}'")
                        mem = cur.fetchall()
                        mnam = mem[0][0]
                        mid = mem[0][1]
                        cour = mem[0][2]

                        # delete record from issued and defaulter tables
                        cur.execute(f"DELETE FROM issued WHERE book_id = '{bid}'")
                        cur.execute(f"DELETE FROM defaulter WHERE book_id = '{bid}'")

                        # record the transaction
                        curtime = datetime.datetime.now()
                        curdate = date.today()
                        tr_id = update_id(0)
                        trans_stmt = f"Books {btit} with {bid} has been retrieved from {mnam} with ID {mid} of {cour}"
                        tran = (tr_id, curdate, curtime, trans_stmt)
                        cur.execute('INSERT into transaction values(%s, %s, %s, %s)', tran)
                        conn.commit()
                        pop("Book retrieved successfully")
                    else:
                        # popup
                        pop("This book is not issued")
                else:
                    # popup
                    pop("book not available")
                conn.close()

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Retrieve books", bg=btn_colors["bg"], fg=btn_colors["fg"], font=bold_font,
               command=retrieve_book_query).place(rely=0.16, relx=0.15)

    # display functions
    def disp_members():
        clear_frame(status)
        col_label = ["Member ID", "Name", "Contact no.", "Address", "Email", "Academic Year", "Division", "Batch",
                     "Roll No.", "Course"]

        def disp_mem():
            columns = ['id', 'name', 'phone no', 'address', 'mail', 'academic year', 'division', 'batch', 'roll no',
                       'course']

            col_text = ["Member ID", "Name", "Contact no.", "Address", "Email", "Academic Year", "Division", "Batch",
                        "Roll No.", "Course"]
            col_ref = ["member_id", "name", "contact_no", "address", "email", "academic_year", "division", "batch",
                       "roll_no", "course"]
            par_list = ["member_id", "name", "contact_no", "address", "email", "academic_year", "division", "batch",
                        "roll_no", "course", ", ", " from members"]
            que_str = "select "

            if b2.cget("bg") == btn_colors["bg"]:
                que_str += par_list[0]
            elif b2.cget("bg") == "red":
                col_ref.remove("member_id")
                col_text.remove("Member ID")
                columns.remove("id")

            if b3.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[1]
                else:
                    que_str += par_list[1]
            elif b3.cget("bg") == "red":
                col_ref.remove("name")
                col_text.remove("Name")
                columns.remove("name")

            if b4.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[2]
                else:
                    que_str += par_list[2]
            elif b4.cget("bg") == "red":
                col_ref.remove("contact_no")
                col_text.remove("Contact no.")
                columns.remove("phone no")

            if b5.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[3]
                else:
                    que_str += par_list[3]
            elif b5.cget("bg") == "red":
                col_ref.remove("address")
                col_text.remove("Address")
                columns.remove("address")

            if b6.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[4]
                else:
                    que_str += par_list[4]
            elif b6.cget("bg") == "red":
                col_ref.remove("email")
                col_text.remove("Email")
                columns.remove("mail")

            if b7.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[5]
                else:
                    que_str += par_list[5]
            elif b7.cget("bg") == "red":
                col_ref.remove("academic_year")
                col_text.remove("Academic Year")
                columns.remove("academic year")

            if b8.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[6]
                else:
                    que_str += par_list[6]
            elif b8.cget("bg") == "red":
                col_ref.remove("division")
                col_text.remove("Division")
                columns.remove("division")

            if b9.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[7]
                else:
                    que_str += par_list[7]
            elif b9.cget("bg") == "red":
                col_ref.remove("batch")
                col_text.remove("Batch")
                columns.remove("batch")

            if b10.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[8]
                else:
                    que_str += par_list[8]
            elif b10.cget("bg") == "red":
                col_ref.remove("roll_no")
                col_text.remove("Roll No.")
                columns.remove("roll no")

            if b11.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[10]
                    que_str += par_list[9]
                else:
                    que_str += par_list[9]
            elif b11.cget("bg") == "red":
                col_ref.remove("course")
                col_text.remove("Course")
                columns.remove("course")

            que_str += par_list[11]

            clear_frame(disp_frame)
            Label(disp_frame, text="Member List", font=("Arial", 20, 'bold'), bg="#999999").pack(side=TOP)
            # 100, 100, 100, 400, 250, 80, 50, 30, 50, 100

            tree = ttk.Treeview(disp_frame, columns=columns, show='headings')
            xscrollbar = ttk.Scrollbar(disp_frame, orient=HORIZONTAL, command=tree.xview)
            tree.configure(xscroll=xscrollbar.set)
            xscrollbar.pack(side=TOP, fill=X)
            yscrollbar = ttk.Scrollbar(disp_frame, orient=VERTICAL, command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=RIGHT, fill=Y)

            for c in range(0, len(columns)):
                tree.heading(columns[c], text=col_text[c])
                tree.column(columns[c], minwidth=0, width=100)

            try:
                con = mysql.connector.connect(user='root', password=db_config["db_password"],
                                              host='127.0.0.1', database=db_config["db_name"])
                cur = con.cursor()
                # print(que_str) print(columns)
                cur.execute(que_str)
                member = cur.fetchall()
                for mem in member:
                    tree.insert('', END, values=mem)
                tree.pack(side=LEFT, expand=YES, fill=BOTH)

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")


        b2 = Button(status, text=col_label[0], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b2))
        b3 = Button(status, text=col_label[1], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b3))
        b4 = Button(status, text=col_label[2], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b4))
        b5 = Button(status, text=col_label[3], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b5))
        b6 = Button(status, text=col_label[4], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b6))
        b7 = Button(status, text=col_label[5], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b7))
        b8 = Button(status, text=col_label[6], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b8))
        b9 = Button(status, text=col_label[7], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b9))
        b10 = Button(status, text=col_label[8], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                     command=lambda: change_color(b10))
        b11 = Button(status, text=col_label[9], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                     command=lambda: change_color(b11))

        b12 = Button(status, text="Generate", pady=3, width=12, font=('Arial', 10, 'bold'), bg="blue", command=disp_mem)

        b2.grid(row=0, column=1)
        b3.grid(row=0, column=2)
        b4.grid(row=0, column=3)
        b5.grid(row=0, column=4)
        b6.grid(row=0, column=5)
        b7.grid(row=1, column=1)
        b8.grid(row=1, column=2)
        b9.grid(row=1, column=3)
        b10.grid(row=1, column=4)
        b11.grid(row=1, column=5)
        b12.grid(row=3, column=1)

        disp_mem()

    def disp_issued():
        clear_frame(status)
        col_label = ["Member ID", "Book ID", "Book Title", "Member Name", "Email ID", "Academic Year",
                     "Course", "Borrow Date", "Borrow Time"]

        def disp_iss():
            columns = ["member id", "book id", "book title", "name", "email", "academic year", "course",
                       "borrow date", "borrow time"]
            col_text = ["Member ID", "Book ID", "Book Title", "Member Name", "Email ID", "Academic Year",
                        "Course", "Borrow Date", "Borrow Time"]

            col_ref = ["member_id", "book_id", "book_title", "name", "email", "academic_year", "course",
                       "borro_date", "borro_time"]
            par_list = ["member_id", "book_id", "book_title", "name", "email", "academic_year", "course",
                        "borro_date", "borro_time", ", ", " from issued"]
            que_str = "select "

            if b2.cget("bg") == btn_colors["bg"]:
                que_str += par_list[0]
            elif b2.cget("bg") == "red":
                col_ref.remove("member_id")
                col_text.remove("Member ID")
                columns.remove("member id")

            if b3.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[1]
                else:
                    que_str += par_list[1]
            elif b3.cget("bg") == "red":
                col_ref.remove("book_id")
                col_text.remove("Book ID")
                columns.remove("book id")

            if b4.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[2]
                else:
                    que_str += par_list[2]
            elif b4.cget("bg") == "red":
                col_ref.remove("book_title")
                col_text.remove("Book Title")
                columns.remove("book title")

            if b5.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[3]
                else:
                    que_str += par_list[3]
            elif b5.cget("bg") == "red":
                col_ref.remove("name")
                col_text.remove("Member Name")
                columns.remove("name")

            if b6.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[4]
                else:
                    que_str += par_list[4]
            elif b6.cget("bg") == "red":
                col_ref.remove("email")
                col_text.remove("Email ID")
                columns.remove("email")

            if b7.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[5]
                else:
                    que_str += par_list[5]
            elif b7.cget("bg") == "red":
                col_ref.remove("academic_year")
                col_text.remove("Academic Year")
                columns.remove("academic year")

            if b8.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[6]
                else:
                    que_str += par_list[6]
            elif b8.cget("bg") == "red":
                col_ref.remove("course")
                col_text.remove("Course")
                columns.remove("course")

            if b9.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[7]
                else:
                    que_str += par_list[7]
            elif b9.cget("bg") == "red":
                col_ref.remove("borro_date")
                col_text.remove("Borrow Date")
                columns.remove("borrow date")

            if b10.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[8]
                else:
                    que_str += par_list[8]
            elif b10.cget("bg") == "red":
                col_ref.remove("borro_time")
                col_text.remove("Borrow Time")
                columns.remove("borrow time")

            que_str += par_list[10]
            # print(que_str)
            clear_frame(disp_frame)
            Label(disp_frame, text="Issued Books", font=("Arial", 20, 'bold'), bg=main_colors["bg"],
                  fg=main_colors["fg"], ).pack(side=TOP)
            # 100, 100, 100, 400, 250, 80, 50, 30, 50, 100

            tree = ttk.Treeview(disp_frame, columns=columns, show='headings')
            xscrollbar = ttk.Scrollbar(disp_frame, orient=HORIZONTAL, command=tree.xview)
            tree.configure(xscroll=xscrollbar.set)
            xscrollbar.pack(side=TOP, fill=X)
            yscrollbar = ttk.Scrollbar(disp_frame, orient=VERTICAL, command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=RIGHT, fill=Y)

            for c in range(0, len(columns)):
                tree.heading(columns[c], text=col_text[c])
                tree.column(columns[c], minwidth=0, width=100)

            try:
                con = mysql.connector.connect(user='root', password=db_config["db_password"],
                                              host='127.0.0.1', database=db_config["db_name"])
                cur = con.cursor()
                # print(que_str) print(columns)
                cur.execute(que_str)
                member = cur.fetchall()
                for mem in member:
                    tree.insert('', END, values=mem)
                tree.pack(side=LEFT, expand=YES, fill=BOTH)

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        b2 = Button(status, text=col_label[0], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b2))
        b3 = Button(status, text=col_label[1], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b3))
        b4 = Button(status, text=col_label[2], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b4))
        b5 = Button(status, text=col_label[3], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b5))
        b6 = Button(status, text=col_label[4], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b6))
        b7 = Button(status, text=col_label[5], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b7))
        b8 = Button(status, text=col_label[6], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b8))
        b9 = Button(status, text=col_label[7], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b9))
        b10 = Button(status, text=col_label[8], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                     command=lambda: change_color(b10))
        b13 = Button(status, text="Generate", pady=3, width=12, font=('Arial', 10, 'bold'), bg="blue",
                     command=disp_iss)

        b2.grid(row=1, column=1)
        b3.grid(row=1, column=2)
        b4.grid(row=1, column=3)
        b5.grid(row=1, column=4)
        b6.grid(row=1, column=5)
        b7.grid(row=2, column=1)
        b8.grid(row=2, column=2)
        b9.grid(row=2, column=3)
        b10.grid(row=2, column=4)
        b13.grid(row=2, column=5)

        disp_iss()

    def disp_book_list():
        clear_frame(status)
        col_label = ["Book Topic", "Author Name", "Description", "Edition", "Price", "Availability", "Title", "Book Id"]

        def disp_books_list():
            columns = ["book topic", "author name", "description", "edition", "price", "availability", "title",
                       "book id"]
            col_text = ["Book Topic", "Author Name", "Description", "Edition", "Price", "Availability", "Title",
                        "Book Id"]
            col_ref = ["book_topic", "author_name", "description", "edition", "price", "availability", "book_title",
                       "book_id"]
            par_list = ["book_topic", "author_name", "description", "edition", "price", "availability", "book_title",
                        "book_id", ", ", " from book_list"]
            que_str = "select "

            if b2.cget("bg") == btn_colors["bg"]:
                que_str += par_list[0]
            elif b2.cget("bg") == "red":
                col_ref.remove("book_topic")
                col_text.remove("Book Topic")
                columns.remove("book topic")

            if b3.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[8]
                    que_str += par_list[1]
                else:
                    que_str += par_list[1]
            elif b3.cget("bg") == "red":
                col_ref.remove("author_name")
                col_text.remove("Author Name")
                columns.remove("author name")

            if b4.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[8]
                    que_str += par_list[2]
                else:
                    que_str += par_list[2]
            elif b4.cget("bg") == "red":
                col_ref.remove("description")
                col_text.remove("Description")
                columns.remove("description")

            if b5.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[8]
                    que_str += par_list[3]
                else:
                    que_str += par_list[3]
            elif b5.cget("bg") == "red":
                col_ref.remove("edition")
                col_text.remove("Edition")
                columns.remove("edition")

            if b6.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[8]
                    que_str += par_list[4]
                else:
                    que_str += par_list[4]
            elif b6.cget("bg") == "red":
                col_ref.remove("price")
                col_text.remove("Price")
                columns.remove("price")

            if b7.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[8]
                    que_str += par_list[5]
                else:
                    que_str += par_list[5]
            elif b7.cget("bg") == "red":
                col_ref.remove("availability")
                col_text.remove("Availability")
                columns.remove("availability")

            if b8.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[8]
                    que_str += par_list[6]
                else:
                    que_str += par_list[6]
            elif b8.cget("bg") == "red":
                col_ref.remove("book_title")
                col_text.remove("Title")
                columns.remove("title")

            if b9.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[8]
                    que_str += par_list[7]
                else:
                    que_str += par_list[7]
            elif b9.cget("bg") == "red":
                col_ref.remove("book_id")
                col_text.remove("Book Id")
                columns.remove("book id")

            que_str += par_list[9]

            clear_frame(disp_frame)

            Label(disp_frame, text="Books' List", font=("Arial", 20, 'bold'), bg=main_colors["bg"],
                  fg=main_colors["fg"]).pack(side=TOP)
            # 100, 100, 100, 400, 250, 80, 50, 30, 50, 100

            Button(disp_frame, text="Display Issued Books", command=disp_issued, font=bold_font, bg=btn_colors["bg"],
                   fg=main_colors["fg"]).place(relx=0.91, rely=0.03, anchor=CENTER)

            tree = ttk.Treeview(disp_frame, columns=columns, show='headings')
            xscrollbar = ttk.Scrollbar(disp_frame, orient=HORIZONTAL, command=tree.xview)
            tree.configure(xscroll=xscrollbar.set)
            xscrollbar.pack(side=TOP, fill=X)
            yscrollbar = ttk.Scrollbar(disp_frame, orient=VERTICAL, command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=RIGHT, fill=Y)

            for c in range(0, len(columns)):
                tree.heading(columns[c], text=col_text[c])
                tree.column(columns[c], minwidth=0, width=100)

            try:
                con = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                              database=db_config["db_name"])
                cur = con.cursor()
                cur.execute(que_str)

                member = cur.fetchall()
                for mem in member:
                    tree.insert('', END, values=mem)
                tree.pack(side=LEFT, expand=YES, fill=BOTH)
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        b2 = Button(status, text=col_label[0], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b2))
        b3 = Button(status, text=col_label[1], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b3))
        b4 = Button(status, text=col_label[2], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b4))
        b5 = Button(status, text=col_label[3], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b5))
        b6 = Button(status, text=col_label[4], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b6))
        b7 = Button(status, text=col_label[5], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b7))
        b8 = Button(status, text=col_label[6], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b8))
        b9 = Button(status, text=col_label[7], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b8))
        b13 = Button(status, text="Generate", pady=3, width=12, font=('Arial', 10, 'bold'), bg="blue",
                     command=disp_books_list)

        b2.grid(row=1, column=1)
        b3.grid(row=1, column=2)
        b4.grid(row=1, column=3)
        b5.grid(row=1, column=4)
        b6.grid(row=1, column=5)
        b7.grid(row=1, column=6)
        b8.grid(row=2, column=1)
        b9.grid(row=2, column=2)
        b13.grid(row=2, column=3)

        disp_books_list()

    def disp_book():
        clear_frame(status)
        col_label = ["Book Topic", "Author Name", "Available", "Total Quantity", "Publisher", "Category", "Title"]

        def disp_books():
            columns = ["book topic", "author name", "available quantity", "total quantity", "publisher", "category",
                       "title"]
            col_text = ["Book Topic", "Author Name", "Available Quantity", "Total Quantity", "Publisher", "Category",
                        "Title"]
            col_ref = ["book_topic", "author_name", "available_quantity", "total_quantity", "publisher", "category",
                       "book_title"]
            par_list = ["book_topic", "author_name", "available_quantity", "total_quantity", "publisher", "category",
                        "book_title", ", ", " from book"]
            que_str = "select "

            if b2.cget("bg") == btn_colors["bg"]:
                que_str += par_list[0]
            elif b2.cget("bg") == "red":
                col_ref.remove("book_topic")
                col_text.remove("Book Topic")
                columns.remove("book topic")

            if b3.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[7]
                    que_str += par_list[1]
                else:
                    que_str += par_list[1]
            elif b3.cget("bg") == "red":
                col_ref.remove("author_name")
                col_text.remove("Author Name")
                columns.remove("author name")

            if b4.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[7]
                    que_str += par_list[2]
                else:
                    que_str += par_list[2]
            elif b4.cget("bg") == "red":
                col_ref.remove("available_quantity")
                col_text.remove("Available Quantity")
                columns.remove("available quantity")

            if b5.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[7]
                    que_str += par_list[3]
                else:
                    que_str += par_list[3]
            elif b5.cget("bg") == "red":
                col_ref.remove("total_quantity")
                col_text.remove("Total Quantity")
                columns.remove("total quantity")

            if b6.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[7]
                    que_str += par_list[4]
                else:
                    que_str += par_list[4]
            elif b6.cget("bg") == "red":
                col_ref.remove("publisher")
                col_text.remove("Publisher")
                columns.remove("publisher")

            if b7.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[7]
                    que_str += par_list[5]
                else:
                    que_str += par_list[5]
            elif b7.cget("bg") == "red":
                col_ref.remove("category")
                col_text.remove("Category")
                columns.remove("category")

            if b8.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[7]
                    que_str += par_list[6]
                else:
                    que_str += par_list[6]
            elif b8.cget("bg") == "red":
                col_ref.remove("book_title")
                col_text.remove("Title")
                columns.remove("title")

            que_str += par_list[8]

            clear_frame(disp_frame)

            Label(disp_frame, text="Books' List", font=("Arial", 20, 'bold'), bg=main_colors["bg"],
                  fg=main_colors["fg"]).pack(side=TOP)
            # 100, 100, 100, 400, 250, 80, 50, 30, 50, 100
            Button(disp_frame, text="All Book List", command=disp_book_list, font=bold_font, bg=btn_colors["bg"],
                   fg=main_colors["fg"]).place(relx=0.09, rely=0.03, anchor=CENTER)

            Button(disp_frame, text="Display Issued Books", command=disp_issued, font=bold_font, bg=btn_colors["bg"],
                   fg=main_colors["fg"]).place(relx=0.91, rely=0.03, anchor=CENTER)

            tree = ttk.Treeview(disp_frame, columns=columns, show='headings')
            xscrollbar = ttk.Scrollbar(disp_frame, orient=HORIZONTAL, command=tree.xview)
            tree.configure(xscroll=xscrollbar.set)
            xscrollbar.pack(side=TOP, fill=X)
            yscrollbar = ttk.Scrollbar(disp_frame, orient=VERTICAL, command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=RIGHT, fill=Y)

            for c in range(0, len(columns)):
                tree.heading(columns[c], text=col_text[c])
                tree.column(columns[c], minwidth=0, width=100)

            try:
                con = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                              database=db_config["db_name"])
                cur = con.cursor()
                # print(que_str) print(columns)
                cur.execute(que_str)
                member = cur.fetchall()
                for mem in member:
                    tree.insert('', END, values=mem)
                tree.pack(side=LEFT, expand=YES, fill=BOTH)

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        b2 = Button(status, text=col_label[0], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b2))
        b3 = Button(status, text=col_label[1], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b3))
        b4 = Button(status, text=col_label[2], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b4))
        b5 = Button(status, text=col_label[3], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b5))
        b6 = Button(status, text=col_label[4], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b6))
        b7 = Button(status, text=col_label[5], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b7))
        b8 = Button(status, text=col_label[6], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b8))
        b13 = Button(status, text="Generate", pady=3, width=12, font=('Arial', 10, 'bold'), bg="blue",
                     command=disp_books)

        b2.grid(row=1, column=1)
        b3.grid(row=1, column=2)
        b4.grid(row=1, column=3)
        b5.grid(row=1, column=4)
        b6.grid(row=2, column=1)
        b7.grid(row=2, column=2)
        b8.grid(row=2, column=3)
        b13.grid(row=2, column=4)

        disp_books()

    def disp_trans():
        clear_frame(status)

        def gen():
            columns = ['transaction id', 'date', 'time', 'operation']
            col_label = ['Transaction ID', 'Date', 'Time', 'Operation']
            col_ref = ['transaction_id', "trans_date", "trans_time", "operation"]
            par_list = ["transaction_id ", "trans_date ", "trans_time ", "operation ", ", ",
                        "from transaction order by trans_date"]
            que_str = "select "

            # events on clicking buttons
            if b2.cget("bg") == btn_colors["bg"]:
                que_str += par_list[0]
            elif b2.cget("bg") == "red":
                columns.remove("transaction id")
                col_ref.remove("transaction_id")
                col_label.remove("Transaction ID")

            if b3.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[4]
                    que_str += par_list[1]
                else:
                    que_str += par_list[1]
            elif b3.cget("bg") == "red":
                columns.remove("date")
                col_ref.remove("trans_date")
                col_label.remove("Date")

            if b4.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[4]
                    que_str += par_list[2]
                else:
                    que_str += par_list[2]
            elif b4.cget("bg") == "red":
                columns.remove("time")
                col_ref.remove("trans_time")
                col_label.remove("Time")

            if b5.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[4]
                    que_str += par_list[3]
                else:
                    que_str += par_list[3]
            elif b5.cget("bg") == "red":
                columns.remove("operation")
                col_ref.remove("operation")
                col_label.remove("Operation")

            que_str += par_list[5]
            global res
            res = que_str

            clear_frame(disp_frame)
            tree = ttk.Treeview(disp_frame, columns=columns, show='headings')
            Label(disp_frame, text="Transaction List", font=("Arial", 20, 'bold'), bg=main_colors["bg"],
                  fg=main_colors["fg"], ).pack(side=TOP)

            xscrollbar = ttk.Scrollbar(disp_frame, orient=HORIZONTAL, command=tree.xview)
            tree.configure(xscroll=xscrollbar.set)
            xscrollbar.pack(side=TOP, fill=X)
            yscrollbar = ttk.Scrollbar(disp_frame, orient=VERTICAL, command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=RIGHT, fill=Y)

            for i in range(0, len(columns)):
                tree.heading(columns[i], text=col_label[i])
                if i == len(columns) - 1:
                    tree.column(columns[i], minwidth=50, width=450)
                else:
                    tree.column(columns[i], minwidth=50, width=150)

            try:
                con = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                              database=db_config["db_name"])
                cur = con.cursor()
                cur.execute(res)
                arr = cur.fetchall()
                con.close()
                # iterate through arr and insert each record
                for b in range(len(arr)):
                    tree.insert('', END, values=arr[b])
                tree.pack(side=LEFT, expand=YES, fill=Y)

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        # buttons for columns
        b2 = Button(status, text="Transaction ID", pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b2))
        b3 = Button(status, text="Date", pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b3))
        b4 = Button(status, text="Time", pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b4))
        b5 = Button(status, text="Operation", pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b5))
        b6 = Button(status, text="Generate", pady=3, width=12, font=('Arial', 10, 'bold'), bg="blue", command=gen)

        b2.grid(row=1, column=1)
        b3.grid(row=1, column=2)
        b4.grid(row=1, column=3)
        b5.grid(row=1, column=4)
        b6.grid(row=1, column=5)

        gen()

    def defaulter():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                           database=db_config["db_name"])
            cur = conn.cursor()
            cur.execute("select name, email, book_title, borro_date from defaulter")
            defaulters = cur.fetchall()
        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(mail_id_name, mail_id_pass)

            if len(defaulters) > 0:
                for i in range(0, len(defaulters)):
                    nam = defaulters[i][0]
                    mem_mail = defaulters[i][1]
                    title = defaulters[i][2]
                    dat = defaulters[i][3]

                    message = f"""Dear {nam},
                     You are informed that you have have to return the book '{title}' which you borrowed from the library on {dat} from the CHM library"""
                    s.sendmail(mail_id_name, mem_mail, message)
                s.quit()
                conn.close()
        except smtplib.SMTPAuthenticationError:
            print("wrong email details, please change to correct details in setting menu")

    def disp_defaulter():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                           database=db_config["db_name"])
            cur = conn.cursor()
            # for testing
            # seven_days_before = date.today() - timedelta(minutes=10)
            seven_days_before = date.today() - timedelta(days=7)
            cur.execute(f"select * from issued where borro_date <= '{seven_days_before}'")
            ans = cur.fetchall()
            for i in range(0, len(ans)):
                cur.execute(f"select book_id from defaulter where book_id = '{ans[i][1]}'")
                chk = cur.fetchall()
                if len(chk) == 0:
                    cur.execute("INSERT INTO defaulter VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", ans[i])
                    conn.commit()
            conn.close()
        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")

        clear_frame(status)
        col_label = ["Member ID", "Book ID", "Book Title", "Member Name", "Email ID", "Academic Year",
                     "Course", "Borrow Date", "Borrow Time"]

        def disp_def():
            columns = ["member id", "book id", "book title", "name", "email", "academic year", "course",
                       "borrow date", "borrow time"]
            col_text = ["Member ID", "Book ID", "Book Title", "Member Name", "Email ID", "Academic Year",
                        "Course", "Borrow Date", "Borrow Time"]

            col_ref = ["member_id", "book_id", "book_title", "name", "email", "academic_year", "course",
                       "borro_date", "borro_time"]
            par_list = ["member_id", "book_id", "book_title", "name", "email", "academic_year", "course",
                        "borro_date", "borro_time", ", ", " from defaulter"]
            que_str = "select "

            if b2.cget("bg") == btn_colors["bg"]:
                que_str += par_list[0]
            elif b2.cget("bg") == "red":
                col_ref.remove("member_id")
                col_text.remove("Member ID")
                columns.remove("member id")

            if b3.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[1]
                else:
                    que_str += par_list[1]
            elif b3.cget("bg") == "red":
                col_ref.remove("book_id")
                col_text.remove("Book ID")
                columns.remove("book id")

            if b4.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[2]
                else:
                    que_str += par_list[2]
            elif b4.cget("bg") == "red":
                col_ref.remove("book_title")
                col_text.remove("Book Title")
                columns.remove("book title")

            if b5.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[3]
                else:
                    que_str += par_list[3]
            elif b5.cget("bg") == "red":
                col_ref.remove("name")
                col_text.remove("Member Name")
                columns.remove("name")

            if b6.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[4]
                else:
                    que_str += par_list[4]
            elif b6.cget("bg") == "red":
                col_ref.remove("email")
                col_text.remove("Email ID")
                columns.remove("email")

            if b7.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[5]
                else:
                    que_str += par_list[5]
            elif b7.cget("bg") == "red":
                col_ref.remove("academic_year")
                col_text.remove("Academic Year")
                columns.remove("academic year")

            if b8.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[6]
                else:
                    que_str += par_list[6]
            elif b8.cget("bg") == "red":
                col_ref.remove("course")
                col_text.remove("Course")
                columns.remove("course")

            if b9.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[7]
                else:
                    que_str += par_list[7]
            elif b9.cget("bg") == "red":
                col_ref.remove("borro_date")
                col_text.remove("Borrow Date")
                columns.remove("borrow date")

            if b10.cget("bg") == btn_colors["bg"]:
                if len(que_str) > 7:
                    que_str += par_list[9]
                    que_str += par_list[8]
                else:
                    que_str += par_list[8]
            elif b10.cget("bg") == "red":
                col_ref.remove("borro_time")
                col_text.remove("Borrow Time")
                columns.remove("borrow time")

            que_str += par_list[10]
            # print(que_str)
            clear_frame(disp_frame)
            Label(disp_frame, text="Defaulter", font=("Arial", 20, 'bold'), bg=main_colors["bg"],
                  fg=main_colors["fg"], ).pack(side=TOP)
            # 100, 100, 100, 400, 250, 80, 50, 30, 50, 100
            Button(disp_frame, text="send", command=defaulter, font=bold_font, bg=btn_colors["bg"],
                   fg=main_colors["fg"]).place(relx=0.95, rely=0.03, anchor=CENTER)

            tree = ttk.Treeview(disp_frame, columns=columns, show='headings')
            xscrollbar = ttk.Scrollbar(disp_frame, orient=HORIZONTAL, command=tree.xview)
            tree.configure(xscroll=xscrollbar.set)
            xscrollbar.pack(side=TOP, fill=X)
            yscrollbar = ttk.Scrollbar(disp_frame, orient=VERTICAL, command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=RIGHT, fill=Y)

            for c in range(0, len(columns)):
                tree.heading(columns[c], text=col_text[c])
                tree.column(columns[c], minwidth=0, width=100)

            try:
                con = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                              database=db_config["db_name"])
                cur = con.cursor()
                # print(que_str)  print(columns)
                cur.execute(que_str)
                member = cur.fetchall()
                for mem in member:
                    tree.insert('', END, values=mem)
                    tree.pack(side=LEFT, expand=YES, fill=BOTH)

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        b2 = Button(status, text=col_label[0], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b2))
        b3 = Button(status, text=col_label[1], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b3))
        b4 = Button(status, text=col_label[2], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b4))
        b5 = Button(status, text=col_label[3], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b5))
        b6 = Button(status, text=col_label[4], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b6))
        b7 = Button(status, text=col_label[5], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b7))
        b8 = Button(status, text=col_label[6], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b8))
        b9 = Button(status, text=col_label[7], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                    command=lambda: change_color(b9))
        b10 = Button(status, text=col_label[8], pady=3, width=12, font=('Arial', 10, 'bold'), bg=btn_colors["bg"],
                     command=lambda: change_color(b10))
        b13 = Button(status, text="Generate", pady=3, width=12, font=('Arial', 10, 'bold'), bg="blue",
                     command=disp_def)

        b2.grid(row=1, column=1)
        b3.grid(row=1, column=2)
        b4.grid(row=1, column=3)
        b5.grid(row=1, column=4)
        b6.grid(row=1, column=5)
        b7.grid(row=2, column=1)
        b8.grid(row=2, column=2)
        b9.grid(row=2, column=3)
        b10.grid(row=2, column=4)
        b13.grid(row=2, column=5)

        disp_def()

    # update functions
    # update single functions
    def update_sin_mem():
        clear_frame(disp_frame)
        mem_attr = ["member_id", "name", "contact_no", "address", "email", "academic_year", "division", "batch",
                    "roll_no", "course"]
        Label(disp_frame, text="search member to be updated: ", font=bold_font, fg=main_colors["fg"],
              bg=main_colors["bg"]).place(relx=0.2, rely=0.1, anchor=CENTER)
        e1 = Entry(disp_frame, font=bold_font)
        e1.place(relx=0.4, rely=0.1, anchor=CENTER)

        def search():
            condition = e1.get()
            table_frame = Frame(disp_frame, bg="black", width=800, height=400, background=main_colors["bg"])
            table_frame.place(relx=0.1, rely=0.25)
            table_frame.pack_propagate(False)

            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                cur.execute(f"select * from members where member_id = '{condition}'")
                ans = cur.fetchall()
                # print(ans[0][10])
                if len(ans) > 0:
                    Label(table_frame, text=mem_attr[0], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.05, anchor=CENTER)
                    Label(table_frame, text=mem_attr[1], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.15, anchor=CENTER)
                    Label(table_frame, text=mem_attr[2], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.25, anchor=CENTER)
                    Label(table_frame, text=mem_attr[3], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.35, anchor=CENTER)
                    Label(table_frame, text=mem_attr[4], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.45, anchor=CENTER)
                    Label(table_frame, text=mem_attr[5], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.55, anchor=CENTER)
                    Label(table_frame, text=mem_attr[6], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.65, anchor=CENTER)
                    Label(table_frame, text=mem_attr[7], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.75, anchor=CENTER)
                    Label(table_frame, text=mem_attr[8], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.85, anchor=CENTER)
                    Label(table_frame, text=mem_attr[9], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.95, anchor=CENTER)

                    Label(table_frame, text=ans[0][0], font=normal_font, bg="grey", fg=main_colors["fg"], width=70,
                          anchor="w").place(relx=0.7, rely=0.05, anchor=CENTER)
                    Label(table_frame, text=ans[0][1], font=normal_font, bg="grey", fg=main_colors["fg"], width=70,
                          anchor="w").place(relx=0.7, rely=0.15, anchor=CENTER)

                    en3 = Entry(table_frame, font=normal_font, width=70)
                    en3.place(relx=0.7, rely=0.25, anchor=CENTER)
                    en3.insert(0, ans[0][2])

                    en4 = Entry(table_frame, font=normal_font, width=70)
                    en4.place(relx=0.7, rely=0.35, anchor=CENTER)
                    en4.insert(0, ans[0][3])

                    en5 = Entry(table_frame, font=normal_font, width=70)
                    en5.place(relx=0.7, rely=0.45, anchor=CENTER)
                    en5.insert(0, ans[0][4])

                    en6 = Entry(table_frame, font=normal_font, width=70)
                    en6.place(relx=0.7, rely=0.55, anchor=CENTER)
                    en6.insert(0, ans[0][5])

                    en7 = Entry(table_frame, font=normal_font, width=70)
                    en7.place(relx=0.7, rely=0.65, anchor=CENTER)
                    en7.insert(0, ans[0][6])

                    en8 = Entry(table_frame, font=normal_font, width=70)
                    en8.place(relx=0.7, rely=0.75, anchor=CENTER)
                    en8.insert(0, ans[0][7])

                    en9 = Entry(table_frame, font=normal_font, width=70)
                    en9.place(relx=0.7, rely=0.85, anchor=CENTER)
                    en9.insert(0, ans[0][8])

                    en10 = Entry(table_frame, font=normal_font, width=70)
                    en10.place(relx=0.7, rely=0.95, anchor=CENTER)
                    en10.insert(0, ans[0][9])

                    conn.commit()
                    conn.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

                def upd_book_query():
                    mid = e1.get()
                    c3 = en3.get()
                    c4 = en4.get()
                    c5 = en5.get()
                    c6 = en6.get()
                    c7 = en7.get()
                    c8 = en8.get()
                    c9 = en9.get()
                    c10 = en10.get()
                    upd_tuple = [c3, c4, c5, c6, c7, c8, c9, c10]

                    try:
                        conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                                       database=db_config["db_name"])
                        cur = conn.cursor()
                        cur.execute(
                            f"""Update members SET contact_no = %s, address = %s, email = %s, academic_year = %s, division = %s, batch = %s, roll_no = %s, course = %s WHERE member_id = '{mid}' """,
                            upd_tuple)
                        conn.commit()

                        # "member_id", "name", "contact_no", "address", "email", "academic_year", "division", "batch", "roll_no", "course"
                        # record the transaction
                        curtime = datetime.datetime.now()
                        curdate = date.today()
                        tr_id = update_id(0)
                        trans_stmt = f"Details of member with {mid} were updated"
                        tran = (tr_id, curdate, curtime, trans_stmt)
                        cur.execute('INSERT into transaction values(%s, %s, %s, %s)', tran)
                        pop("Member Details updated successfully")
                        conn.commit()
                        conn.close()
                    except (mysql.connector.errors.ProgrammingError):
                        print("wrong database pass, please change it in the setting")

                Button(disp_frame, text="Set", command=upd_book_query, background=btn_colors["bg"],
                       foreground=btn_colors["fg"], font=normal_font).place(rely=0.9, relx=0.9)
            else:
                pop(f"This book with id '{condition}' does not exists")

        Button(disp_frame, text="Search", command=search, font=bold_font, bg=btn_colors["bg"],
               fg=main_colors["fg"]).place(relx=0.7, rely=0.1, anchor=CENTER)

    # single and multiple
    # single
    def update_single_book():
        clear_frame(disp_frame)
        book_attr = ["Book Topic", "Author Name", "Description", "Edition", "Price", "Book Title", "Availablity",
                     "Book Id"]

        Label(disp_frame, text="Enter id of book to be updated: ", font=bold_font, fg=main_colors["fg"],
              bg=main_colors["bg"]).place(relx=0.2, rely=0.1, anchor=CENTER)
        e1 = Entry(disp_frame, font=bold_font)
        e1.place(relx=0.4, rely=0.1, anchor=CENTER)

        def search():
            condition = e1.get()
            table_frame = Frame(disp_frame, bg="black", width=800, height=400, background=main_colors["bg"])
            table_frame.place(relx=0.1, rely=0.25)
            table_frame.pack_propagate(False)

            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                cur.execute(f"select * from book_list where book_id = '{condition}'")
                ans = cur.fetchall()
                print(ans)
                # print(ans[0][10])
                if len(ans) > 0:
                    Label(table_frame, text=book_attr[0], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.15, anchor=CENTER)
                    Label(table_frame, text=book_attr[1], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.25, anchor=CENTER)
                    Label(table_frame, text=book_attr[2], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.35, anchor=CENTER)
                    Label(table_frame, text=book_attr[3], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.45, anchor=CENTER)
                    Label(table_frame, text=book_attr[4], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.55, anchor=CENTER)
                    Label(table_frame, text=book_attr[5], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.65, anchor=CENTER)
                    Label(table_frame, text=book_attr[6], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.75, anchor=CENTER)
                    Label(table_frame, text=book_attr[7], font=bold_font, background=main_colors["bg"],
                          foreground=main_colors["fg"]) \
                        .place(relx=0.1, rely=0.85, anchor=CENTER)

                    Label(table_frame, text=ans[0][0], font=normal_font, bg="grey", fg=main_colors["fg"], width=70,
                          anchor="w").place(relx=0.7, rely=0.15, anchor=CENTER)
                    Label(table_frame, text=ans[0][1], font=normal_font, bg="grey", fg=main_colors["fg"], width=70,
                          anchor="w").place(relx=0.7, rely=0.25, anchor=CENTER)

                    en4 = Entry(table_frame, font=normal_font, width=70)
                    en4.place(relx=0.7, rely=0.35, anchor=CENTER)
                    en4.insert(0, ans[0][2])

                    en5 = Entry(table_frame, font=normal_font, width=70)
                    en5.place(relx=0.7, rely=0.45, anchor=CENTER)
                    en5.insert(0, ans[0][3])

                    en6 = Entry(table_frame, font=normal_font, width=70)
                    en6.place(relx=0.7, rely=0.55, anchor=CENTER)
                    en6.insert(0, ans[0][4])
                    Label(table_frame, text=ans[0][5], font=normal_font, bg="grey", fg=main_colors["fg"], width=70,
                          anchor="w").place(relx=0.7, rely=0.65, anchor=CENTER)
                    Label(table_frame, text=ans[0][6], font=normal_font, bg="grey", fg=main_colors["fg"], width=70,
                          anchor="w").place(relx=0.7, rely=0.75, anchor=CENTER)
                    Label(table_frame, text=ans[0][7], font=normal_font, bg="grey", fg=main_colors["fg"], width=70,
                          anchor="w").place(relx=0.7, rely=0.85, anchor=CENTER)
                    conn.commit()
                    conn.close()

            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

                def upd_book_query():
                    bid = e1.get()
                    c4 = en4.get()
                    c5 = en5.get()
                    c6 = en6.get()
                    upd_tuple = [c4, c5, c6]

                    try:
                        conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                                       database=db_config["db_name"])
                        cur = conn.cursor()
                        cur.execute(
                            f"""Update book_list SET description = %s, edition = %s, price = %s WHERE book_id = '{ans[0][7]}' """,
                            upd_tuple)

                        # record the transaction
                        curtime = datetime.datetime.now()
                        curdate = date.today()
                        tr_id = update_id(0)
                        trans_stmt = f"Details of book with {bid} were updated"
                        tran = (tr_id, curdate, curtime, trans_stmt)
                        cur.execute('INSERT into transaction values(%s, %s, %s, %s)', tran)
                        pop("Book Details updated successfully")
                        conn.commit()
                        conn.close()
                    except (mysql.connector.errors.ProgrammingError):
                        print("wrong database pass, please change it in the setting")

                Button(disp_frame, text="Set", command=upd_book_query, background=btn_colors["bg"],
                       foreground=btn_colors["fg"], font=normal_font).place(rely=0.9, relx=0.9)
            else:
                pop(f"This book with id '{condition}' does not exists")

        Button(disp_frame, text="Search", command=search, font=bold_font, bg=btn_colors["bg"],
               fg=main_colors["fg"]).place(relx=0.7, rely=0.1, anchor=CENTER)

    # search functions
    def search_mem_vin():
        clear_frame(status)
        clear_frame(disp_frame)

        tr_frame = Frame(disp_frame, bg=main_colors["bg"])
        tr_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(disp_frame, text="Search Member", font=bold_font, background=main_colors["bg"],
              foreground=main_colors["fg"]).place(rely=0.1, relx=0.07)
        e1 = Entry(disp_frame, font=bold_font)
        e1.place(rely=0.1, relx=0.2)

        def set_var(val):
            global search_attr
            search_attr = val
            CmdBtn.configure(text=val)

        CmdBtn = Menubutton(disp_frame, text='Search by', fg=btn_colors["fg"], bg=btn_colors["bg"], font=bold_font)
        CmdBtn.place(rely=0.1, relx=0.4)
        CmdBtn.menu = Menu(CmdBtn)
        CmdBtn.menu.add_command(label='Id', underline=0, command=lambda: set_var("member_id"))
        CmdBtn.menu.add_command(label='Name', underline=0, command=lambda: set_var("name"))
        CmdBtn.menu.add_command(label='Academic Year', underline=0, command=lambda: set_var("academic_year"))
        CmdBtn.menu.add_command(label='Division', underline=0, command=lambda: set_var("division"))
        CmdBtn.menu.add_command(label='Course', underline=0, command=lambda: set_var("course"))
        CmdBtn['menu'] = CmdBtn.menu

        def disp_search_mem():
            clear_frame(tr_frame)
            columns = ['id', 'name', 'phone no', 'address', 'mail', 'academic year', 'division', 'batch', 'roll no',
                       'course']
            col_text = ["Member ID", "Name", "Contact no.", "Address", "Email", "Academic Year", "Division", "Batch",
                        "Roll No.", "Course"]

            tree = ttk.Treeview(tr_frame, columns=columns, show='headings')
            xscrollbar = ttk.Scrollbar(tr_frame, orient=HORIZONTAL, command=tree.xview)
            tree.configure(xscroll=xscrollbar.set)
            xscrollbar.pack(side=TOP, fill=X)
            yscrollbar = ttk.Scrollbar(tr_frame, orient=VERTICAL, command=tree.yview)
            tree.configure(yscroll=yscrollbar.set)
            yscrollbar.pack(side=RIGHT, fill=Y)

            for c in range(0, len(columns)):
                tree.heading(columns[c], text=col_text[c])
                tree.column(columns[c], minwidth=0, width=100)

            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                search_key = e1.get()

                cur.execute(f"select * from members where {search_attr} LIKE '%{search_key}%'")
                res = cur.fetchall()
                for rec in res:
                    tree.insert('', END, values=rec)
                tree.pack()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Button(disp_frame, text="Search", background=btn_colors["bg"],
               foreground=btn_colors["fg"], font=bold_font, command=disp_search_mem).place(rely=0.2, relx=0.4)

    b2 = Button(menu, text="Search Member", font=bold_font, bg=btn_colors["bg"], command=search_mem_vin,
                fg=main_colors["fg"], pady=0, relief=RAISED, width=13)
    b2.place(rely=0.2, relx=0.7, anchor=CENTER)

    def search_book_vin():
        clear_frame(status)
        clear_frame(disp_frame)

        tr_frame = Frame(disp_frame, bg=main_colors["bg"])
        tr_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(disp_frame, text="Search Book", font=bold_font, background=main_colors["bg"],
              foreground=main_colors["fg"]).place(rely=0.1, relx=0.07)
        e1 = Entry(disp_frame, font=bold_font)
        e1.place(rely=0.1, relx=0.2)

        def set_var(val):
            global search_attr
            search_attr = val
            CmdBtn.configure(text=val)

        CmdBtn = Menubutton(disp_frame, text='Search by', fg=btn_colors["fg"], bg=btn_colors["bg"], font=bold_font)
        CmdBtn.place(rely=0.1, relx=0.4)
        CmdBtn.menu = Menu(CmdBtn)
        CmdBtn.menu.add_command(label='Book Topic', underline=0, command=lambda: set_var("book_topic"))
        CmdBtn.menu.add_command(label='Author Name', underline=0, command=lambda: set_var("author_name"))
        CmdBtn.menu.add_command(label='Publisher', underline=0, command=lambda: set_var("publisher"))
        CmdBtn.menu.add_command(label='Category', underline=0, command=lambda: set_var("category"))
        CmdBtn.menu.add_command(label='Book Title', underline=0, command=lambda: set_var("book_title"))
        CmdBtn.menu.add_command(label='Book Id', underline=0, command=lambda: set_var("book_id"))
        CmdBtn['menu'] = CmdBtn.menu

        def disp_search_book():
            try:
                conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                               database=db_config["db_name"])
                cur = conn.cursor()
                search_key = e1.get()

                if search_attr == "book_id":
                    clear_frame(tr_frame)
                    columns = ["book topic", "author name", "description", "edition", "price", "availability", "title",
                               "book id"]
                    col_text = ["Book Topic", "Author Name", "Description", "Edition", "Price", "Availability", "Title",
                                "Book Id"]
                    cur.execute(f"select * from book_list where {search_attr} = '%{search_key}%'")
                    res = cur.fetchall()
                    tree = ttk.Treeview(tr_frame, columns=columns, show='headings')
                    xscrollbar = ttk.Scrollbar(tr_frame, orient=HORIZONTAL, command=tree.xview)
                    tree.configure(xscroll=xscrollbar.set)
                    xscrollbar.pack(side=TOP, fill=X)
                    yscrollbar = ttk.Scrollbar(tr_frame, orient=VERTICAL, command=tree.yview)
                    tree.configure(yscroll=yscrollbar.set)
                    yscrollbar.pack(side=RIGHT, fill=Y)

                    for c in range(0, len(columns)):
                        tree.heading(columns[c], text=col_text[c])
                        tree.column(columns[c], minwidth=0, width=100)
                    for rec in res:
                        tree.insert('', END, values=rec)
                    tree.pack()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")


            else:
                clear_frame(tr_frame)
                columns = ["book topic", "author name", "available quantity", "total quantity", "publisher", "category",
                           "title"]
                col_text = ["Book Topic", "Author Name", "Available Quantity", "Total Quantity", "Publisher",
                            "Category", "Title"]
                cur.execute(f"select * from book where {search_attr} LIKE '%{search_key}%'")
                res = cur.fetchall()
                tree = ttk.Treeview(tr_frame, columns=columns, show='headings')
                xscrollbar = ttk.Scrollbar(tr_frame, orient=HORIZONTAL, command=tree.xview)
                tree.configure(xscroll=xscrollbar.set)
                xscrollbar.pack(side=TOP, fill=X)
                yscrollbar = ttk.Scrollbar(tr_frame, orient=VERTICAL, command=tree.yview)
                tree.configure(yscroll=yscrollbar.set)
                yscrollbar.pack(side=RIGHT, fill=Y)

                for c in range(0, len(columns)):
                    tree.heading(columns[c], text=col_text[c])
                    tree.column(columns[c], minwidth=0, width=100)
                for rec in res:
                    tree.insert('', END, values=rec)
                tree.pack()

        Button(disp_frame, text="Search", background=btn_colors["bg"],
               foreground=btn_colors["fg"], font=bold_font, command=disp_search_book).place(rely=0.2, relx=0.4)

    b3 = Button(menu, text="Search Book", font=bold_font, bg=btn_colors["bg"], command=search_book_vin,
                fg=main_colors["fg"], pady=0, relief=RAISED, width=13)
    b3.place(rely=0.7, relx=0.7, anchor=CENTER)

    # import function (excel file)
    def multiple_import():
        clear_frame(status)
        clear_frame(disp_frame)

        def import_exc():
            try:
                con = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                              database=db_config["db_name"])
                cur = con.cursor()
                # path to the file    # pth = 'C:/Users/Admin/Downloads/Book_list.xlsx'
                pth = e1.get()
                # read from this file
                data = pd.read_excel(pth)
                # no of records in excel file
                total = len(data["book_id"])
                already_exists_list = []
                try:
                    # iterate through all records in excel file
                    for i in range(0, total):
                        # search in book table for a book with this book_title
                        cur.execute(
                            f"select total_quantity, available_quantity, book_topic, book_title from book where book_title = '{data['book_title'][i]}'")
                        ans = cur.fetchall()

                        # search in book_list table for a book with this book_id
                        cur.execute(f"select book_title from book_list where book_id = '{data['book_id'][i]}'")
                        ans1 = cur.fetchall()

                        # books of this title are already available then update
                        if len(ans) > 0:
                            # no book of this id exists (update)
                            if len(ans1) == 0:
                                # increase total and available quantity of book with this title by 1
                                cur.execute(
                                    f"UPDATE book SET available_quantity = '{ans[0][1] + 1}', total_quantity = '{ans[0][0] + 1}' where book_title = '{data['book_title'][i]}'")
                                con.commit()

                                # insert into book list one record
                                book_list_insert = (
                                ans[0][2], data['author name'][i], "", "", int(data['price'][i]), ans[0][3], "yes",
                                str(data['book_id'][i]))
                                cur.execute("INSERT INTO book_list VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                            book_list_insert)
                            # book of this id already exists (popup)
                            else:
                                # insert already existing book_id into this list
                                already_exists_list.append(data['book_id'][i])
                        # book of this title does not exist then insert
                        else:
                            # no book of this id exists (insert)
                            if len(ans1) == 0:
                                # increase total and available quantity of book with this title by 1
                                book_insert = ("", data['author name'][i], 1, 1, data['publisher'][i], data['category'][i],
                                               data['book_title'][i])
                                cur.execute("INSERT INTO book VALUES(%s, %s, %s, %s, %s, %s, %s)", book_insert)

                                # insert a record in book_list table
                                book_list_insert = (
                                "", data['author name'][i], "", "", int(data['price'][i]), data['book_title'][i], "yes",
                                str(data['book_id'][i]))
                                cur.execute("INSERT INTO book_list VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                            book_list_insert)
                                con.commit()

                            # book of this id already exists (popup)
                            else:
                                # insert already existing book_id into this list
                                already_exists_list.append(data['book_id'][i])

                    curtime = datetime.datetime.now()
                    curdate = date.today()
                    tr_id = update_id(0)
                    trans_stmt = f"Books were imported from excel file"
                    tran = (tr_id, curdate, curtime, trans_stmt)
                    cur.execute('INSERT into transaction values(%s, %s, %s, %s)', tran)
                    # improved transaction statement

                    # popup that books with these ids already exist
                    if len(already_exists_list) > 0:
                        str_alr_exis = ""
                        for book in already_exists_list:
                            str_alr_exis = str_alr_exis + f" {book}"
                        pop(f"Books with id {str_alr_exis} were not inserted because these books already exists")
                except ValueError:
                    # popup
                    pop("There was some error importing the records from the file")
                con.commit()
                con.close()
            except (mysql.connector.errors.ProgrammingError):
                print("wrong database pass, please change it in the setting")

        Label(disp_frame, text="Enter the path of the Excel file: ", fg=main_colors["fg"], bg=main_colors["bg"],
              font=normal_font).place(relx=0.12, rely=0.3, anchor=CENTER)
        e1 = Entry(disp_frame, fg=main_colors["bg"], bg=main_colors["fg"], font=normal_font, width=40)
        e1.place(relx=0.42, rely=0.3, anchor=CENTER)

        Button(disp_frame, text="Import", command=import_exc, fg=btn_colors["fg"], bg=btn_colors["bg"],
               font=normal_font).place(relx=0.4, rely=0.5, anchor=CENTER)

    # Export functions for generating pdf reports
    def exp_mem():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                           host='127.0.0.1', database=db_config["db_name"])
            cur = conn.cursor()
            cur.execute("select * from members")
            result = cur.fetchall()
            conn.close()

            pdf = FPDF("L")
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            # 276.9975833333333
            pdf.set_font('Times', 'B', 14)
            pdf.cell(page_width, 0.0, 'Member Data', align='C')
            pdf.ln(10)
            pdf.set_font('Times', '', 10)

            pdf.ln(1)
            th = pdf.font_size
            pdf.cell(16, th, "Member ID", border=1)
            pdf.cell(55, th, "Name", border=1)
            pdf.cell(25, th, "Contact No.", border=1)
            pdf.cell(75, th, "Address", border=1)
            pdf.cell(55, th, "Email Address", border=1)
            pdf.cell(16, th, "Acad. Year", border=1)
            pdf.cell(8, th, "Div.", border=1)
            pdf.cell(8, th, "Batch", border=1)
            pdf.cell(8, th, "RollNo.", border=1)
            pdf.cell(10, th, "Course", border=1)
            pdf.ln(th)

            for row in range(0, len(result)):
                pdf.cell(16, th, str(result[row][0]), border=1)
                pdf.cell(55, th, result[row][1], border=1)
                pdf.cell(25, th, result[row][2], border=1)
                pdf.cell(75, th, result[row][3], border=1)
                pdf.cell(55, th, result[row][4], border=1)
                pdf.cell(16, th, result[row][5], border=1)
                pdf.cell(8, th, result[row][6], border=1)
                pdf.cell(8, th, result[row][7], border=1)
                pdf.cell(8, th, str(result[row][8]), border=1)
                pdf.cell(10, th, result[row][9], border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.output("member.pdf")

        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")


    def exp_book():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                           database=db_config["db_name"])
            cur = conn.cursor()
            cur.execute("select * from book")
            result = cur.fetchall()
            conn.close()

            pdf = FPDF("L")
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            # 276.9975833333333
            pdf.set_font('Times', 'B', 14)
            pdf.cell(page_width, 0.0, 'Types of Book', align='C')
            pdf.ln(10)
            pdf.set_font('Times', '', 10)
            pdf.ln(1)

            th = pdf.font_size
            pdf.cell(25, th, "Book Topic", border=1)
            pdf.cell(35, th, "Author Name", border=1)
            pdf.cell(15, th, "Available Quantity", border=1)
            pdf.cell(15, th, "Total Quantity", border=1)
            pdf.cell(25, th, "Publisher", border=1)
            pdf.cell(35, th, "Category", border=1)
            pdf.cell(75, th, "Book_title", border=1)
            pdf.ln(th)

            for row in range(0, len(result)):
                pdf.cell(25, th, result[row][0], border=1)
                pdf.cell(35, th, result[row][1], border=1)
                pdf.cell(15, th, str(result[row][2]), border=1)
                pdf.cell(15, th, str(result[row][3]), border=1)
                pdf.cell(25, th, result[row][4], border=1)
                pdf.cell(35, th, result[row][5], border=1)
                pdf.cell(75, th, result[row][6], border=1)
                pdf.ln(th)
            pdf.ln(10)

            pdf.output("books.pdf")

        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")

    def exp_book_list():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                           host='127.0.0.1', database=db_config["db_name"])
            cur = conn.cursor()
            cur.execute("select * from book_list")
            result = cur.fetchall()
            conn.close()

            pdf = FPDF("L")
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            # 276.9975833333333
            pdf.set_font('Times', 'B', 14)
            pdf.cell(page_width, 0.0, 'All Book List', align='C')
            pdf.ln(10)
            pdf.set_font('Times', '', 10)

            pdf.ln(1)
            th = pdf.font_size
            pdf.cell(25, th, "Book Topic", border=1)
            pdf.cell(35, th, "Author Name", border=1)
            pdf.cell(40, th, "Description", border=1)
            pdf.cell(12, th, "Edition", border=1)
            pdf.cell(9, th, "Price", border=1)
            pdf.cell(75, th, "Book_title", border=1)
            pdf.cell(8, th, "Availability", border=1)
            pdf.cell(20, th, "Book ID", border=1)
            pdf.ln(th)

            for row in range(0, len(result)):
                pdf.cell(25, th, result[row][0], border=1)
                pdf.cell(35, th, result[row][1], border=1)
                pdf.cell(40, th, result[row][2], border=1)
                pdf.cell(12, th, result[row][3], border=1)
                pdf.cell(9, th, str(result[row][4]), border=1)
                pdf.cell(75, th, result[row][5], border=1)
                pdf.cell(8, th, result[row][6], border=1)
                pdf.cell(20, th, result[row][7], border=1)
                pdf.ln(th)
            pdf.ln(10)
            pdf.output("books_list.pdf")

        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")

    def exp_issued():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"], host='127.0.0.1',
                                           database=db_config["db_name"])
            cur = conn.cursor()
            cur.execute("select * from issued")

            result = cur.fetchall()
            conn.close()

            pdf = FPDF("L")
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            # 276.9975833333333
            pdf.set_font('Times', 'B', 14)
            pdf.cell(page_width, 0.0, 'Issued Books', align='C')
            pdf.ln(10)
            pdf.set_font('Times', '', 10)

            pdf.ln(1)
            th = pdf.font_size
            pdf.cell(16, th, "Member ID", border=1)
            pdf.cell(16, th, "Book ID", border=1)
            pdf.cell(55, th, "Book Title", border=1)
            pdf.cell(65, th, "Name", border=1)
            pdf.cell(65, th, "Email Address", border=1)
            pdf.cell(18, th, "Acad. Year", border=1)
            pdf.cell(12, th, "Course", border=1)
            pdf.cell(16, th, "Issue Date", border=1)
            pdf.cell(16, th, "Issue Time", border=1)
            pdf.ln(th)

            for row in range(0, len(result)):
                pdf.cell(16, th, str(result[row][0]), border=1)
                pdf.cell(16, th, str(result[row][1]), border=1)
                pdf.cell(55, th, result[row][2], border=1)
                pdf.cell(65, th, result[row][3], border=1)
                pdf.cell(65, th, result[row][4], border=1)
                pdf.cell(18, th, result[row][5], border=1)
                pdf.cell(12, th, result[row][6], border=1)
                pdf.cell(16, th, str(result[row][7]), border=1)
                pdf.cell(16, th, str(result[row][8]), border=1)
                pdf.ln(th)

            pdf.ln(10)
            pdf.output("issued.pdf")

        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")

    def exp_def():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                           host='127.0.0.1', database=db_config["db_name"])
            cur = conn.cursor()
            cur.execute("select * from defaulter")
            result = cur.fetchall()
            conn.close()

            pdf = FPDF("L")
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            # 276.9975833333333
            pdf.set_font('Times', 'B', 14)
            pdf.cell(page_width, 0.0, 'Defaulter List', align='C')
            pdf.ln(10)
            pdf.set_font('Times', '', 10)

            pdf.ln(1)
            th = pdf.font_size
            pdf.cell(16, th, "Member ID", border=1)
            pdf.cell(16, th, "Book ID (IND)", border=1)
            pdf.cell(55, th, "Book Title", border=1)
            pdf.cell(65, th, "Name", border=1)
            pdf.cell(65, th, "Email Address", border=1)
            pdf.cell(18, th, "Acad. Year", border=1)
            pdf.cell(12, th, "Course", border=1)
            pdf.cell(16, th, "Issue Date", border=1)
            pdf.cell(16, th, "Issue Time", border=1)
            pdf.ln(th)

            for row in range(0, len(result)):
                pdf.cell(16, th, str(result[row][0]), border=1)
                pdf.cell(16, th, str(result[row][1]), border=1)
                pdf.cell(55, th, result[row][2], border=1)
                pdf.cell(65, th, result[row][3], border=1)
                pdf.cell(65, th, result[row][4], border=1)
                pdf.cell(18, th, result[row][5], border=1)
                pdf.cell(12, th, result[row][6], border=1)
                pdf.cell(16, th, str(result[row][7]), border=1)
                pdf.cell(16, th, str(result[row][8]), border=1)
                pdf.ln(th)
            pdf.ln(10)
            pdf.output("defaulter.pdf")

        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")

    def exp_trans():
        try:
            conn = mysql.connector.connect(user='root', password=db_config["db_password"],
                                           host='127.0.0.1', database=db_config["db_name"])
            cur = conn.cursor()
            cur.execute("select * from transaction order by trans_date")

            result = cur.fetchall()
            conn.close()

            pdf = FPDF("L")
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            # 276.9975833333333
            pdf.set_font('Times', 'B', 14)
            pdf.cell(page_width, 0.0, 'Transaction Log', align='C')
            pdf.ln(10)
            pdf.set_font('Times', '', 10)

            pdf.ln(1)
            th = pdf.font_size
            pdf.cell(25, th, "Transaction ID", border=1)
            pdf.cell(25, th, "Transaction Date", border=1)
            pdf.cell(25, th, "Transaction Time", border=1)
            pdf.cell(200, th, "Operation", border=1)
            pdf.ln(th)

            for row in range(0, len(result)):
                pdf.cell(25, th, str(result[row][0]), border=1)
                pdf.cell(25, th, str(result[row][1]), border=1)
                pdf.cell(25, th, str(result[row][2]), border=1)
                pdf.cell(200, th, result[row][3], border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.output("trans_log.pdf")
        except (mysql.connector.errors.ProgrammingError):
            print("wrong database pass, please change it in the setting")

    def exp_vin():
        clear_frame(status)
        clear_frame(disp_frame)
        Button(disp_frame, text="Member", command=exp_mem, font=bold_font, background=btn_colors["bg"],
               foreground=btn_colors["fg"], width=20).place(relx=0.2, rely=0.08, anchor=CENTER)
        Button(disp_frame, text="Books Quantity list", command=exp_book, font=bold_font, background=btn_colors["bg"],
               foreground=btn_colors["fg"], width=20).place(relx=0.2, rely=0.16, anchor=CENTER)
        Button(disp_frame, text="All Books List", command=exp_book_list, font=bold_font, background=btn_colors["bg"],
               foreground=btn_colors["fg"], width=20).place(relx=0.2, rely=0.24, anchor=CENTER)
        Button(disp_frame, text="Currently Issued Books", command=exp_issued, font=bold_font,
               background=btn_colors["bg"], foreground=btn_colors["fg"], width=20).place(relx=0.2, rely=0.32,
                                                                                         anchor=CENTER)
        Button(disp_frame, text="Defaulter list", command=exp_def, font=bold_font, background=btn_colors["bg"],
               foreground=btn_colors["fg"], width=20).place(relx=0.2, rely=0.4, anchor=CENTER)
        Button(disp_frame, text="Transaction list", command=exp_trans, font=bold_font, background=btn_colors["bg"],
               foreground=btn_colors["fg"], width=20).place(relx=0.2, rely=0.48, anchor=CENTER)

    # labels for buttons
    button_list = ["Add books", "Remove books", "Add members", "Remove member", "Issue Book", "Retrieve Book",
                   "Defaulter List", "Member List", "Books List", "Transaction Log", "Update Member", "Update Book",
                   "Export", "Import"]

    # commands for buttons
    command_list = [add_book_vin, rem_book_vin, add_mem_vin, rem_mem_vin, issue_book_vin,
                    retrieve_book_vin, disp_defaulter, disp_members, disp_book, disp_trans, update_sin_mem,
                    update_single_book, exp_vin, multiple_import]

    # loop which packs above listed buttons
    for i in range(0, len(button_list)):
        Button(f1, text=button_list[i], width=20, font=('calibri', '15', 'bold'),
               fg=mbtn_colors["fg"], bg=mbtn_colors["bg"], relief=RAISED, borderwidth=2, command=command_list[i],
               pady=6) \
            .pack(side=TOP)
    root.mainloop()


# login window
def login_page():
    # sends password to the registered email id on request
    def notify():
        f = open("pass.txt", "r+")
        pv = f.readline()
        f.close()

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(mail_id_name, mail_id_pass)
            message = f"Your LMS passvord is {pv}"
            s.sendmail(mail_id_name, mail_id_name, message)
            s.quit()
        except smtplib.SMTPAuthenticationError:
            print("wrong email details, please change to correct details in setting menu")

    # to check if the entered password is correct
    def check(eee):
        clear_frame(f2)
        ff = open("pass.txt", "r")
        pv = ff.readline()
        pvv = ff.read()
        print(pvv)
        ent = eee.get()
        ff.close()

        if ent == pv:
            root.destroy()
            app_start()
        else:
            Label(f2, text="Incorrect Password!, Please Try again.", bg="#333111", fg="red",
                  font=["calibri", 12, "bold"]).pack()

    # actual login window
    def login():
        Label(f1, text="Smt. CHM College", bg=main_colors["bg"], fg=main_colors["fg"], font=bold_font) \
            .place(relx=0.5, rely=0.05, anchor=CENTER)
        Label(f1, text="Password: ", bg=main_colors["bg"], fg=main_colors["fg"], font=["calibri", 12, "bold"]) \
            .place(relx=0.3, rely=0.6, anchor=CENTER)
        e2 = Entry(f1, show='*', font=["calibri", 12, "bold"])
        e2.place(relx=0.6, rely=0.6, anchor=CENTER)
        e2.focus()

        b1 = Button(f1, text="Login", bg=btn_colors["bg"], fg=main_colors["fg"], font=["calibri", 12, "bold"],
                    command=lambda: check(e2))
        b2 = Button(f1, text="Forgot", bg="red", fg=main_colors["fg"], font=["calibri", 12, "bold"], command=forgot)
        b1.place(relx=0.5, rely=0.8, anchor=CENTER)
        b2.place(relx=0.8, rely=0.8, anchor=CENTER)

    # called when user clicks on forgot password button
    def forgot():
        notify()
        Label(f1, text="Password has been sent to the registered email", bg=main_colors["bg"], fg=main_colors["fg"]) \
            .place(relx=0.5, rely=0.9, anchor=CENTER)

    # main window definition for login window
    root = Tk()
    root.title('C.H.M Library')

    root.geometry("540x400+200+200")
    root.configure(bg=main_colors["bg"])
    root.resizable(False, False)
    f1 = Frame(root, height=400, width=400, bg=main_colors["bg"])
    f1.place(relx=0.5, rely=0.5, anchor=CENTER)
    f1.pack_propagate(False)

    f2 = Frame(f1)
    f2.place(relx=0.5, rely=0.9, anchor=CENTER)

    login()
    root.mainloop()


# main function call
login_page()




