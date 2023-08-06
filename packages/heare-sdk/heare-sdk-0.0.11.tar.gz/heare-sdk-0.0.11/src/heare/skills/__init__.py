from typing import List

from adapt.intent import Intent
import json

from heare.config import SettingsDefinition

from heare.client.events.message import Message
from heare.logging import get_logger


# TODO: code organization: where should this live?
RELOAD_EVENT = 'heare.skills.reload'


class IntentSerializer(object):
    @staticmethod
    def to_dict(intent: Intent) -> dict:
        return {
            'name': intent.name,
            'requires': intent.requires,
            'at_least_one': intent.at_least_one,
            'optional': intent.optional
        }

    @staticmethod
    def serialize(intent: Intent) -> str:
        json.dumps(IntentSerializer.to_dict(intent))

    @staticmethod
    def from_dict(intent_dict: dict) -> Intent:
        return Intent(
            name=intent_dict.get('name', []),
            requires=intent_dict.get('requires', []),
            at_least_one=intent_dict.get('at_least_one', []),
            optional=intent_dict.get('optional', [])
        )

    @staticmethod
    def deserialize(intent_str) -> Intent:
        intent_dict = json.loads(intent_str)
        return IntentSerializer.from_dict(intent_dict)


class Skill(object):
    """
    Base class for a Heare Skill.
    """
    def __init__(self, event_source):
        self.logger = get_logger(self.__class__.__name__)
        self.__event_source = event_source
        # it seems iffy that this would work, as it's trying to discover properties
        # of the subclass, but in unit tests it works, so I'm going to trust that
        # it's the expected behavior of the language. If I find a language spec that
        # clarifies, I'll link it here. TODO
        Skill.bind(self)
        self.__event_source.on(RELOAD_EVENT, self.reload)
        self.__event_handlers: List[tuple] = []

    @staticmethod
    def bind(instance) -> None:
        for method in [m for m in dir(instance) if callable(getattr(instance, m)) and m.startswith("on_")]:
            event_name = method[3:]
            instance.__event_source.on(event_name, getattr(instance, method))

    def load(self, settings: SettingsDefinition = None):
        """
        load
        Method for executing skill bootstrap code.
        This is where intent and vocab registration should occur.
        :return:
        """
        raise NotImplementedError("Oh noes!")

    def reload(self, _: Message = None):
        """
        reload
        Handler to trigger reloading the skill.
        By default, this will simply call load again.
        Override if there are resources to clean up.
        The most likely trigger is a start or restart of the IntentSkill.
        :return:
        """
        for event_name, handler in self.__event_handlers:
            self.__event_source.remove(event_name, handler)
        self.__event_handlers.clear()
        self.load()

    def register_intent(self, intent: Intent):
        self.emit(
            message_type='register_intent',
            data=IntentSerializer.to_dict(intent)
        )

    def register_vocabulary(self,
                            entity_type: str,
                            entity_value: str,
                            entity_aliases: List[str] = None):
        self.emit(
            message_type='register_entity',
            data=dict(
                entity_type=entity_type,
                entity_value=entity_value,
                entity_aliases=entity_aliases or []
            )
        )

    def register_regex_matcher(self, regex_matcher: str):
        self.emit(
            message_type='register_regex',
            data=regex_matcher
        )

    @staticmethod
    def __reply_metadata(message: Message) -> dict:
        metadata = message.metadata if message else {}
        return {
            'target': metadata.get('source')
        }

    def emit(self, message_type, data, metadata={}, reply_to: Message = None):
        self.__event_source.emit(Message(
            message_type=message_type,
            data=data,
            metadata=metadata or self.__reply_metadata(reply_to)
        ))

    def speak(self, message: str, metadata: dict = None, reply_to: Message = None) -> None:
        self.emit(
            message_type='speak',
            data={
                'text': message
            },
            metadata=metadata or self.__reply_metadata(reply_to)
        )

    def on(self, event_name, event_handler):
        self.__event_handlers.append((event_name, event_handler))
        self.__event_source.on(event_name, event_handler)
