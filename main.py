# This is a Coding Challenge for Slang!
import pprint
import requests
import logging
import sys

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class Challenge:
    """This is the coding challenge base class.

    This class has three methods, one for fetching activities from source, process it and send results back.
    """

    activities: list
    results: list
    SESSION_MINUTES = 5
    ACCESS_KEY = "MjY6SHdDdlFqYnEzZHRIT0hxcHdXaFVCRVFKNmk3U1kyMjNKYUZ0akRBMHpwND0="
    BASE_URL = "https://api.slangapp.com/challenges/v1/activities"
    ERROR_MESSAGES = {
        400: "There was a problem calling the server. (Error 400)",
        401: "You have not permissions to access the server. (Error 401)",
        429: "You have made too many requests. (Error 429)"
    }

    def __init__(self):
        self.activities = []
        self.results = []

    def fetch_activities(self):
        """
        Fetch activities from server

        :return: None
        """
        logging.info('Fetching activities')

        r = requests.get(self.BASE_URL, headers={'Authorization': f"Basic {self.ACCESS_KEY}"})

        # Check errors in call
        if r.status_code in self.ERROR_MESSAGES.keys():
            logging.error(self.ERROR_MESSAGES[r.status_code])
            exit()
        elif r.status_code != 200:
            logging.error('There was an error calling the server.')
            exit()

        # Save data in instance
        response = r.json()

        # Check response format
        if "activities" not in response.keys():
            logging.error('The information is not in a valid format.')
            exit()

        self.activities = response['activities']

    def process_challenges(self):
        """
        Process data from server and save it into the class instance

        :return: None
        """
        pass

    def send_results(self):
        """
        Save results in server

        :return: None
        """
        pass


if __name__ == '__main__':
    challenge = Challenge()
    challenge.fetch_activities()
    challenge.process_challenges()
    challenge.send_results()
