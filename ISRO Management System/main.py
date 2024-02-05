import pandas as pd
import customtkinter as ctk
import mysql.connector as msc
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from tkvideo import tkvideo
from demo import emp, miss

cou = 0
def startup():
    global cou
    try:
        global host,use,passss
        a = pd.read_csv("C:\\ProgramData\\ISRO_log.csv")
        host = a.iloc[0, 1]
        use = a.iloc[1, 1]
        passss = a.iloc[2, 1]
        connection = msc.connect(host=host, user=use, password=passss)
        cursor = connection.cursor()
        print("_________________________________________MySQL connected successfully_________________________________________")
    except:
        if cou == 0:
            print("_________________________________________Enter login credentials_________________________________________")
        else:
            print("_________________________________________Invalid login credentials_________________________________________")
        host = input("Enter host: ")
        use = input("Enter user: ")
        passss = input("Enter password: ")
        log = pd.DataFrame(data=[host, use, passss])
        log.to_csv("C:\\ProgramData\\ISRO_log.csv")
        cou += 1
        startup()

def connection():
    global con
    global cur
    con = msc.connect(host=host, user=use, password=passss, database="ISRO")
    cur = con.cursor()
    return con, cur

def database():
    connection = msc.connect(host=host, user=use, password=passss)
    cursor = connection.cursor()
    create_database = f"CREATE DATABASE if not exists ISRO;"
    cursor.execute(create_database)
    connection.close()

def users_table():
    connection()
    create_table = f"CREATE TABLE if not exists users(name varchar(30), username varchar(20) unique,gender char(1), password varchar(8),email varchar(100), city varchar(30),dob date, role varchar(30));"
    cur.execute(create_table)
    con.close()
    try:
        add_emp()
    except:
        pass

