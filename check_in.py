class CheckIn:
    """Performs the check in and records the state of the individual"""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Helloooooo! :wave: We're so glad you're here! :blush:\n\n"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "ee-bot"
        self.icon_emoji = ""
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_check_in_block(),
            ],
        }

    def _get_check_in_block(self):
        text = (
            f"How are you doing??\n\n"
        )
        information = (
            f"Stay tuned for more updates :hamster_dance:"
        )
        return self._get_task_block(text, information)

    # TODO: Add functionality for our questions
    def _get_reaction_block(self):
        task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f"{task_checkmark} *Add an emoji reaction to this message* :thinking_face:\n"
            "You can quickly respond to any message on Slack with an emoji reaction."
            "Reactions can be used for any purpose: voting, checking off to-do items, showing excitement."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
            "Learn How to Use Emoji Reactions>*"
        )
        return self._get_task_block(text, information)

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]
