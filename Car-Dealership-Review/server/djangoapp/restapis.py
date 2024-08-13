import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarDealer


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    # print(kwargs)
    print("GET from {}".format(url))
    status_code = None
    try:
        # Call the get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs)

        status_code = response.status_code

    except Exception as e:
        # If any error occurs
        print("Network exception occurred, {}".format(e))
        staus_code = None

    print("With status {} ".format(status_code))

    if status_code is not None:
        json_data = json.loads(response.text)
        return json_data
    else:
        return None


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    # print(kwargs)
    print("POST from {}".format(url))
    status_code = None
    try:
        # Call the get method of requests library with URL and parameters
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json',
                     'X-CSRFToken': 'csrftoken'},
            params=kwargs,
            json=json_payload)

        status_code = response.status_code

    except Exception as e:
        # If any error occurs
        print("Network exception occurred, {}".format(e))
        staus_code = None

    print("With status {} ".format(status_code))

    if status_code is not None:
        json_data = json.loads(response.text)
        return json_data
    else:
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    # convert the id to int
    id = int(id)
    json_result = get_request(url, id=id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result

        # For each dealer object
        for review in reviews:
            # # now process the sentiment analysis
            sentiment = analyze_review_sentiments(
                dealerreview=review["review"])

            # # add the sentiment to the review_info dictionary
            review["sentiment"] = sentiment

            print("Sentiment", sentiment)

            # # Append the review information to the results list
            results.append(review)

    return results


def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # print("Dealer", dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    url = "https://api.jp-tok.natural-language-understanding.watson.cloud.ibm.com/instances/5441da18-b35f-4a52-99b7-939a4278655c"
    params = {
        'text': dealerreview,
        "features": {
            'sentiment': {
                'targets': ['good', 'bad']
            }
        }
    }

    # print(kwargs)
    print("GET from {}".format(url))
    status_code = None
    try:
        # Call the get method of requests library with URL and parameters
        response = requests.get(url,
                                headers={'Content-Type': 'application/json'},
                                params=params,
                                auth=HTTPBasicAuth('apikey', 'BIW7_bMakNxDXaJF3aZJiiD4zTs55qTrv5HV_u99ceSQ'))

        status_code = response.status_code

    except Exception as e:
        # If any error occurs
        print("Network exception occurred, {}".format(e))
        status_code = None  # Fix the variable name here

    print("With status {} ".format(status_code))

    if status_code is not None:
        json_data = json.loads(response.text)
        return json_data
    else:
        return None
