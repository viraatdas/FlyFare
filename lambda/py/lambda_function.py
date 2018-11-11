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

@sb.request_handler(can_handle_func=is_intent_name("FlightMatchIntent"))
def flightMatchHandler(handler_input):
    cityA = handler_input.request_envelope.request.intent.slots["cityA"].value
    cityB = handler_input.request_envelope.request.intent.slots["cityB"].value
    date = handler_input.request_envelope.request.intent.slots["date"].value

    print(cityA)
    print(cityB)

    if cityA.lower() == "chicago":
        speech = "The three cheapest available prices for your your trip from {} to {} on {} ".format(cityA, cityB, date), ', '.join(FlightPriceList[0])
    elif cityA.lower() == "los angeles":
        speech = "The three cheapest available prices for your your trip from {} to {} on {} ".format(cityA, cityB, date), ', '.join(
            FlightPriceList[1])
    elif cityA.lower() == "houston":
        speech = "The three cheapest available prices for your your trip from {} to {} on {} ".format(cityA, cityB, date), ', '.join(
            FlightPriceList[2])
    else:
        speech = "Sorry. Currently there are no available flights for the provided specifications."
    
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

