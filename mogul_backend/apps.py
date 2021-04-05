from django.apps import AppConfig
from dynamic_preferences.registries import preference_models
from mogul_backend.registries import character_preferences_registry


class MogulBackendConfig(AppConfig):
    name = 'mogul_backend'

    def ready(self):
        CharacterPreferenceModel = self.get_model('CharacterPreferenceModel')

        preference_models.register(CharacterPreferenceModel, character_preferences_registry)
        import mogul_backend.signals