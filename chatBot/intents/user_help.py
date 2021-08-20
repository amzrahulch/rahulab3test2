import random
import json
import boto3

class UserHelp:
    def __init__(self,intent_request):
        self.intent_request = intent_request
        self.SAMPLE_QUESTIONS = [
            'What metrics are available?',
            'What is EMR',
            'what is genome sequencing',
            'What is a variant?',
            'Define annotation'
        ]

    def execute(self):
        question = self.intent_request['inputTranscript'].lower()
        response = ""

        #help
        if len(response) < 1:
            for h in ['help','assist','heelp','hhelp','hheellpp','heeelp','asssist','helpp','question']:
                if h in question:
                    new_question = random.choice(self.SAMPLE_QUESTIONS)
                    response = f"Try asking a question like '{new_question}' "

        # greeting
        if len(response) < 1:
            for greeting in ['hi','hello','yo','greeting']:
                if greeting in question:
                    response = "Hello, I am Answer Bot. Ask me a question about Genome Sequencing and I will try to answer."

        # parting
        if len(response) < 1:
            for bye in ['bye','goodby','stop','end']:
                if bye in question:
                    response = "Goodbye, thanks for talking!"

        if len(response) < 1:
            response = "Sorry, I couldn't understand. Try asking for help. "

        return response
