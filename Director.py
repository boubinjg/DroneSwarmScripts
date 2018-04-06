import socket
from Tkinter import *
import time, thread, sys, struct, os

HOST = "127.0.0.1";
PORT = 45453;
#TK pane for network monitoring
updatePanes = None;
#TK window root
root = None;
root = None;
updatePanes = None;

conns = [{1 : [0,0]}, {2 : [0,0]}]

def con(IP, VMIP, drone):
    global conns
    conns[drone-1] = [IP, VMIP];

    #make it test the connection:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    try:
        s.connect((IP, PORT));
        conns[drone-1] = [IP, VMIP];
    except Exception as e:
        print(e);
    finally:
        s.close();
    '''
def changeDropdown(one, two, three):
    print(one)
    print(two)
    print(three)

def loadConnPane(root):
    ConnPane = Frame(root);
    p1 = Frame(ConnPane);
    p2 = Frame(ConnPane);

    p1Label = Label(p1, text = "Connect to Drone 1:");
    p1.pack(side=LEFT, padx = 2, pady = 2);
    p1IPlabel = Label(p1, text = "Drone 1 Host IP:");
    p1IPlabel.pack(side=LEFT, padx = 2, pady = 2);

    p1IPBox = Entry(p1);
    p1IPBox.delete(0,END);
    p1IPBox.insert(0,"127.0.0.1");
    p1IPBox.pack(side = LEFT, padx = 2, pady = 2);

    p1VMIPlabel = Label(p1, text = "Middleware IP:");
    p1VMIPlabel.pack(side=LEFT, padx = 2, pady = 2);

    p1VMIPBox = Entry(p1);
    p1VMIPBox.delete(0,END);
    p1VMIPBox.insert(0,"192.168.2.22");
    p1VMIPBox.pack(side = LEFT, padx = 2, pady = 2);

    p1B = Button(p1, text="Connect", width=6,
          command = lambda: con(p1IPBox.get(), p1VMIPBox.get(), 1));
    p1B.pack(side=LEFT,padx=2, pady=2)

    p1.pack(side=TOP, fill=X);

    p2Label = Label(p2, text = "Connect to Drone 2:");
    p2.pack(side=LEFT, padx = 2, pady = 2);
    p2IPlabel = Label(p2, text = "Drone 2 Host IP:");
    p2IPlabel.pack(side=LEFT, padx = 2, pady = 2);

    p2IPBox = Entry(p2);
    p2IPBox.delete(0,END);
    p2IPBox.insert(0,"127.0.0.1");
    p2IPBox.pack(side = LEFT, padx = 2, pady = 2);

    p2VMIPlabel = Label(p2, text = "Middleware IP:");
    p2VMIPlabel.pack(side=LEFT, padx = 2, pady = 2);

    p2VMIPBox = Entry(p2);
    p2VMIPBox.delete(0,END);
    p2VMIPBox.insert(0,"192.168.2.22");
    p2VMIPBox.pack(side = LEFT, padx = 2, pady = 2);

    p2B = Button(p2, text="Connect", width=6,
          command = lambda: con(p2IPBox.get(), p2VMIPBox.get(), 2));
    p2B.pack(side=LEFT,padx=2, pady=2)

    p2.pack(side=TOP, fill=X);
    ConnPane.pack(side=TOP, fill=X);

def loadInfoPane(root):
    window = PanedWindow(orient=HORIZONTAL)
    window.pack(fill=BOTH,expand=1)

    leftSubwindow = PanedWindow(orient=VERTICAL);
    bottomLeft = PanedWindow(orient=HORIZONTAL);
    bottomLeft.pack();

    readout = Text(root, height = 20, width = 50);
    readout.pack(side = LEFT);
    readout.config(state=DISABLED);

    leftSubwindow.add(readout);
    leftSubwindow.add(bottomLeft);

    window.add(leftSubwindow);

    rsw = PanedWindow(orient=HORIZONTAL);
    buttonArray = PanedWindow(orient=HORIZONTAL);
    buttonArray.pack();
    br = PanedWindow(orient=HORIZONTAL);
    br.pack();

    rsw.add(buttonArray);
    rsw.add(br);

    rsw.pack();

    window.add(rsw);

    window.add(buttonArray);

    return [readout,buttonArray,br, bottomLeft]

def updateReadoutWindow(textWindow, text):
    textWindow.config(state=NORMAL)
    textWindow.delete('1.0', END)
    textWindow.insert(END, text);
    textWindow.config(state=DISABLED);

def CreateCommandWindow(pane, drone):
    commandPane = Frame(pane);
    mpLabel = Label(commandPane, text = "Send Command To Drone " + str(drone));
    mpLabel.pack(side=TOP, padx=2, pady=2);

    rtnPane = Frame(commandPane);

    rlab = Label(rtnPane, text = "Driver:         ")
    rlab.pack(side=LEFT, padx=2, pady=2);

    routineBox = Entry(rtnPane);
    routineBox.delete(0,END);
    routineBox.insert(0,"rtn");
    routineBox.pack(side=LEFT, padx=2, pady=2);

    rtnPane.pack(side=TOP, padx=2, pady=2);

    cmdPane = Frame(commandPane);

    clab = Label(cmdPane, text = "Command:   ")
    clab.pack(side=LEFT, padx=2, pady=2);

    commandBox = Entry(cmdPane);
    commandBox.delete(0,END);
    commandBox.insert(0,"start");
    commandBox.pack(side=TOP, padx=2, pady=2);

    cmdPane.pack(side=TOP, padx=2, pady=2)

    pPane = Frame(commandPane);

    plab = Label(pPane, text = "Parameter 1:");
    plab.pack(side=LEFT, padx=2, pady=2);

    paramBox = Entry(pPane);
    paramBox.delete(0,END);
    paramBox.insert(0,"Detect");
    paramBox.pack(side=TOP, padx=2, pady=2);

    pPane.pack(side=TOP, padx=2, pady=2);

    p2Pane = Frame(commandPane);

    p2lab = Label(p2Pane, text = "Parameter 2:");
    p2lab.pack(side=LEFT, padx=2, pady=2);

    param2Box = Entry(p2Pane);
    param2Box.delete(0,END);
    param2Box.insert(0,"");
    param2Box.pack(side=TOP, padx=2, pady=2);

    p2Pane.pack(side=TOP, padx=2, pady=2);

    ex = Button(commandPane, text="Execute", width=10,
          command = lambda: execute(routineBox.get(), commandBox.get(), paramBox.get(), param2Box.get(), drone));
    ex.pack(side=LEFT,padx=2, pady=2)

    bcast = Button(commandPane, text="Broadcast", width=10,
            command = lambda: bc(routineBox.get(), commandBox.get(), paramBox.get(), param2Box.get()));
    bcast.pack(side=LEFT, padx=2, pady=2);

    commandPane.pack(side=TOP, padx=2, pady=2);


def execute(rtn, cmd, p1, p2, drone):
    cmd = "edn="+str(rtn)+"-dc="+str(cmd);
    if p1 != "":
        cmd += "-dp="+str(p1)
    if p2 != "":
        cmd += "-dp="+str(p2)
    conninfo = conns[drone-1];

    print(cmd);
    print(conninfo);

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.connect((conninfo[0], PORT));
    s.send(str(conninfo[1])+","+str(cmd));

def bc(rtn, cmd, p1, p2):
    #execute for both drones
    execute(rtn, cmd, p1, p2, 1)
    execute(rtn, cmd, p1, p2, 2)

def kill():
    bc("FlyDroneDriver","lnd","","")

def loadKillswitch(pane):
    ex = Button(pane, text="Execute", width=10,
          command = lambda: kill());
    ex.pack(side=LEFT, padx=2, pady=2)

def main():
    global root
    global updatePanes

    root = Tk()
    root.title("Swarm Director (Demo Version)");
    root.geometry("920x420");
    loadConnPane(root);
    updatePanes = loadInfoPane(root);
    updateReadoutWindow(updatePanes[0], "Connect Drones");
    CreateCommandWindow(updatePanes[1], 2);
    CreateCommandWindow(updatePanes[2], 1);
    loadKillswitch(updatePanes[3])
    root.mainloop()

if __name__ == "__main__":
    main()
