"""richsmi.py"""

import time
from datetime import datetime
from shutil import get_terminal_size
from typing import Iterable, Optional

from librichsmi import NvmlWrapper
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.padding import PaddingDimensions
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich.table import Table
from rich.text import Text
from tap import Tap

from . import filesize


class ArgumentParser(Tap):
    loop: Optional[float] = None  # Interval seconds. If not specified, show only once.
    id: Optional[int] = None  # Target a specific GPU. If not specified, show all GPU info.


class Header:
    """Display header with clock."""

    def __init__(self, nvml_version: str, timestamp: datetime) -> None:
        self.nvml_version = nvml_version
        self.timestamp = timestamp

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            f"[b]H-SMI[/] powered by NVML {self.nvml_version}",
            self.timestamp.ctime().replace(":", "[blink]:[/]"),
        )

        return Panel(grid, style="white", box=box.SQUARE)


class Footer:
    """Display footer."""

    def __init__(self, driver_version: str, cuda_version: int) -> None:
        self.driver_version = driver_version
        self.cuda_version = cuda_version

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="right")
        grid.add_row(
            Text(f"Copyright © {datetime.now().year} ") +
            Text("urasakikeisuke", style="link https://github.com/urasakikeisuke"),
            Text(f"Driver Version {self.driver_version} CUDA Version {self.cuda_version}"),
        )

        return Panel(grid, style="bright_black", box=box.SQUARE)


