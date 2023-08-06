from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

from heare.skills import Skill, IntentSerializer, RELOAD_EVENT
from heare.client.events.message import  Message


class AdaptIntentSkill(Skill):
    def __init__(self, event_source):
        Skill.__init__(self, event_source=event_source)
        self.engine = None

    def load(self, _: Message = None):
        self.engine = IntentDeterminationEngine()
        # Trigger a reload of all skills, so that vocabulary and intents are registered.
        self.emit(RELOAD_EVENT, data={})
        self.register_intent(IntentBuilder('heare.agent.reload').require("AgentReloadTrigger").build())
        self.register_vocabulary('AgentReloadTrigger', 'AgentReload')
        self.on('heare.agent.reload', self.load)

    def reload(self, _: Message = None):
        """
        Overriding reload. If left implemented, will cause a recursive loop, as load triggers a reload across the entire system.
        :param _: ignored; the message routing client always passes in the message
        :return:
        """
        pass

    def on_utterance(self, utterance_event: Message):
        self.logger.info(utterance_event)
        utterances = utterance_event.data.get('utterances', [
            {'text': utterance_event.data.get('text'), 'confidence': 1.0}
        ])

        best_intent = None
        for scored_utterance in utterances:
            utterance = scored_utterance.get('text')
            confidence = scored_utterance.get('confidence')
            for intent in self.engine.determine_intent(utterance, num_results=100):
                intent['utterance'] = utterance
                intent['confidence'] *= confidence
                best_confidence = best_intent.get('confidence') if best_intent else 0.0
                cur_confidence = intent.get('confidence', 0.0)
                if cur_confidence > best_confidence:
                    best_intent = intent

        if best_intent:
            self.emit(message_type=intent.get('intent_type'), data=intent, metadata=utterance_event.metadata)
        elif not utterance_event.metadata.get('suppress_fallback', False):
            self.emit(message_type='fallback_error', data=utterance_event.data, metadata=utterance_event.metadata)

    def on_register_intent(self, register_intent_event: Message):
        intent = IntentSerializer.from_dict(register_intent_event.data)
        self.engine.register_intent_parser(intent_parser=intent)

    def on_register_entity(self, register_entity_event: Message):
        payload = register_entity_event.data
        self.engine.register_entity(
            entity_type=payload['entity_type'],
            entity_value=payload['entity_value']
        )

        for alias in payload.get('entity_aliases', []):
            self.engine.register_entity(
                entity_type=payload['entity_type'],
                entity_value=alias,
                alias_of=payload['entity_value']
            )

    def on_register_regex(self, register_regex_event: Message):
        self.engine.register_regex_entity(register_regex_event.data)
