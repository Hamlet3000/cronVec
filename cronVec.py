import time
import datetime
import random
import urllib
import feedparser
import json
import config
import os
import email
import imaplib
import paho.mqtt.client as mqtt
import anki_vector
from anki_vector.faces import Face

LAST_NAME = ""

###############################################################################
# average --
#
# Arguments:
#
# Result:
#
def average(number1, number2):
    return (number1 + number2) / 2

###############################################################################
# get_weather --
#   gets the weather form openweathermap.org and let Vector say it
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_weather(robot):
   
    if config.api_weather == "":
        return
    if config.api_weather == "YOUR_WEATHER_API_KEY":
        return
       
    weather = []
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?APPID={config.api_weather}&q={config.weather_location}&units={config.temperature}"
        req = urllib.request.Request(
            url,
            data=None,
            headers={}
        )
        data = urllib.request.urlopen(req).read()
        output = json.loads(data)

        section = output["list"][0]
        forecast_condition = section["weather"][0]["description"]
        forecast_humidity = section["main"]["humidity"]
        forecast_temp = output["list"][0]["main"]["temp"]
        forecast_temp_high = int(round(section["main"]["temp_min"]))
        forecast_temp_low = int(round(section["main"]["temp_max"]))
        forecast_temp_avg = int(round(average(forecast_temp_high, forecast_temp_low)))
        forecast_wind = int(round(section["wind"]["speed"]))

        if config.temperature == "imperial":
            wind_speed = " miles per hour"
        else:
            wind_speed = " kilometers per hour"

        weather.append(f". And now for some weather. Today, it will be {forecast_condition}, with a temperature of {forecast_temp_high} degrees, and wind speeds around {forecast_wind}{wind_speed}.")
        weather.append(f". Later today, it will be {forecast_condition}, with a high of {forecast_temp_high} degrees and a low of {forecast_temp_low} degrees.")
        weather.append(f". Here's your local weather. The high today will be {forecast_temp_high} degrees, and look for a low of around {forecast_temp_low}. Winds will be {forecast_wind}{wind_speed}.")
        weather.append(f". Later today it will be {forecast_condition}, with an average temperature of {forecast_temp_avg} degrees, and wind speeds around {forecast_wind}{wind_speed}.")
        
    except Exception as inst:
        weather.append("I'm more of an indoor robot.")
        weather.append("I have no idea what it is like out there.")
        weather.append("I'm a robot, not a weather forecaster.")
        weather.append("I had trouble getting the weather for you.")

    to_say = random.choice(weather)
    say_text(robot, to_say)

###############################################################################
# get_weather --
#   gets the news form a rss feed from the config file and let Vector say it
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_news(robot):

    if config.news_feed == "":
        return
    if config.news_feed == "YOUR_NEWS_FEED":
        return

    say_count = 0
    intro = "Here comes the news. "
    bridge = [". And in other news. ", ". In OTHER news... ", ". Taking a look at other news. ", ". Here is another news item. "]
    news = ""
    news_count = config.news_count
    feed = feedparser.parse(config.news_feed)
    listeTitle = []
   
    for post in feed.entries:
        listeTitle.append(post.title)
       

    for i in range(news_count):
        if i == 0:
            news = listeTitle[i]
        else:
            news = news + random.choice(bridge) + listeTitle[i]

    to_say = intro + news
    say_text(robot, to_say)

###############################################################################
# load_file --
#   Load jokes or facts from file into a list called 'text"
#
# Arguments:
#   jf = jokes or facts
#
# Result:
#   text = list of jokes or facts
#
def load_file(jf):

    pyPath = os.path.realpath(__file__)
    pyPath1 = os.path.dirname(pyPath)

    if jf == "jokes":
        filePath = os.path.join(pyPath1, "jokes.txt")
    else:
        filePath = os.path.join(pyPath1, "facts.txt")

    # Load jokes or facts into a list called 'text"
    try:
        with open(filePath, 'r') as f:
            text = [line.rstrip('\n') for line in f]
    except:
        text = ["oh... I forgot what I want to say"]

    return text

###############################################################################
# get_fact --
#   lets Vecor tell a random fact
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_fact(robot):

    intro = "I have an interesting fact for you REPLACENAMEVAR. "

    facts = load_file("facts")

    num = len(facts)
    my_rand = random.randint(0,num-1)
    raw_fact = facts[my_rand]
    to_say = intro + raw_fact
    say_text(robot, to_say)

###############################################################################
# get_joke --
#   lets Vecor tell a random joke and giggle
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_joke(robot):

    intro = []
    intro.append("Do you already know this one REPLACENAMEVAR? ")
    intro.append("REPLACENAMEVAR I will tell you a joke. ")
    intro.append("Coz-mo told me a funny joke. ")
    intro.append("I know a funny joke. ")
    rnd_intro = random.choice(intro)
   
    jokes = load_file("jokes")

    num = len(jokes)
    my_rand = random.randint(0,num-1)
    raw_joke = jokes[my_rand]
    to_say = rnd_intro + raw_joke
    say_text(robot, to_say)

    # Play random giggle animation
    joke_anim = []
    anim_names = robot.anim.anim_list
    for anim_name in anim_names:
        if "giggle" in anim_name:
            joke_anim.append(anim_name)
    
    robot.anim.play_animation(random.choice(joke_anim))

