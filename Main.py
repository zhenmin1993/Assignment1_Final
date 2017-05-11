from xml.dom.minidom import parse
import xml.dom.minidom

import MySQLdb

from Tkinter import *
import tkMessageBox
import Tkinter as tk

from BaseClass import *
from DBoperat_class import *

from GUI_Class import *
from Build_YMatrix import *
from SearchFile import *


import sys
import os
import time



#define the function of LogIn Button
#This button is used to connect the MySQL Server
def LoginButtonFunc(): 
    #print 'Connecting to MySQL server'
    Message = 'Connecting to MySQL server'

    var_Log.set(Message)
    Stat_Para_Log_Init = {'bd':1,'anchor':W, 'fg':'black'}
    win.AddStatus(Stat_Para_Log_Init, LogStructStatus, var_Log.get())
    win.root.update()

    host =  var_host.get()
    user = var_user.get()
    passwd =  var_passwd.get()
    db =  var_dbName.get()
    port =  var_port.get()
    port = int(port)

    try:
        global conn
        global cur
        conn=MySQLdb.connect(host,user,passwd,db,port)
        cur = conn.cursor()
        Message = 'Connected to MySQL server'
        #print 'Connected to MySQL server\n'

        var_Log.set(Message)
        Stat_Para_Log_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
        win.AddStatus(Stat_Para_Log_success, LogStructStatus, var_Log.get())
        win.root.update()
        tkMessageBox.showinfo(title='Computer Application', \
            message='Server Connected! Please Continue!')


    except:
        Message = 'Connection Failed! Please Check!'
        #print 'Connection Failed! Please Check!'

        var_Log.set(Message)
        Stat_Para_Log_fail = {'bd':1,'anchor':W, 'fg':'red'}
        win.AddStatus(Stat_Para_Log_fail, LogStructStatus, var_Log.get())
        win.root.update()




#Define the ExitButtonFunction
def ExitButtonFunc():
    answer = tkMessageBox.askquestion('Computer Application', 'Are you sure to EXIT?')

    if answer == 'yes':
        win.DestroySelf()      
        sys.exit()

#When there is a new status, update it instantaneously
def Update_Status(New_Message, Fon_Color):    
    var_TotStatus.set(New_Message)
    Stat_Para_Tot_update= {'bd':1,'anchor':W, 'fg':Fon_Color}
    TotStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
    win.AddStatus(Stat_Para_Tot_update, TotStructStatus, var_TotStatus.get())
    win.root.update()



