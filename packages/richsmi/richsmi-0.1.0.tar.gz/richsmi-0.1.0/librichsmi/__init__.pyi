"""Python binding of librichsmi"""

from __future__ import annotations
import librichsmi
from typing import List, Dict, Tuple
import datetime

__all__ = [
    "NvmlWrapper"
]


class NvmlWrapper():
    def __init__(self) -> None: ...

    def get_clocks(self) -> List[Dict[str, int]]:
        """get clock info

        Returns:
            List[Dict[str, int]]: clock info of respective gpus. key: `graphics` `memory` `sm` `video`
        """

    def get_compute_procs(self) -> List[List[Tuple[str, int, int]]]:
        """get compute procs info

        Returns:
            List[List[Tuple[str, int, int]]]: compute procs info of respective gpus. (`name` `pid` `memory`)
        """

    def get_cuda_version(self) -> str:
        """get cuda version

        Returns:
            str: cuda version
        """

    def get_driver_version(self) -> str:
        """get driver version

        Returns:
            str: nvidia driver version
        """

    def get_fan_speeds(self) -> List[Dict[str, int]]:
        """get fan speed info

        Returns:
            List[Dict[str, int]]: fan speed info of respective gpus. key: `speed`
        """

    def get_gpu_names(self) -> List[str]:
        """get gpu names

        Returns:
            List[str]: device name of respective gpus
        """

    def get_graphics_procs(self) -> List[List[Tuple[str, int, int]]]:
        """get graphics procs info

        Returns:
            List[List[Tuple[str, int, int]]]: graphics procs info of respective gpus. (`name` `pid` `memory`)
        """

    def get_memories(self) -> List[Dict[str, int]]:
        """get memory info

        Returns:
            List[Dict[str, int]]: memory info of respective gpus. key: `free` `used` `total`
        """

    def get_nvml_version(self) -> str:
        """get nvml version

        Returns:
            str: nvml version
        """

    def get_powers(self) -> List[Dict[str, float]]:
        """get power info

        Returns:
            List[Dict[str, float]]: power info of respective gpus. key: `limit` `usage` `energy`
        """

    def get_temperatures(self) -> List[Dict[str, int]]:
        """get temperature info

        Returns:
            List[Dict[str, int]]: temperature info of respective gpus. key: `board` `thresh_shutdown` `thresh_slowdown`
        """

    def get_timestamp(self) -> datetime.datetime:
        """get timestamp

        Returns:
            datetime.datetime: timestamp
        """

    def get_utilizations(self) -> List[Dict[str, int]]:
        """get utilization info

        Returns:
            List[Dict[str, int]]: utilization info of respective gpus. key: `gpu` `memory`
        """

    def query(self, init: bool = False) -> None:
        """Query GPU infos. Must call to update infos.

        Args:
            init (bool): if `true`, update static info
        """
    pass
