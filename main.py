#  module that lets python talk to us
import pyttsx3
import speech_recognition as sr
#  allows us to open any kind of browser
import webbrowser
import datetime
# allows us to open youtube and more
import pywhatkit
#  finance actions
import yfinance as yf
import pyjokes
import wikipedia

name = "elad"


# listen to the microphone and return the audio as text using google
def transform():
    r = sr.Recognizer()  # recognize the speach
    with sr.Microphone() as source:
        r.pause_threshold = 0.8  # we wait as we listen
        said = r.listen(source)
        try:
            print('im listening')
            q = r.recognize_google(said, language="en")  # let google recognize the audio
            return q
        except sr.UnknownValueError:
            print('what ?')
            return "im waiting"
        except sr.RequestError:
            print('service is down')
            return "im waiting "
        except:
            return "im waiting"


# func to let the assistant speak back using pyttsx3
def speaking(massage):
    engine = pyttsx3.init()  # initialiize the engine
    engine.say(massage)
    engine.runAndWait()


# returns the weekday name
def query_day():
    day = datetime.date.today()
    # print(day)
    weekday = day.weekday()
    # print(weekday)
    mapping = {
        0: 'monday',
        1: 'Tuseday',
        2: 'wedensday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'sunday'
    }
    try:
        speaking(f'today is {mapping[weekday]}')
    except:
        pass


# returns the time
def query_time():
    time = datetime.datetime.now().strftime("%I:%M:%S")  # better date-time abriviation
    speaking(f"{time[0:2]} o'clock and {time[3:5]} minutes")
    # print(time)


# Intro greeting at startup
def intro_greeting():
    speaking(
        f'''
        hello , my name is {name} . 
        I am your personal assistant
        what can i do for you today?
        '''
    )


# the heart of the assistant , takes queries and return answers
def quering():
    intro_greeting()
    stat = True
    while (stat):
        q = transform().lower()

        if 'start youtube' in q:
            speaking('starting youtube,just a second')
            webbrowser.open('https://www.youtube.com')
            continue


        elif 'start webbrowser' in q:
            speaking('opening browser,just a second')
            webbrowser.open('https://www.google.com')
            continue

        elif 'what day is it' in q:
            query_day()
            continue

        elif 'whats time is it' in q:
            query_time()
            continue

        elif 'from wikipedia' in q:
            speaking('checking wikipedia')
            q = q.replace("wikipedia", "")
            result = wikipedia.summary(q, sentences=2)
            speaking('found on wikipedia')
            speaking(result)
            continue

        elif "your name" in q:
            speaking(f'I am {name}')
            continue

        elif "search web" in q:
            pywhatkit.search(q)
            speaking('that is what i found')
            continue

        elif "play" in q:
            search = q.split("play")[-1].strip()
            speaking(f'playing {search}')
            pywhatkit.playonyt(q)
            continue

        elif "joke" in q:
            speaking(pyjokes.get_joke())
            continue

        elif "stock price" in q:
            search = q.split("of")[-1].strip()
            lookup = {'apple': 'AAPL',
                      'amazon': 'AMZN',
                      'google': 'GOOGL'}
            try:
                stock = lookup[search]
                stock = yf.ticker(stock)
                concurrentprice = stock.info["regularMarketPrice"]
                speaking(f'i found it , the price fot {search} is {concurrentprice}')
                continue

            except:
                speaking(f'sorry i dont know')
                continue


        elif ('stop' or 'shut down') in q:
            speaking("goodbye")
            stat = False


if __name__ == '__main__':
    print('''
    the assistant commands :
    * start youtube
    * start webbrowser
    * what day is it
    * whats time is it 
    * from wikipedia + __search__
    * search web + __search__
    * play + __song__
    * joke
    * stock price of + __stock__ 
    * your name (Repeat its name) 
    * "shut down" or "stop" 
    ''')
    quering()
