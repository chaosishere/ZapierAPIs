from django.contrib import admin
from django.apps import apps

# Automatically register all models in the current app
app = apps.get_app_config('zap_hooks')  # Replace 'your_app_name' with your app's name
for model in app.models.values():
    admin.site.register(model)
