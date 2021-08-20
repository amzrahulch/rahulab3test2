import json
import intents
from intents.user_help import UserHelp
from intents.answer_help import AnswerHelp
from intents.query_help import QueryHelp

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = ""
    if 'name' in intent_request['currentIntent']:
        intent_name = intent_request['currentIntent']['name']
    elif 'intentName' in intent_request['currentIntent']:
        intent_name = intent_request['currentIntent']['intentName']

    response = ""
    if intent_name == 'queryIntent':
        response = QueryHelp(intent_request).execute()
    elif intent_name == 'AnswerHelpQuestion':
        response = AnswerHelp(intent_request).execute()
    elif intent_name == 'help':
        response = UserHelp(intent_request).execute()
    else:
        response = f"Invalid input. Try asking a question or say 'help' for more information. "
    return response

def close(fulfillment_state, message):
    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    #logger.debug(event)
    print(event,context)

    try:
        response = dispatch(event)
    except Exception as e:
        response = str(e)
        logging.exception(e)
    finally:
        # provide the response
        return close(
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': response
            }
        )
