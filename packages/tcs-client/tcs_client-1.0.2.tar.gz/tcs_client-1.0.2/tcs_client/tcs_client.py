#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Diego Gomez, Simon Torres"
__copyright__ = "Copyright 2022, TcsClient"
__credits__ = ['Diego Gomez", "Simon Torres']
__license__ = "GPL"
__maintainer__ = "Diego Gomez"
__email__ = "diego.gomez@noirlab.edu, simon.torres@noirlab.edu"
__status__ = "Development"
__name__ = "TCS Client"

"""
TCS
This library handles the TCS communication, translate instructions to TCS commands and takes appropriate steps
"""

import sys
import argparse
import logging
import json

from argparse import Namespace
from importlib.metadata import version
from importlib.metadata import PackageNotFoundError
from typing import Union, Callable
from time import sleep
from scln_client import SclnClient, SclnClientError

from astropy.coordinates import Angle
from astropy import units as u

try:
    __version__ = version("tcs_client")
except PackageNotFoundError:
    pass


def angle(angle: Union[str, float], f: str = "deg", t: str = "deg"):
    """
    It converts an angle from one format to another

    Args:
      angle (Union[str, float]): The angle to convert.
      f (str): The format of the input angle. Defaults to deg
      t (str): The type of angle you want to convert to. Defaults to deg

    Returns:
      the angle in the desired format.
    """
    if f == "deg" or f == "dms":
        angle = Angle(angle, unit=u.deg)
    elif f == "hms":
        angle = Angle(angle, unit=u.hour)

    if t == "deg":
        return angle.deg
    elif t == "dms":
        return angle.to_string(unit=u.deg, sep=":")
    elif t == "hms":
        return angle.to_string(unit=u.hour, sep=":")


class TcsClientError(Exception):
    pass


