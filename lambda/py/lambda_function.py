# -*- coding: utf-8 -*-

# This is a Color Picker Alexa Skill.
# The skill serves as a simple sample on how to use
# session attributes.

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from typing import Union, Dict, Any, List
from ask_sdk_model.dialog import (
    ElicitSlotDirective, DelegateDirective)
from ask_sdk_model import (
    Response, IntentRequest, DialogState, SlotConfirmationStatus, Slot)
from ask_sdk_model.slu.entityresolution import StatusCode
import boto3
from botocore.exceptions import ClientError
import random


skill_name = "Travel Bud"
help_text = ("Please tell me the city you are departing from and arriving to")

cityB_Key = "LOCATION"
cityAslot = "cityA"
cityBslot = "cityB"

from_date_slot = "fromDate"
to_date_slot = "toDate"

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fromDate = ""
toDate = ""
fromLocation = ""
toLocation = ""

FlightPriceList = [["512", "500", "613"], ["772", "812", "830"], ["601", "612", "700"], ["430", "445", "450"]] #[Chicago - Miami, Los Angeles -
                                                                                        # New York, Houston - San Francisco, Any location not identified]
AirlineList = ["Frontier", "Delta", "American Airlines", "United", "Spirit", "JetBlue"]

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""

    speech = "Welcome to Travel Bud."
    handler_input.response_builder.speak(
        speech + " " + help_text).ask(help_text)
    return handler_input.response_builder.response

# FIXME:
# Handle specifycityB
@sb.request_handler(can_handle_func=is_intent_name("specifyCityBIntent"))
def specifycityBIntentHandler(handler_input):
    # slots = handler_input.request_envelope.request.intent.slots[0]
    cityA = handler_input.request_envelope.request.intent.slots["cityA"].value
    cityB = handler_input.request_envelope.request.intent.slots["cityB"].value

    if cityB != None:
        handler_input.attributes_manager.session_attributes[cityB_Key] = cityB
    
    if cityA != None:
        handler_input.attributes_manager.session_attributes[cityA_Key] = cityA

    if cityB_Key in handler_input.attributes_manager.session_attributes:
        TRAVEL_DATA["cityB"] = handler_input.attributes_manager.session_attributes[
            cityB_Key]
        speech = "Great!, you want to go to {}".format(handler_input.attributes_manager.session_attributes[
            cityB_Key])
        # handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "Where did you say you wanted to go? " + help_text
        handler_input.response_builder.ask(help_text)

    # if handler_input.response_builder.speak(speech):
    return handler_input.response_builder.response



# FIXME:
# Handle specifyFromDestination
@sb.request_handler(can_handle_func=is_intent_name("specifyCityAIntent"))
def specifyFromDestinationHandler(handler_input):
    pass

# FIXME:
# Handle specifyDate
@sb.request_handler(can_handle_func=is_intent_name("specifyDateIntent"))
def specifyDateHandler(handler_input):
    pass


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    handler_input.response_builder.speak(help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("LocationIntent"))
def location_handler(handler_input):
    """Check if color is provided in slot values. If provided, then
    set your favorite color from slot value into session attributes.
    If not, then it asks user to provide the color.
    """
    slots = handler_input.request_envelope.request.intent.slots


    if cityAslot in slots:
        cityA = slots[cityAslot].value
        handler_input.attributes_manager.session_attributes[
            location_slot_key] = cityA
    if cityBslot in slots:
        cityB = slots[cityBslot].value
        handler_input.attributes_manager.session_attributes[
            location_slot_key] = cityB
        speech = ("The location you are traveling from is {} and going to is {}. Where will you be going to?"
                  .format(cityA, cityB))
        reprompt = ("Where will you be traveling to?")
    else:
        speech = "I'm not sure what your arrival and departure city is. Try again."
        reprompt = ("Where will you be departing from and arriving to?")

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response



@sb.request_handler(can_handle_func=is_intent_name("DateIntent"))
def date_handler(handler_input):
    """Check if color is provided in slot values. If provided, then
    set your favorite color from slot value into session attributes.
    If not, then it asks user to provide the color.
    """
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots

    if from_date_slot in slots:
        fromDate = slots[from_date_slot].value
        handler_input.attributes_manager.session_attributes[
            location_slot_key] = fromDate
        if to_date_slot in slots:
            toDate = slots[from_date_slot].value
            handler_input.attributes_manager.session_attributes[
                location_slot_key] = toDate
        speech = ("The date you will be leaving is {} and arriving is {}.".format(fromDate, toDate))
        reprompt = ("What date will you be arriving?")
    else:
        speech = "I'm not sure what your date is. Try again."
        reprompt = ("What date will you be arriving?")

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The {} skill can't help you with that.  "
        "Tell me where and when you will be flying").format(skill_name)
    reprompt = ("Tell me where and when you will be flying")
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


