# from flask import Flask, render_template
# import os
# import stat

# app = Flask(__name__)

# # Make the WSGI interface available at the top level so wfastcgi can get it.
# wsgi_app = app.wsgi_app

# FILE_SYSTEM_ROOT = "D:\Knight\static"

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/browser')
# def browse():
#     itemList = os.listdir(FILE_SYSTEM_ROOT)
#     return render_template('browse.html', itemList=itemList)

# @app.route('/browser/<path:urlFilePath>')
# def browser(urlFilePath):
#     nestedFilePath = os.path.join(FILE_SYSTEM_ROOT, urlFilePath)
#     if os.path.isdir(nestedFilePath):
#         itemList = os.listdir(nestedFilePath)
#         fileProperties = {"filepath": nestedFilePath}
#         if not urlFilePath.startswith("/"):
#             urlFilePath = "/" + urlFilePath
#         return render_template('browse.html', urlFilePath=urlFilePath, itemList=itemList)
#     if os.path.isfile(nestedFilePath):
#         fileProperties = {"filepath": nestedFilePath}
#         sbuf = os.fstat(os.open(nestedFilePath, os.O_RDONLY)) #Opening the file and getting metadata
#         fileProperties['type'] = stat.S_IFMT(sbuf.st_mode) 
#         fileProperties['mode'] = stat.S_IMODE(sbuf.st_mode) 
#         fileProperties['mtime'] = sbuf.st_mtime 
#         fileProperties['size'] = sbuf.st_size 

# import os

# def deletefile(path):
#     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#     global filename
#     file1 = "static/assets/" + path + "/" + filename
#     my_file = os.path.join(THIS_FOLDER, "static/assets/", path, filename)
#     os.remove(str(my_file))
#     return 'The File has been deleted successfully'

# filename = input("filename")
# path = input("path")
# print(deletefile(path))

# Python program to demonstrate 
# creating a new file 
  
  
# importing module 
# import os 
  
# # path of the current script 
# path = 'D:\Knight'
  
# # Before creating 
# dir_list = os.listdir(path)  
# print("List of directories and files before creation:") 
# print(dir_list) 
# print() 
  
# # Creates a new file 
# with open('myfile.txt', 'w') as fp: 
#     pass
#     # To write data to new file uncomment 
#     # this fp.write("New file created") 
  
# # After creating  
# dir_list = os.listdir(path) 
# print("List of directories and files after creation:") 
# print(dir_list) 

# myfile=open(r"myFile.txt","r")
# str=myfile.readline()       # why? And why not str=” “ as given above .   check for ur self
# l=0
# while str :
#      str=myfile.readline() 
#      l+=1
# print("lines",l)
# myfile.close()

import secrets
print(secrets.token_urlsafe(50))
input()

