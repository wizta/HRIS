#import file by tkinter
from tkinter import filedialog
from tkinter import *

root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "C:\\Users\marnitw\Desktop\examplefile",title = "Select file",filetypes = (("Text File","*.txt"),("all files","*.*")))
print (root.filename)

#start read and remove whitespace
with open(root.filename, 'r') as f:
   strip1 = f.readlines()
   strip1 = [line.replace('                  ', ' ')for line in strip1]

#strip whitespace round1
with open("1.txt",'w')as f:
   f.writelines(strip1)

with open("1.txt",'r')as f:
   strip2 = f.readlines()
   strip2 = [line.replace('    ', ' ')for line in strip2]

#strip whitespace round2
with open("2.txt",'w')as f:
   f.writelines(strip2)
   f.close()

with open("2.txt",'r')as f:
   strip3 = f.readlines()
   strip3 = [line.replace('      ', ' ')for line in strip3]

#strip whitespace round3
with open("3.txt",'w')as f:
   f.writelines(strip2)
   f.close()

with open("3.txt",'r')as f:
   strip4 = f.readlines()
   strip4 = [line.replace('     ', ' ')for line in strip3]

#open and write into final file
with open("4.txt",'w')as f:
   f.writelines(strip4)
   f.close()

#Replace C/In status
with open("4.txt",'r')as f:
   statusin = f.readlines()
   statusin = [line.replace("C/In   ", 'I ')for line in statusin]

with open("4.txt",'w')as f:
   f.writelines(statusin)
   f.close()

#Replace C/Out status
with open("4.txt",'r')as f:
   statusout = f.readlines()
   statusout = [line.replace("C/Out  ", 'O ')for line in statusout]

with open("5.txt",'w')as f:
   f.writelines(statusout)

#Replace Out Back status
with open("5.txt","r")as f:
   outback = f.readlines()
   outback = [line.replace("Out Back   ", 'O ')for line in outback]

with open("6.txt",'w')as f:
   f.writelines(outback)
   f.close()

#Replace OverTime Out status
with open("6.txt","r")as f:
   otout = f.readlines()
   otout  = [line.replace("OverTime Out ", 'O ')for line in otout ]

with open("7.txt",'w')as f:
   f.writelines(otout)
   f.close()

#Replace OverTime In status
with open("7.txt","r")as f:
   otin = f.readlines()
   otin = [line.replace("OverTime In ", 'I ')for line in otin ]

with open("8.txt",'w')as f:
   f.writelines(otin)
   f.close()

#Replace Out status
with open("8.txt","r")as f:
   outstate = f.readlines()
   outstate= [line.replace("Out   ", 'O ')for line in outstate ]

with open("9.txt",'w')as f:
   f.writelines(outstate)
   f.close()
#final alignment
with open("9.txt","r")as f:
   finalalign = f.readlines()
   finalalign = [line.replace("  ", ' ')for line in finalalign ]

with open("10.txt",'w')as f:
   f.writelines(finalalign)
   f.close()
"""
#Remove file after converted
"""
import os
os.remove("1.txt")
os.remove("2.txt")
os.remove("3.txt")
os.remove("4.txt")
os.remove("5.txt")
os.remove("6.txt")
os.remove("7.txt")
os.remove("8.txt")
os.remove("9.txt")
os.remove("10.txt")

#export to final file by tkinter
from tkinter import filedialog
from tkinter import *

root = Tk()
root.filename =  filedialog.asksaveasfilename(initialdir = "C:\\Users\marnitw\Desktop\examplefile\Converted",title = "Select file",filetypes = (("Text File","*.txt"),("all files","*.*")))
#write into final file
with open(root.filename,'w')as f:
    f.writelines(finalalign)
    f.close()


