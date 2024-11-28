import eel 
import requests
import io
from PIL import Image
import ctypes
import os
import time
import urllib.request
import customtkinter as ctk
from PIL import Image, ImageTk
from threading import Thread
import socket, errno
import sys
import webbrowser as wb
from win32com.shell import shell, shellcon
from win32com.client import Dispatch
from dotenv import load_dotenv
import subprocess

eel.init("iter3")

try:
    print("0" + str(sys.argv[0]))
    print("1:" + str(sys.argv[1]))
except IndexError:
    print("hola")


get_var=0
client_id =''
check_var=0

path_a = f"{os.path.dirname(os.path.abspath(__file__))}\\iter3"
path_b = f"{os.path.dirname(os.path.abspath(__file__))}/iter3/load"
path_c = f"{os.path.dirname(os.path.abspath(__file__))}\iter3\load\low"
path_d = f"{os.path.dirname(os.path.abspath(__file__))}\iter3\load\high"
path_e = f"{os.path.dirname(os.path.abspath(__file__))}\iter3\load\\aut"
path_f = f"{os.path.dirname(os.path.abspath(__file__))}\iter3\load\\aut_page"
path_g = f"{os.path.dirname(os.path.abspath(__file__))}\iter3\load\\img_res_link"

path_x_raw = f"{os.path.dirname(os.path.abspath(__file__))}"
path_x_processed = path_x_raw.split("\_internal", 1)
path_x = path_x_processed[0]
print(path_x)

def get_key():
    global get_var,client_id
    print(get_var)
    if get_var==0:
        load_dotenv()
        client_id = os.getenv('api_key')

@eel.expose
def env_get():
    try:
        with open(f"{path_x}/.env","r") as doc:
            doc.readline()
            doc.close()
    except FileNotFoundError:
        try:
            eel.status_ok(0)
        except AttributeError:
            print("adding wallpaper")

env_get()


@eel.expose
def saveEnv(key):
    save=open(f"{path_x}/.env","w")
    save.write(f"api_key='{key}'")
    save.close()
    envCheck(key,0,0)

def envCheck(key,n,m):
    global get_var,check_var
    url = f"https://api.unsplash.com/photos/random?query=small&orientation=landscape&content_filter=low&client_id={key}"
    try:
        urllib.request.urlopen("https://www.google.com")
        data_check = requests.get(url)
        if data_check.status_code == 401:
            print(data_check.status_code)
            get_var=0
            eel.status_ok(0)
            eel.invalid_key(0)
            if m == 1:
                check_var=1
        if data_check.status_code == 200:
            if m == 0:
                if n==0:
                    print("here")
                    eel.status_ok(1)
                    if check_var==1:
                        print("hi")
                        eel.resetDialog()
                        time.sleep(10)
                        eel.destroyer()
    except urllib.error.URLError:
        eel.invalid_key(1)


@eel.expose
def check_internet():
    try:
        urllib.request.urlopen("https://www.google.com")
        Img()
        eel.new_wall2()
    except urllib.error.URLError:
        eel.notify_internet()

def checkFolder():
    path_list = [path_a,
                path_b,
                path_c,
                path_d,
                path_e,
                path_f,
                path_g]

    for paths in path_list:
        if os.path.exists(paths):
            continue
        else:
            os.mkdir(paths)

checkFolder()



# Exposing the random_python function to javascript 
def Img():
    global get_var,client_id

    try:

        get_key()
        get_var=1

        print(client_id)

        envCheck(client_id,1,1)
        
        #get resolution
        res = res_get()


        #get sources
        query = query_get()

        #get filter
        content_filter = con_fil_get()

        print("res: "+res+"\nsource: "+query+"\nfilter: "+content_filter)

        #path setting for rearranging and rearranging
        rearrange(path_c,1)
        rearrange(path_d,1)
        rearrange(path_e,2)
        rearrange(path_f,3)
        rearrange(path_g,4)

        #url and data request
        url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&content_filter={content_filter}&client_id={client_id}"
        data = requests.get(url).json()
        img_author = (data["user"]["name"])#author name
        img_page = (data["user"]["links"]["html"])#author page
        img_url= data["urls"]#img urls
        img_data_low = requests.get(data["urls"]["regular"]).content
        img_low = Image.open(io.BytesIO(img_data_low))
        y_low = img_low.save(f"{path_c}/wall.png")#save low res image   
        img_data_high = requests.get(data["urls"][res]).content
        img_high = Image.open(io.BytesIO(img_data_high))
        y = img_high.save(f"{path_d}/wall.png")#save high res image 

        set_wallpaper(0,1)

        #saving authors name
        ptr = 1

        auth = open(f"{path_b}/author_temp.htm","r")
        content=(auth.readlines())
        auth.close() 

        print(content)

        auth = open(f"{path_e}/author.htm","a")
        for line in content:
            if ptr == 36:
                auth.writelines(f'<a href="{img_page}?utm_source=ShiftWall&utm_medium=referral" target="_blank"><h1>{img_author}</h1></a>\n')
            else:
                auth.writelines(line)
            ptr +=1

        auth.close()

        auth_page = open(f"{path_f}/author_page.txt","w")
        auth_page.writelines(f"{img_page}?utm_source=ShiftWall&utm_medium=referral")
        auth_page.close()

        #saving urls
        urls = open(f"{path_g}/img_resget.txt", "w")
        urls.writelines(f'{res}\n{img_url["raw"]}\n{img_url["full"]}')
        urls.close()
    
    except Exception as e:
        print(e)
        raise (ValueError)

