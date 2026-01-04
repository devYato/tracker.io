# Notes

## Learnings
- In each declarated `Model` in my apps, Django automatically creates a default manager called `objects` that allows querying the database for instances of that model.
- Django is only capable of identify my models even if registered if i create an `apps.py` file in each app folder and declare the app config class, and then reference it in the `INSTALLED_APPS` list in settings.
- Django only identifies my changes in models if i create and run migrations after changing the models. So each app need to have its `own migrations folder.`