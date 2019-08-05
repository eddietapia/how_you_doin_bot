class CheckIn:
    """Performs the check in and records the state of the individual.
    
    A check in is composed of multiple questions, each which will (hopefully) garner
    a response, in the form of a slack reaction.
    """

    def __init__(self, channel):
        self.channel = channel
        self.username = "how you doin'"
        self.icon_emoji = ""
        self.timestamp = ""
        self.questions = [{
            "question": "How are we feelin' emotionally today?",
            "response_options": [{
                "title": ":cry:",
                "description": "I feel terrible today"
            }, {
                "title": ":slightly_frowning_face:",
                "description": "I don't feel great today"
            }, {
                "title": ":neutral_face:",
                "description": "I feel ambivalent today"
            }, {
                "title": ":simple_smile:",
                "description": "I feel good today"
            }, {
                "title": ":smile:",
                "description": "I feel great today"
            }],
            "response": "",
            "ts": ""
        }, {
           "question": "How are we feelin' energetically today?",
           "response_options": [{
                "title": ":one:",
                "description": "I feel terrible"
            }, {
                "title": ":two:",
                "description": "I feel amazing"
            }],
           "response": "",
           "ts": ""
        }]
        self.current_question = 0
    
    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": self._get_question_block(),
        }

    def _get_question_block(self):
        blocks = []
        if self.current_question >= len(self.questions):
            blocks.append(CheckIn.format_text_block(f"That's all the questions we have for you today! See you next time :blush:\n"))
        else:
            if self.current_question == 0:
                blocks.append(CheckIn.format_text_block(f"Good afternoon! We have {len(self.questions)} questions for you today.\n\n"))
        
            current_question = self.questions[self.current_question]
            text = f"Question number {self.current_question + 1}: {current_question['question']} \n\n" 
            blocks.append(CheckIn.format_text_block(text))
            blocks.append(CheckIn.format_question_block(current_question))
        print(blocks)
        return blocks
    

    # BLOCK FORMATTING METHODS
    @staticmethod
    def format_text_block(text):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

    @staticmethod
    def format_question_block(question_info):
        buttons = [CheckIn.format_response_option(r) for r in question_info["response_options"]]
        return {
            "type": "actions",
            "elements": buttons
        }
       
    
    @staticmethod
    def format_response_option(response_option):
        return {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": f"{response_option['title']} {response_option['description']}",
                "emoji": True
            },
            "value": response_option['title']
        }