def Red():
    eel.status_ok(0)
    eel.invalid_key(0)

@eel.expose
def get_high_res(n):
    for files in os.listdir(path_g):
        resfiles =  open(f"{path_g}/{files}","r")
        info=resfiles.readlines()
        resfiles.close()
        info_res=info[0]
        print(info_res)
        file = files.replace("img_resget","")
        file = file.replace(".txt","img")
        if info_res=="regular\n":
            if file=="img":
                info_link=info[n]
                high_res_data = requests.get(info_link).content
                high_res_img = Image.open(io.BytesIO(high_res_data))
                high_res_img.save(f"{path_d}/wall.png")#save high res image 


            else:
                file = file.replace("img","")
                info_link=info[n]
                high_res_data = requests.get(info_link).content
                high_res_img = Image.open(io.BytesIO(high_res_data))
                high_res_img.save(f"{path_d}/wall{file}.png")#save high res image 


            resfiles =  open(f"{path_g}/{files}","w")
            resfiles.write("full")
            resfiles.close()


@eel.expose	 
def Check():

    num =[]
    
    file=os.listdir(path_d)
    
    for i in  file:
        filt1 = i.replace("wall","")
        filt2 = filt1.replace(".png","")
        try:
           num.append(int(filt2))
        except ValueError:
            continue
        
    num.sort()

    try:
        i=(num[-1])
        if i == 9:
            i=9
            return i
        if i < 9:
            i = i+1
            return i
    except IndexError:
        i=0
        return i
    
def rearrange(path_ex,i):
    index=-1
    li=[]

    path = path_ex

    for file in os.listdir(path):
        li.append(file)
        index=index+1
    
    li.sort(reverse=True)

    if i ==1:

        if index == 10:
            index=index-1
            os.remove(f"{path}/wall{index}.png")
            li.clear()
            for file in os.listdir(path):
                li.append(file)
                li.sort(reverse=True)

        for element in li:
            os.rename(f"{path}/{element}",f"{path}/wall{index}.png")
            index=index-1
    if i == 2:
        if index == 10:
            index=index-1
            os.remove(f"{path}/author{index}.htm")
            li.clear()
            for file in os.listdir(path):
                li.append(file)
                li.sort(reverse=True)

        for element in li:
            os.rename(f"{path}/{element}",f"{path}/author{index}.htm")
            index=index-1
    
    if i == 3:
        if index == 10:
            index=index-1
            os.remove(f"{path}/author_page{index}.txt")
            li.clear()
            for file in os.listdir(path):
                li.append(file)
                li.sort(reverse=True)

        for element in li:
            os.rename(f"{path}/{element}",f"{path}/author_page{index}.txt")
            index=index-1
    
    if i == 4:
        if index == 10:
            index=index-1
            os.remove(f"{path}/img_resget{index}.txt")
            li.clear()
            for file in os.listdir(path):
                li.append(file)
                li.sort(reverse=True)

        for element in li:
            os.rename(f"{path}/{element}",f"{path}/img_resget{index}.txt")
            index=index-1

@eel.expose
def set_wallpaper(index,method):
    #wallpaper setting
    if method == 1:
        wallpaper_path = (f"{path_d}/wall.png")
    
    if method == 2:
        wall_list = []

        file=os.listdir(path_d)

        for files in file:
            wall_list.append(files)

        wall_list.sort() 

        wallpaper_path = (f"{path_d}/{wall_list[index]}")

        wall_list.clear()
    
    # 0: Center, 1: Stretch, 2: Tile, 6: Fit
    wallpaper_style = 0
    
    SPI_SETDESKWALLPAPER = 20
    image = ctypes.c_wchar_p(wallpaper_path)
    
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, wallpaper_style)


@eel.expose
def revoke_():
    path_list=[path_c,path_d,path_e,path_f]
    
    for path in path_list:
        for file in os.listdir(path):
            if file=="wall.png" or file=="author.htm" or file=="author_page.txt":
                continue
            else:
                os.system(f'del "{path}\{file}"')