###############################################################################
# get_time --
#   lets Vecor tell the current time
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_time(robot):

    intro = []
    intro.append("Right now it's ")
    intro.append("The time is ")
    intro.append("It's ")
    rnd_intro = random.choice(intro)
    
    raw_time = time.strftime("%I:%M %p")
    
    to_say = rnd_intro + raw_time
    say_text(robot, to_say)

###############################################################################
# get_greeting --
#   lets Vecor greet you
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_greeting(robot):

    text = []
    text.append("Hey REPLACENAMEVAR, what's up?")
    text.append("Hey REPLACENAMEVAR, how are you?")
    text.append("Oooh REPLACENAMEVAR, my favorite human!")
    text.append("Hi REPLACENAMEVAR, nice to see you.")
    
    to_say = random.choice(text)
    say_text(robot, to_say)

###############################################################################
# get_mail --
#   lets Vecor check your e-mails
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_email(robot):
   
    if config.mail_account == "":
        return
    if config.mail_account == "YOUR_E_MAIL":
        return

    mail_imap = config.mail_imap
    mail_account = config.mail_account
    mail_pw = config.mail_pw 

    mail = imaplib.IMAP4_SSL(mail_imap)
    mail.login(mail_account, mail_pw)

    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
    i = len(data[0].split())

    email_message = ""
    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

    # Header Details
    last_mail = ""
    if email_message != "":
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
            email_from = str(email_from.split("<")[0].strip())
            #subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
            last_mail = email_from

    if last_mail != "":
        intro = "You got mail from: "
        to_say = intro + last_mail
        say_text(robot, to_say)


###############################################################################
# get_mqtt_info --
#   gets battery info and state for publish for mqtt
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def get_mqtt_info(robot):

   battery_state = robot.get_battery_state()
   voltage  = battery_state.battery_volts
   docked   = battery_state.is_on_charger_platform
   ltime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")

   # In the openHAB channel, use a jsonpath transform to get specific values like this: JSONPATH:$..voltage
   data = {}
   data['robots'] = []
   data['robots'].append({
       'name': 'Vector',
       'voltage': voltage,
       'docked': docked,
       'time': ltime
   })
                  
   # Configure and publish data to mqtt
   do_mqtt(data)


###############################################################################
# get_vector_status --
#   returns what ever Vector ist doing right now
#
# Arguments:
#   robot = Vector object
#
# Result:
#   status = what Vector ist doing
#
def get_vector_status(robot):

   status = "error"
   if robot.status.are_motors_moving:
      status = "Vector is moving"
   if robot.status.are_wheels_moving:
      status = "Vector's wheels are moving"
   if robot.status.is_animating:
      status = "Vector is animating"
   if robot.status.is_being_held:
      status = "Vector is being held"
   if robot.status.is_button_pressed:
      status = "Vector's button was button pressed"
   if robot.status.is_carrying_block:
      status = "Vector is carrying his block"
   if robot.status.is_charging:
      status = "Vector is currently charging"
   if robot.status.is_cliff_detected:
      status = "Vector has detected a cliff"
   if robot.status.is_docking_to_marker:
      status = "Vector has found a marker and is docking to it"
   if robot.status.is_falling:
      status = "Vector is falling"
   if robot.status.is_head_in_pos:
      status = "Vector's head is in position"
   if robot.status.is_in_calm_power_mode:
      status = "Vector is in calm power mode"
   if robot.status.is_lift_in_pos:
      status = "Vector's arm is in position"
   if robot.status.is_on_charger:
      status = "Vector is on the charger"
   if robot.status.is_pathing:
      status = "Vector is traversing a path"
   if robot.status.is_picked_up:
      status = "Vector is picked up"
   if robot.status.is_robot_moving:
      status = "Vector is in motion"

   return status

###############################################################################
# on_publish --
#   when mqtt is publishing
#
# Arguments:
#   client
#   userdata
#   mid
#
# Result:
#
def on_publish(client, userdata, mid):
        print("Message published to broker")

###############################################################################
# do_mqtt --
#   configure everything for mqtt and publish
#
# Arguments:
#   data = data to publis
#
# Result:
#
def do_mqtt(data):
        
   name = data['robots'][0]['name']

   # define variables for MQTT
   MQTT_HOST = config.mqtt_broker_ip
   MQTT_TOPIC = name
   MQTT_PORT = 1883
   MQTT_KEEPALIVE_INTERVAL = 20
   MQTT_USER = config.mqtt_user
   MQTT_PW = config.mqtt_pw

   if MQTT_HOST == "":
       return
   if MQTT_HOST == "YOUR_MQTT_BROKER_IP":
       return

   # Convert it to text? Not sure why I did this but it works. Yay, 1am programming.
   MQTT_MSG = str(data)
   #print(MQTT_MSG)

   # Initiate MQTT Client
   mqttc = mqtt.Client()

   # Set username and password for the Broker
   #mqttc.username_pw_set(MQTT_USER, MQTT_PW)

   # Register publish callback function
   #mqttc.on_publish = on_publish

   # Connect with MQTT Broker
   mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

   # Publish message to MQTT Broker
   mqttc.publish(MQTT_TOPIC,MQTT_MSG)

   # Disconnect from MQTT_Broker
   mqttc.disconnect()


