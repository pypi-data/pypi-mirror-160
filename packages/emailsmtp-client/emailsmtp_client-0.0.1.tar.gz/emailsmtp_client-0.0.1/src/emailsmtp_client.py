def help():
    print("Fancy email emailsmtp_client.fancy_email()")
    print("Multiple client Server emailsmtp_client.multiple_client_server()")
    print("Database CURD emailsmtp_client.db_curd()")
    print("calculator emailsmtp_client.calc()")
    print("GUI Form emailsmtp_client.gui_form()")
    print("Text attachment email emailsmtp_client.text_attachment()")
    print("Image attachment email emailsmtp_client.image_attachment()")
    print("Audio attachment email emailsmtp_client.audio_attachment()")
    print("Font Editor emailsmtp_client.font_editor()")

def fancy_email():
    print("""
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "balasahebjagtap2001@gmail.com"
    receiver_email = "khushbugupta14044@gmail.com"
    password = "asrbifjvzwzlmgmj"

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    body = \"""\
    <html>
    <head>
    <title> Fancy email </title>
    </head>
    <body>
    <h1> Hello Khushbu </h2>
    <p>Good Afternoon, How are you?>
    <br>
    <i> Thank You </i>
    <br>
    <b><u> Bye </u></b>
    <br>
    <a href="http://www.google.com">GOOGLE</a> 
    </p>
    </body>
    </html>
    \"""

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(body, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    #message.attach(part2)

    # Create secure connection with server and send email
    #context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465,) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    print("Html content is sent...")


    """)

def multiple_client_server():
    print("""
    import socket
import re
import threading

class Verification:
    def __init__(self, ip:str, port:int) -> None:
        self.ip = ip
        self.port = port

    def verify(self) -> dict:
        match = {}
        ip_regEx = r"^[0-3][0-9]{2}\.[0-9]{3}\.[0-9]+\.[0-9]+"
        result = re.match(ip_regEx, self.ip)
        if result != None:
            match["ip"] = True
        else:
            match["ip"] = False
        if self.port>=1 and self.port<=65535:
            match["port"] = True
        else:
            match["port"] = False

        return match

class ListningServer:
    def __init__(self, ip, port) -> None:
        assert Verification(ip, port).verify()["ip"] == True and Verification(ip, port).verify()["port"] == True, "Invalid IP/port"
        self.ip = ip
        self.port = port
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_connection.bind((self.ip, self.port))
        self.disconnection_message = "-disconnect"

    def handel_client(self, conn, addr):
        print(f"[NEW CONNECTION][{addr}]")
        try:
            connection = True
            while connection == True:
                message_length = conn.recv(64).decode("utf-8")
                if message_length:
                    message_length = int(message_length)
                    message = conn.recv(message_length).decode("utf-8")
                    stripped_message = message.strip('\r')
                    stripped_message = stripped_message.strip('\n')
                    if stripped_message == "-disconnect":
                        connection = False
                    print(f"[{addr}]> {stripped_message}")
        except Exception as e:
            print(e)

    def start_server(self):
        print("[+] The server is ready to accept incoming connections")
        try:
            self.socket_connection.listen()
            print("[+] Server Listning.....")
            while True:
                connection, address = self.socket_connection.accept()
                if connection:
                    print(f"[+] Recived a TCP connection from {address}")
                    thread = threading.Thread(target=self.handel_client(conn=connection, addr=address), args=(connection, address))
                    thread.start()
        except socket.error as e:
            print("[-] Error occured while trying to connect")
        except Exception as e:
            print(e)

if __name__=="__main__":
    ip = "192.168.2.204"
    port = 1842
    server_obj = ListningServer(ip, port)
    try:
        server_obj.start_server()
    except KeyboardInterrupt:
        print("Exitted")
    """)

def db_curd():
    print("""
    import mysql.connector

def create_database():
    connection = mysql.connector.connect(host="localhost", user="root", passwd="python_practical")
    mycursor = connection.cursor()
    mycursor.execute("create database teachers")
    print("[+] Database created")

def create_table(db_name):
    connection = mysql.connector.connect(host="localhost", user="root", passwd="python_practical", database=db_name)
    mycursor = connection.cursor()
    mycursor.execute("create table teachers(name VARCHAR(50), subject VARCHAR(25), salary VARCHAR(25))")
    print("[+] Table created")

def insert(name, subject, salary):
    connection = mysql.connector.connect(host="localhost", user="root", passwd="python_practical", database="teachers")
    mycursor = connection.cursor()
    sql_query = "insert into teachers(name, subject, salary) values(%s, %s, %s)"
    values = (name, subject, salary)
    mycursor.execute(sql_query, values)
    connection.commit()

def read(column_name, table_name):
    connection = mysql.connector.connect(host="localhost", user="root", passwd="python_practical", database="teachers")
    mycursor = connection.cursor()
    mycursor.execute(f"select {column_name} from {table_name}")
    output = mycursor.fetchall()
    for single_teacher_info in output:
        print(single_teacher_info)

def update():
    connection = mysql.connector.connect(host="localhost", user="root", passwd="python_practical", database="teachers")
    mycursor = connection.cursor()
    mycursor.execute("Update teachers SET name='Madhvi' WHERE name='shweta'")
    connection.commit()
 
def delete():
    connection = mysql.connector.connect(host="localhost", user="root", passwd="python_practical", database="teachers")
    mycursor = connection.cursor()
    mycursor.execute("DELETE from teachers where name='Prajwal'")
    connection.commit()

#create_database()
#create_table("teachers")
#insert("Shweta", "CN", "65000")
#insert("Ninad", "Crypto", "60000")
#insert("Prajwal", "FCS", "60000")
#read("*", "teachers")
#update()
#delete()
    """)