class TcsClient:
    """
    TcsClient
    The TcsClient object to carry out functions executions and translations
    """

    def __init__(
        self,
        host: str,
        port: int,
        timeout: float = 1.5,
        max_tx_retries=12,
        max_rx_retries=3,
        max_reconnect_attempts=0,
        max_reconnect_on_message=5,
        connect_on_create=True,
    ):
        """
        The function `__init__` initializes the class `TcsClient` by setting the host, port, and
        timeout, and then initializing the `SclnClient` object, and then calling the `infoa` function

        Args:
          host (str): The IP address of the TCS
          port (int): The port number to connect to.
          timeout (float): The default timeout to tx/rx commands
          max_tx_retries: The number of times to retry sending a command to the TCS. Defaults to 12
          max_rx_retries: The number of times to retry receiving a response from the TCS. Defaults to 3
          max_reconnect_attempts: The number of times to attempt to reconnect to the TCS before giving
        up. Defaults to 0 (no limit)
          max_reconnect_on_message: The maximum number of times to attempt to reconnect to the TCS when
        a message is received. Defaults to 5
          connect_on_create: Flag to decide if connect on object creation
        """
        # External Inputs
        self._logger = logging.getLogger()  # Logger object
        self._host = host  # TCP/IP Host
        self._port = port  # TCP/IP Port
        self._timeout = timeout  # The default timeout to tx/rx commands

        # Variables
        self.info = {}  # Dictionary with TCS info
        self.lamps = {}  # Dictionary with possible lamps
        self.selected_instrument = None  # Current selected instrument
        self.automatic_mount = False  # Current mount state (automatic/manual)

        self._scln = SclnClient(
            self._host,
            self._port,
            timeout=self._timeout,
            max_tx_retries=max_tx_retries,
            max_rx_retries=max_rx_retries,
            max_reconnect_attempts=max_reconnect_attempts,
            max_reconnect_on_message=max_reconnect_on_message,
            connect_on_create=connect_on_create,
        )
        self.infoa()
        self._logger.info(json.dumps(self.info, indent=4))

    def is_connected(self):
        """
        If the connection is not None, then return the connection status

        Returns:
          The is_connected method is being returned.
        """
        if self._scln:
            return self._scln.is_connected
        else:
            return False

    def send_command(self, command: str, timeout: Union[float, None] = None):
        """
        It takes a command string, sends it to the instrument, and returns a dictionary of the response

        Args:
          command (str): The command to send to the device.
          timeout (Union[float, None]): The timeout for the command. If the command doesn't return
        within this time, the command will be aborted.

        Returns:
          A dictionary with the raw response, the response, and the key value pairs.
        """
        res = self._scln.send_command(command, timeout=timeout)
        self._logger.debug(f"Tx Command: {command}")
        self._logger.debug(f"Rx Command: {res}")
        response_dict = {"raw_response": res, "response": []}
        for pair in res.split():
            if "=" in pair:
                key, val = pair.split("=")
                key = key.strip()
                if key in response_dict:
                    key = f"{key}[{sum([1 if k.startswith(key) else 0 for k in response_dict])}]"
                response_dict[key] = val.strip()
            else:
                response_dict["response"].append(pair)
        return response_dict

    def send_command_loop(
        self,
        cmd_name: str,
        parameters: str,
        timeout: Union[float, None],
        retry: Union[int, None] = None,
        active_callback: Union[Callable, None] = None,
        polling_time: float = 0.5,
    ):
        """
        It sends a command to the SCLN server, and if the response is "ACTIVE", it will keep sending the
        command until the response is no longer "ACTIVE"

        Args:
          cmd_name (str): The name of the command to send.
          parameters (str): str
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, an exception will be raised.
          retry (Union[int, None]): How many times to retry the command if it fails.
          active_callback (Union[Callable, None]): A function that will be called every time the command
        is still active.
          polling_time (float): How long to wait between polling the status of the command.

        Returns:
          A dictionary with the following keys:
            - 'response': A list of strings, each string is a line of the response.
            - 'error': A list of strings, each string is a line of the error.
            - 'status': A string, either 'OK' or 'ERROR'.
            - 'command': A string, the command that was sent.
        """
        res = self.send_command(f"{cmd_name} {parameters}", timeout=timeout)
        if res["response"][0] != "ACTIVE":
            return res
        else:
            if active_callback is not None:
                active_callback(res)

        while True:
            try:
                res = self.send_command(f"{cmd_name} STATUS", timeout=timeout)
                if res["response"][0] != "ACTIVE":
                    return res
                else:
                    if active_callback is not None:
                        active_callback(res)
            except SclnClientError as e:
                if retry is not None:
                    if retry == 0:
                        raise SclnClientError(
                            f"Maximum retries reached. Error: {str(e)}"
                        )
                    else:
                        retry -= 1
            if polling_time != 0:
                sleep(polling_time)

    def way(self, timeout: Union[float, None] = None):
        """
        It sends a command to the server and returns the response

        Args:
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within the timeout, a TcsClientError will be raised.

        Returns:
          The raw response from the server.
        """
        try:
            res = self.send_command("WAY", timeout=timeout)
            return res["raw_response"][len("DONE ") :]
        except SclnClientError as e:
            raise TcsClientError(f"WAY command error - {str(e)}")

    def offset(
        self, offset_ra: float, offset_dec: float, timeout: Union[float, None] = None
    ):
        """
        The function sends the command "OFFSET" to the telescope, and then sends the command "MOVE E/W
        offset_ra N/S offset_dec" to the telescope.

        The function returns the string "OFFSET DONE E/W offset_ra N/S offset_dec" if the command is
        successful.

        The function raises an error if the command is not successful.

        Args:
          offset_ra (float): The offset in RA in arcseconds.
          offset_dec (float): The offset in declination in arcseconds.
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The response from the SCLN server.
        """
        try:
            ra = ""
            dec = ""
            if offset_ra == 0 and offset_dec == 0:
                return "OFFSET not needed for offset_ra=0 and offset_dec=0"

            if offset_ra > 0:
                ra = f"E {100 if offset_ra > 100 else abs(offset_ra):.1f}"
            else:
                ra = f"W {100 if offset_ra < -100 else abs(offset_ra):.1f}"

            if offset_dec > 0:
                dec = f"N {100 if offset_dec > 100 else abs(offset_dec):.1f}"
            else:
                dec = f"S {100 if offset_dec < -100 else abs(offset_dec):.1f}"

            res = self.send_command_loop("OFFSET", f"MOVE {ra} {dec}", timeout=timeout)
            if res["response"][0] == "DONE":
                return f"OFFSET DONE {ra} {dec}"
            else:
                raise TcsClientError(f"OFFSET command error - {res['raw_response']}")
        except SclnClientError as e:
            raise TcsClientError(f"OFFSET command error - {str(e)}")

    def focus(
        self,
        value: int,
        move_type: str = "absolute",
        timeout: Union[float, None] = None,
    ):
        """
        The function sends a command to the TCS to move the focuser to a specified position

        Args:
          value (int): The value to move to.
          move_type (str): "absolute" or "relative". Defaults to absolute
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The response from the server.
        """
        try:
            if move_type == "absolute":
                res = self.send_command_loop(
                    "FOCUS", f"MOVEABS {value}", timeout=timeout
                )
            elif move_type == "relative":
                res = self.send_command_loop(
                    "FOCUS", f"MOVEREL {value}", timeout=timeout
                )
            else:
                raise TcsClientError(
                    f"FOCUS command error - Invalid move type {move_type}"
                )

            if res["response"][0] == "DONE":
                return f"FOCUS MOVE successfully - {res['raw_response']}"
            else:
                raise TcsClientError(f"FOCUS command error - {res['raw_response']}")
        except SclnClientError as e:
            raise TcsClientError(f"FOCUS move error - {str(e)}")

    def clm(self, position: str, timeout: Union[float, None] = None):
        """
        It moves the CLM to the specified position, and returns a string with the result

        Args:
          position (str): str
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The return value is a string.
        """
        try:
            position = position.upper()
            if position not in ["IN", "OUT"]:
                raise TcsClientError(f"CLM command error - Invalid position {position}")
            # Get current position
            res = self.send_command("CLM STATUS", timeout=timeout)
            current_position = res["response"][1]
            if current_position == position:
                return f"CLM already {position}"
            elif position == "IN":
                self.guider("DISABLE")
            res = self.send_command_loop("CLM", position, timeout=timeout)
            if res["response"][0] == "DONE":
                return f"CLM succesfully moved {position} - {res['raw_response']}"
            else:
                raise TcsClientError(f"CLM command error - {res['raw_response']}")
        except SclnClientError as e:
            raise TcsClientError(f"CLM command error - {str(e)}")

    def guider(self, state: str, timeout: Union[float, None] = None):
        """
        The function takes a string argument, state, and an optional float argument, timeout. It then
        checks if the state is valid, and if so, sends the command to the TCS. If the command is
        successful, it returns a string with the command and the response. If the command is
        unsuccessful, it raises an error

        Args:
          state (str): str
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The return value is a string.
        """
        try:
            state = state.upper()
            if state not in ["ENABLE", "DISABLE", "PARK", "CENTER"]:
                raise TcsClientError(f"GUIDER command error - Invalid state {state}")
            res = self.send_command_loop("GUIDER", state, timeout=timeout)
            if res["response"][0] == "DONE":
                return f"GUIDER command {state} successfully {res['raw_response']}"
            else:
                raise TcsClientError(f"GUIDER command error - {res['raw_response']}")
        except SclnClientError as e:
            raise TcsClientError(f"GUIDER command error - {str(e)}")

    def whitespot(
        self, percentage: int, turn_on: bool = True, timeout: Union[float, None] = None
    ):
        """
        It turns on the whitespot at a given percentage, or turns it off

        Args:
          percentage (int): int - The percentage of the white spot to turn on.
          turn_on (bool): bool = True. Defaults to True
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The return value is a string.
        """
        try:
            if turn_on:
                res = self.send_command_loop(
                    "WHITESPOT", f"ON {percentage}", timeout=timeout
                )
                if res["response"][0] == "DONE":
                    return f"WHITESPOT successfully turned ON at {percentage} - {res['raw_response']}"
                else:
                    raise TcsClientError(
                        f"WHITESPOT command error - {res['raw_response']}"
                    )
            else:
                res = self.send_command_loop("WHITESPOT", "OFF", timeout=timeout)
                if res["response"][0] == "DONE":
                    return f"WHITESPOT successfully turned OFF - {res['raw_response']}"
                else:
                    raise TcsClientError(
                        f"WHITESPOT command error - {res['raw_response']}"
                    )
        except SclnClientError as e:
            raise TcsClientError(f"WHITESPOT command error - {str(e)}")

    def get_lamp_number(self, name: str):
        """
        This function takes a string as an argument and returns the number of the lamp that matches
        the string

        Args:
          name (str): The name of the lamp to turn on.

        Returns:
          The lamp number.
        """
        try:
            return self.lamps[name]["number"]
        except KeyError:
            raise TcsClientError(
                f"Lamp {name} not found in lamp options {', '.join(self.lamps.keys())}"
            )

    def lamp(
        self,
        lamp: str,
        state: str = "ON",
        percentage: int = 0,
        timeout: Union[float, None] = None,
    ):
        """
        The function takes a lamp name or number, a state (ON or OFF), a percentage (0-100), and a
        timeout. It then checks the current state of the lamp and if it's not the same as the desired
        state, it sends a command to the TCS to change the state

        Args:
          lamp (str): The name of the lamp to turn on or off.
          state (str): ON or OFF. Defaults to ON
          percentage (int): int = 0, timeout: Union[float, None] = None. Defaults to 0
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The return value is a string.
        """
        try:
            state = state.upper()
            if state not in ["ON", "OFF"]:
                raise TcsClientError(f"LAMP command error - Invalid state {state}")
            if type(lamp) is str:
                lamp_number = self.get_lamp_number(lamp)
            elif type(lamp) is int:
                lamp_number = lamp
            elif type(lamp) is float:
                lamp_number = int(lamp)
            else:
                raise TcsClientError(
                    "LAMP command error - Lamp name or lamp number must be provided"
                )

            res = self.send_command(f"LAMP L{lamp_number} STATUS", timeout=timeout)

            current_state = res["response"][2]
            if len(res["response"]) > 4:
                current_percentage = float(res["response"][4])
                if percentage is None:
                    raise TcsClientError(
                        f"LAMP command error - Percentage required for lamp {lamp_number}"
                    )
                else:
                    try:
                        percentage = float(percentage)
                    except ValueError:
                        raise TcsClientError(
                            f"LAMP command error - Percentage is not a number for lamp {lamp_number}"
                        )

                if current_state != state or current_percentage != percentage:
                    res = self.send_command_loop(
                        f"LAMP L{lamp_number}",
                        f"{state} {percentage}",
                        timeout=timeout,
                        retry=10,
                    )
                    if res["response"][0] == "DONE":
                        return f"LAMP {lamp_number} successfully turned {state} at {percentage}"
                    else:
                        raise TcsClientError(
                            f"LAMP command error - {res['raw_response']}"
                        )
                else:
                    return f"LAMP command not needed - Lamp {lamp_number} already {state} at {percentage}"
            else:
                if current_state != state:
                    res = self.send_command_loop(
                        f"LAMP L{lamp_number}", state, timeout=timeout, retry=10
                    )
                    if res["response"][0] == "DONE":
                        return f"LAMP {lamp_number} successfully turned {state}"
                    else:
                        raise TcsClientError(
                            f"LAMP command error - {res['raw_response']}"
                        )
                else:
                    return (
                        f"LAMP command not needed - Lamp {lamp_number} already {state}"
                    )

        except SclnClientError as e:
            raise TcsClientError(f"LAMP command error - {str(e)}")

    def lamps_turn_on(
        self, lamps: Union[dict, list, tuple], timeout: Union[float, None] = None
    ):
        """
        It takes a list of lamps, and turns them on, and turns all other lamps off

        Args:
          lamps (Union[dict, list, tuple]): A dictionary, list or tuple of lamps to turn on.
          timeout (Union[float, None]): The time in seconds to wait for the command to complete.

        Returns:
          A boolean value.
        """
        turned_on = False
        for lamp in self.lamps:
            if lamp in lamps:
                if type(lamps) is dict:
                    res = self.lamp(
                        lamp, state="ON", percentage=lamps[lamp], timeout=timeout
                    )
                elif type(lamps) is tuple or type(lamps) is list:
                    res = self.lamp(lamp, state="ON", timeout=timeout)
                else:
                    raise TcsClientError(
                        "LAMPS OFF command error - Is not a dictionary, list or tuple"
                    )
                if "successfully turned ON" in res:
                    turned_on = True
            else:
                res = self.lamp(lamp, state="OFF", timeout=timeout)
        return turned_on

    def infoa(self, timeout: Union[float, None] = None):
        """
        It reads the TCS status and updates the `self.info` dictionary with the new values

        Args:
          timeout (Union[float, None]): The timeout for the command in seconds.

        Returns:
          The return value is a dictionary with the following keys:
        """
        try:
            res = self.send_command("INFOA", timeout=timeout)
            del res["raw_response"]
            del res["response"]
            if self.info is None:
                self.info = dict(res)
            else:
                for key in res:
                    self.info[key] = res[key]

            if "TCS_INSTRUMENT" in self.info:
                self.selected_instrument = self.info["TCS_INSTRUMENT"]

            if "TCS_SYN" in self.info:
                self.automatic_mount = True if self.info["TCS_SYN"] == "TRUE" else False

            tags = [k for k in self.info.keys() if k.startswith("TAG_")]
            for tag in tags:
                key = self.info[tag]
                if key in self.lamps:
                    # key = "%s[%s]" %(key, sum([1 if k.startswith(key) else 0 for k in self.lamps]))
                    continue
                self.lamps[key] = {
                    "number": int(tag[len("TAG_") :]),
                    "state": self.info[f'LAMP_{int(tag[len("TAG_"):])}'],
                }
            return res

        except SclnClientError as e:
            raise TcsClientError("INFOA command error - " + str(e))

    def rotator(self, state: str, timeout: Union[float, None] = None):
        """
        The function checks the current state of the rotator, and if it's not the desired state, it
        sends a command to change it

        Args:
          state (str): str
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The return value is a string.
        """
        try:
            state = state.upper()
            if state not in ["TRACK_OFF", "TRACK_ON"]:
                raise TcsClientError(f"ROTATOR command error - Invalid state {state}")
            res = self.send_command("ROTATOR STATUS", timeout=timeout)
            if res["response"][0] == "DONE":
                if res["response"][1] != state:
                    res = self.send_command_loop("ROTATOR", state, timeout=timeout)
                    if res["response"][0] == "DONE":
                        return (
                            f"ROTATOR command succesfully done - Rotator set to {state}"
                        )
                    else:
                        raise TcsClientError(
                            f"ROTATOR command error - {res['raw_response']}"
                        )
                else:
                    return (
                        f"ROTATOR command not needed - Rotator already set to {state}"
                    )
            else:
                raise TcsClientError(f"ROTATOR command error - {res['raw_response']}")
        except SclnClientError as e:
            raise TcsClientError(f"ROTATOR command error - {str(e)}")

    def ipa(self, angle: float, timeout: Union[float, None] = None):
        """
        `ipa` sets the instrument position angle (IPA) to the specified angle

        Args:
          angle (float): The angle to set the IPA to.
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within this time, the command will be aborted.

        Returns:
          The return value is a string.
        """
        try:
            angle = float(angle)
            res = self.send_command_loop("IPA", f"MOVE {angle}", timeout=timeout)
            if res["response"][0] == "DONE":
                return f"IPA successfully set to {angle} degrees"
            else:
                raise TcsClientError(f"IPA command error - {res['raw_response']}")
        except ValueError:
            raise TcsClientError("IPA command error - Angle is not a number")

    def target_move(
        self,
        ra: float,
        dec: float,
        epoch: float,
        proper_motion_ra: float,
        proper_motion_dec: float,
        original_target: bool = True,
        timeout: Union[float, None] = None,
    ):
        """
        The function first checks if the target is reachable. If it is, it moves the telescope to the
        target. If it isn't, it recursively moves the telescope to the middle of the current position
        and the target.

        Args:
          ra (float): float
          dec (float): Declination of the target in degrees
          epoch (float): The epoch of the coordinates.
          proper_motion_ra (float): Proper motion in RA in arcsec/year
          proper_motion_dec (float): float
          original_target (bool): bool = True. Defaults to True
          timeout (Union[float, None]): The timeout for the command.

        Returns:
          The original_target flag.
        """
        try:
            res = self.send_command(
                f"TARGET CHECK "
                f"RA={angle(ra, f='deg', t='hms')} "
                f"DEC={angle(dec, f='deg', t='dms')} "
                f"EPOCH={epoch}",
                timeout=timeout,
            )
            if res["response"][0] == "DONE":
                res = self.send_command_loop(
                    "TARGET",
                    f"MOVE RA={angle(ra, f='deg', t='hms')} "
                    f"DEC={angle(dec, f='deg', t='dms')} "
                    f"EPOCH={epoch} "
                    f"DRACOSD={proper_motion_ra} "
                    f"DDEC={proper_motion_dec}",
                    timeout=timeout,
                )
                if res["response"][0] == "DONE":
                    return original_target
                else:
                    raise TcsClientError(
                        f"TARGET command error - {res['raw_response']}"
                    )
            elif res["response"][0] == "WARNING":
                mnt = self.get_mount_position()  # Update mount position
                middle_ra = (angle(mnt["ra"], f="hms", t="deg") + ra) / 2
                middle_dec = (angle(mnt["dec"], f="dms", t="deg") + dec) / 2
                self.target_move(
                    middle_ra,
                    middle_dec,
                    epoch,
                    proper_motion_ra,
                    proper_motion_dec,
                    original_target=False,
                    timeout=timeout,
                )
            else:
                raise TcsClientError(f"TARGET command error - {res['raw_response']}")
        except SclnClientError as e:
            raise TcsClientError(f"TARGET command error - {str(e)}")

    def target(
        self,
        ra: float,
        dec: float,
        epoch: float,
        proper_motion_ra: float,
        proper_motion_dec: float,
        timeout: Union[float, None] = None,
    ):
        """
        The function takes in a bunch of parameters and then moves the telescope to the target
        coordinates

        Args:
          ra (float): float
          dec (float): float
          epoch (float): The epoch of the coordinates.
          proper_motion_ra (float): float, proper_motion_dec: float,
          proper_motion_dec (float): float
          timeout (Union[float, None]): The time in seconds to wait for the telescope to reach the
        target. If None, the telescope will wait indefinitely.

        Returns:
          a string with the target coordinates.
        """
        target_done = False
        while not target_done:
            target_done = self.target_move(
                ra,
                dec,
                epoch,
                proper_motion_ra,
                proper_motion_dec,
                original_target=True,
                timeout=timeout,
            )
        return f"Telescope moved to target coords RA: {ra} - Dec: {dec}"

    def get_mount_position(self, timeout: Union[float, None] = None):
        """
        This function returns the current RA and DEC of the telescope mount

        Args:
          timeout (Union[float, None]): The timeout in seconds.

        Returns:
          A dictionary with the keys 'ra' and 'dec' and the values of the current mount position.
        """
        self.infoa(timeout=timeout)
        return {"ra": self.info["MOUNT_RA"], "dec": self.info["MOUNT_DEC"]}

    def adc(
        self, percentage: int, park: bool = False, timeout: Union[float, None] = None
    ):
        """
        The function takes in a percentage and a boolean value and returns a string

        Args:
          percentage (int): int
          park (bool): bool = False. Defaults to False
          timeout (Union[float, None]): The timeout for the command. If the command is not completed
        within the timeout, the command will be aborted.

        Returns:
          The return value is a string.
        """
        try:
            try:
                percentage = int(percentage)
            except ValueError:
                raise TcsClientError("ADC command error - ADC percentage not numeric")
            if park:
                res = self.send_command_loop("ADC", "PARK", timeout=timeout)
                if res["response"][0] == "DONE":
                    return "ADC PARK successfully"
                else:
                    raise TcsClientError(f"ADC command error - {res['raw_response']}")
            else:
                if 0 <= percentage <= 100:
                    res = self.send_command_loop("ADC", "IN", timeout=timeout)
                    if res["response"][0] == "DONE":
                        res = self.send_command_loop(
                            "ADC", f"MOVE {percentage}", timeout=timeout
                        )
                        if res["response"][0] == "DONE":
                            return f"ADC set successfully IN at {percentage}"
                        else:
                            raise TcsClientError(
                                f"ADC command error - {res['raw_response']}"
                            )
                    else:
                        raise TcsClientError(
                            f"ADC command error - {res['raw_response']}"
                        )
                else:
                    raise TcsClientError(
                        "ADC command error - Percentage should be greather than or equal 0"
                    )
        except SclnClientError as e:
            raise TcsClientError(f"WHITESPOT command error - {str(e)}")


