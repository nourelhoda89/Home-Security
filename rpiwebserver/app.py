import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
import send_email
from flask import Flask, render_template,request,redirect

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define sensors GPIO's
button = 17
senPIR = 21
#actuators GPIO
light  = 4
#0=OFF 1=ON

buttonSts = GPIO.LOW
senPIRSts = GPIO.LOW
ledlightSts=GPIO.LOW

   
# Set button and PIR sensor pins as an input
GPIO.setup(button, GPIO.IN)   
GPIO.setup(senPIR, GPIO.IN)
GPIO.setup(light,GPIO.OUT) #light is output



@app.route("/", methods=['GET'])
def index():
   
               
    # Read Sensors Status
    buttonSts = GPIO.input(button)
    senPIRSts = GPIO.input(senPIR)
    ledlightSts=GPIO.input(light)
    
    
    
    if senPIRSts==0: #When output from motion sensor is LOW
        message="No intruders"
        GPIO.output(light, 0)  #Turn OFF LED
   
    elif senPIRSts==1 :
       
        #When output from motion sensor is HIGH
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        message="Intruder detected on "+ dt_string
        start_time=time.time()
        

        while True:
            
            buttonSts=GPIO.input(button)
            mode=request.args.get('mode')
            print("The mode now is", mode, start_time)
            #print(request.args);
                
            if mode=='1':
                print("changing button")
                buttonSts=False
                
            if  buttonSts==False :
                message="False Alarm! No Intruder"
                GPIO.output(light, False)#turn off
                break
            
            #if a min has passed without the safe button being pressed send an email 
            elif buttonSts==True  and (time.time()-start_time >60):
                message="One minute has passed owner alerted via Email"
                send_email.send()
                break
                
            else:
            
                GPIO.output(light,True)   #light on
                time.sleep(0.4)      #Time delay 

                GPIO.output(light,False)   #light off        
                time.sleep(0.4)                
                
    templateData = {
        'title'   : 'Security System!',
        'button'  : buttonSts,
        'senPIR'  : senPIRSts,
        'light'   : ledlightSts,
        'message'  :message
       
        }
    

    return render_template('index.html', **templateData)

@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
   
    return "nothing"
    
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)