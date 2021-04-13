import time
import random
import urllib
import feedparser
import json
import csv
import config
import os, sys, traceback
import email
import imaplib
import anki_vector
from anki_vector.events import Events
from anki_vector.faces import Face
from anki_vector.util import degrees, distance_mm, speed_mmps
from anki_vector import audio
from anki_vector.connection import ControlPriorityLevel
from anki_vector.user_intent import UserIntent, UserIntentEvent
from anki_vector.objects import CustomObjectMarkers, CustomObjectTypes


# get the path of the local files
pyPath = os.path.realpath(__file__)
pyPath1 = os.path.dirname(pyPath)
jokesPath = os.path.join(pyPath1, "jokes.txt")
factsPath = os.path.join(pyPath1, "facts.txt")

# Load the jokes into a list called 'jokes'. Try local, then download. Need to figure out a better way to do do this... 
try:
    with open(jokesPath, 'r') as f:
        jokes = [line.rstrip('\n') for line in f]
except:
    print("Downloading jokes from Website...")
    jokes = []
    content=urllib.request.urlopen("http://www.cuttergames.com/vector/jokes.txt") 
    
    for line in content:
        line = line.decode("utf-8")
        jokes.append(line.rstrip('\n'))

# Load the facts into a list called 'facts'. Try local, then download. Need to figure out a better way to do do this... 
try:
    with open(factsPath, 'r') as f:
        facts = [line.rstrip('\n') for line in f]
except:
    print("Downloading facts from Website...")
    facts = []
    content=urllib.request.urlopen("http://www.cuttergames.com/vector/facts.txt") 
    
    for line in content:
        line = line.decode("utf-8")
        facts.append(line.rstrip('\n'))


###############################################################################
def average(number1, number2):
    return (number1 + number2) / 2

###############################################################################
def get_weather(robot):
    
    try:
        #location can be city, state; city, country; zip code.
        url = f"http://api.openweathermap.org/data/2.5/forecast?APPID={config.api_weather}&q={config.weather_location}&units={config.temperature}"
        req = urllib.request.Request(
            url,
            data=None,
            headers={}
        )
        data = urllib.request.urlopen(req).read()
        output = json.loads(data)

        section =output["list"][0]
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

        weather = []
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
def get_news(robot):

    say_count = 0
    intro = "Here comes the news. "
    bridge = [". And in other news. ", ". In OTHER news... ", ". Taking a look at other news. ", ". Here is another news item. ", ". Here is an interesting story. "]
    news = ""
    news_count = config.news_count
    feed = feedparser.parse(config.news_feed)
    
    listeTitle = []
    for post in feed.entries:
        listeTitle.append(post.title)
       
    while say_count < news_count:
        news = news + listeTitle[say_count] + random.choice(bridge)
        say_count = say_count+1
        news = news + listeTitle[say_count+1]
    
    to_say = intro + news
    say_text(robot, to_say)

###############################################################################
def get_fact(robot):

    intro = "I have an interesting fact for you. "
    num = len(facts)
    my_rand = random.randint(0,num-1)
    raw_fact = facts[my_rand]
    outro = " interesting, right?"
    to_say = intro + raw_fact + outro
    say_text(robot, to_say)

###############################################################################
def get_joke(robot):

    intro = []
    intro.append("Do you already know this one? ")
    intro.append("I will tell you a joke. ")
    intro.append("Coz-mo told me a funny joke. ")
    intro.append("I know a funny joke. ")
    rnd_intro = random.choice(intro)
    
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

    outro = []
    outro.append(" wasn't that funny?")
    outro.append(" hiie hiie hiie")
    outro.append(" that was funny!")
    outro.append(" funny...")
    rnd_outro = random.choice(outro)
    say_text(robot, rnd_outro)


###############################################################################
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
def get_greeting(robot):

    text = []
    text.append("Hey, what's up?")
    text.append("Hey, how are you?")
    text.append("Oooh, my favorite human!")
    text.append("Hi, nice to see you.")
    
    to_say = random.choice(text)
    say_text(robot, to_say)

###############################################################################
# Check for new E-Mails
def get_email(robot):
    
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
def wake_up(robot):

    text = []
    text.append("I have enough energy to play now.")
    text.append("Now I'm fully charged.")
    text.append("My Battery is fully charged now.")
    text.append("I had a good recharging nap.")
    
    to_say = random.choice(text)
    say_text(robot, to_say)

    # Drive off the charger
    robot.behavior.drive_off_charger()

###############################################################################
def say_text(robot, to_say):

    # Slow voice down slightly to make him easier to understand
    robot.behavior.say_text(to_say, duration_scalar=1.15) 

###############################################################################
def run_behavior(robot, arg_name):

    if arg_name == "pass"     : return
    if arg_name == "greeting" : get_greeting(robot)
    if arg_name == "time"     : get_time(robot) 
    if arg_name == "joke"     : get_joke(robot)
    if arg_name == "fact"     : get_fact(robot)
    if arg_name == "news"     : get_news(robot)
    if arg_name == "weather"  : get_weather(robot)

###############################################################################
# MAIN
def main():

    with anki_vector.Robot(enable_face_detection=True) as robot:
       
        # check e-mail
        get_email(robot)
        
        #run_behavior(robot, "news")
        #return


        # only if Vector sees a face
        last_face = ""
        seen_faces = robot.world.visible_faces
        for face in seen_faces:
            last_face = face.face_id
            
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
        run_behavior(robot, rnd_reaction)


###############################################################################
if __name__ == "__main__":
    main()
