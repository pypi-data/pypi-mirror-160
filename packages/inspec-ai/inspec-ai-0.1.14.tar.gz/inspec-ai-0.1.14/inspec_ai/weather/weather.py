import requests
import datetime
from typing import Union
import pandas as pd
from requests.adapters import HTTPAdapter, Retry
import logging
import re


class Weather:
    def __init__(
        self,
        access_token: str,
    ):
        self.headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json", "accept": "application/json"}

        self.url = "https://inspec-meteo-dev-app.azurewebsites.net/Weather"

        self.periodicities = ["H", "D", "W", "M", "W-MON", "W-TUE", "W-WED", "W-THU", "W-FRI", "W-SAT", "W-SUN"]

        self.possible_features = [
            "temperature",
            "wind",
            "temperaturefeels",
            "dewpoint",
            "humidity",
            "pressure",
            "winddir",
            "windspeedgust",
            "sky",
            "precipitation",
            "snow",
            "solarrad",
            "weathercoded",
            "weatherprimarycoded",
            "cloudscoded",
            "isday",
        ]

        self.periodicity_features = {
            "H": [
                "temperature",
                "wind",
                "temperaturefeels",
                "dewpoint",
                "humidity",
                "pressure",
                "winddir",
                "windspeedgust",
                "sky",
                "precipitation",
                "snow",
                "solarrad",
                "weathercoded",
                "weatherprimarycoded",
                "cloudscoded",
                "isday",
            ],
            "D": [
                "temperature",
                "wind",
                "temperaturefeels",
                "dewpoint",
                "humidity",
                "pressure",
                "winddir",
                "windspeedgust",
                "sky",
                "precipitation",
                "snow",
                "solarrad",
            ],
            "W": [
                "temperature",
                "wind",
                "temperaturefeels",
                "dewpoint",
                "humidity",
                "pressure",
                "winddir",
                "windspeedgust",
                "sky",
                "precipitation",
                "snow",
                "solarrad",
            ],
            "M": [
                "temperature",
                "wind",
                "temperaturefeels",
                "dewpoint",
                "humidity",
                "pressure",
                "winddir",
                "windspeedgust",
                "sky",
                "precipitation",
                "snow",
                "solarrad",
            ],
        }

        self.aggregations = {
            "temperature": ["avg", "max", "min", "spread"],
            "wind": ["avg", "max", "min", "spread"],
            "temperaturefeels": ["avg", "max", "min", "spread"],
            "dewpoint": ["avg", "max", "min", "spread"],
            "humidity": ["avg", "max", "min", "spread"],
            "pressure": ["avg", "max", "min", "spread"],
            "winddir": ["avg", "max", "min", "spread"],
            "windspeedgust": ["avg", "max", "min", "spread"],
            "sky": ["avg", "max", "min", "spread"],
            "precipitation": ["avg", "max", "min", "spread", "sum"],
            "snow": ["avg", "max", "min", "spread", "sum"],
            "solarrad": ["avg", "max", "min", "spread", "sum"],
        }

        self.earliest_date = datetime.datetime.fromisoformat("2011-04-01T00:00:00+00:00")

    def get_weather(
        self,
        coordinates: Union[dict, list],
        start_date: str = None,
        end_date: str = None,
        timezone_offset=None,
        periodicity="H",
        features=None,
        verbose=True,
    ):

        """Retrieve weather information
           Args:
               coordinates: list of dict or one dictionary with lat: double representing the latitude of the desired location
                            and long: double representing the longitude of the desired location, {'lat':45,'long':-75}
               start_date: string in iso format: YYYY-MM-DDTHH:MM:SS-HH:MM or YYYY-MM-DDTHH:MM:SS+HH:MM
               end_date: start_date: string in iso format: YYYY-MM-DDTHH:MM:SS-HH:MM or YYYY-MM-DDTHH:MM:SS+HH:MM
               timezone_offset: string for the timezone offset, ex: +01:30 or -05:00
               periodicity: string representing the time aggregation. Choice is among: "H", "D", "W", "M",
               "W-MON", "W-TUE", "W-WED", "W-THU", "W-FRI", "W-SAT", "W-SUN"
               features: list of features
               verbose: Whether to print the detailed results when available.
        Returns: A dataframe containing the results aggregated
        """

        start_date, end_date, coordinates, timezone_offset, features = self._normalize_parameters(
            start_date, end_date, coordinates, timezone_offset, features, periodicity
        )

        start_str, end_str, coordinates, periodicity, features, timezone_offset = self._verify_query(
            start_date, end_date, coordinates, periodicity, features, timezone_offset
        )

        query = []
        offset = timezone_offset[0]
        for i in range(len(coordinates)):
            el = coordinates[i]
            if len(timezone_offset) > 1:
                offset = timezone_offset[i]
            query.append(
                {
                    "from": f"{start_str}",
                    "to": f"{end_str}",
                    "lat": el["lat"],
                    "long": el["long"],
                    "periodicity": periodicity,
                    "timeOffset": offset,
                    "features": features,
                }
            )

        logging.basicConfig(level=logging.DEBUG)
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504], method_whitelist=["POST"])
        s.mount("http://", HTTPAdapter(max_retries=retries))

        response = s.post(self.url, headers=self.headers, json=query)

        if response.status_code in [401, 403]:
            raise Exception("Please verify that the token used when constructing the Weather class is valid")

        try:
            dfs = [pd.json_normalize(data) for data in response.json()]
            df = pd.concat(dfs)
            df.columns = [col.split(".")[1] if len(col.split(".")) > 1 else col.split(".")[0] for col in df.columns]

            df["datetime"] = pd.to_datetime(df["datetime"])
            df["is_forecast"] = df["datetime"] > datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

            if verbose:
                print(f"Response time: {response.elapsed.total_seconds()}")
                print(f"Successfully fetched {df.shape[0]} values for {df.shape[1] - 4} features")
                if len(df.loc[:, df.isna().any()].columns):
                    print("The columns", df.loc[:, df.isna().any()].columns.to_list(), "contain null values")
                    print("The number of rows containing null values is: ", df[df.isna().any(axis=1)].shape[0])
                    print("The dates which contain null values are: ", df[df.isna().any(axis=1)]["datetime"].to_list())
                else:
                    print("The dataframe contains no null values")
            return df

        except Exception:
            raise Exception(response.text)

    # Normalize parameters
    def _normalize_parameters(self, start_date, end_date, coordinates, timezone_offset, features, periodicity):

        if coordinates is None:
            raise Exception("Please provide coordinates")

        if type(coordinates) is dict:
            coordinates = [coordinates]

        utc_now = datetime.datetime.utcnow()

        if start_date is None:
            start_date = (datetime.datetime.utcnow() - datetime.timedelta(7)).isoformat()
        if end_date is None:
            end_date = utc_now.isoformat()

        if timezone_offset is None:
            timezone_offset = "+00:00"
            print(
                "\nWARNING: No timezone offset was specified, default set to UTC+0. The daily, weekly and monthly "
                "aggregations will be made using the start and end of the day in UTC+0 time."
            )

        if type(timezone_offset) is str:
            timezone_offset = [timezone_offset]

        if periodicity.upper() not in self.periodicities:
            raise Exception(f"Periodicity {periodicity} not supported")
        if features is None:
            features = self.periodicity_features[periodicity.split("-")[0].upper()]

        return start_date, end_date, coordinates, timezone_offset, features

    # Verify request parameters
    def _verify_query(self, start_date, end_date, coordinates, periodicity, features, timezone_offset):

        start_str, end_str = self._check_start_end_dates(start_date, end_date)

        for tz_offset in timezone_offset:
            try:
                sign, hours, minutes = re.match(r"([+\-]?)(\d{2}):(\d{2})", tz_offset).groups()
                sign = -1 if sign == "-" else 1
                hours, minutes = int(hours), int(minutes)
                datetime.timezone(sign * datetime.timedelta(hours=hours, minutes=minutes))
            except Exception:
                raise Exception(f"The timezone offset: {tz_offset} was not provided in the correct format, eg: +03:00")

        self._check_coordinates(coordinates)

        if len(timezone_offset) not in [1, len(coordinates)]:
            raise Exception(
                "Please provide either one timezone offset that will be applied to all locations "
                "or a list of timezone offsets corresponding to each coordinates, in the same order."
            )

        period_parts = periodicity.split("-")

        if features is not None:
            for feat in features:
                parts = feat.split("-")
                if parts[0].lower() not in self.possible_features:
                    raise Exception(f"Feature {parts[0]} not available")
                if parts[0].lower() not in self.periodicity_features[period_parts[0].upper()]:
                    raise Exception(f"Feature {parts[0]} not available for this periodicity")
                if len(parts) > 1:
                    if parts[1].lower() not in self.aggregations[parts[0].lower()]:
                        raise Exception(f"Aggregation {parts[1]} not available for {parts[0]}")

        return start_str, end_str, coordinates, periodicity, features, timezone_offset

    def _check_coordinates(self, coordinates):

        if type(coordinates) is not list:
            raise Exception("Coordinates must be a dictionary containing the latitude and longitude or a list of coordinates")

        if len(coordinates) == 0:
            raise Exception("Please provide coordinates")

        for element in coordinates:
            if (len(element.keys()) != 2) or ("lat" not in element.keys()) or ("long" not in element.keys()):
                raise Exception(f"The provided location {element} is invalid, eg of correct format: {{'lat': 43,'long': 18}}")
            if element["lat"] > 90 or element["lat"] < -90 or element["long"] > 180 or element["long"] < -180:
                raise Exception(f"The provided location is invalid: lat: {element['lat']}, long: {element['long']}")

    def _check_start_end_dates(self, start_date, end_date):
        try:
            start_obj, end_obj = datetime.datetime.fromisoformat(start_date), datetime.datetime.fromisoformat(end_date)
        except ValueError:
            raise Exception("Please provide the start and end date in isoformat, ex:2022-05-25T14:25:00 ")

        utc_now = datetime.datetime.utcnow()

        max_forecast = (utc_now + datetime.timedelta(days=15)).replace(tzinfo=datetime.timezone.utc)
        end_obj_utc = (datetime.datetime.utcfromtimestamp(end_obj.timestamp())).replace(tzinfo=datetime.timezone.utc)

        LOCAL_TIMEZONE = datetime.datetime.now().astimezone().tzinfo
        if not start_obj.tzinfo:
            start_obj = start_obj.replace(tzinfo=LOCAL_TIMEZONE)
            print(f"\nWARNING: No timezone was specified for the start date, default set to your local time zone: {start_obj.strftime('%Z %z')}")

        # Save timezone info
        end_tzinfo = end_obj.tzinfo
        if not end_tzinfo:
            end_obj = end_obj.replace(tzinfo=LOCAL_TIMEZONE)
            print(f"\nWARNING: No timezone was specified for the end date, default set to your local time zone: {end_obj.strftime('%Z %z')}")

        if end_obj_utc > max_forecast:
            end_obj = max_forecast
            if not end_tzinfo:
                end_obj = end_obj.astimezone(LOCAL_TIMEZONE)
            else:
                end_obj = end_obj.astimezone(end_tzinfo)
            print(f"\nWARNING: Forecast only available until {end_obj}")

        if start_obj < self.earliest_date:
            raise Exception(f"Historical data is not available before {self.earliest_date}")

        if start_obj > end_obj:
            raise Exception("Start date must be earlier than end date")

        return start_obj.isoformat(), end_obj.isoformat()
