"""
Cal Facts Lambda Function

Created by Zac Patel on 2/9/17

Code skeleton taken from Lambda python template

Fact sources: 
"""

from __future__ import print_function
from random import randint
# --------------- Helpers that build all of the responses ----------------------

def get_fact_intent_handler(intent):
    """
    grabs a random fact from the list of facts, and returns it to the user
    """
    # finding the index of the fact to get, and pulling it from the list
    rand = randint(0, len(FACTS_ARRAY) - 1)
    fact = FACTS_ARRAY[rand]

    # session attributes remain empty
    session_attributes = {}
    # getting a fact should end the session
    should_end_session = False
    # no reprompt text because the session should end after a single fact is returned
    reprompt_text = ""
    # the title displayed on the phone app
    title = "Cal Fact #" + str(rand + 1)
    
    # generating our speechlet response
    sp_res = build_speechlet_response(title, fact, reprompt_text, should_end_session)
    return build_response(session_attributes, sp_res)

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Cal Facts. Ask me for a fact."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I know " + str(len(FACTS_ARRAY)) + " facts about the University of California."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for using Cal facts."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GETFACTINTENT":
        return get_fact_intent_handler(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

# Array to hold all our facts
# storing all our facts in an array is just generally less of a hassle than a text file
# (though facts are stored in their formatted form in Facts.docx for spellcheck purposes)
# most facts are taken from https://en.wikipedia.org/wiki/University_of_California,_Berkeley
# (but some are common knowledge)
FACTS_ARRAY = ["Berkeley athletes have won 117 gold medals, 51 silver medals, and 39 bronze medals at the Olympics.", 
"The University of California was created on March 5, 1868 by the Dwinelle Bill as the merger of two existing colleges.", 
"Professors or alumni of Cal have won 13 Fields medals, the most prestigious award in math.", 
"The motto of the University of California is Fiat Lux, which means Let There be Light in Latin.", 
"The University, along with Berkeley Lab, has discovered 16 elements on the periodic table, more than any other university in the world.", 
"Berkelium is element 97 on the periodic table, but there is no Stanfordium.", 
"Berkeley Memes for Edgy Teens is the largest University Facebook meme page in the world.", 
"The winner of the annual Big Game versus Stanford has taken home the Stanford Axe since 1933.", 
"The 74 mile long Hayward fault runs directly underneath Memorial Stadium.", 
"The University has 32 different libraries, and is the 4th largest academic library system in the United States.", 
"The current Cal faculty includes 8 Nobel Laureates. A total of 92 Laureates are associated with the University as alumni, faculty or researchers.", 
"The Berkeley Software Distribution license, developed in the 1970s, was a leading cause in the popularity of open source computer software.", 
"During the 1960s, Berkeley was noted for having student led Free Speech, and Anti-Vietnam movements.", 
"Several school spirit songs refer to the Cal mascot, Oski, as being able to fly.", 
"Oski was designed William Rockwell, and debuted during a football game on September 27, 1941.", 
"Sather tower houses some of the Integrative Biology department's fossils due to its cool, dry interior.", 
"Sather tower is 22 feet taller than Stanford University's Hoover Tower.", 
"The oldest building on campus, South Hall, was built in 1873.", 
"Cal's daily newspaper, the Daily Cal, has been independent since 1971.",
"Before it became a residential dorm, what is now known as the Clark Kerr Campus was originally the State Asylum for the Deaf, Dumb and Blind.",
"The largest class on campus is Computer Science 61 A, which enrolled nearly 1,800 students in Fall 2016.",
"The libraries Main Stacks, which runs under Memorial Glade, and Moffitt are connected by an underground passage.",
"Three metal seals lie on the ground around Memorial Glade. Stepping on a seal is considered bad luck and is rumored to lower your G P A.",
"The University of California, Berkeley is the oldest of the ten schools in the U C system.",
"Berkeley's originally colors were Yale blue and gold because many of the Universities founders were Yale graduates.",
"The stadium card stunt, popular during football games, was invted at Cal in 1910.",
"The only time the California Victory Cannon, which fires after every score at football games, has only run out of ammunition once, in 1991."]
