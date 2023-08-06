import importlib
import sys

from heare.config import SettingsDefinition, ListSetting

from heare.client.events.ws import HeareClient, HeareClientSettings
from heare.logging import get_logger
from heare.skills import Skill


class ContainerSettings(SettingsDefinition):
    skill = ListSetting(str)


def main(args):
    logger = get_logger(__name__)
    container_settings = ContainerSettings.load(args=args)
    heare_client_settings = HeareClientSettings.load(args=args)
    client = HeareClient(config=heare_client_settings)

    skill_classes = []
    for skill_str in container_settings.skill.get():
        try:
            module_name, klass_name = skill_str.rsplit('.', 1)
            mod = importlib.import_module(module_name)
            skill_classes.append(
                getattr(mod, klass_name)
            )
        except Exception as e:
            logger.exception(f"Error loading skill: {skill_str}.")

    def wire_skills():
        for klass in skill_classes:
            try:
                skill: Skill = klass(event_source=client)
                config = None
                if hasattr(klass, '__SETTINGS__'):
                    config = getattr(klass, '__SETTINGS__').load(args=args)
                skill.load(settings=config)
            except Exception as e:
                logger.exception(f"Error instantiating skill {klass}")

    client.once('open', wire_skills)
    client.run_forever()


if __name__ == '__main__':
    main(sys.argv[1:])
