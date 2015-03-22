# metaeditor
A Django application for editing metadata of public datasets.

## Social authentication setup.

Given you are running metaeditor app on metaeditor.org

### Google.
1. Go to https://console.developers.google.com/ and create a new project.
2. Under APIs and Auth > Credentials, create a new Client ID. Choose Web application while creating client ID.
3. Make sure to specify the right callback URL (Authorized redirect URIs): (http://metaeditor.org/complete/google-oauth2/ for our example)
    Copy the values into local_settings.py file:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "..."  # Client Id
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "..."  # Client secret

    TODO: describe env vars populating too.
4. Make sure the Google+ API is in the list of enabled APIs on the Google Developer Console (under APIs)
5. Now try to log in and log out.

### Facebook.
1. Go to https://developers.facebook.com/apps/?action=create and click the green “Create New App” button. Select WWW app.
2. In the settings of the newly-created application, click “Add Platform”. From the options provided, choose Web, and fill in the URL of the site (http://metaeditor.org for our example).
3. Copy the App ID and App Secret, and place them into local_settings.py file:
    SOCIAL_AUTH_FACEBOOK_KEY = "..."  # App ID
    SOCIAL_AUTH_FACEBOOK_SECRET = "..."  # App secret
    TODO: describe env vars populating too.
4. Now try to log in and log out.

## Email notification setup.
1. Add your email to ADMINS settings.
2. Set up your email account as described here - <TODO: link to django site>