class RichSMI:
    def __init__(
        self,
        loop: Optional[float] = None,
        id: Optional[int] = None,
    ) -> None:
        self.console = Console()
        self.layout = self.make_layout()

        try:
            self.nvml = NvmlWrapper()
        except RuntimeError:
            self.console.print_exception(width=get_terminal_size().columns)

        self.header = Header(self.nvml.get_nvml_version(), self.nvml.get_timestamp())
        self.layout["header"].update(self.header)
        self.layout["footer"].update(Footer(self.nvml.get_driver_version(), self.nvml.get_cuda_version()))

        self.loop = loop
        self.gpu_id = id

    def make_layout(self) -> Layout:
        """Define the layout."""

        layout = Layout(name="root")

        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        layout["main"].split_column(
            Layout(name="main_0"),
            Layout(name="main_1"),
            Layout(name="main_2"),
        )
        layout["main_0"].split_row(Layout(name="memory", ratio=10), Layout(name="clock", ratio=6))
        layout["main_1"].split_row(Layout(name="utilization", ratio=2), Layout(name="power", ratio=2),
                                   Layout(name="temperature", ratio=1), Layout(name="fan_speed", ratio=1))
        layout["main_2"].split_row(Layout(name="compute_procs"), Layout(name="graphics_procs"))

        return layout

    def render_file_unit(self, completed: int, total: Optional[int] = None) -> Text:
        """
        Calculate common unit for completed and total.
        Borrowed from https://github.com/Textualize/rich
        """

        unit_and_suffix_calculation_base = (
            int(total) if total is not None else completed
        )
        unit, suffix = filesize.pick_unit_and_suffix(
            unit_and_suffix_calculation_base,
            ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"],
            1024,
        )

        precision = 0 if unit == 1 else 1

        completed_ratio = completed / unit
        completed_str = f"{completed_ratio:,.{precision}f}"

        if total is not None:
            total = int(total)
            total_ratio = total / unit
            total_str = f"{total_ratio:,.{precision}f}"

            completed_txt = Text(f"{completed_str}", style=self.get_style(completed / total * 100.))
            return completed_txt + Text(f"/{total_str} {suffix}", style="white")
        else:
            return Text(f"{completed_str}", style="bright_green") + Text(f" {suffix}", style="white")

    def render_energy_unit(self, energy: float) -> Text:
        """
        Calculate common unit for completed and total.
        Borrowed from https://github.com/Textualize/rich
        """

        unit, suffix = filesize.pick_unit_and_suffix(
            int(energy),
            ["J", "kJ", "MJ", "GJ", "TJ", "PJ", "EJ", "ZJ", "YJ"],
            1000,
        )

        precision = 0 if unit == 1 else 1

        energy_ratio = energy / unit
        energy_str = f"{energy_ratio:,.{precision}f}"

        return Text(f"{energy_str}", style="bright_green") + Text(f" {suffix}", style="white")

    def get_style(self, percent: float) -> str:
        style = "bright_green"
        if 50.0 < percent <= 80.0:
            style = "bright_yellow"
        elif percent > 80.0:
            style = "bright_red"

        return style

    def create_table(self, headers: Iterable, padding: PaddingDimensions = 0) -> Table:
        table = Table(expand=True, padding=padding, box=box.SIMPLE)

        for header in headers:
            table.add_column(header, justify="left", no_wrap=True)

        return table

    def update_memory_panel(self) -> None:
        gpu_names = self.nvml.get_gpu_names()
        memories = self.nvml.get_memories()

        memory_table = self.create_table(
            ["[b]GPU ID[/]", "[b]GPU Name[/]", "[b]Usage[/]", "[b]Percent[/]", "[b]Used/Total[/]"])

        for i, memory in enumerate(memories):
            used = memory["used"]
            total = memory["used"] + memory["free"]
            percent = used / total * 100.

            memory_bar = Progress(BarColumn(complete_style=self.get_style(percent)))
            memory_bar.add_task(f"{i}", completed=used, total=total)
            memory_table.add_row(Text(f"{i}", style="bright_magenta"), Text(f"{gpu_names[i]}", style="bright_cyan"), memory_bar,
                                 Text(f"{percent:>3.0f}", style=self.get_style(percent)) + Text(" %", style="white"), self.render_file_unit(used, total))

        memory_panel = Panel(memory_table, title=":cd: Memory Usage :cd:",
                             title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["memory"].update(memory_panel)

    def update_utilization_panel(self) -> None:
        utilizations = self.nvml.get_utilizations()

        utilization_table = self.create_table(["[b]GPU ID[/]", "[b]GPU Util.[/]", "[b]Memory Util.[/]"])

        for i, utilization in enumerate(utilizations):
            utilization_table.add_row(
                Text(f"{i}", style="bright_magenta"),
                Text(f"{utilization['gpu']}", style=self.get_style(utilization['gpu'])) + Text(" %", style="white"),
                Text(f"{utilization['memory']}", style=self.get_style(
                    utilization['memory'])) + Text(" %", style="white")
            )

        utilization_panel = Panel(utilization_table, title=":chart_increasing: Utilization :chart_increasing:",
                                  title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["utilization"].update(utilization_panel)

    def update_clock_panel(self) -> None:
        clocks = self.nvml.get_clocks()

        clock_table = self.create_table(["[b]GPU ID[/]", "[b]Graphics[/]", "[b]Memory[/]", "[b]SM[/]", "[b]Video[/]"])

        for i, clock in enumerate(clocks):
            clock_table.add_row(
                Text(f"{i}", style="bright_magenta"),
                Text(f"{clock['graphics']}", style="bright_green") + Text(" MHz", style="white"),
                Text(f"{clock['memory']}", style="bright_green") + Text(" MHz", style="white"),
                Text(f"{clock['sm']}", style="bright_green") + Text(" MHz", style="white"),
                Text(f"{clock['video']}", style="bright_green") + Text(" MHz", style="white"),
            )

        clock_panel = Panel(clock_table, title=":clock8: Clock :clock8:",
                            title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["clock"].update(clock_panel)

    def update_power_panel(self) -> None:
        powers = self.nvml.get_powers()

        power_table = self.create_table(["[b]GPU ID[/]", "[b]Usage/Limit[/]", "[b]Total Energy[/]"])

        for i, power in enumerate(powers):
            usage = power['usage']
            limit = power['limit']
            percent = usage / limit * 100.

            power_table.add_row(
                Text(f"{i}", style="bright_magenta"),
                Text(f"{usage:.1f}", style=self.get_style(percent)) + Text(f"/{limit:.1f} W", style="white"),
                self.render_energy_unit(power["energy"]),
            )

        power_panel = Panel(power_table, title=":high_voltage: Power :high_voltage:",
                            title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["power"].update(power_panel)

    def update_temperature_panel(self) -> None:
        temperatures = self.nvml.get_temperatures()

        temperature_table = self.create_table(["[b]GPU ID[/]", "[b]Temp.[/]"])

        for i, temperature in enumerate(temperatures):
            board = temperature['board']
            slowdown = temperature['thresh_slowdown']
            shutdown = temperature['thresh_shutdown']

            style = "bright_green"
            warning = ""
            if slowdown < board <= shutdown:
                style = "bright_yellow"
                warning = "(Thermal Throttling) "
            elif shutdown < board:
                style = "bright_red"
                warning = "(Thermal Throttling) "

            temperature_table.add_row(
                Text(f"{i}", style="bright_magenta"),
                Text(f"{board} {warning}", style=style) + Text(f"℃", style="white"),
            )

        temperature_panel = Panel(temperature_table, title=":thermometer: Temperature :thermometer:",
                                  title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["temperature"].update(temperature_panel)

    def update_fan_speed_panel(self) -> None:
        fan_speeds = self.nvml.get_fan_speeds()

        fan_speed_table = self.create_table(["[b]GPU ID[/]", "[b]Speed[/]"])

        for i, fan_speed in enumerate(fan_speeds):
            speed = fan_speed['speed']

            fan_speed_table.add_row(
                Text(f"{i}", style="bright_magenta"),
                Text(f"{speed}", style=self.get_style(speed)) + Text(f" %", style="white"),
            )

        fan_speed_panel = Panel(fan_speed_table, title=":leaf_fluttering_in_wind: Fan Speed :leaf_fluttering_in_wind:",
                                title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["fan_speed"].update(fan_speed_panel)

    def update_compute_procs_panel(self) -> None:
        all_procs = self.nvml.get_compute_procs()

        compute_procs_table = self.create_table(
            ["[b]GPU ID[/]", "[b]PID[/]", "[b]Name[/]", "[b]Memory Usage[/]"])

        for gpu_id, procs in enumerate(all_procs):
            for proc in procs:
                name, pid, memory = proc
                name = name.strip('\n')
                compute_procs_table.add_row(
                    Text(f"{gpu_id}", style="bright_magenta"),
                    Text(f"{pid}", style="bright_black"),
                    Text(f"{name}", style="bright_blue"),
                    self.render_file_unit(memory),
                )

        compute_procs_panel = Panel(compute_procs_table, title=":memo: Compute Processes :memo:",
                                    title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["compute_procs"].update(compute_procs_panel)

    def update_graphics_procs_panel(self) -> None:
        all_procs = self.nvml.get_graphics_procs()

        graphics_procs_table = self.create_table(
            ["[b]GPU ID[/]", "[b]PID[/]", "[b]Name[/]", "[b]Memory Usage[/]"])

        for gpu_id, procs in enumerate(all_procs):
            for proc in procs:
                name, pid, memory = proc
                name = name.strip('\n')
                graphics_procs_table.add_row(
                    Text(f"{gpu_id}", style="bright_magenta"),
                    Text(f"{pid}", style="bright_black"),
                    Text(f"{name}", style="bright_blue"),
                    self.render_file_unit(memory),
                )

        graphics_procs_panel = Panel(graphics_procs_table, title=":paintbrush: Graphics Processes :paintbrush:",
                                     title_align="left", border_style="#7be9e0", padding=(1, 2, 1, 2), box=box.SQUARE)
        self.layout["graphics_procs"].update(graphics_procs_panel)

    def call_once(self) -> None:
        self.nvml.query(False)

        # Update timestamp
        timestamp = self.nvml.get_timestamp()
        self.header.timestamp = timestamp

        # Memory
        self.update_memory_panel()

        # Utilization
        self.update_utilization_panel()

        # Clock
        self.update_clock_panel()

        # Power
        self.update_power_panel()

        # Temperature
        self.update_temperature_panel()

        # Fan Speed
        self.update_fan_speed_panel()

        # Compute Process
        self.update_compute_procs_panel()

        # Graphics Process
        self.update_graphics_procs_panel()

    def call(self) -> None:
        with Live(self.layout, console=self.console, refresh_per_second=30, screen=False if self.loop is None else True):
            while True:
                self.call_once()

                if self.loop is None:
                    break
                else:
                    time.sleep(self.loop)


def main():
    args = ArgumentParser(underscores_to_dashes=True).parse_args()

    app = RichSMI(args.loop, args.id)

    try:
        app.call()
    except KeyboardInterrupt:
        pass
    except:
        app.console.print_exception()


if __name__ == "__main__":
    main()