@eel.expose
def resolution(res):
    res_list = ["raw" , "full","regular"]
    with open(f"{path_b}/res.txt","w") as doc:
        doc.writelines(res_list[res])
        doc.close()


@eel.expose
def sources(query):
    with open(f"{path_b}/source.txt","w") as doc:
        doc.writelines(query)
        doc.close()

@eel.expose
def con_filter(filter):
    filter_list = ["high","low"]
    with open(f"{path_b}/filter.txt","w") as doc:
        doc.writelines(filter_list[filter])
        doc.close()


@eel.expose
def res_get():
    try:
        with open(f"{path_b}/res.txt","r") as doc:
            res=doc.readline()
            doc.close()
            return res
    except FileNotFoundError:
        with open(f"{path_b}/res.txt","w") as doc:
            doc.writelines("full")
            res="full"
            doc.close()
            return res



@eel.expose
def query_get():
    try:
        with open(f"{path_b}/source.txt","r") as doc:
            query=doc.readline()
            doc.close()
            return query
    except FileNotFoundError:
        with open(f"{path_b}/source.txt","w") as doc:
            doc.writelines("featured")
            query="featured"
            doc.close()
            return query



@eel.expose
def con_fil_get():
    try:
        with open(f"{path_b}/filter.txt","r") as doc:
            content_filter=doc.readline()
            doc.close()
            return content_filter
    except FileNotFoundError:
        with open(f"{path_b}/filter.txt","w") as doc:
            doc.writelines("low")
            content_filter="low"
            doc.close()
            return content_filter
        
@eel.expose
def interval_get():
    try:
        with open(f"{path_b}/interval.txt","r") as doc:
            interval=doc.readline()
            doc.close()
            return interval
    except FileNotFoundError:
        with open(f"{path_b}/interval.txt","w") as doc:
            doc.writelines("never")
            interval="never"
            doc.close()
            return interval

@eel.expose
def interval_Secget():
    try: 
        with open(f"{path_b}/interval_timing.txt","r") as doc:
            interval=doc.readline()
            doc.close()
            return interval
    except FileNotFoundError:
        with open(f"{path_b}/interval_timing.txt","w") as doc:
            doc.writelines("never")
            interval="never"
            doc.close()
            return interval


@eel.expose
def interval(interval):

    minute = 60
    hour = 3600
    week = (hour*24)*7

    interval_list = ["15 minute","30 minute","1 hour","3 hour","6 hour","12 hour","24 hour","48 hour","1 week","never"]

    interval_list_sec = [15*minute,30*minute,1*hour,3*hour,6*hour,12*hour,24*hour,48*hour,week,"never"]

    with open(f"{path_b}/interval_timing.txt","w") as doc:
        doc.writelines(str(interval_list_sec[interval]))
        doc.close()

    with open(f"{path_b}/interval.txt","w") as doc:
        doc.writelines(interval_list[interval])
        doc.close()

@eel.expose
def con_startup(val):

    start_list = ["never","on"]

    with open(f"{path_b}/start_list_val.txt","w") as doc:
        doc.writelines(str(val))
        doc.close()

    with open(f"{path_b}/start_list.txt","w") as doc:
        doc.writelines(start_list[val])
        doc.close()

@eel.expose
def con_startup_get():
    start_list = ["never","on"]
    try:
        with open(f"{path_b}/start_list.txt","r") as doc:
            start=doc.readline()
            doc.close()
    except FileNotFoundError:
        with open(f"{path_b}/start_list.txt","w") as doc:
            doc.writelines("never")
            start="never"
            doc.close()
    finally:
        print(start)
        if start==start_list[0]:
            get_startup(0,0)
        if start==start_list[1]:
            get_startup(0,1)
        return start

        

        

def check_internet_connection(inst):
    def else_internet():
        try:
            urllib.request.urlopen("https://www.google.com")
        except urllib.error.URLError:
            print("")

    if bool(inst):
        try:
            if sys.argv[1]=="launch":
                try:
                    urllib.request.urlopen("https://www.google.com")
                    start_load(0)
                    os._exit(0)
                except urllib.error.URLError:
                    trip = 0
                    connect = False
                    while True:
                        try:
                            urllib.request.urlopen("https://www.google.com")
                            connect = True
                        except urllib.error.URLError:
                            print("")
                        if connect:
                            break
                        if trip == 60:
                            break
                        time.sleep(10)
                        trip += 1
                    if connect:                        
                        start_load(0)
                    os._exit(0)
            else:
                else_internet()
        except IndexError:
            else_internet()
    else:
        else_internet()
        