###############################################################################
# wake_up --
#   lets Vecor say a text and drive off his charger
#
# Arguments:
#   robot = Vector object
#
# Result:
#
def wake_up(robot):

    text = []
    text.append("I have enough energy to play now REPLACENAMEVAR.")
    text.append("Now I'm fully charged.")
    text.append("My Battery is fully charged now.")
    text.append("I had a good recharging nap.")
    text.append("Now I'm ready to play REPLACENAMEVAR.")
    
    to_say = random.choice(text)
    say_text(robot, to_say)

    # Drive off the charger
    robot.behavior.drive_off_charger()

###############################################################################
# say_text --
#   replaces some special characters, replace name if found, slow down Vectors
#   voice and let him say a text
#
# Arguments:
#   robot = Vector object
#   to_say = text that Vector should say
#
# Result:
#
def say_text(robot, to_say):
    global LAST_NAME

    # replace special characters
    to_say = to_say.replace("ä","ae").replace("Ä","Äe").replace("ö","oe").replace("Ö","oe").replace("ü","ue").replace("Ü","ue").replace("ß","ss")

    # TODO maybe remove some other unknown characters
#    listeSonderzeichen = ["ä", "ö", "ü", "ß"]
#    for sonderzeichen in listeSonderzeichen:
#       news = news.replace(sonderzeichen, " ")


#    print(">>>" + LAST_NAME + "<<<")

    # when person is recognized, say their name
    to_say = to_say.replace("REPLACENAMEVAR",LAST_NAME)

    # Slow voice down slightly to make him easier to understand
    robot.behavior.say_text(to_say, duration_scalar=1.15) 

###############################################################################
# run_behavior --
#   distinguishes between the different behaviors
#
# Arguments:
#   robot = Vector object
#   arg_name = could be: pass, greeting, time, joke, fact, news, weather
#
# Result:
#
def run_behavior(robot, arg_name):

    if arg_name == "pass"     : return
    if arg_name == "weather"  : get_weather(robot)
    if arg_name == "time"     : get_time(robot) 
    if arg_name == "fact"     : get_fact(robot)
    if arg_name == "joke"     : get_joke(robot)
    if arg_name == "news"     : get_news(robot)
    if arg_name == "greeting" : get_greeting(robot)


###############################################################################
# is_allowed --
#   checks if the action may be executed
#
# Arguments:
#   reaction = could be: greeting, time, joke, fact, news, weather
#
# Result:
#
def is_allowed(reaction):

    timestamp = time.time()

    try:
        timedict = json.load(open("timestamps.txt"))
    except:
        timedict={"greeting" : 0,
                  "news" : 0,
                  "joke" : 0,
                  "fact" : 0,
                  "time" : 0,
                  "weather" : 0}

    timediff = timestamp - timedict[reaction]
    mintime = get_mintime(reaction)

    if timediff > mintime:
       timedict.update({reaction: timestamp})
       json.dump(timedict, open("timestamps.txt",'w'))
       return 1
    else:
       return 0

###############################################################################
# get_mintime --
#   the minimum time that must elapse to perform the same action again
#
# Arguments:
#   reaction = could be: greeting, time, joke, fact, news, weather
#
# Result:
#   time in seconds
#
def get_mintime(reaction):
    if reaction == "greeting":
        return 180 # 3 minutes
    elif reaction == "news":
        return 900 # 15 minutes
    elif reaction == "joke":
        return 300 # 5 minutes
    elif reaction == "fact":
        return 300 # 5 minutes
    elif reaction == "time":
        return 1800 # 30 minutes
    elif reaction == "weather":
        return 1800 # 30 minutes


###############################################################################
# main --
#   checks e-mail, when Vector sees a face do some random stuff
#
# Arguments:
#
# Result:
#
def main():
    global LAST_NAME

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial,
                           enable_face_detection=True,
                           cache_animation_lists=False) as robot:

        # check e-mail
        get_email(robot)

        # publish mqtt infos
        get_mqtt_info(robot)

        #run_behavior(robot, "news")
        #return
        
        # only if Vector sees a face
        last_face = ""
        seen_faces = robot.world.visible_faces
        for face in seen_faces:
            last_face = face.face_id
            LAST_NAME = face.name

        if last_face == "":
            return

        # if on charger
        if robot.status.is_on_charger:
            battery_state = robot.get_battery_state()
            # if fully charged
            if battery_state.battery_level == 3:
                # move from charger
                wake_up(robot)

        # do random stuff
        reaction = ["greeting", "news", "joke", "fact", "time", "weather"]
        rnd_reaction = random.choice(reaction)
        if is_allowed(rnd_reaction):
           run_behavior(robot, rnd_reaction)


###############################################################################
if __name__ == "__main__":
    main()
