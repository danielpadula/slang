# This is a Coding Challenge for Slang!


class Challenge:
    """This is the coding challenge base class.

    This class has three methods, one for fetching activities from source, process it and send results back.
    """
    activities: list
    results: list
    SESSION_MINUTES = 5
    BASE_URL = ""

    def __init__(self):
        self.activities = []
        self.results = []

    def fetch_activities(self):
        """
        Fetch activities from server

        :return: None
        """
        pass

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
