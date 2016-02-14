# metaeditor
A Django application for editing metadata of public datasets.

## Install.
* Clone repo.
* Setup database. TODO: Explain or add link to django docs.
* Migrate database. TODO: Explain or add link to django docs.
* Load initial sources:
```bash
python manage.py load_sources
```
* Create roots (each tree will have exactly one root - invisible for project users)
```bash
python manage.py create_roots
```
* Setup ambry search system (used for typeahead in the dataset's coverage):
```bash
python manage.py setup_ambry_search
```
If automatic ambry search system (previous step) failed, try install it manually:
```bash
$ ambry config install
$ ambry info                 # Verify version >= 0.3.705.
$ ambry sync                 # Verify that you are geting the civicknowledge.com-terms-0.0.3 bundle
$ ambry list terms           # Should return civicknowledge.com-terms
$ ambry search terms         # Should return civicknowledge.com-terms
$ ambry search -R            # Rebuilds place identifiers; datasets built during sync
$ ambry search -i California # Should return California state and a lot of counties. 
```

## Social authentication setup.

Given you are running metaeditor app on metaeditor.org

### Google.
* Go to https://console.developers.google.com/ and create a new project.
* Under APIs and Auth > Credentials, create a new Client ID. Choose Web application while creating client ID.
* Make sure to specify the right callback URL (Authorized redirect URIs): (http://metaeditor.org/complete/google-oauth2/ for our example)
    Copy the values into local_settings.py file:
```python
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "..."  # Client Id
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "..."  # Client secret
```
* Make sure the Google+ API is in the list of enabled APIs on the Google Developer Console (under APIs)
* Now try to log in and log out.

### Facebook.
* Go to https://developers.facebook.com/apps/?action=create and click the green “Create New App” button. Select WWW app.
* In the settings of the newly-created application, click “Add Platform”. From the options provided, choose Web, and fill in the URL of the site (http://metaeditor.org for our example).
* Copy the App ID and App Secret, and place them into local_settings.py file:
```python
SOCIAL_AUTH_FACEBOOK_KEY = "..."  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "..."  # App secret
```
* Now try to log in and log out.

# Email notification setup.
1. Add your email to ADMINS settings.
2. Set up your email account as described here https://sendgrid.com/docs/Integrate/Frameworks/django.html

## Importing initial data.

### Importing sources.
Sources will be imported from editor/data/sources.csv.

To import sources use load_sources management command:
```bash
python manage.py load_sources
```

If you already have sources call load_sources with --delete option. (this will delete all dataset too):
```bash
python manage.py load_sources --delete
```

## Testing

### Running unit tests
Install dependencies from requirements_dev.txt.
Run
```bash
python manage.py test
```

### Running functional tests (Requires Firefox)
Install dependencies from requirements_dev.txt.
Add `lettuce` to INSTALLED_APPS.
Run
```bash
python manage.py harvest --no-server editor/features
```
