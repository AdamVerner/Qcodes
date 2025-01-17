from typing import Any, Callable

from qcodes.parameters import Parameter

from ._AimTTi_PL_P import AimTTi, AimTTiChannel


class AimTTiQL355TP(AimTTi):
    """
    This is the QCoDeS driver for the Aim TTi QL355TP series power supply.
    """

    def __init__(self, name: str, address: str, **kwargs: Any) -> None:
        """
        Args:
            name: Name to use internally in QCoDeS.
            address: VISA resource address
        """

        super().__init__(name, address, **kwargs)

        for channel in [self.ch1, self.ch2]:
            channel.over_voltage_protection = Parameter(
                "over_voltage_protection",
                get_cmd=self._get_value_reader(channel, "OVP"),
                get_parser=float,
                set_cmd=f"OVP{channel.channel} {{}}",
                label="Over voltage protection",
                unit="V",
                instrument=channel,
            )

            channel.over_current_protection = Parameter(
                "over_current_protection",
                get_cmd=self._get_value_reader(channel, "OCP"),
                get_parser=float,
                set_cmd=f"OCP{channel.channel} {{}}",
                label="Over current protection",
                unit="A",
                instrument=channel,
            )

    def _get_value_reader(self, channel: "AimTTiChannel", command: str) -> Callable[[], float]:
        def _value_reader() -> float:
            channel_id = channel.channel
            _value = channel.ask_raw(f"{command}{channel_id}?")
            _value_split = _value.split()
            return float(_value_split[1])
        return _value_reader

    def trip_reset(self) -> None:
        """Clear all trip conditions on the device"""
        self.write("TRIPRST")
