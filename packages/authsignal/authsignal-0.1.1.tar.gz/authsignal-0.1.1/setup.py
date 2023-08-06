# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authsignal']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'authsignal',
    'version': '0.1.1',
    'description': 'Authsignal Python SDK for Passwordless Step Up Authentication',
    'long_description': '# Authsignal Server Python SDK\n\n[Authsignal](https://www.authsignal.com/?utm_source=github&utm_medium=python_sdk) provides passwordless step up authentication (Multi-factor Authentication - MFA) that can be placed anywhere within your application. Authsignal also provides a no-code fraud risk rules engine to manage when step up challenges are triggered.\n\n## Installation\n\nPython 3\n\n```bash\npip3 install authsignal\n```\n\nor install newest source directly from GitHub:\n\n```bash\npip3 install git+https://github.com/authsignal/authsignal-python\n```\n\n## Configuration\nInitialize the Authsignal Python SDK, ensuring you do not hard code the Authsignal Secret Key, always keep this safe.\n\n```python\nimport authsignal.client\n\nauthsignal_client = authsignal.Client(api_key=\'<SECRET API KEY HERE>\')\n```\n\n## Usage\n\nAuthsignal\'s server side signal API has four main calls `track_action`, `get_action`, `get_user`, `identify`, `enrol_authenticator`\n\nThese examples assume that the SDK is being called from a Starlette based framework like FastAPI, adapt depending on your app server framework.\n\n### Track Action\nThe track action call is the main api call to send actions to authsignal, the default decision is to `ALLOW` actions, this allows you to call track action as a means to keep an audit trail of your user activity.\n\nAdd to the rules in the admin portal or the change default decision to influence the flows for your end users. If a user is not enrolled with authenticators, the default decision is to `ALLOW`.\n\n```python\n# OPTIONAL: The Authsignal cookie available when using the authsignal browser Javascript SDK\n# you could you use own device/session/fingerprinting identifiers.\nauthsignal_cookie = request.cookies.get(\'__as_aid\')\n\n# OPTIONAL: The idempotency_key is a unique identifier per track action\n# this could be for a unique object associated to your application\n# like a shopping cart check out id\n# If ommitted, Authsignal will generate the idempotencyKey and return in the response\nimport uuid\nidempotency_key = uuid.uuid4()\n\n# OPTIONAL: If you\'re using a redirect flow, set the redirect URL, this is the url authsignal will redirect to after a Challenge is completed.\nredirect_url = "https://www.yourapp.com/back_to_your_app"\n\nresponse = authsignal_client.track_action(\n    user_id="python:1",\n    action_code="testPython",\n    payload={\n        "redirectUrl": "https://www.example.com/",\n        "email": "test@python.com",\n        "deviceId": authsignal_cookie,\n        "userAgent": request.headers["user-agent"],\n        "ipAddress": request.headers["x-forwarded-for"],\n        "custom": {\n            "yourOwnCustomBoolean": True,\n            "yourOwnCustomString": "Blue",\n            "yourOwnCustomDecimal": 100.00,\n        },\n    }\n)\n\n```\n*Response*\n```python\nresponse = authsignal_client.track_action(...)\nmatch response["state"]\ncase authsignal.client.ALLOW:\n    # Carry on with your operation/business logic\ncase authsignal.client.BLOCK:\n    # Stop your operations\ncase authsignal.client.CHALLENGE_REQUIRED:\n    # Step up authentication required, redirect or pass the challengeUrl to the front end\n    response["challengeUrl"]\n```\n\n### Get Action\nCall get action after a challenge is completed by the user, after a redirect or a succesful browser challenge pop-up flow, and if the state of the action is `CHALLENGE_SUCCEEDED` you can proceed with completing the business logic.\n\n```python\nresponse = authsignal_client.get_action(\n    user_id="1234",\n    action_code="signIn",\n    idempotency_key="0ae73782-d8c1-49bc-be75-09612a3b9d1c",\n)\n\nif response["state"] == "CHALLENGE_SUCCEEDED":\n    print("Procceed with business logic")\n    # The user has successfully completed the challenge, and you should proceed with\n    # the business logic\n```\n\n### Get User\nGet user retrieves the current enrolment state of the user, use this call to redirect users to the enrolment or management flows so that the user can do self service management of their authenticator factors. User the `url` in the response to either redirect or initiate the pop up client side flow.\n\n```python\nresponse = authsignal_client.get_user(user_id="1234", redirect_url="http://www.yourapp.com/path-back")\n\nis_enrolled = response["isEnrolled"]\nurl = response["url"]\n```\n\n### Identify\nGet identify to link and update additional user indetifiers (like email) to the primary record.\n\n```python\nresponse = authsignal_client.identify(user_id="python:1", user_payload={"email": "new@email.com"})\n```\n\n### Enrol Authenticator\nIf your application already has a valid authenticator like a validated phone number for your customer, you can enrol the authenticator on behalf of the user using this function\n\n```python\nresponse = authsignal_client.enrol_authenticator(user_id="1234", authenticator_payload={"oobChannel": "SMS", "phoneNumber": "+64277770770"})\n```',
    'author': 'justinsoong',
    'author_email': 'justinsoong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.authsignal.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
