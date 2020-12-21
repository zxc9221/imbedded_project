import pygame
import random
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera

ForwardPin = 12
ReversePin = 13
EnablePin = 19

SensorPin = 20
servoPin = 21
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

pygame.init()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SensorPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(servoPin, GPIO.OUT)

GPIO.setup(ForwardPin, GPIO.OUT)
GPIO.setup(ReversePin, GPIO.OUT)
GPIO.setup(EnablePin, GPIO.OUT)

GPIO.output(EnablePin, GPIO.HIGH)
GPIO.output(ForwardPin, GPIO.LOW)
GPIO.output(ReversePin, GPIO.LOW)

servo = GPIO.PWM(servoPin, 50)
servo.start(0)
camera = PiCamera()

return_falg = False
servo_flag = True
run = False

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class passward_box():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
           
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),2)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


class Intruder(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load("intruder.jpg").convert_alpha()

    def draw(self):
        win.blit(self.image, (self.x, self.y))

passward_size = ""

num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

sampleNumber = random.sample(num, 10)
Button0 = button((0,255,0), 20, 90, 120, 100,str(sampleNumber[0]))
Button1 = button((0,255,0), 180, 90, 120, 100,str(sampleNumber[1]))
Button2 = button((0,255,0), 340, 90, 120, 100,str(sampleNumber[2]))
Button3 = button((0,255,0), 20, 210, 120, 100,str(sampleNumber[3]))
Button4 = button((0,255,0), 180, 210, 120, 100,str(sampleNumber[4]))
Button5 = button((0,255,0), 340, 210, 120, 100,str(sampleNumber[5]))
Button6 = button((0,255,0), 20, 330, 120, 100,str(sampleNumber[6]))
Button7 = button((0,255,0), 180, 330, 120, 100,str(sampleNumber[7]))
Button8 = button((0,255,0), 340, 330, 120, 100,str(sampleNumber[8]))
Button9 = button((0,255,0), 180, 450, 120, 100,str(sampleNumber[9]))

Buttonst = button((0,255,0), 20, 450, 120, 100, '*')
Buttonsh = button((0,255,0), 340, 450, 120, 100, '#')

Passward_box = passward_box((0,0,0), 20, 20, 440, 50, str(passward_size))            


def callback(channel):
    global return_flag
    global run
    global servo_flag
    
    if GPIO.input(SensorPin):
        print("20 Rising")
        run = True
        lock_screen()    
    else:
        print("20 Falling")
        run = False
        servo_flag = True
        return_flag = True
        win.fill((0,0,0))
        pygame.display.update()
        
 


#GPIO.add_event_detect(SensorPin, GPIO.BOTH, callback=callback)

def setServoPos(deg):
    if deg > 180:
        deg = 180
    elif deg < 0:
        deg = 0

    duty = SERVO_MIN_DUTY + (deg * (SERVO_MAX_DUTY - SERVO_MIN_DUTY)/180.0)

    print("Degree: {} to {}".format(deg, duty))

    servo.ChangeDutyCycle(duty)


f = open("./password.txt", 'r')
password = ""
chackpassword = f.readline()
f.close()


win = pygame.display.set_mode((480,640))
win.fill((255,255,255))

Buttonlock = button((0,255,0), 40, 20, 400, 180,'Lock')
Buttonphoto = button((0,255,0), 40, 230, 400, 180,'check')
Buttonrepassword = button((0,255,0), 40, 440, 400, 180,'Fix Password')

def lock():
    setServoPos(120)
    sleep(0.5)
    GPIO.output(ForwardPin,GPIO.HIGH)
    GPIO.output(ReversePin,GPIO.LOW)
    sleep(1)
    GPIO.output(ForwardPin,GPIO.LOW)
    servo.start(0)

def Fix_password():
    global chackpassword 
    password = ""
    
    lock_screen()

    while 1: 
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button0.isOver(pos):
                    password += str(sampleNumber[0])
                    refrash_screen()
                elif Button1.isOver(pos):
                    password += str(sampleNumber[1])
                    refrash_screen()
                elif Button2.isOver(pos):
                    password += str(sampleNumber[2])
                    refrash_screen()
                elif Button3.isOver(pos):
                    password += str(sampleNumber[3])
                    refrash_screen()
                elif Button4.isOver(pos):
                    password += str(sampleNumber[4])
                    refrash_screen()
                elif Button5.isOver(pos):
                    password += str(sampleNumber[5])
                    refrash_screen()
                elif Button6.isOver(pos):
                    password += str(sampleNumber[6])
                    refrash_screen()
                elif Button7.isOver(pos):
                    password += str(sampleNumber[7])
                    refrash_screen()
                elif Button8.isOver(pos):
                    password += str(sampleNumber[8])
                    refrash_screen()
                elif Button9.isOver(pos):
                    password += str(sampleNumber[9])
                    refrash_screen()
                elif Buttonst.isOver(pos):
                    password = ""
                    lock_screen()
                elif Buttonsh.isOver(pos):
                    f = open("password.txt", "wt")
                    f.seek(0)
                    f.write(str(password))
                    chackpassword = password


                    return
                
def chack_intruder():
    intruder = Intruder()
    win.fill((255, 255, 255))
    intruder.draw()

    pygame.display.update()


def unlock_screen():
    global return_flag
    win.fill((255,255,255))
    Buttonlock.draw(win)
    Buttonphoto.draw(win)
    Buttonrepassword.draw(win)
    pygame.display.update()
    return_flag = False
    while 1: 
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return_flag = True
                if Buttonlock.isOver(pos):
                    lock()
                    win.fill((0,0,0))
                    pygame.display.update()
        
                elif Buttonphoto.isOver(pos):
                    chack_intruder()
                elif Buttonrepassword.isOver(pos):
                    Fix_password()
                    lock()
                    lock_screen()
        if return_flag == True:
            return

def refrash_screen():
    global passward_size
   
    passward_size +='*'
    Passward_box = passward_box((0,0,0), 20, 20, 440, 50,str(passward_size))

    win.fill((255,255,255))

    Button0.draw(win)
    Button1.draw(win)
    Button2.draw(win)
    Button3.draw(win)
    Button4.draw(win)
    Button5.draw(win)
    Button6.draw(win)
    Button7.draw(win)
    Button8.draw(win)
    Button9.draw(win)
    Buttonst.draw(win)
    Buttonsh.draw(win)
    Passward_box.draw(win)
    pygame.display.update()


def lock_screen():
    global Button0
    global Button1
    global Button2
    global Button3
    global Button4
    global Button5
    global Button6
    global Button7
    global Button8
    global Button9
    global Passward_box
    global passward_size
    global sampleNumber

    passward_size = ""
    
    sampleNumber = random.sample(num, 10)
    Button0 = button((0,255,0), 20, 90, 120, 100,str(sampleNumber[0]))
    Button1 = button((0,255,0), 180, 90, 120, 100,str(sampleNumber[1]))
    Button2 = button((0,255,0), 340, 90, 120, 100,str(sampleNumber[2]))
    Button3 = button((0,255,0), 20, 210, 120, 100,str(sampleNumber[3]))
    Button4 = button((0,255,0), 180, 210, 120, 100,str(sampleNumber[4]))
    Button5 = button((0,255,0), 340, 210, 120, 100,str(sampleNumber[5]))
    Button6 = button((0,255,0), 20, 330, 120, 100,str(sampleNumber[6]))
    Button7 = button((0,255,0), 180, 330, 120, 100,str(sampleNumber[7]))
    Button8 = button((0,255,0), 340, 330, 120, 100,str(sampleNumber[8]))
    Button9 = button((0,255,0), 180, 450, 120, 100,str(sampleNumber[9]))

    Passward_box = passward_box((0,0,0), 20, 20, 440, 50, str(passward_size))

    win.fill((255,255,255))

    Button0.draw(win)
    Button1.draw(win)
    Button2.draw(win)
    Button3.draw(win)
    Button4.draw(win)
    Button5.draw(win)
    Button6.draw(win)
    Button7.draw(win)
    Button8.draw(win)
    Button9.draw(win)
    Buttonst.draw(win)
    Buttonsh.draw(win)
    Passward_box.draw(win)
    pygame.display.update()

run = True
lock_screen()
while 1:
    
    if run == True:
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button0.isOver(pos):
                    password += str(sampleNumber[0])
                    refrash_screen()
                elif Button1.isOver(pos):
                    password += str(sampleNumber[1])
                    refrash_screen()
                elif Button2.isOver(pos):
                    password += str(sampleNumber[2])
                    refrash_screen()
                elif Button3.isOver(pos):
                    password += str(sampleNumber[3])
                    refrash_screen()
                elif Button4.isOver(pos):
                    password += str(sampleNumber[4])
                    refrash_screen()
                elif Button5.isOver(pos):
                    password += str(sampleNumber[5])
                    refrash_screen()
                elif Button6.isOver(pos):
                    password += str(sampleNumber[6])
                    refrash_screen()
                elif Button7.isOver(pos):
                    password += str(sampleNumber[7])
                    refrash_screen()
                elif Button8.isOver(pos):
                    password += str(sampleNumber[8])
                    refrash_screen()
                elif Button9.isOver(pos):
                    password += str(sampleNumber[9])
                    refrash_screen()
                elif Buttonst.isOver(pos):
                    password = ""
                    lock_screen()
                elif Buttonsh.isOver(pos):
                    print(password)
                    print(chackpassword)
                    
                    if password == "":
                        print("false")
                    elif int(password) == int(chackpassword):
                        print("true")
                        password = ""
                        GPIO.output(ForwardPin,GPIO.LOW)
                        GPIO.output(ReversePin,GPIO.HIGH)
                        sleep(3)
                        GPIO.output(ReversePin,GPIO.LOW)
                        setServoPos(0)
                        unlock_screen()
                        sleep(0.5)
                        servo.start(0)
                    else :
                        print("false")
                        camera.capture('./intruder.jpg')
                        password = ""
                        lock_screen()
    else:
        if servo_flag == True:
            lock()
            servo_flag = False
            password = ""

    
 