def convert_speech_to_text(ssml_speech):
    """convert ssml speech to text, by removing html tags."""
    # type: (str) -> str
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


@sb.global_response_interceptor()
def add_card(handler_input, response):
    """Add a card by translating ssml text to card content."""
    # type: (HandlerInput, Response) -> None
    response.card = SimpleCard(
        title=skill_name,
        content=convert_speech_to_text(response.output_speech.ssml))


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Log response from alexa service."""
    # type: (HandlerInput, Response) -> None
    print("Alexa Response: {}\n".format(response))


@sb.global_request_interceptor()
def log_request(handler_input):
    """Log request to alexa service."""
    # type: (HandlerInput) -> None
    print("Alexa Request: {}\n".format(handler_input.request_envelope.request))


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> None
    print("Encountered following exception: {}".format(exception))

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


def add_speech(speech):
    new_speech = speech + " Would you like me to send you an with the link"

    return new_speech

def email(recipient):
    # This address must be verified with Amazon SES.
    SENDER = "viraat.laldas@gmail.com"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = recipient

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET
    CONFIGURATION_SET = "/Users/owner/.aws/credentials"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-west-2"

    # The subject line for the email.
    SUBJECT = "Amazon SES Test (SDK for Python)"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

@sb.request_handler(can_handle_func=is_intent_name("FlightMatchIntent"))
def flightMatchHandler(handler_input):
    cityA = handler_input.request_envelope.request.intent.slots["cityA"].value
    cityB = handler_input.request_envelope.request.intent.slots["cityB"].value
    date = handler_input.request_envelope.request.intent.slots["date"].value

    print(cityA)
    print(cityB)

    if cityA.lower() == "chicago":
        speech = "The three cheapest available prices for your your trip from {} to {} on {} ".format(cityA, cityB, date), ', ' \
            .join([FlightPriceList[2][i] + " with " + AirlineList[random.randint(0, len(AirlineList))]] for i in range(3))
        speech += add_speech(speech)

    elif cityA.lower() == "los angeles":
        speech = "The three cheapest available prices for your your trip from {} to {} on {} ".format(cityA, cityB,
            date), ', '.join([FlightPriceList[2][i] + " with " + AirlineList[random.randint(0, len(AirlineList))]] for i in range(3))
        speech += add_speech(speech)
    elif cityA.lower() == "houston":
        speech = "The three cheapest available prices for your your trip from {} to {} on {} ".format(cityA, cityB, date), ', '.join([FlightPriceList[2][i] + " with " + AirlineList[random.randint(0, len(AirlineList))]] for i in range(3))
        speech += add_speech(speech)
    else:
        speech = "Sorry. Currently there are no available flights for the provided specifications."


    return handler_input.response_builder.speak(speech).response

@sb.request_handler(can_handle_func=is_intent_name("FlightMatchIntent"))
def emailHandler(handler_input):
    recipient = "viraat.laldas@gmail.com"
    speech = ""
    response = handler_input.request_envelope.request.intent.slots["response"].value
    if (response == "Yes"):
        speech += " I will go ahead and send it to you."
        email("viraat.laldas@gmail.com")
    else:
        speech = " Ok. I won't send it to you."
    return handler_input.response_builder.speak(speech).response

@sb.request_handler(can_handle_func=is_intent_name("PredictBestPrice"))
def predictMatchHandler(handler_input):
    cityA = handler_input.request_envelope.request.intent.slots["cityA"].value
    cityB = handler_input.request_envelope.request.intent.slots["cityB"].value
    date = ["November 20, 2018", "December 1, 2018", "December 3, 2018", "December 10, 2018"]


    speech = "According to your preferences and previous flight history, you should fly to {} from {} on {} for the " \
             "cheapest travel".format(cityA, cityB,date[random.randint(0, len(date))])
    speech += " The three listed cheap price is {} ".format(', '.join(FlightPriceList[random.randint(0, len(FlightPriceList))]))

    return handler_input.response_builder.speak(speech).response

######## Convert SSML to Card text ############
# This is for automatic conversion of ssml to text content on simple card
# You can create your own simple cards for each response, if this is not
# what you want to use.

from six import PY2
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if not PY2:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)

################################################


# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()

