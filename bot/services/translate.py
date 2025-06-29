import requests

def translate_request(request: str, lang: str) -> str:
    """ Translates request from user language to English """
    url = "http://localhost:5000/translate"
    data = {
        "q": request,
        "source": lang,
        "target": "en",
        "format": "text"
    }
    get_request = requests.post(url, json=data)
    return get_request.json().get("translatedText")

def translate_response(response: str, lang: str) -> str:
    """ Translates response from English into the user's language """
    url = "http://localhost:5000/translate"
    data = {
        "q": response,
        "source": "en",
        "target": lang,
        "format": "text"
    }
    get_response = requests.post(url, json=data)
    return get_response.json().get("translatedText")