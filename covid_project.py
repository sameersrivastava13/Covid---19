#import all the necessary libraries

import bs4
import requests
import tkinter as tk
import plyer
import time
from time import strftime
import datetime
import threading

def get_html_data(url):
    data=requests.get(url)
    return data

def get_corona_detail_india():
    url="https://www.mohfw.gov.in/"
    html_data=get_html_data(url)
    bs=bs4.BeautifulSoup(html_data.text,'html.parser')
    li=('blue','green','red','orange')
    li2=('Active Cases','Cured / Discharged','Deaths','Migrated')
    all_details=""
    for i in range(4):
        info=bs.find("div",class_="site-stats-count").find_all("li",class_="bg-"+str(li[i]))
        for j in info:
            data=j.find("strong").get_text()
            all_details+=li2[i]+" : "+data+"\n"

    return(all_details)

def main():
    get_corona_detail_india()

if __name__=="__main__":
    main()

def refresh():
    new_data=get_corona_detail_india()
    print("Refreshing...")
    main_label['text']=new_data

#notification
def notify_user():
    while True:
        plyer.notification.notify(
            title='Covid - 19 cases of INDIA ',
            message=get_corona_detail_india(),
            timeout=10,
            #app_icon='icon.png'
        )
        time.sleep(20)

#creating GUI for our project

root=tk.Tk()
root.geometry("550x500")
root.iconbitmap("coronavirus.png")
root.title("COVID - 19 Live Data Tracker for India")

l0=tk.Label(root,text="",bg="olive drab")
l0.pack()

root.configure(bg='olive drab')
f=("Franklin Gothic Heavy",25,"bold")

banner=tk.PhotoImage(file="icon.png")
banner_label=tk.Label(root,image=banner,bg="white",relief="solid")
banner_label.pack()

l1=tk.Label(root,text="",bg="olive drab")
l1.pack()

main_label=tk.Label(root,text=get_corona_detail_india(),font=f,bg="white",padx=20,relief="solid")
main_label.pack()

l2=tk.Label(root,text="",bg="olive drab")
l2.pack()

f1=("Franklin Gothic Heavy",15,"bold")
btn=tk.Button(root,text="REFRESH",font=f1,relief="solid",command=refresh)
btn.pack()

#create thread
t1=threading.Thread(target=notify_user)
t1.setDaemon(True)
t1.start()


root.mainloop()
