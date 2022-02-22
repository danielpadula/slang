# This is a Coding Challenge for Slang!
import itertools
import pprint
import requests
import logging
import sys
from datetime import datetime, timedelta

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

        # Lambda to get user ID key
        key_func = lambda x: x["user_id"]

        # Group activities by user
        for key, group in itertools.groupby(self.activities, key_func):
            user_sessions = dict({key: []})

            # Order each user activities by first seen date time
            user_activities = sorted(list(group), key=lambda i: i['first_seen_at'])

            # Get first activity timestamp
            activity_start = datetime.fromisoformat(user_activities[0]['first_seen_at'])
            activity_end = datetime.fromisoformat(user_activities[0]['answered_at'])

            # Create first session
            session = {
                "started_at": activity_start,
                "ended_at": activity_end,
                "activity_ids": {user_activities[0]['id']},
                "duration_seconds": (activity_end - activity_start) // timedelta(seconds=1)
            }

            # Check session
            for activity in user_activities:
                activity_answered_at = datetime.fromisoformat(activity['answered_at'])
                activity_first_seen_at = datetime.fromisoformat(activity['first_seen_at'])
                minutes_diff = (activity_answered_at - session["started_at"]) // timedelta(minutes=1)

                # Is more than SESSION_MINUTES?
                if minutes_diff < self.SESSION_MINUTES:
                    session["activity_ids"].add(activity['id'])
                    session['ended_at'] = activity_answered_at
                    session['duration_seconds'] = (activity_answered_at - session["started_at"]) // timedelta(seconds=1)
                else:
                    # Add current session and create new one
                    user_sessions[key].append(session)

                    session = {
                        "started_at": activity_first_seen_at,
                        "ended_at": activity_answered_at,
                        "activity_ids": {activity['id']},
                        "duration_seconds": (activity_answered_at - activity_first_seen_at) // timedelta(seconds=1)
                    }

            # Add last session
            else:
                user_sessions[key].append(session)

            # Add result
            self.results.append(user_sessions)

    def send_results(self):
        """
        Save results in server

        :return: None
        """

        pp.pprint(self.results)


if __name__ == '__main__':
    challenge = Challenge()
    challenge.fetch_activities()
    challenge.process_challenges()
    challenge.send_results()
