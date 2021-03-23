import socket
from threading import Thread
import sys
import tkinter

GUI = tkinter.Tk()

GUI.title("Chatroom") # GUI TITLE

GUI.geometry('500x520') # gui window size

GUI.configure(bg='grey27') # gui background colour

window = tkinter.Frame(GUI,width= 300, height = 100) # frame size for gui 


# ------------------------------------------------------------------------ GUI initialising ^^


# GUI takes clients name in chat box
if len(sys.argv) !=3:

    print("Not enough command line arguments given. Host and port set to default")

    host = '0.0.0.0' # default host

    port = 8080 # default port

else:
    host = sys.argv[1] # host given in command line 

    port = int(sys.argv[2]) # port given in command line must be called an an int


address = (host, int(port))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating an INET streaming socket

client_socket.connect(address) # calling connect on host and port to start a 3 way handshake to ensure a reliable connection

def acquire(): # functoion for clients recieving messages
    while True:
        try:
            data = client_socket.recv(1024).decode() # setting buffer size as 1024 and calling decode() on that to decode a UTF8 encoded byte string.

            message_history.insert(tkinter.END, data) # inserts the messages that the connected clients have sent into the chat box

        except OSError:  # An error that is raised if a client has left the chat

            break


def send_msg(event=None):  # sends messages to clients
    
    data = input_text.get() # gets users message that they have inputed

    input_text.set("")  # puts the text field back to blank for users next message

    client_socket.send(data.encode()) # sending the encoded data

    if data == "{quit}": # if message is equal to exit then close connection

        client_socket.close() # closing the client socket

        GUI.quit() # quiting the gui


def close(event=None): # function which sets the input text in the gui to {quit} when the window is closed
   
    input_text.set("{quit}")

    send_msg() 



input_text = tkinter.StringVar()  # the message that the user inputs

scrollbar = tkinter.Scrollbar(window)  # scrollbar for the chat box

input_text.set("Type here") # inout box for the users which has "Type here" set as default
message_history = tkinter.Listbox(window, height=25, width=70, yscrollcommand=scrollbar.set,bg='grey80',highlightbackground='gold',highlightthickness=9,borderwidth=10,relief='solid') # im here
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_history.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

window.pack() # organising before placing into parent widget

enter_box = tkinter.Entry(GUI,textvariable=input_text,) # Entry box

enter_box.bind("<Return>", send_msg)

send_button = tkinter.Button(GUI, text="Send", command=send_msg, width = 14,height=2,bg='red3',relief='raised') # send_msg button for gui calls on send_msg function

send_button.pack(side=tkinter.BOTTOM,pady=2,expand=5) # 

enter_box.pack(side=tkinter.TOP, pady= 1,expand=5)

GUI.protocol("Closing chat", close) # calling back to close function


if __name__ == '__main__':

    start = Thread(target=acquire)

    start.start() # starting thread

    tkinter.mainloop()  # Starts GUI execution.
