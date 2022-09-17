from bs4 import BeautifulSoup
import requests
import os
import time
import threading 

access_token = '' #cannot be made public
timing = 3600 #interval of waiting time 
timeout_time = 6  #timeout  
start_hour =3 #start time 
end_hour =19 #end time

def get_https(port):

    url = f"http://219.86.140.31:{port}/cgi-bin/viewer/video.jpg?streamid=0"
    
    try:
        response = requests.get(url, headers={  
            'Authorization': 'Basic {}'.format(access_token) # using Authorization put header ,then get request
        },timeout =timeout_time ) 

        response.raise_for_status()  #status != 200 
        print(f"get {response.status_code}")

    except requests.exceptions.HTTPError:
        print("HTTP error ")
        response =get_https(port)
    
    except requests.exceptions.RequestException:
        print("request error")
        response =get_https(port)

    return response

def createTimer():

    t = threading.Timer(timing,save_image)
    t.start()

def save_image():

    createTimer() #execute new thread
    if(time.localtime().tm_hour>=start_hour and time.localtime().tm_hour<=end_hour): #save images ,when in time
        
        for i in range(3):

            port =8902+i
            response = get_https(port)

            if not os.path.exists("leaves images"):
                os.mkdir("leaves images")  # create folder
            if not os.path.exists(f"leaves images\\camera {port-8901}"):
                os.mkdir(f"leaves images\\camera {port-8901}")  # create camera folder

            current_date_and_time = time.strftime("%Y.%m.%d %H.%M.%S")
            with open(f"leaves images\\camera {port-8901}\\camera {port-8901} {current_date_and_time}.jpg","wb") as file: 
                file.write(response.content)  # save image 
    else :
        print(f"current time is out of {start_hour} - {end_hour}")

save_image()