import requests
import sys
import requests
import json


class ValdForceDecksAPI:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scope: str = "api.forcedecks",
        auth_url: str = "https://security.valdperformance.com/connect/token",
        base_url: str = "https://fdapi.valdperformance.com/v2019q3",
    ):
        """Python class to work with VALD Dashboard API.

        Args:
            client_id (str): The API client_id provided by Vald customer support.
            client_secret (str): The API client_secret provided by Vald customer support.
            scope (str): Scope of the Oauth2 request. Default is api.forcedecks. Yes there's a typo in dashboard.
            auth_url (str): URL for authentication with OAuth2. Defaults to https://security.valdperformance.com/connect/token.
            base_url (str): Base URL for all API requests. Defaults to https://fdapi.valdperformance.com/v2019q3.
        """
        self.scope = scope
        self.auth_url = auth_url
        self.base_url = base_url
        self.token = self._get_token(client_id, client_secret)

    def _get_token(self, client_id: str, client_secret: str):
        """Get a new Oauth2 bearer token.

        Args:
            client_id (str): The API client_id provided by Vald customer support.
            client_secret (str): The API client_secret provided by Vald customer support.
        """

        token_req_payload = {"grant_type": "client_credentials", "scope": self.scope}
        token_response = requests.post(
            self.auth_url,
            data=token_req_payload,
            auth=(client_id, client_secret),
        )
        if token_response.status_code != 200:
            print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        else:
            print("Successfuly obtained a new token")
            tokens = json.loads(token_response.text)
            return tokens["access_token"]

    def _make_request(self, method: str, path: str, parameters: dict = None):
        """Function to standardize requests made to the API.

        Args:
            method (str): Method to use. GET, POST, etc.
            path (str): API path to query.
            parameters (dict, optional): Parameters to pass the queried path. See the official API documentation here: https://dbapi.valdperformance.com/index.html
        """

        url = self.base_url + path
        params = {}
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        s = requests.Session()
        if parameters:
            params.update(parameters)
        response = s.request(method, url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(
                str(response.status_code)
                + ": "
                + response.reason
                + ": "
                + str(response.content)
            )
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def get_teams(self):
        """Returns a collection of Teams."""
        return self._make_request("GET", "/teams")

    def get_team_athletes(self, team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d"):
        """Returns the complete list of all athletes of a given team.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
        """
        return self._make_request("GET", f"/teams/{team_id}/athletes")

    def get_athlete_tests(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        athlete_id: str = "5b054239-93c4-43db-8793-4264c352d6ff",
        page_number: int = 1,
    ):
        """Provides all of the Tests for the provided Team and Athlete Ids, optionally filtered by test last modified date/time. Tests are ordered in descending order, by Record Time. Dates should be specified as UTC in the ISO8601 format e.g yyyy-mm-ddThh:mm:ssZ This endpoint is paged.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            athlete_id (str): The ID of the athlete. Defaults to '5b054239-93c4-43db-8793-4264c352d6ff'.
            page_number (int): The page number to request. Defaults to 1.
        """
        return self._make_request(
            "GET", f"/teams/{team_id}/athlete/{athlete_id}/tests/{page_number}"
        )

    def get_athlete_tests_by_date(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        athlete_id: str = "5b054239-93c4-43db-8793-4264c352d6ff",
        page_number: int = 1,
        date_from: str = "2022-01-01",
        date_to: str = "2022-12-31",
    ):
        """Returns all of the Tests for a given Athlete within the specified date range.
        Tests are ordered in descending order, by Start Time. Dates should be in the ISO8601 format e.g yyyy-mm-dd,

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            athlete_id (str): The ID of the athlete. Defaults to '5b054239-93c4-43db-8793-4264c352d6ff'.
            page_number (int): The page number to request. Defaults to 1.
            date_from (str): The start date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-01-01.
            date_to (str): The end date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-12-31.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/athletes/{athlete_id}/tests/{date_from}/{date_to}/{page_number}",
        )

    def get_team_tests(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        page_number: int = 1,
        modified_from: str = None,
    ):
        """Provides all of the Tests for the provided Team Id, optionally filtered by test last modified date/time. Tests are ordered in descending order, by Record Time. Dates should be specified as UTC in the ISO8601 format e.g yyyy-mm-ddThh:mm:ssZ This endpoint is paged.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            page_number (int): The page number to request. Defaults to 1.
            modified_from (str): The datetime to start filter results with. Defaults to None.
        """
        if modified_from:
            return self._make_request(
                "GET",
                f"/teams/{team_id}/tests/{page_number}",
                parameters={"modifiedFrom": modified_from},
            )
        else:
            return self._make_request("GET", f"/teams/{team_id}/tests/{page_number}")

    def get_team_tests_by_date(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        page_number: int = 1,
        date_from: str = "2022-01-01",
        date_to: str = "2022-12-31",
    ):
        """Returns all of the Tests for a given Team within the specified recording date range.
        Tests are returned in descending order of date and time of recording. Dates should be in the ISO8601 format e.g yyyy-mm-dd.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            page_number (int): The page number to request. Defaults to 1.
            date_from (str): The start date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-01-01.
            date_to (str): The end date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-12-31.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/tests/{date_from}/{date_to}/{page_number}",
        )

    def get_team_tests_summary_by_date(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        page_number: int = 1,
        date_from: str = "2022-01-01",
        date_to: str = "2022-12-31",
    ):
        """Returns a summary list of the Tests recorded in a given Team within the specified recording date range.
        Dates should be in the ISO8601 format e.g yyyy-mm-dd. This endpoint is not paged.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            page_number (int): The page number to request. Defaults to 1.
            date_from (str): The start date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-01-01.
            date_to (str): The end date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-12-31.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/tests/summary/{date_from}/{date_to}/{page_number}",
        )

    def get_team_tests_summary_by_athlete_by_date(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        date_from: str = "2022-01-01",
        date_to: str = "2022-12-31",
    ):
        """Returns summary of the Tests recorded for each athlete in a given Team within the specified recording date range.
        Dates should be in the ISO8601 format e.g yyyy-mm-dd.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            date_from (str): The start date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-01-01.
            date_to (str): The end date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-12-31.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/tests/typesummarybyathlete/{date_from}/{date_to}",
        )

    def get_team_tests_deleted(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        date_from: str = None,
    ):
        """Provides information on all of the Tests deleted for a given Team, optionally filtered by date/time of deletion.
        Dates should be specified as UTC in the ISO8601 format e.g yyyy-mm-ddThh:mm:ssZ This endpoint is not paged.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            date_from (str): The start date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-01-01.
        """
        if date_from:
            return self._make_request(
                "GET",
                f"/teams/{team_id}/tests/deleted/",
                parameters={"deletedFrom": date_from},
            )
        else:
            return self._make_request(
                "GET",
                f"/teams/{team_id}/tests/deleted/",
            )

    def get_team_tests_detailed_by_date(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        date_from: str = "2022-01-01",
        date_to: str = "2022-12-31",
    ):
        """Note: This should be considered a legacy API - the recommended way to retrieve detailed test results is test-by-test using the tests/{testId}/trials endpoint.
        Returns all of the Tests for a given Team recorded within the specified date range with trial and results details. Note that this only returns CMJ/SJ-related results.
        Tests are returned in descending order of date and time of recording. Dates should be in the ISO8601 format e.g yyyy-mm-dd.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            date_from (str): The start date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-01-01.
            date_to (str): The end date in ISO8601 format (yyyy-mm-dd). Defauls to 2022-12-31.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/tests/detailed/{date_from}/{date_to}",
        )

    def get_team_tests_trials(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        test_id: str = "a625dca5-c0f2-4406-b83a-6fd8911b6bad",
    ):
        """Provides all of the Trials for the provided Test Id. Trials are ordered in ascending order, by Start Time.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            test_id (str): The ID of the team. Defaults to 'a625dca5-c0f2-4406-b83a-6fd8911b6bad'.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/tests/{test_id}/trials",
        )

    def get_team_tests_recording(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        test_id: str = "a625dca5-c0f2-4406-b83a-6fd8911b6bad",
        include_sample_data: bool = False,
    ):
        """Returns details of the Test Recording. Set includeSampleData query parameter true to includ the full recording force-time sample data.
        Each sample point is returned by an array of values, the ordering of these values is described in the RecordingDataHeader field.
        Note that the recording includes sample data from all tests performed within the same recording.
        The test trial start and end times indicate the parts of the recording for each trial.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            test_id (str): The ID of the team. Defaults to 'a625dca5-c0f2-4406-b83a-6fd8911b6bad'.
            include_sample_data (bool): True to include sample data within the response, false (default) to return only meta-data..
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/tests/{test_id}/recording",
            parameters={"includeSampleData": include_sample_data},
        )

    def get_team_tests_recording_file(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        test_id: str = "a625dca5-c0f2-4406-b83a-6fd8911b6bad",
    ):
        """Returns details of the Test Recording.
        Set includeSampleData query parameter true to includ the full recording force-time sample data.
        Each sample point is returned by an array of values, the ordering of these values is described in the RecordingDataHeader field.
        Note that the recording includes sample data from all tests performed within the same recording.
        The test trial start and end times indicate the parts of the recording for each trial.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            test_id (str): The ID of the team. Defaults to 'a625dca5-c0f2-4406-b83a-6fd8911b6bad'.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/tests/{test_id}/recording/file",
        )

    def get_team_recording(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        recording_id: str = "a625dca5-c0f2-4406-b83a-6fd8911b6bad",
        include_sample_data: bool = False,
    ):
        """Returns details of a Recording.
        Set includeSampleData query parameter true to includ the full recording force-time sample data.
        Each sample point is returned by an array of values, the ordering of these values is described in the RecordingDataHeader field.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            recording_id (str): The Id of the Recording to retrieve. Defaults to ''.
            include_sample_data (bool): True to include sample data within the response, false (default) to return only meta-data..
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/recordings/{recording_id}",
            parameters={"includeSampleData": include_sample_data},
        )

    def get_team_recording_file(
        self,
        team_id: str = "a9f999be-249f-466a-b98e-b70605adee6d",
        recording_id: str = "a625dca5-c0f2-4406-b83a-6fd8911b6bad",
    ):
        """Returns the full Recording csv data file compressed using gzip.

        Args:
            team_id (str): The ID of the team. Defaults to 'a9f999be-249f-466a-b98e-b70605adee6d'.
            recording_id (str): The Id of the Recording to retrieve. Defaults to ''.
        """
        return self._make_request(
            "GET",
            f"/teams/{team_id}/recordings/{recording_id}/file",
        )