def starting():
    try: 
        with open(f"{path_b}/start_list_val.txt","r") as doc:
            start=doc.readline()
            doc.close()
    except FileNotFoundError:
        with open(f"{path_b}/start_list_val.txt","w") as doc:
            doc.writelines("0")
            start="0"
            doc.close()
    check_internet_connection(int(start))


def start_load(operation):
    def center_window(window):
        window.update_idletasks()
        width = 600
        height = 400
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    def Img1():

        global get_var,client_id

        try:

            get_key()
            get_var=1

            progressbar.set(0.1)
            
            #get resolution
            res = res_get()

            #get sources
            query = query_get()

            #get filter
            content_filter = con_fil_get()

            
            progressbar.set(0.2)


            print("res: "+res+"\nsource: "+query+"\nfilter: "+content_filter)

        #path setting for rearranging and rearranging
            rearrange(path_c,1)
            rearrange(path_d,1)
            rearrange(path_e,2)

            
            progressbar.set(0.4)


            #url and data request
            url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&content_filter={content_filter}&client_id={client_id}"
            data = requests.get(url).json()
            img_author = (data["user"]["name"])#author name
            img_url= data["urls"]#img urls
            
            
            progressbar.set(0.6)
            
            
            img_data_low = requests.get(data["urls"]["regular"]).content
            img_low = Image.open(io.BytesIO(img_data_low))
            y_low = img_low.save(f"{path_c}/wall.png")#save low res image   
            img_data_high = requests.get(data["urls"][res]).content
            img_high = Image.open(io.BytesIO(img_data_high))
            y = img_high.save(f"{path_d}/wall.png")#save high res image 
            
            
            progressbar.set(0.8)
            
            
            set_wallpaper(0,1)

            #saving authors name
            ptr = 1

            auth = open(f"{path_b}/author_temp.htm","r")
            content=(auth.readlines())
            auth.close() 

            print(content)
            

            progressbar.set(0.9)


            auth = open(f"{path_e}/author.htm","a")
            for line in content:
                if ptr == 32:
                    auth.writelines(f"<h1>{img_author}</h1>\n")
                else:
                    auth.writelines(line)
                ptr +=1

            auth.close()

            #saving urls
            urls = open(f"{path_g}/img_resget.txt", "w")
            urls.writelines(f'{res}\n{img_url["raw"]}\n{img_url["full"]}')
            urls.close()

            progressbar.set(1)

            root.destroy()

        except Exception as e:
            label_center.configure(text = "Error While Adding Wallpaper..")
            destroyer()

    
    def destroyer():
        time.sleep(5)
        root.destroy()


    # Example usage:
    root = ctk.CTk()
    root.title("Centered Window")
    root.overrideredirect(True)
    center_window(root)
    font1=ctk.CTkFont(family='Verdana', size=18)
    if operation==0:
        progressbar = ctk.CTkProgressBar(root,orientation="horizontal")
        progressbar.place(relx=0.5, rely=0.4, anchor='c')
        label_center = ctk.CTkLabel(root, text="Adding Wallpaper....",font=font1,justify="center")
        label_center.place(relx=0.5, rely=0.5, anchor='c')
        label_center1 = ctk.CTkLabel(root, text="You Can DISABLE This In SETTINGS.",font=font1, justify="center")
        label_center1.place(relx=0.5, rely=0.6, anchor='c')
        Thread(target=Img1).start()
    if operation==1:
        label_center = ctk.CTkLabel(root, text="SHIFTWALL is already running..",font=font1,justify="center")
        label_center.place(relx=0.5, rely=0.5, anchor='c')
        Thread(target=destroyer).start()
    root.mainloop()


@eel.expose
def get_startup(common,condition):
    start_folder = shell.SHGetFolderPath(0, (shellcon.CSIDL_STARTUP, shellcon.CSIDL_COMMON_STARTUP)[common], None, 0)
    if bool(condition):
       
        path = (fr"{start_folder}\ShiftWall.lnk")  #This is where the shortcut will be created
        target = (fr"{path_x}\ShiftWall.exe")  # directory to which the shortcut is created

        shelll = Dispatch('WScript.Shell')
        shortcut = shelll.CreateShortCut(path)
        shortcut.Targetpath = f"{target}"
        shortcut.Arguments = 'launch'
        shortcut.Workingdirectory = f"{path_x}"
        shortcut.save()
    else:
        try:
            os.remove(f"{start_folder}\ShiftWall.lnk")
        except FileNotFoundError :
            print()

#get_startup(0) 'C:\\Users\\<USERNAME>\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
#get_startup(1)  'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'

starting()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", 8000))
        launch = True
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            start_load(1)
            os._exit(0)
        else:
            # something else raised the socket.error exception
            print(e)
    s.close()
    if launch:
        eel.start("main.html")