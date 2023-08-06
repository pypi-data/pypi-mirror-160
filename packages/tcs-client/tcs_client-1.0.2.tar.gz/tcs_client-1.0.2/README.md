# TCS Client

Library to handle TCS (Telescope Control System) commands and work as client.

This library implements a TCP/IP socket following the SCLN protocol, this is 4 bytes to define the message length followed by the message itself using a big-endian and ASCII coding.

It will triggers a TCSError exception on failure, otherwise each command will return a dictionary with two keys, `raw_response` and `response`.
```json
{
  raw_response: "<COMMAND RESPONSE>",
  response: [],
  key1: "value1",
  key2: "value2"
}
```

- `raw_response` value is a string with the TCS response.
- `response` value is a list of all single words received in the TCS response.
- All other strings which match the format `key=value` are splitted and appended to the response dictionary, as shown for `key1` and `key2`, if more than 1 key is received, the next keys will be named `key[i]` with i an increasing index.