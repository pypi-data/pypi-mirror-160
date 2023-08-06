from django.apps import (
    AppConfig,
)


class FunctionToolsConfig(AppConfig):
    name = 'function_tools'
    label = 'function_tools'

    def ready(self):
        """
        На момент готовности приложения, необходимо добавить зарегистрированные стратегии в модель-перечисление
        ImplementationStrategy
        """
        from function_tools.models import (
            EntityType,
            ImplementationStrategy,
        )
        from function_tools.storages import (
            EntityStorage,
        )

        entity_storage = EntityStorage()
        entity_storage.prepare()

        strategies = entity_storage.entities[EntityType.STRATEGY.key]

        for strategy in strategies.values():
            if strategy['class'].key:
                ImplementationStrategy.extend(
                    key=strategy['class'].key.upper(),
                    title=strategy['class'].title,
                )
