import requests


def qotd_call() -> str:
    access_token = '1kXdqGlNlzGT8nUbclpLFllzqvInGkyBHz1B4xTT' # Bad practice <---

    url = "https://quotes.rest/qod?language=en"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    # Check if the response was successful (status code 200)

    if response.status_code == 200:
        # set the JSON response
        json_object = response.json()
        q = json_object.get('contents').get('quotes')[0].get('quote')
        a = json_object.get('contents').get('quotes')[0].get('author')
        qotd_return = q + ": " + a


    else:
        # set default quote
        qotd_return = "If you looked in the mirror and did not like what you saw, you would have to be mad to attack " \
                      "the image in the mirror. That is precisely what you do when you are in a state of " \
                      "nonacceptance. And, of course, if you attack the image, it attacks you back. If you accept the " \
                      "image, no matter what it is, if you become friendly toward it, it cannot not become friendly " \
                      "toward you. This is how you change the world. (from The Power of Now by Eckhart Tolle) "

    return qotd_return