#Define the function of the button confirm
def ConfirmButtonFunc():
    #Get the file name from the user's input
    fname_EQ =  var_EQName.get()
    fname_SSH = var_SSHName.get()
    global collection_EQ
    global collection_SSH
    #The below loop is used to identify whether the file name is correct or not, and which file name is wrong
    while True:

        identify = 0
        try:
            DOMTree_EQ = xml.dom.minidom.parse(fname_EQ)
            collection_EQ = DOMTree_EQ.documentElement
            print '\nEQ data read success\n'

            var_EQCheck.set('EQ data read succeed!')
            Stat_Para_EQCheck_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
            win.AddStatus(Stat_Para_EQCheck_success, EQCheckStructStatus, var_EQCheck.get())
            win.root.update()

            identify = 1

        except:
            identify = 3
            print '\nWrong EQ file name or file does not exist!'

            var_EQCheck.set('Wrong EQ file name or file does not exist!')

            Stat_Para_EQCheck_fail = {'bd':1,'anchor':W, 'fg':'red'}
            win.AddStatus(Stat_Para_EQCheck_fail, EQCheckStructStatus, var_EQCheck.get())
            win.root.update()
            break
            


        if identify ==1:

            try:
                DOMTree_SSH = xml.dom.minidom.parse(fname_SSH)
                collection_SSH = DOMTree_SSH.documentElement
                print 'SSH data read success\n'

                var_SSHCheck.set('SSH data read succeed!')

                Stat_Para_SSHCheck_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
                win.AddStatus(Stat_Para_SSHCheck_success, SSHCheckStructStatus, var_SSHCheck.get())
                win.root.update()
                identify =2

                var_TabCheck.set('File Name checking passed!')
                Stat_Para_TabCheck_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
                win.AddStatus(Stat_Para_TabCheck_success, TabCheckStructStatus, var_TabCheck.get())
                win.root.update()

                break
            
        
            

            except:
                identify = 3
                print 'Wrong SSH file name or file does not exist!\n'

                var_SSHCheck.set('Wrong SSH file name or file does not exist!')

                Stat_Para_SSHCheck_fail= {'bd':1,'anchor':W, 'fg':'red'}
                win.AddStatus(Stat_Para_SSHCheck_fail, SSHCheckStructStatus, var_SSHCheck.get())
                win.root.update()
                break
    #Find all the Child Nodes
    if identify ==2:
        try:
            Childs = AllChilds(collection_EQ,collection_SSH)
            Needed_Child = Childs.pick_Needed_Child()

            New_Message = 'All ChildNodes Found!'
            Update_Status(New_Message, '#228B22')

        except:
            identify = 3
            var_WriteStatus.set('Searching File Failed')
            Stat_Para_NoConnect = {'bd':1,'anchor':W, 'fg':'red'}
            WriteStructStatus = {'row':15, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
            win.AddStatus(Stat_Para_NoConnect, WriteStructStatus, var_WriteStatus.get())


    if identify == 3: 

        New_Message = 'Failed! Please check above message!'
        Update_Status(New_Message, 'red')


    #Check the server connection condition
    try:
        cur_test = cur
        conn_test = conn
        connect_condition = 'OK'

    except:
        tkMessageBox.showinfo(title='Computer Application', \
            message='No Connection to MySQL Server! Please First Login!')
        New_Message = 'No Connection to MySQL Server! Please First Login!'
        Update_Status(New_Message, 'red')

    #Ask whether the user want to create fresh tables or not
    if connect_condition is 'OK':
        try:
            answer = tkMessageBox.askquestion('Computer Application', 'Creating new tables?')
            New_Table_Choice = 0

            if answer == 'yes': New_Table_Choice = 1
            #Create/Check tables and then write all the data into tables
            execfile('Find_Feed.py')

            New_Message = '''Succeed! Please Exit and check Database 5bus!\nServer Now Disconnected for Protection!'''
            Update_Status(New_Message, '#228B22')

            tkMessageBox.showinfo(title='Computer Application', message='All Tables Are Now Ready!')


        except:
            New_Message = '''Failed! Please Check'''
            Update_Status(New_Message, 'red')




#Define the function of 'Show' Button
def BusButtonFunc():
    #Connect with MySQL server
    print 'Connecting to MySQL server'
    Message = 'Connecting to MySQL server'

    var_ConnectCheck.set('Connecting to MySQL server')
    Stat_Para_ConnectCheck = {'bd':1,'anchor':W, 'fg':'black'}
    ConnectCheckStructStatus = {'row':12, 'sticky':N+E+S+W, 'columnspan':5, 'column':6}
    win.AddStatus(Stat_Para_ConnectCheck, ConnectCheckStructStatus, var_ConnectCheck.get())
    win.root.update()

    host =  var_host.get()
    user = var_user.get()
    passwd =  var_passwd.get()
    db =  var_dbName.get()
    port =  var_port.get()
    port = int(port)

    try:
        conn=MySQLdb.connect(host,user,passwd,db,port)
        cur = conn.cursor()
        Message = 'Connected to MySQL server'
        print 'Connected to MySQL server\n'
        var_ConnectCheck.set('Connected to MySQL server')
        Stat_Para_ConnectCheck = {'bd':1,'anchor':W, 'fg':'#228B22'}
        ConnectCheckStructStatus = {'row':12, 'sticky':N+E+S+W, 'columnspan':5, 'column':6}
        win.AddStatus(Stat_Para_ConnectCheck, ConnectCheckStructStatus, var_ConnectCheck.get())
        win.root.update()


    except:
        Message = 'Connection Failed! Please Check!'
        print 'Connection Failed! Please Check!'

        var_ConnectCheck.set('Connection Failed! Please Check!')
        Stat_Para_ConnectCheck = {'bd':1,'anchor':W, 'fg':'red'}
        ConnectCheckStructStatus = {'row':12, 'sticky':N+E+S+W, 'columnspan':5, 'column':6}
        win.AddStatus(Stat_Para_ConnectCheck, ConnectCheckStructStatus, var_ConnectCheck.get())
        win.root.update()
    
    #Build Y Matrix
    Matrix = YMatrixBuild(cur,conn)
    YMatrix = Matrix.build_YMatrix()
    busName = Matrix.matrix_bus_name
    duplicate_busbar = Matrix.duplicate_bus_name

    #Claculte how many buses we have
    bus_Numbers = len(YMatrix)
    Bus_row = list()
    Bus_column = list()

    for item in range(bus_Numbers):
        item = item + 1
        Bus_row.append(item)
        Bus_column.append(item)



    Lab_Para_Show_Button = {'bg':None, 'fg':'black'}
    BusStructLabShow_Button = {'row':11,'columnspan':5, 'sticky':N+E+S+W, 'rowspan':1, 'column':6}
    win.AddLabel('' , Lab_Para_Show_Button, BusStructLabShow_Button)
    var_Ybus = dict()

    for iter_row in Bus_row:
        for iter_column in Bus_column:
            var_Ybus[str(iter_row)+str(iter_column)]=StringVar()
            try:
                #Pick the real part and imaginary part
                real_part = round(YMatrix[iter_row][iter_column].real, 5)
                imagin_part = round(YMatrix[iter_row][iter_column].imag, 5)
                if imagin_part>=0:
                    target = str(real_part) + '+' + str(imagin_part) + 'i'
                if imagin_part<0:
                    target = str(real_part) + str(imagin_part) + 'i'
                var_Ybus[str(iter_row)+str(iter_column)].set(target)
            except:
                var_Ybus[str(iter_row)+str(iter_column)].set(0.0)

            #Display the element
            Stat_Para_Bus_ele = {'bd':1,'anchor':W, 'fg':'black'}
            BusStructStat_ele = {'row':2*iter_row,'columnspan':1, 'sticky':N+E+S+W, 'column':5+iter_column}
            win.AddStatus( Stat_Para_Bus_ele, BusStructStat_ele,var_Ybus[str(iter_row)+str(iter_column)].get() )

            #Add label for all the elements
            if iter_column % 2 != 0 : bg_color = 'grey'
            if iter_column % 2 == 0 : bg_color = 'grey65'
            Lab_Para_Bus_ele = {'bg':bg_color, 'fg':'black'}
            BusStructLab_ele = {'row':2*iter_row -1,'columnspan':1, 'sticky':N+E+S+W, 'rowspan':1, 'column':5+iter_column}
            win.AddLabel('Y'+str(iter_row)+str(iter_column), Lab_Para_Bus_ele, BusStructLab_ele)
        current_row = 2*iter_row

    var_ConnectCheck.set('Ybus Matrix Build Succeed!')
    Stat_Para_ConnectCheck = {'bd':1,'anchor':W, 'fg':'#228B22'}
    ConnectCheckStructStatus = {'row':current_row+2, 'sticky':N+E+S+W, 'columnspan':5, 'column':6}
    win.AddStatus(Stat_Para_ConnectCheck, ConnectCheckStructStatus, var_ConnectCheck.get())

    Lab_Para_Bus_Title = {'bg':'grey60', 'fg':'black'}
    BusStructLabTitle = {'row':0,'columnspan':len(Bus_column), 'sticky':N+E+S+W, 'rowspan':1, 'column':6}
    win.AddLabel('Y-Bus Matrix' , Lab_Para_Bus_Title, BusStructLabTitle)
    
    win.root.update()
    

    Exit3StructButt = {'row':1+2*len(Bus_column),'column':5+len(Bus_column),'padx':0,'pady':1}
    win.AddButton('Exit', ExitButtonFunc, Exit3StructButt)

    #Add notes
    note = 'Note : '

    Note_Para_Bus = {'bg':None, 'fg':'black'}
    BusStructNote = {'row':current_row+3,'columnspan':len(Bus_column), 'sticky':W, 'rowspan':1, 'column':6}
    win.AddLabel(note , Note_Para_Bus, BusStructNote)

    #Add the bus name
    num_note_column = 6
    for key_Name,value_Name in busName.items():

        Note_bus_No_Para_Bus = {'bg':None, 'fg':'black'}
        BusStructNote_bus_No = {'row':current_row+4,'columnspan':1, 'sticky':N+E+S+W, 'rowspan':1, 'column':num_note_column}
        win.AddLabel('Bus No.'+ str(key_Name) , Note_bus_No_Para_Bus, BusStructNote_bus_No)

        Note_bus_No_Para_Bus = {'bg':None, 'fg':'black'}
        BusStructNote_bus_No = {'row':current_row+5,'columnspan':1, 'sticky':N+E+S+W, 'rowspan':1, 'column':num_note_column}
        win.AddLabel(value_Name , Note_bus_No_Para_Bus, BusStructNote_bus_No)

        num_note_column = num_note_column +1

    #If busbars are connected with only breakers and the breaker is conducting, 
    #means those nodes are duplicated
    note_dup = ''
    for key_dup, value_dup in duplicate_busbar.items():
        note_dup = note_dup + '\nDuplicate Bus Group' + str(key_dup) + ' :  '
        for item in value_dup:
            note_dup = note_dup + item + ' ,  '

    Note_bus_dup_Para_Bus = {'bg':None, 'fg':'black'}
    BusStructNote_bus_dup = {'row':current_row+6,'columnspan':5, 'sticky':W, 'rowspan':1, 'column':6}
    win.AddLabel(note_dup , Note_bus_dup_Para_Bus, BusStructNote_bus_dup)

    win.root.update()




#Initialize the GUI window frame
win = MyWindow()


Lab_Para_Title = {'bg':'grey', 'fg':'black'}
TitleStructLab = {'row':0,'columnspan':4, 'sticky':N+E+S+W , 'rowspan':1, 'column':0}
win.AddLabel('Computer Application in Power Systems\n Assignment 1' , Lab_Para_Title, TitleStructLab  )


Lab_Para_Log = {'bg':'brown', 'fg':'white'}
LogStructLab = {'row':1,'columnspan':4, 'sticky':N+E+S+W , 'rowspan':1, 'column':0}
win.AddLabel('Please Log In First' , Lab_Para_Log, LogStructLab )


Lab_Para_host = {'bg':None, 'fg':'black'}
hostStructLab = {'row':2,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('host' , Lab_Para_host, hostStructLab)


global var_host
var_host=StringVar()
var_host.set('localhost')

Entr_Para_host = {'off':400,'on':300, 'show':None}
hostStructEntr = {'row':2, 'column':1,'sticky':W}
win.AddEntry(var_host , Entr_Para_host , hostStructEntr)


Lab_Para_User = {'bg':None, 'fg':'black'}
UserStructLab = {'row':3,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('User' , Lab_Para_User, UserStructLab)


global var_user
var_user=StringVar()
var_user.set('root')

Entr_Para_User = {'off':400,'on':300, 'show':None}
UserStructEntr = {'row':3, 'column':1,'sticky':W}
win.AddEntry(var_user, Entr_Para_User , UserStructEntr)



Lab_Para_Passwd = {'bg':None, 'fg':'black'}
PasswdStructLab = {'row':4,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Password' , Lab_Para_Passwd, PasswdStructLab)


global var_passwd
var_passwd=StringVar()
var_passwd.set('1993')

Entr_Para_Passwd = {'off':400,'on':300, 'show':'*'}
PasswdStructEntr = {'row':4, 'column':1,'sticky':W}
win.AddEntry(var_passwd, Entr_Para_Passwd , PasswdStructEntr)



Lab_Para_dbName = {'bg':None, 'fg':'black'}
dbNameStructLab = {'row':5,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Database Name' , Lab_Para_dbName, dbNameStructLab)


global var_dbName
var_dbName=StringVar()
var_dbName.set('Input Database Name here')

Entr_Para_dbName = {'off':400,'on':300, 'show':None}
dbNameStructEntr = {'row':5, 'column':1,'sticky':W}
win.AddEntry(var_dbName, Entr_Para_dbName , dbNameStructEntr)



Lab_Para_Port = {'bg':None, 'fg':'black'}
PortStructLab = {'row':6,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Port' , Lab_Para_Port, PortStructLab)


global var_port
var_port=StringVar()
var_port.set(3306)

Entr_Para_Port = {'off':400,'on':300, 'show':None}
PortStructEntr = {'row':6, 'column':1,'sticky':W}
win.AddEntry(var_port, Entr_Para_Port , PortStructEntr)



LogStructImag = {'row':2,'rowspan':4,'columnspan':2, 'column':2,'sticky':W+E+N+S, 'padx':5, 'pady':5}
file_name = 'pic2.gif'
win.AddImage('pic2.gif', LogStructImag)


LogStructButt = {'row':7,'column':2,'padx':4,'pady':1}
win.AddButton('Log In', LoginButtonFunc, LogStructButt)


ExitStructButt = {'row':7,'column':3,'padx':4,'pady':1}
win.AddButton('Exit', ExitButtonFunc, ExitStructButt)



global var_Log
var_Log=StringVar()
var_Log.set('Waiting For Operation')


Stat_Para_Log = {'bd':1,'anchor':W, 'fg':'black'}
LogStructStatus = {'row':8, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}

win.AddStatus(Stat_Para_Log, LogStructStatus, var_Log.get())



Lab_Para_FileName = {'bg':'brown', 'fg':'white'}
FileNameStructLab = {'row':9,'columnspan':4, 'sticky':N+E+S+W, 'rowspan':1, 'column':0}
win.AddLabel('Input the file name here' , Lab_Para_FileName, FileNameStructLab)



Lab_Para_EQName = {'bg':None, 'fg':'black'}
EQNameStructLab = {'row':10,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('EQ File Name' , Lab_Para_EQName, EQNameStructLab)

global var_EQName
var_EQName=StringVar()
var_EQName.set('Please input EQ file name here')

Entr_Para_EQName = {'off':400,'on':300, 'show':None}
EQNameStructEntr = {'row':10, 'column':1,'sticky':W}
win.AddEntry(var_EQName, Entr_Para_EQName , EQNameStructEntr)


Lab_Para_SSHName = {'bg':None, 'fg':'black'}
SSHNameStructLab = {'row':11,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('SSH File Name' , Lab_Para_SSHName, SSHNameStructLab)


global var_SSHName
var_SSHName=StringVar()
var_SSHName.set('Please input SSH file name here')

Entr_Para_SSHName = {'off':400,'on':300, 'show':None}
SSHNameStructEntr = {'row':11, 'column':1,'sticky':W}
win.AddEntry(var_SSHName, Entr_Para_SSHName , SSHNameStructEntr )



ConfirmStructButt = {'row':12,'column':2,'padx':4,'pady':1}
win.AddButton('Confirm', ConfirmButtonFunc, ConfirmStructButt)

Exit2StructButt = {'row':12,'column':3,'padx':4,'pady':1}
win.AddButton('Exit', ExitButtonFunc, Exit2StructButt)


global var_EQCheck
var_EQCheck=StringVar()

Stat_Para_EQCheck = {'bd':1,'anchor':W, 'fg':'black'}
EQCheckStructStatus = {'row':13, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
win.AddStatus(Stat_Para_EQCheck, EQCheckStructStatus, var_EQCheck.get())


global var_SSHCheck
var_SSHCheck=StringVar()

Stat_Para_SSHCheck = {'bd':1,'anchor':W, 'fg':'black'}
SSHCheckStructStatus = {'row':14, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
win.AddStatus(Stat_Para_SSHCheck, SSHCheckStructStatus, var_SSHCheck.get())


global var_TabCheck
var_TabCheck=StringVar()

Stat_Para_TabCheck = {'bd':1,'anchor':W, 'fg':'black'}
TabCheckStructStatus = {'row':15, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
win.AddStatus(Stat_Para_TabCheck, TabCheckStructStatus, var_TabCheck.get())


global var_WriteStatus
var_WriteStatus=StringVar()

Stat_Para_Write = {'bd':1,'anchor':W, 'fg':'black'}
WriteStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
win.AddStatus(Stat_Para_Write, WriteStructStatus, var_WriteStatus.get())


global var_TotStatus
var_TotStatus=StringVar()

Stat_Para_Tot = {'bd':1,'anchor':W, 'fg':'black'}
TotStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
win.AddStatus(Stat_Para_Tot, TotStructStatus, var_TotStatus.get())

Lab_Para_Separate = {'bg':None, 'fg':None}
SeparateStructLab = {'row':0,'columnspan':1, 'sticky':E, 'rowspan':17, 'column':4}
win.AddLabel(None, Lab_Para_Separate, SeparateStructLab)

BusStructButt = {'row':11,'column':9,'padx':0,'pady':1}
win.AddButton('Show', BusButtonFunc, BusStructButt)


Lab_Para_Bus_Title = {'bg':'grey60', 'fg':'black'}
BusStructLabTitle = {'row':0,'columnspan':5, 'sticky':N+E+S+W, 'rowspan':1, 'column':6}
win.AddLabel('Y-Bus Matrix' , Lab_Para_Bus_Title, BusStructLabTitle)


Label_Message = 'If this is the first time you run this program \nYou have to finish LEFT part first in order to see Y-Bus Matrix !\n\n If you have changed some value in SSH/EQ files,\nyou have to run the LEFT part again as well!'
Lab_Para_Bus = {'bg':'brown', 'fg':'white'}
BusStructLab = {'row':1,'columnspan':5, 'sticky':N+E+S+W, 'rowspan':10, 'column':6}
win.AddLabel(Label_Message , Lab_Para_Bus, BusStructLab)


global var_ConnectCheck
var_ConnectCheck=StringVar()

Stat_Para_ConnectCheck = {'bd':1,'anchor':W, 'fg':'black'}
ConnectCheckStructStatus = {'row':12, 'sticky':N+E+S+W, 'columnspan':5, 'column':6}
win.AddStatus(Stat_Para_ConnectCheck, ConnectCheckStructStatus, var_ConnectCheck.get())


win.root.mainloop()