# This file is part of Astarte.
#
# Copyright 2023 SECO Mind Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

""" Device publication example

This module shows an example usage of the Astarte device SDK.
Here we show how to simply connect your device to Astarte to start publishing on various
interfaces.
All the interfaces we are going to use are located in the `interface` directory and are used as
follows:
1. AvailableSensors: to publish single properties
2. Values: to publish single datastreams
3. Geolocation: to publish an object aggregated datastream

"""
import argparse
import tempfile
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from random import random

from astarte.device import DeviceMqtt

_INTERFACES_DIR = Path(__file__).parent.joinpath("interfaces").absolute()
_CONFIGURATION_FILE = Path(__file__).parent.joinpath("config.toml").absolute()


def main(duration: int, persistency_dir: str):
    """
    Main function
    """

    with open(_CONFIGURATION_FILE, "rb") as config_fp:
        config = tomllib.load(config_fp)
        _DEVICE_ID = config["DEVICE_ID"]
        _REALM = config["REALM"]
        _CREDENTIALS_SECRET = config["CREDENTIALS_SECRET"]
        _PAIRING_URL = config["PAIRING_URL"]

    # Instance the device
    device = DeviceMqtt(
        device_id=_DEVICE_ID,
        realm=_REALM,
        credentials_secret=_CREDENTIALS_SECRET,
        pairing_base_url=_PAIRING_URL,
        persistency_dir=persistency_dir,
    )
    # Load all the interfaces
    device.add_interfaces_from_dir(_INTERFACES_DIR)
    # Connect the device
    device.connect()
    while not device.is_connected():
        pass

    # Set properties
    sensor_id = "b2c5a6ed_ebe4_4c5c_9d8a_6d2f114fc6e5"
    device.send(
        "org.astarte-platform.genericsensors.AvailableSensors",
        f"/{sensor_id}/name",
        "randomThermometer",
    )
    device.send(
        "org.astarte-platform.genericsensors.AvailableSensors",
        f"/{sensor_id}/unit",
        "°C",
    )

    # Sleep for one second
    time.sleep(1)

    # Unset property
    device.send(
        "org.astarte-platform.genericsensors.AvailableSensors",
        "/wrongId/name",
        "randomThermometer",
    )
    device.unset_property("org.astarte-platform.genericsensors.AvailableSensors", "/wrongId/name")

    max_temp = 30

    end_time = time.time() + duration
    while time.time() < end_time:
        now = datetime.now(tz=timezone.utc)

        # Send single datastream
        temp = round(random() * max_temp, 2)
        device.send(
            "org.astarte-platform.genericsensors.Values",
            f"/{sensor_id}/value",
            temp,
            now,
        )

        # Send object aggregated datastream
        geo_data = {
            "accuracy": 1.0,
            "altitude": 331.81,
            "altitudeAccuracy": 1.0,
            "heading": 0.0,
            "latitude": 43.32215,
            "longitude": 11.3259,
            "speed": 0.0,
        }
        device.send_aggregate(
            "org.astarte-platform.genericsensors.Geolocation", "/gps", geo_data, now
        )

        time.sleep(5)


if __name__ == "__main__":
    # Accept an argument to specify a set time duration for the example
    parser = argparse.ArgumentParser(description="Sample for the Astarte device SDK Python")
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=30,
        help="Approximated duration in seconds for the example (default: 30)",
    )
    args = parser.parse_args()

    # Creating a temporary directory
    with tempfile.TemporaryDirectory(prefix="python_sdk_examples_") as temp_dir:
        main(args.duration, temp_dir)