def get_args(arguments: Union[list, None] = None) -> Namespace:
    """
    It parses the command line arguments and returns them as a Namespace object

    Args:
      arguments (Union[list, None]): Union[list, None] = None

    Returns:
      The arguments that are passed to the program.
    """
    parser = argparse.ArgumentParser(
        description=f"Handles the TCS communication"
        f"\n\nCurrent Version: {__version__}"
    )

    parser.add_argument(
        "--host",
        action="store",
        type=str,
        dest="host",
        help="String with tcp/ip socket host of the TCS",
    )

    parser.add_argument(
        "--port",
        action="store",
        type=int,
        dest="port",
        help="Number with tcp/ip socket port of the TCS",
    )

    parser.add_argument(
        "--timeout",
        action="store",
        type=float,
        default=1.5,
        dest="timeout",
        help="Default timeout",
    )

    parser.add_argument(
        "--max-rx-retries",
        action="store",
        type=int,
        default=3,
        dest="max_rx_retries",
        help="Number of attempts to receive a message",
    )

    parser.add_argument(
        "--max-tx-retries",
        action="store",
        type=int,
        default=12,
        dest="max_tx_retries",
        help="Number of attempts to send a message",
    )

    parser.add_argument(
        "--max-reconnect-attempts",
        action="store",
        type=int,
        default=0,
        dest="max_reconnect_attempts",
        help="Number of attempts to connect the TCP socket",
    )

    parser.add_argument(
        "--max-reconnect-on-message",
        action="store",
        type=int,
        default=5,
        dest="max_reconnect_on_message",
        help="Number of attempts to reconnect while receiving a message",
    )

    parser.add_argument(
        "--connect-on-create",
        action="store",
        type=bool,
        default=True,
        dest="connect_on_create",
        help="Flag to decide if connect on instantiation of TcsClient",
    )

    args = parser.parse_args(args=arguments)

    if args.host is None or args.port is None:
        parser.print_help()
        sys.exit(0)

    return args


def tcs_infoa(arguments: Union[list, None] = None):
    """
    It prints out the infoa response from the TCS server.

    Args:
      arguments (Union[list, None]): Union[list, None] = None
    """
    log = logging.getLogger()

    args = get_args(arguments=arguments)
    print("Creating tcs object")
    print(args)
    tcs = TcsClient(
        args.host,
        args.port,
        timeout=args.timeout,
        max_tx_retries=args.max_tx_retries,
        max_rx_retries=args.max_rx_retries,
        max_reconnect_attempts=args.max_reconnect_attempts,
        max_reconnect_on_message=args.max_reconnect_on_message,
        connect_on_create=args.connect_on_create,
    )
    print("Created")

    try:
        while not tcs.is_connected():
            sleep(1)
        res = tcs.infoa()
        log.info(json.dumps(res, indent=2))
        print(json.dumps(res, indent=2))
    except KeyboardInterrupt:
        print("Goodbye")
        sys.exit(0)
