<!--
Copyright 2023 SECO Mind Srl

SPDX-License-Identifier: Apache-2.0
-->

# Astarte device SDK Python GRPC example
This is an example of how to use the device SDK to connect a to an existing Astarte message hub
instance and handle datastream messages from/to the node.

## Prerequisites

An instance of the message hub should be running on an available machine. See the
[documentation](https://docs.rs/astarte-message-hub/latest/astarte_message_hub/) for the
Astarte message hub for more information.

## Usage
### Configuration file
Before running the example the configuration file `config.toml` should be updated to contain user
specific configuration.

```toml
SERVER_ADDR = "<SERVER_ADDR>"
NODE_UUID = "<NODE_UUID>"
```

The `SERVER_ADDR` should be set to the address of the message hub. For example for an instance
of the message hub running on the same host and using the socket port `50051` a valid value
would be `localhost:50051`.
The `NODE_UUID` can be choosed from the user and should be the string representation of an UUID.

### 3. Running the example

To run the example the Astarte device SDK should be installed. Installing the latest release can be
done through pip with:
```shell
pip install astarte-device-sdk
```
Then to start the example run in the example directory the following command:
```shell
python main.py
```
