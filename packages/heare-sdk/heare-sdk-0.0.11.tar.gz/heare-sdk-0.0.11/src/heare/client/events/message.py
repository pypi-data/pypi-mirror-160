from typing import Dict

import json


class Message(object):
    """
    Represents a well-defined payload to be transmitted across the Heare
    message bus. There are three types of data:
    Args:
        message_type (str): This is the canonical name of an event. A running
        system has an effective enum of event_names, and they are used for
        routing messages based on subscriptions and permissions model.

        data (Dict): This is the payload of the event message. The contents
        of this message are defined and populated by the sender. This
        intentionally has no schema, other than being defined as a dictionary.

        metadata (Dict): This is metadata about the message. It may be
        populated by end users, but the contents may be merged with metadata
        from the client or server. Metadata should be namespaced with nested
        dictionaries, i.e.
            {metadata: {server: timestamp: '2020-02-02 08:00:00-08'}}
    """

    def __init__(self, message_type: str, data: Dict[str, object],
                 metadata: Dict[str, object] = None):
        self.message_type = message_type
        self.data = data
        self.metadata = metadata or {}

    def __str__(self) -> str:
        return json.dumps(self.__dict__)


class Serializer(object):
    def __init__(self, serializer=json):
        """
        Constructor for Serializer
        :param serializer: a module that takes the shape of python's built-in
        `json`, specifically implementing `dumps`.
        """
        self.serializer = serializer

    def serialize(self, message: Message) -> str:
        return self.serializer.dumps(message.__dict__)


class Deserializer(object):
    def __init__(self, deserializer=json):
        """
        Constructor for deserializer
        :param deserializer: a module that takes the shape of python's built-in
        `json`, specifically implementing `loads`.
        """
        self.deserializer = deserializer

    def deserialize(self, payload: str) -> Message:
        deserialized = self.deserializer.loads(payload)
        return Message(
            message_type=deserialized.get('message_type'),
            data=deserialized.get('data'),
            metadata=deserialized.get('metadata')
        )