def calc():
    print("""
    from tkinter import *

root = Tk()
root.geometry("1200x600")

scvalue = StringVar()
scvalue.set("")

screen = Entry(root, textvar = scvalue, font=("Lucide 40 bold"))
screen.pack(fill=X)

def click(event):
  global scvalue
  text = event.widget.cget("text")

  if text == "=":
    if scvalue.get().isdigit():
      value = int(scvalue.get())
    else:
      value = eval(screen.get())
           
    scvalue.set(value)
    screen.update()
  elif text == "C":
    scvalue.set("")
    screen.update()
  else:
    scvalue.set(scvalue.get() + text)
    screen.update()


f = Frame(root, bg="grey")
f.pack()
b = Button(f, text="9", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="8", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="7", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

f = Frame(root, bg="grey")
f.pack()
b = Button(f, text="6", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT, expand = True, fill="both")

b = Button(f, text="5", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="4", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

f = Frame(root, bg="grey")
f.pack()
b = Button(f, text="3", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="2", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="1", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

f = Frame(root, bg="grey")
f.pack()
b = Button(f, text="0", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="-", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="*", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

f = Frame(root, bg="grey")
f.pack()
b = Button(f, text="/", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="%", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

b = Button(f, text="= ", font=("lucida 35 bold"))
b.bind("<Button-1>",click)
b.pack(side=LEFT)

root.mainloop()
    """)

def gui_form():
    print("""
    from tkinter import *

root = Tk()

label1 = Label(text="ICE-CREAM",font= ("Arial", 17, "bold")).grid(row=0, column=0)
options = ['Choclate', ' Ice cream', 'biscuit']
clicked = StringVar()
clicked.set('Choclate')

dropdown = OptionMenu(root, clicked, *options).grid(row=1, column=1)

label2 = Label(text="Which ice cream flavour you want>").grid(row=1, column=0)

label3 = Label(text="How would you like to have it?").grid(row=3, column=0)
C1 = Checkbutton(root, text="Music", variable="CheckVar1",).grid(row=3,column=1)
C2 = Checkbutton(root, text="Music", variable="CheckVar2",).grid(row=3,column=2)
C3 = Checkbutton(root, text="Music", variable="CheckVar3",).grid(row=3,column=3)
label4 = Label(text="How many people you will serve").grid(row=4, column=0)
ent4 = Entry(root).grid(row=4, column=1
    """)

def text_attachment():
    print("""import smtplib, ssl
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "temporarywebhosting@gmail.com"
receiver_email = "lilcutepaws@gmail.com"
password = "ziqugajgcndntyqz"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
body = "This is mail with attachement a text document"

# Turn these into plain/html MIMEText objects
part = MIMEText(body, "html")

filename = "document.txt"
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)

# Set mail headers
part.add_header(
    "Content-Disposition",
    "attachment", filename= filename
)
message.attach(part)
#message.attach(part2)

# Create secure connection with server and send email
#context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465,) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print("Audio file attachment mail is sent....")
print("Check your mail..")""")

def image_attachment():
    print("""
    import smtplib, ssl
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "temporarywebhosting@gmail.com"
receiver_email = "lilcutepaws@gmail.com"
password = "ziqugajgcndntyqz"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
body = "This is mail with attachement a text document"

# Turn these into plain/html MIMEText objects
part = MIMEText(body, "html")

filename = "images.jpeg"
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)

# Set mail headers
part.add_header(
    "Content-Disposition",
    "attachment", filename= filename
)
message.attach(part)
#message.attach(part2)

# Create secure connection with server and send email
#context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465,) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print("Image attachment mail is sent....")
print("Check your mail...")
    """)

def audio_attachment():
    print("""
    import smtplib, ssl
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "balasahebjagtap2001@gmail.com"
receiver_email = "khushbugupta14044@gmail.com"
password = "mmzvwyazbkbhglcx"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
body = "This is mail with attachement a text document"

# Turn these into plain/html MIMEText objects
part = MIMEText(body, "html")

filename = "/home/jagtap/Downloads/Kaun Tujhe Yun Pyar Karega Jaise Mai Karti Hu Lyrics - Palak Muchhal - Amaal Mallik - Melody Cafe.mp4"
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)

# Set mail headers
part.add_header(
    "Content-Disposition",
    "attachment", filename= filename
)
message.attach(part)
#message.attach(part2)

# Create secure connection with server and send email
#context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465,) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print("Audio file attachment mail is sent....")
print("Check your mail..")
    """)

def font_editor():
    print("""
    import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    \"""Open a file for editing.\"""
    filepath = askopenfilename(
        filetypes=[("Text Files", ".txt"), ("All Files", ".*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Text Editor Application - {filepath}")

def save_file():
    \"""Save the current file as a new file.\"""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", ".txt"), ("All Files", ".*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Text Editor Application - {filepath}")

window = tk.Tk()
window.title("Text Editor Application")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
    """)