def add_emp():
    connection()
    sql = "INSERT INTO users (name,username,gender,password,email,city,dob,role) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
    data = emp
    for x in data:
        cur.execute(sql, (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
    con.commit()
    con.close()

def mission():
    connection()
    create_table = f"CREATE TABLE if not exists mission(name varchar(50) primary key, launch_vehicle varchar(50),orbit_type varchar(50), application varchar(50),launch_date date);"
    cur.execute(create_table)
    con.close()
    try:
        add_miss()
    except:
        pass

def add_miss():
    connection()
    sql = "INSERT INTO mission (name,launch_vehicle,orbit_type,application,launch_date) VALUES(%s,%s,%s,%s,%s);"
    data = miss
    for x in data:
        cur.execute(sql, (x[0], x[1], x[2], x[3], x[4]))
    con.commit()
    con.close()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ISRO Management System-login_win")
        self.resizable(width=False, height=False)
        self.iconbitmap("py.ico")

        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        width = s_width * 0.2
        height = s_height * 0.35
        width_position = ((s_width / 2) - width / 2)
        height_position = ((s_height / 2) - height / 2)

        self.geometry("%dx%d+%d+%d" % (width, height, width_position, height_position))

        self.heading = ctk.CTkLabel(self, text="LOGIN", font=("Helvetica", 26, "bold"))
        self.heading.place(relx=0.37, rely=0.08)

        self.uname = ctk.CTkLabel(self, text="Username:", font=("Helvetica", 14, "bold"))
        self.uname.place(relx=0.1, rely=0.25)

        self.username = ctk.CTkEntry(self, placeholder_text="Username", font=("Helvetica", 12, "italic"),corner_radius=25, width=250)
        self.username.place(relx=0.1, rely=0.34)

        self.pwd = ctk.CTkLabel(self, text="Password:", font=("Helvetica", 14, "bold"))
        self.pwd.place(relx=0.1, rely=0.48)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", font=("Helvetica", 12, "italic"),corner_radius=25, show="*", width=250)
        self.password.place(relx=0.1, rely=0.57)

        self.signin = ctk.CTkButton(self, text="Signin", command=self.signin, corner_radius=25,hover_color="dark green", fg_color="green", width=100)
        self.signin.place(relx=0.14, rely=0.8)

        self.signup = ctk.CTkButton(self, text="Signup", command=self.signup, corner_radius=25,hover_color="dark green", fg_color="green", width=100)
        self.signup.place(relx=0.54, rely=0.8)

    def signin(self):
        global user, pas
        user = self.username.get()
        pas = self.password.get()
        def fetch_login():
            global user_id
            connection()
            query = f"select username,password from users where username = '{user}' and password = '{pas}';"
            cur.execute(query)
            x = cur.fetchall()
            user_id = x
            if user_id == [(user, pas)]:
                self.destroy()
                home().mainloop()
            else:
                self.error()
            con.close()
        fetch_login()

    def signup(self):
        self.destroy()
        add_user().mainloop()

    def error(self):
        messagebox.showerror("Error", "Invalid Credentials")

class add_user(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ISRO Management System-new_user")
        self.resizable(width=False, height=False)
        self.iconbitmap("py.ico")

        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        width = s_width * 0.25
        height = s_height * 0.5
        width_position = ((s_width / 2) - width / 2)
        height_position = ((s_height / 2) - height / 2)
        self.geometry("%dx%d+%d+%d" % (width, height, width_position, height_position))

        self.heading = ctk.CTkLabel(self, text="Create your account", font=("Helvetica", 26, "bold"))
        self.heading.place(relx=0.15, rely=0.1)

        frame = ctk.CTkScrollableFrame(self, width=300, height=200, corner_radius=25, bg_color="transparent",orientation="vertical")
        frame.place(relx=0.05, rely=0.2)

        self.NAME = ctk.CTkLabel(frame, text="Name:", font=("Helvetica", 14, "bold"))
        self.NAME.pack(pady=0, anchor=ctk.W)

        self.name = ctk.CTkEntry(frame, placeholder_text="Name", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, width=300)
        self.name.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="Username:", font=("Helvetica", 14, "bold"))
        self.uname.pack(pady=0, anchor=ctk.W)

        self.new_username = ctk.CTkEntry(frame, placeholder_text="Username", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, width=300)
        self.new_username.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.gen = ctk.CTkLabel(frame, text="Gender:", font=("Helvetica", 14, "bold"))
        self.gen.pack(pady=0, anchor=ctk.W)

        self.gender = ctk.CTkComboBox(frame, values=["M", "F"])
        self.gender.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.ro = ctk.CTkLabel(frame, text="Role:", font=("Helvetica", 14, "bold"))
        self.ro.pack(pady=0, anchor=ctk.W)

        self.role = ctk.CTkComboBox(frame, values=["None", "Scientist", "Administrative Officer", "Technical Assistant","Purchase & Stores Officer"])
        self.role.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.phone = ctk.CTkLabel(frame, text="Email ID:", font=("Helvetica", 14, "bold"))
        self.phone.pack(pady=0, anchor=ctk.W)

        self.phn = ctk.CTkEntry(frame, placeholder_text="eg-'abc@gmail.com'", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, width=300)
        self.phn.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.c = ctk.CTkLabel(frame, text="City:", font=("Helvetica", 14, "bold"))
        self.c.pack(pady=0, anchor=ctk.W)

        self.city = ctk.CTkEntry(frame, placeholder_text="eg-'ranchi'", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, width=300)
        self.city.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.p = ctk.CTkLabel(frame, text="Password:", font=("Helvetica", 14, "bold"))
        self.p.pack(pady=0, anchor=ctk.W)

        self.new_password = ctk.CTkEntry(frame, placeholder_text="Password", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, show="*", width=300)
        self.new_password.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.r = ctk.CTkLabel(frame, text="Rewrite password:", font=("Helvetica", 14, "bold"))
        self.r.pack(pady=0, anchor=ctk.W)

        self.rewrite_password = ctk.CTkEntry(frame, placeholder_text="Rewrite password",font=("Helvetica", 12, "bold", "italic"), corner_radius=25, show="*",width=300)
        self.rewrite_password.pack(pady=0)

        self.uname = ctk.CTkLabel(frame, text="", font=("Helvetica", 2))
        self.uname.pack(pady=0)

        self.dob = ctk.CTkLabel(frame, text="DOB", font=("Helvetica", 14, "bold"))
        self.dob.pack(pady=0, anchor=ctk.W)

        self.year = ctk.CTkEntry(frame, placeholder_text="YYYY", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, width=100)
        self.year.pack(pady=0, anchor=ctk.W, side=ctk.LEFT)

        self.mon = ctk.CTkEntry(frame, placeholder_text="MM", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, width=100)
        self.mon.pack(pady=0, anchor=ctk.CENTER, side=ctk.LEFT)

        self.date = ctk.CTkEntry(frame, placeholder_text="DD", font=("Helvetica", 12, "bold", "italic"),corner_radius=25, width=100)
        self.date.pack(pady=0, anchor=ctk.E, side=ctk.LEFT)

        self.submit = ctk.CTkButton(self, text="Create your account", command=self.submit, corner_radius=25,hover_color="dark green", fg_color="green")
        self.submit.place(relx=0.3, rely=0.90)

        self.back = ctk.CTkButton(self, text="← Back", command=self.back, corner_radius=1000, hover_color="blue",fg_color="grey", width=0.5)
        self.back.place(relx=0.01, rely=0.01)

    def back(self):
        self.destroy()
        login().mainloop()

    def submit(self):
        global name ,new_user ,sex ,new_pas ,re_pas ,contact ,city ,dob ,rol
        name = self.name.get()
        new_user = self.new_username.get()
        sex = self.gender.get()
        new_pas = self.new_password.get()
        re_pas = self.rewrite_password.get()
        contact = self.phn.get()
        city = self.city.get()
        dob = f"{self.year.get()}-{self.mon.get()}-{self.date.get()}"
        rol = self.role.get()

        if new_pas == re_pas:
            def username():
                global user_name
                connection()
                query1 = f"select username from users where username = '{new_user}';"
                cur.execute(query1)
                x = cur.fetchall()
                user_name = x
                try:
                    add_val = f"INSERT INTO users(name,username,gender,password,email,city,dob,role) VALUES('{name}','{new_user}', '{sex}','{new_pas}','{contact}','{city}','{dob}','{rol}');"
                    cur.execute(add_val)
                    con.commit()
                    print(f"new username = {self.new_username.get()}")
                    print(f"new password = {self.new_password.get()}")
                    print(cur.rowcount, "record inserted.")
                    self.created()
                    self.user_new()
                except:
                    self.exist()
                con.close()
            username()
        else:
            self.dif()

    def created(self):
        messagebox.showinfo("Welcome", f"Hello {name}, your account is created.")

    def exist(self):
        messagebox.showwarning("Duplicate data", "Username already exists")

    def dif(self):
        messagebox.showerror("Error", "New password and Rewrite password are not same")

    def user_new(self):
        self.destroy()
        login().mainloop()

class home(ctk.CTk):
    def __init__(self):
        super().__init__()
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        width = s_width
        height = s_height
        width_position = (0)
        height_position = (0)

        self.geometry("%dx%d+%d+%d" % (width, height, width_position, height_position))
        self.resizable(width=True, height=True)
        self.title("ISRO Management System-Home Page")
        self.iconbitmap("py.ico")

        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1, uniform='a')

        self.left_frame = ctk.CTkFrame(self, fg_color="white", border_width=2)
        self.left_frame.grid(row=0, column=0, rowspan=2, sticky=ctk.NSEW)

        logo = ImageTk.PhotoImage(Image.open("ISRO.png").resize((100, 96)))

        logo_label = ctk.CTkButton(self.left_frame, command=self.info, image=logo, text="", bg_color="transparent",fg_color="white", hover_color="#F5F5F5", height=100)
        logo_label.pack(pady=10)

        self.top_frame = ctk.CTkFrame(self, fg_color="#1B0838", border_width=2)
        self.top_frame.grid(row=0, column=1, columnspan=3, sticky=ctk.NSEW)

        c_name = ctk.CTkLabel(self.top_frame, text="INDIAN SPACE RESEARCH ORGANISATION", font=("Helvetica", 30, "bold"),bg_color="transparent", fg_color="transparent", text_color="white")
        c_name.pack(pady=10, expand=True)

        self.bottom_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", border_width=2)
        self.bottom_frame.grid(row=2, column=0, rowspan=12, sticky=ctk.NSEW)

        self.bottom_frame.columnconfigure((0), weight=1)
        self.bottom_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        hp = ImageTk.PhotoImage(Image.open("home.png").resize((50, 50)))
        home = ctk.CTkButton(self.bottom_frame, command=self.homepage, image=hp, text="Home",font=("Helvetica", 18, "bold"),text_color="black", bg_color="transparent", fg_color="transparent", anchor=ctk.W,hover_color="orange", width=350)
        home.grid(row=0, column=0, sticky=ctk.NS, pady=15, padx=2)

        fp = ImageTk.PhotoImage(Image.open("profile.png").resize((50, 50)))
        profile = ctk.CTkButton(self.bottom_frame, command=self.profile, image=fp, text="Profile",font=("Helvetica", 18, "bold"),text_color="black", bg_color="transparent", fg_color="transparent", anchor=ctk.W,hover_color="orange", width=350)
        profile.grid(row=1, column=0, sticky=ctk.NS, pady=15, padx=2)

        pro = ImageTk.PhotoImage(Image.open("project.png").resize((50, 50)))
        projects = ctk.CTkButton(self.bottom_frame, command=self.projects, image=pro, text="Spacecraft missions",font=("Helvetica", 18, "bold"),text_color="black", bg_color="transparent", fg_color="transparent", anchor=ctk.W,hover_color="orange", width=350)
        projects.grid(row=2, column=0, sticky=ctk.NS, pady=15, padx=2)

        img = ImageTk.PhotoImage(Image.open("employee.png").resize((50, 50)))
        employee = ctk.CTkButton(self.bottom_frame, command=self.employees, image=img, text="Employees",font=("Helvetica", 18, "bold"),text_color="black", bg_color="transparent", fg_color="transparent", anchor=ctk.W,hover_color="orange", width=350)
        employee.grid(row=3, column=0, sticky=ctk.NS, pady=15, padx=2)

        ab = ImageTk.PhotoImage(Image.open("about.png").resize((50, 50)))
        about = ctk.CTkButton(self.bottom_frame, command=self.about, image=ab, text="About",font=("Helvetica", 18, "bold"),text_color="black", bg_color="transparent", fg_color="transparent", anchor=ctk.W,hover_color="orange", width=350)
        about.grid(row=4, column=0, sticky=ctk.NS, pady=15, padx=2)

        logout = ImageTk.PhotoImage(Image.open("logout.png").resize((50, 50)))
        logout_profile = ctk.CTkButton(self.bottom_frame, command=self.logout, image=logout, text="Logout",font=("Helvetica", 18, "bold"),text_color="black", bg_color="transparent", fg_color="transparent", anchor=ctk.W,hover_color="red", width=350)
        logout_profile.grid(row=6, column=0, sticky=ctk.NS, pady=15, padx=2)

        self.main = ctk.CTkFrame(self, fg_color="white", border_width=2)
        self.main.grid(row=1, column=1, rowspan=13, columnspan=3, sticky=ctk.NSEW)
        self.main.columnconfigure((0), weight=1, uniform='a')
        self.main.rowconfigure((0), weight=1, uniform='a')

        self.right_frame = ctk.CTkFrame(self.main, fg_color="white")
        self.right_frame.grid(row=0, column=0, sticky=ctk.NSEW, pady=2, padx=2)
        self.right_frame.columnconfigure((0), weight=1, uniform='a')
        self.right_frame.rowconfigure((0), weight=1, uniform='a')
        self.homepage()

    def homepage(self):
        self.right_frame.destroy()
        self.right_frame = ctk.CTkFrame(self.main, fg_color="white")
        self.right_frame.grid(row=0, column=0, sticky=ctk.NSEW, pady=2, padx=2)
        self.right_frame.columnconfigure((0), weight=1, uniform='a')
        self.right_frame.rowconfigure((0), weight=1, uniform='a')

        home_frame = ctk.CTkFrame(self.right_frame)
        home_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        home_frame.columnconfigure((0), weight=1, uniform='a')
        home_frame.rowconfigure((0), weight=1, uniform='a')

        space_label = tk.Label(home_frame)
        space_label.grid(row=0, column=0, sticky=ctk.NSEW)

        space = tkvideo("space.mp4", space_label, loop=1, size=(1371, 771))
        space.play()

    def profile(self):
        self.right_frame.destroy()
        self.right_frame = ctk.CTkFrame(self.main, fg_color="white")
        self.right_frame.grid(row=0, column=0, sticky=ctk.NSEW, pady=2, padx=2)
        self.right_frame.columnconfigure((0), weight=1, uniform='a')
        self.right_frame.rowconfigure((0), weight=1, uniform='a')

        home_frame = ctk.CTkFrame(self.right_frame)
        home_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        home_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        home_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1, uniform='a')

        one = ImageTk.PhotoImage(Image.open("bg.png"))
        bg = ctk.CTkLabel(home_frame, image=one, text="")
        bg.grid(row=0, column=0, rowspan=12, columnspan=6, sticky=ctk.NSEW)

        profile_frame = ctk.CTkFrame(home_frame, fg_color="#D7B4F3", border_color="#1B0838", border_width=3,corner_radius=0)
        profile_frame.grid(row=1, column=2, rowspan=8, columnspan=2, sticky=ctk.NSEW)
        profile_frame.columnconfigure((0, 1), weight=1, uniform='a')
        profile_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')

        canvas = ctk.CTkCanvas(profile_frame, borderwidth=0)
        canvas.place(relx=0, rely=0, relheight=1, relwidth=1)
        canvas.columnconfigure((0, 1), weight=1, uniform='a')
        canvas.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')

        canvas.create_image(0, 0, image=one, anchor=ctk.NW)

        naam = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        naam.grid(row=1, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        naam.columnconfigure((0, 1), weight=1, uniform='a')

        nam = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        nam.grid(row=2, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        nam.columnconfigure((0, 1), weight=1, uniform='a')

        var = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        var.grid(row=3, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        var.columnconfigure((0, 1), weight=1, uniform='a')

        var1 = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        var1.grid(row=4, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        var1.columnconfigure((0, 1), weight=1, uniform='a')

        var2 = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        var2.grid(row=5, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        var2.columnconfigure((0, 1), weight=1, uniform='a')

        var3 = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        var3.grid(row=6, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        var3.columnconfigure((0, 1), weight=1, uniform='a')

        var4 = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        var4.grid(row=7, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        var4.columnconfigure((0, 1), weight=1, uniform='a')

        var5 = ctk.CTkFrame(profile_frame, fg_color="#D7B4F3")
        var5.grid(row=8, column=0, columnspan=2, sticky=ctk.NSEW, padx=50, pady=10)
        var5.columnconfigure((0, 1), weight=1, uniform='a')

        e = ImageTk.PhotoImage(Image.open("edit.png").resize((25, 25)))
        edit = ctk.CTkButton(profile_frame, image=e, text="", bg_color="transparent", hover_color="#D7B4F3",fg_color="#7C629B", border_width=2, width=30, height=30, corner_radius=0,border_color="#321D4F")
        edit.grid(row=0, column=1, sticky=ctk.NE, padx=10, pady=10)

        delete = ctk.CTkButton(home_frame, command=self.dlt, text="DELETE YOUR ACCOUNT", font=("Helvetica", 14, "bold"),corner_radius=0, hover_color="red", text_color="white", fg_color="#7C629B",border_color="#321D4F", border_width=3)
        delete.grid(row=9, column=3, pady=2, padx=2, sticky=ctk.NSEW)

        cp = ctk.CTkButton(home_frame, command=self.change_pass, text="CHANGE PASSWORD", font=("Helvetica", 14, "bold"),corner_radius=0, hover_color="#D7B4F3", text_color="white", fg_color="#7C629B",border_color="#321D4F", border_width=3)
        cp.grid(row=9, column=2, pady=2, padx=2, sticky=ctk.NSEW)

        connection()
        query = f"select name from users where username = '{user}';"
        cur.execute(query)
        x = cur.fetchall()
        x = (str(x))[3:-4]

        query2 = f"select gender from users where username = '{user}';"
        cur.execute(query2)
        y = cur.fetchall()
        y = (str(y))[3:-4]

        query3 = f"select dob from users where username = '{user}';"
        cur.execute(query3)
        m = cur.fetchall()
        n = (str(m))[-6:-4]
        o = (str(m))[21:23]
        p = (str(m))[16:20]
        z = f"{n}-{o}-{p}"

        query4 = f"select role from users where username = '{user}';"
        cur.execute(query4)
        post = cur.fetchall()
        post = (str(post))[3:-4]

        query5 = f"select city from users where username = '{user}';"
        cur.execute(query5)
        sehar = cur.fetchall()
        sehar = (str(sehar))[3:-4]

        query6 = f"select email from users where username = '{user}';"
        cur.execute(query6)
        chi = cur.fetchall()
        chi = (str(chi))[3:-4]
        con.close()

        n = ctk.CTkLabel(naam, text="NAME:", font=("Helvetica", 20, "bold"))
        n.grid(row=0, column=0, padx=2, pady=2, sticky=ctk.W)

        nn = ctk.CTkLabel(naam, text=x.upper(), font=("Helvetica", 14, "bold"))
        nn.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

        u = ctk.CTkLabel(nam, text="USERNAME:", font=("Helvetica", 20, "bold"))
        u.grid(row=0, column=0, padx=2, pady=2, sticky=ctk.W)

        un = ctk.CTkLabel(nam, text=user, font=("Helvetica", 14, "bold"))
        un.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

        p = ctk.CTkLabel(var, text="PASSWORD:", font=("Helvetica", 20, "bold"))
        p.grid(row=0, column=0, padx=8, pady=2, sticky=ctk.W)

        pp = ctk.CTkLabel(var, text=pas, font=("Helvetica", 14, "bold"))
        pp.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

        g = ctk.CTkLabel(var1, text="GENDER:", font=("Helvetica", 20, "bold"))
        g.grid(row=0, column=0, padx=8, pady=2, sticky=ctk.W)

        gg = ctk.CTkLabel(var1, text=y, font=("Helvetica", 14, "bold"))
        gg.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

        d = ctk.CTkLabel(var2, text="DOB:", font=("Helvetica", 20, "bold"))
        d.grid(row=0, column=0, padx=8, pady=2, sticky=ctk.W)

        dd = ctk.CTkLabel(var2, text=z, font=("Helvetica", 14, "bold"))
        dd.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

        r = ctk.CTkLabel(var3, text="ROLE:", font=("Helvetica", 20, "bold"))
        r.grid(row=0, column=0, padx=8, pady=2, sticky=ctk.W)

        rr = ctk.CTkLabel(var3, text=post, font=("Helvetica", 14, "bold"))
        rr.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

        s = ctk.CTkLabel(var4, text="CITY:", font=("Helvetica", 20, "bold"))
        s.grid(row=0, column=0, padx=8, pady=2, sticky=ctk.W)

        ss = ctk.CTkLabel(var4, text=sehar, font=("Helvetica", 14, "bold"))
        ss.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

        c = ctk.CTkLabel(var5, text="EMAIL ID:", font=("Helvetica", 20, "bold"))
        c.grid(row=0, column=0, padx=8, pady=2, sticky=ctk.W)

        cc = ctk.CTkLabel(var5, text=chi, font=("Helvetica", 10, "bold"))
        cc.grid(row=0, column=1, padx=2, pady=2, sticky=ctk.W)

    def employees(self):
        self.right_frame.destroy()
        self.right_frame = ttk.Frame(self.main)
        self.right_frame.grid(row=0, column=0, sticky=tk.NSEW, pady=2, padx=2)
        self.right_frame.columnconfigure((0), weight=1, uniform='a')
        self.right_frame.rowconfigure((0), weight=1, uniform='a')

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")

        style.map("Treeview", background=[("selected", "#347083")])

        tree_frame = ttk.Frame(self.right_frame)
        tree_frame.pack(pady=10, fill=tk.Y, expand=True)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.tree.pack(fill=tk.Y, expand=True)

        tree_scroll.config(command=self.tree.yview)

        self.tree['columns'] = ("Username", "Name", "Sex", "Email", "City", "DOB", "Role")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Username", anchor=tk.CENTER, width=200)
        self.tree.column("Name", anchor=tk.CENTER, width=200)
        self.tree.column("Sex", anchor=tk.CENTER, width=80)
        self.tree.column("Email", anchor=tk.CENTER, width=350)
        self.tree.column("City", anchor=tk.CENTER, width=200)
        self.tree.column("DOB", anchor=tk.CENTER, width=150)
        self.tree.column("Role", anchor=tk.CENTER, width=230)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Username", anchor=tk.CENTER, text="Username")
        self.tree.heading("Name", anchor=tk.CENTER, text="Name")
        self.tree.heading("Sex", anchor=tk.CENTER, text="Sex")
        self.tree.heading("Email", anchor=tk.CENTER, text="Email")
        self.tree.heading("City", anchor=tk.CENTER, text="City")
        self.tree.heading("DOB", anchor=tk.CENTER, text="DOB")
        self.tree.heading("Role", anchor=tk.CENTER, text="Role")

        self.tree.tag_configure("oddrows", background="white")
        self.tree.tag_configure("evenrows", background="lightblue")

        self.call_users()

        self.data = ttk.LabelFrame(self.right_frame, text="Records")
        self.data.pack(fill=tk.X, expand=True, padx=20)

        un = ttk.Label(self.data, text="Username:")
        un.grid(row=0, column=0, padx=10, pady=10)
        self.une = ttk.Entry(self.data)
        self.une.grid(row=0, column=1, padx=10, pady=10)

        n = ttk.Label(self.data, text="Name:")
        n.grid(row=1, column=0, padx=10, pady=10)
        self.ne = ttk.Entry(self.data)
        self.ne.grid(row=1, column=1, padx=10, pady=10)

        s = ttk.Label(self.data, text="Sex:")
        s.grid(row=1, column=2, padx=10, pady=10)
        self.se = ttk.Combobox(self.data, values=["M", "F"])
        self.se.grid(row=1, column=3, padx=10, pady=10)

        e = ttk.Label(self.data, text="Email:")
        e.grid(row=1, column=4, padx=10, pady=10)
        self.ee = ttk.Entry(self.data)
        self.ee.grid(row=1, column=5, padx=10, pady=10)

        c = ttk.Label(self.data, text="City:")
        c.grid(row=1, column=6, padx=10, pady=10)
        self.ce = ttk.Entry(self.data)
        self.ce.grid(row=1, column=7, padx=10, pady=10)

        d = ttk.Label(self.data, text="DOB:")
        d.grid(row=1, column=8, padx=10, pady=10)
        self.de = DateEntry(self.data, date_pattern="YYYY-MM-DD")
        self.de.grid(row=1, column=9, padx=10, pady=10)

        r = ttk.Label(self.data, text="Role:")
        r.grid(row=0, column=2, padx=10, pady=10)
        self.re = ttk.Combobox(self.data, values=["None", "Scientist", "Administrative Officer", "Technical Assistant","Purchase & Stores Officer"])
        self.re.grid(row=0, column=3, padx=10, pady=10)

        self.key = ttk.LabelFrame(self.right_frame, text="Commands")
        self.key.pack(fill=tk.X, expand=True, padx=20)

        ad = ttk.Button(self.key, text="Add record", command=self.add_rec)
        ad.grid(row=0, column=0, padx=10, pady=10)

        rem = ttk.Button(self.key, text="Delete record", command=self.del_rec)
        rem.grid(row=0, column=1, padx=10, pady=10)

        up = ttk.Button(self.key, text="Update record", command=self.up)
        up.grid(row=0, column=2, padx=10, pady=10)

        sel = ttk.Button(self.key, text="Clear entry boxes", command=self.clr)
        sel.grid(row=0, column=3, padx=10, pady=10)

        res = ttk.Button(self.key, text="Reset default table", command=self.org)
        res.grid(row=0, column=4, padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.selected)

    def projects(self):
        self.right_frame.destroy()
        self.right_frame = ttk.Frame(self.main)
        self.right_frame.grid(row=0, column=0, sticky=tk.NSEW, pady=2, padx=2)
        self.right_frame.columnconfigure((0), weight=1, uniform='a')
        self.right_frame.rowconfigure((0), weight=1, uniform='a')

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")

        style.map("Treeview", background=[("selected", "#347083")])

        tree_frame = ttk.Frame(self.right_frame)
        tree_frame.pack(pady=10, fill=tk.Y, expand=True)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.ptree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.ptree.pack(fill=tk.Y, expand=True)

        tree_scroll.config(command=self.ptree.yview)

        self.ptree['columns'] = ("Name", "Launch Vehicle", "Orbit Type", "Application", "Launch Date")

        self.ptree.column("#0", width=0, stretch=tk.NO)
        self.ptree.column("Name", anchor=tk.CENTER, width=250)
        self.ptree.column("Launch Vehicle", anchor=tk.CENTER, width=200)
        self.ptree.column("Orbit Type", anchor=tk.CENTER, width=350)
        self.ptree.column("Application", anchor=tk.CENTER, width=350)
        self.ptree.column("Launch Date", anchor=tk.CENTER, width=200)

        self.ptree.heading("#0", text="", anchor=tk.W)
        self.ptree.heading("Name", anchor=tk.CENTER, text="Name")
        self.ptree.heading("Launch Vehicle", anchor=tk.CENTER, text="Launch Vehicle")
        self.ptree.heading("Orbit Type", anchor=tk.CENTER, text="Orbit Type")
        self.ptree.heading("Application", anchor=tk.CENTER, text="Application")
        self.ptree.heading("Launch Date", anchor=tk.CENTER, text="Launch Date")

        self.ptree.tag_configure("oddrows", background="white")
        self.ptree.tag_configure("evenrows", background="lightblue")

        self.call_miss()

        self.reco = ttk.LabelFrame(self.right_frame, text="Records")
        self.reco.pack(fill=tk.X, expand=True, padx=20)

        f = ttk.Label(self.reco, text="Name:")
        f.grid(row=0, column=0, padx=10, pady=10)
        self.fe = ttk.Entry(self.reco)
        self.fe.grid(row=0, column=1, padx=10, pady=10)

        g = ttk.Label(self.reco, text="Launch Vehicle:")
        g.grid(row=1, column=0, padx=10, pady=10)
        self.ge = ttk.Entry(self.reco)
        self.ge.grid(row=1, column=1, padx=10, pady=10)

        h = ttk.Label(self.reco, text="Orbit Type:")
        h.grid(row=1, column=2, padx=10, pady=10)
        self.he = ttk.Entry(self.reco)
        self.he.grid(row=1, column=3, padx=10, pady=10)

        i = ttk.Label(self.reco, text="Application:")
        i.grid(row=1, column=4, padx=10, pady=10)
        self.ie = ttk.Entry(self.reco)
        self.ie.grid(row=1, column=5, padx=10, pady=10)

        j = ttk.Label(self.reco, text="Launch Date:")
        j.grid(row=1, column=6, padx=10, pady=10)
        self.je = DateEntry(self.reco, date_pattern="YYYY-MM-DD")
        self.je.grid(row=1, column=7, padx=10, pady=10)

        self.ptree.bind("<ButtonRelease-1>", self.sel)

        self.key = ttk.LabelFrame(self.right_frame, text="Commands")
        self.key.pack(fill=tk.X, expand=True, padx=20)

        ad = ttk.Button(self.key, text="Add record", command=self.add_record)
        ad.grid(row=0, column=0, padx=10, pady=10)

        rem = ttk.Button(self.key, text="Delete record", command=self.dele)
        rem.grid(row=0, column=1, padx=10, pady=10)

        up = ttk.Button(self.key, text="Update record", command=self.upd)
        up.grid(row=0, column=2, padx=10, pady=10)

        sel = ttk.Button(self.key, text="Clear entry boxes", command=self.clrent)
        sel.grid(row=0, column=3, padx=10, pady=10)

        res = ttk.Button(self.key, text="Reset default table", command=self.reset)
        res.grid(row=0, column=4, padx=10, pady=10)

    def ent_box(self):
        global b1,b2,b3,b4,b5
        b1 = self.fe.get()
        b2 = self.ge.get()
        b3 = self.he.get()
        b4 = self.ie.get()
        b5 = self.je.get()

    def sel(self, event):
        self.fe.delete(0, tk.END)
        self.ge.delete(0, tk.END)
        self.he.delete(0, tk.END)
        self.ie.delete(0, tk.END)
        self.je.delete(0, tk.END)

        selected = self.ptree.focus()
        value = self.ptree.item(selected, "values")

        self.fe.insert(0, value[0])
        self.ge.insert(0, value[1])
        self.he.insert(0, value[2])
        self.ie.insert(0, value[3])
        self.je.insert(0, value[4])

    def call_miss(self):
        connection()
        cur.execute("SELECT NAME, launch_vehicle, orbit_type, application, launch_date from mission;")
        records = cur.fetchall()
        global ginti
        ginti = 0
        for x in records:
            if ginti % 2 == 0:
                self.ptree.insert(parent="", index="end", iid=ginti, text="",
                                  values=(x[0], x[1], x[2], x[3], x[4]), tags=("evenrows",))
            else:
                self.ptree.insert(parent="", index="end", iid=ginti, text="",
                                  values=(x[0], x[1], x[2], x[3], x[4]), tags=("oddrows",))
            ginti += 1
        con.close()

    def add_record(self):
        self.ent_box()
        if messagebox.askyesno("Add record", "Do you want to add the record?"):
            connection()
            com = f"INSERT INTO mission(name,launch_vehicle,orbit_type,application,launch_date) VALUES('{b1}','{b2}','{b3}','{b4}','{b5}');"
            cur.execute(com)
            con.commit()
            con.close()
            self.projects()

    def upd(self):
        self.ent_box()
        if messagebox.askyesno("Update", "Do you want to update the record?"):
            connection()
            com = f"UPDATE MISSION SET launch_vehicle='{b2}',orbit_type='{b3}',application='{b4}',launch_date='{b5}' WHERE name = '{b1}';"
            cur.execute(com)
            con.commit()
            if cur.rowcount != 0:
                self.projects()
            else:
                messagebox.showerror("Invalid username", "Username doesn't exist")
            con.close()

    def clrent(self):
        self.fe.delete(0, tk.END)
        self.ge.delete(0, tk.END)
        self.he.delete(0, tk.END)
        self.ie.delete(0, tk.END)
        self.je.delete(0, tk.END)

    def reset(self):
        if messagebox.askyesno("Reset", "Do you want to reset to the default table?") == True:
            connection()

            drop = "delete from mission;"
            cur.execute(drop)
            con.commit()
            con.close()
            add_miss()
            self.projects()

    def dele(self):
        if messagebox.askyesno("Delete", "Do you want to delete the record?") == True:
            connection()
            selected = self.ptree.focus()
            values = self.ptree.item(selected, "values")
            v = values[0]
            sql = f"DELETE FROM mission WHERE name ='{v}';"
            cur.execute(sql)
            con.commit()
            con.close()
            self.projects()

    def entry_box(self):
        global a1, a2, a3, a4, a5, a6, a7
        a1 = self.une.get()
        a2 = self.ne.get()
        a3 = self.se.get()
        a4 = self.ee.get()
        a5 = self.ce.get()
        a6 = self.de.get()
        a7 = self.re.get()

    def selected(self, event):
        self.une.delete(0, tk.END)
        self.ne.delete(0, tk.END)
        self.se.delete(0, tk.END)
        self.ee.delete(0, tk.END)
        self.ce.delete(0, tk.END)
        self.de.delete(0, tk.END)
        self.re.delete(0, tk.END)

        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        self.une.insert(0, values[0])
        self.ne.insert(0, values[1])
        self.se.insert(0, values[2])
        self.ee.insert(0, values[3])
        self.ce.insert(0, values[4])
        self.de.insert(0, values[5])
        self.re.insert(0, values[6])

    def call_users(self):
        connection()
        cur.execute("SELECT Username, NAME, GENDER, EMAIL, CITY, DOB, ROLE from users")
        records = cur.fetchall()
        global count
        count = 0
        for x in records:
            if count % 2 == 0:
                self.tree.insert(parent="", index="end", iid=count, text="",
                                 values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6]), tags=("evenrows",))
            else:
                self.tree.insert(parent="", index="end", iid=count, text="",
                                 values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6]), tags=("oddrows",))
            count += 1
        con.close()

    def add_rec(self):
        self.entry_box()
        if messagebox.askyesno("Add record", "Do you want to add the record?"):
            connection()
            com = f"INSERT INTO USERS(username,name,gender,email,city,dob,role) VALUES('{a1}','{a2}','{a3}','{a4}','{a5}','{a6}','{a7}');"
            cur.execute(com)
            con.commit()
            con.close()
            self.employees()

    def up(self):
        self.entry_box()
        if messagebox.askyesno("Update", "Do you want to update the record?"):
            connection()
            com = f"UPDATE USERS SET name = '{a2}',gender='{a3}',email='{a4}',city='{a5}',dob='{a6}',role='{a7}' WHERE username = '{a1}';"
            cur.execute(com)
            con.commit()
            if cur.rowcount != 0:
                self.employees()
            else:
                messagebox.showerror("Invalid username", "Username doesn't exist")
            con.close()

    def clr(self):
        self.une.delete(0, tk.END)
        self.ne.delete(0, tk.END)
        self.se.delete(0, tk.END)
        self.ee.delete(0, tk.END)
        self.ce.delete(0, tk.END)
        self.de.delete(0, tk.END)
        self.re.delete(0, tk.END)

    def del_rec(self):
        if messagebox.askyesno("Delete", "Do you want to delete the record?") == True:
            connection()
            selected = self.tree.focus()
            values = self.tree.item(selected, "values")
            v = values[0]
            sql = f"DELETE FROM USERS WHERE username ='{v}';"
            cur.execute(sql)
            con.commit()
            con.close()
            self.employees()

    def org(self):
        if messagebox.askyesno("Reset", "Do you want to reset to the default table?") == True:
            connection()
            drop = "delete from users;"
            cur.execute(drop)
            con.commit()
            con.close()
            add_emp()
            self.employees()

    def about(self):
        self.right_frame.destroy()
        self.right_frame = ctk.CTkFrame(self.main, fg_color="white")
        self.right_frame.grid(row=0, column=0, sticky=ctk.NSEW, pady=2, padx=2)
        self.right_frame.columnconfigure((0), weight=1, uniform='a')
        self.right_frame.rowconfigure((0), weight=1, uniform='a')

        home_frame = ctk.CTkFrame(self.right_frame)
        home_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        home_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        home_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1, uniform='a')

        one = ImageTk.PhotoImage(Image.open("ab.png"))
        bg = ctk.CTkLabel(home_frame, image=one, text="")
        bg.grid(row=0, column=0, rowspan=12, columnspan=6, sticky=ctk.NSEW)

    def info(self):
        messagebox.showinfo("Shaurya Verma", "Created by Shaurya Verma")

    def dlt(self):
        if messagebox.askyesno("Delete your account","Your account will be deleted permanently. \n Do you want to continue?") == True:
            connection()
            query = f"delete from users where username = '{user}';"
            cur.execute(query)
            con.commit()
            self.destroy()
            messagebox.showinfo("Account deleted", "Your account is permanently deleted")
            login().mainloop()

    def change_pass(self):
        self.destroy()
        add_newpass().mainloop()

    def logout(self):
        self.destroy()
        login().mainloop()


class add_newpass(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ISRO Management System-change_password")
        self.resizable(width=False, height=False)
        self.iconbitmap("py.ico")

        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        width = s_width * 0.25
        height = s_height * 0.5
        width_position = ((s_width / 2) - width / 2)
        height_position = ((s_height / 2) - height / 2)

        self.geometry("%dx%d+%d+%d" % (width, height, width_position, height_position))

        self.heading = ctk.CTkLabel(self, text="Change your password", font=("Helvetica", 26, "bold"))
        self.heading.place(relx=0.15, rely=0.1)

        self.uname = ctk.CTkLabel(self, text="Username:", font=("Helvetica", 14, "bold"))
        self.uname.place(relx=0.10, rely=0.25)

        self.username = ctk.CTkEntry(self, placeholder_text="Username", font=("Helvetica", 12, "italic"),corner_radius=25, width=300)
        self.username.place(relx=0.1, rely=0.32)

        self.pwd = ctk.CTkLabel(self, text="Current password:", font=("Helvetica", 14, "bold"))
        self.pwd.place(relx=0.10, rely=0.45)

        self.cur_password = ctk.CTkEntry(self, placeholder_text="Current password", font=("Helvetica", 12, "italic"),corner_radius=25, show="*", width=300)
        self.cur_password.place(relx=0.1, rely=0.52)

        self.npwd = ctk.CTkLabel(self, text="New password:", font=("Helvetica", 14, "bold"))
        self.npwd.place(relx=0.10, rely=0.65)

        self.new_password = ctk.CTkEntry(self, placeholder_text="New password", font=("Helvetica", 12, "italic"),corner_radius=25, show="*", width=300)
        self.new_password.place(relx=0.1, rely=0.72)

        self.submit = ctk.CTkButton(self, text="Change password", command=self.c_pass, corner_radius=25,hover_color="dark green", fg_color="green")
        self.submit.place(relx=0.3, rely=0.90)

        self.back = ctk.CTkButton(self, text="← Back", command=self.back, corner_radius=1000, hover_color="blue",fg_color="grey", width=0.5)
        self.back.place(relx=0.01, rely=0.01)

    def back(self):
        self.destroy()
        home().mainloop()

    def c_pass(self):
        global user
        global cur_pass
        global new_pass
        user = self.username.get()
        cur_pass = self.cur_password.get()
        new_pass = self.new_password.get()
        def password():
            global x
            connection()
            query2 = f"select password from users where username = '{user}';"
            cur.execute(query2)
            x = cur.fetchall()
            con.close()
            if x != [(str(cur_pass),)]:
                messagebox.showerror("Error", "Incorrect password")
            else:
                if cur_pass == new_pass:
                    messagebox.showwarning("Warning", "New password and current password cannot be same")
                else:
                    global new
                    connection()
                    change = f"UPDATE users SET password = '{new_pass}' Where username = '{user}';"
                    cur.execute(change)
                    x = con.commit()
                    new = x
                    con.close()
                    messagebox.showinfo("Password changed", "Password changed")
                    self.destroy()
                    login().mainloop()
        password()

if __name__ == '__main__':
    startup()
    database()
    users_table()
    mission()
    login().mainloop()
