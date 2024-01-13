import aiohttp
import asyncio
import ssl
import re

PATHS = {
    'SYSTEM_INFO': '/gen.info.table.sys.js',
    'MEASUREMENTS': '/gen.measurements.table.js',
    'YIELD_DAY': '/gen.yield.day.chart.js',
    'YIELD_MONTH': '/gen.yield.month.chart.js',
    'YIELD_YEAR': '/gen.yield.year.chart.js',
    'YIELD_TOTAL': '/gen.yield.total.chart.js'
}

class SolarFrontierWebInfoParser:
    """Parser class for Solar Frontier inverter system information."""

    @staticmethod
    def parse_system_info(html_content: str) -> dict:
        """Parse the system information from the inverter's output."""
        info = {}

        # Extract model name
        model_match = re.search(r"<td>Name</td><td>(.*?)</td>", html_content)
        if model_match:
            info["model_name"] = model_match.group(1)

        # Extract nominal power with various unit formats (e.g., W, kW)
        power_match = re.search(r"<td>Nominal Power</td><td>([\d.]+\s?[kM]?W)</td>", html_content)
        if power_match:
            info["nominal_power"] = power_match.group(1)

        return info
    
    @staticmethod
    def parse_measurements(html_content: str) -> dict:
        """Parse the measurements from the inverter's output."""
        name_mapping = {
            "P DC": "dc_power",
            "U DC": "dc_voltage",
            "I DC": "dc_current",
            "U AC1": "ac_voltage_phase_1",
            "U AC2": "ac_voltage_phase_2",
            "U AC3": "ac_voltage_phase_3",
            "I AC1": "ac_current_phase_1",
            "I AC2": "ac_current_phase_2",
            "I AC3": "ac_current_phase_3",
            "F AC": "ac_frequency",
            "F AC1": "ac_frequency_phase_1",
            "F AC2": "ac_frequency_phase_2",
            "F AC3": "ac_frequency_phase_3",
            "P AC": "ac_power",
            "P AC1": "ac_power_phase_1",
            "P AC2": "ac_power_phase_2",
            "P AC3": "ac_power_phase_3"
        }
        units_data = {}
        table_rows = re.findall(r"<tr><td>(.*?)</td><td align='right'>(.*?)</td><td>(.*?)</td></tr>", html_content)
        for name, value, unit in table_rows:
            key = name_mapping.get(name.strip(), name.strip().replace(" ", "_").lower())
            try:
                numeric_value = float(value.strip())
            except ValueError:
                numeric_value = None
            units_data[key] = f"{numeric_value}{unit.strip()}" if numeric_value is not None else None

        return units_data

    @staticmethod
    def parse_yield(html_content: str) -> str:
        """Parse the day yield from the inverter's output."""
        yield_match = re.search(r"document\.getElementById\(\"labelValueId\"\)\.innerHTML\s*=\s*\"[^\"]*?(\d+(\.\d+)?[kM]?Wh)", html_content)
        if yield_match:
            return yield_match.group(1)
        return "Yield value not found"

class WebRequestManager:
    async def get(self, url: str) -> tuple[int, str]:
        """Get the content of a URL."""
        try:
            # Using a single `with` statement for multiple contexts
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            async with aiohttp.ClientSession() as session, session.get(url, timeout=5, ssl=ssl_context) as response:
                html_content = await response.text()
                return response.status, html_content

        except aiohttp.ClientError as e:
            print(f"Connection error: {e}")
        return ""

class SolarFrontierConnectionChecker:
    """Check connection to inverter on LAN."""

    def __init__(self, host: str) -> None:
        """Initialize."""
        self.host = host

    async def connect(self) -> bool:
        """Test if we can connect with the host."""
        url = f"http://{self.host}{PATHS['SYSTEM_INFO']}"

        status, html_content = await WebRequestManager().get(url)
        parser = SolarFrontierWebInfoParser()
        system_info = parser.parse_system_info(html_content)
        return system_info.get('model_name') != None

async def main():
    host = '192.168.50.101'
    checker = SolarFrontierConnectionChecker(host)
    success = await checker.connect()
    print(f"Connection successful: {success}")

    parser = SolarFrontierWebInfoParser()
    day_yield_url = f"http://{host}{PATHS['YIELD_DAY']}"
    month_yield_url = f"http://{host}{PATHS['YIELD_MONTH']}"
    year_yield_url = f"http://{host}{PATHS['YIELD_YEAR']}"
    total_yield_url = f"http://{host}{PATHS['YIELD_TOTAL']}"

    status, html_content = await WebRequestManager().get(f"http://{host}{PATHS['SYSTEM_INFO']}")
    system_info = parser.parse_system_info(html_content)
    print(f"System info: {system_info}")

    status, html_content = await WebRequestManager().get(day_yield_url)
    day_yield = parser.parse_yield(html_content)
    print(f"Day yield: {day_yield}")

    status, html_content = await WebRequestManager().get(month_yield_url)
    month_yield = parser.parse_yield(html_content)
    print(f"Month yield: {month_yield}")

    status, html_content = await WebRequestManager().get(year_yield_url)
    year_yield = parser.parse_yield(html_content)
    print(f"Year yield: {year_yield}")

    status, html_content = await WebRequestManager().get(total_yield_url)
    total_yield = parser.parse_yield(html_content)
    print(f"Total yield: {total_yield}")

    status, html_content = await WebRequestManager().get(f"http://{host}{PATHS['MEASUREMENTS']}")
    measurements = parser.parse_measurements(html_content)
    print(f"Measurements: {measurements}")


# Run the async main function
asyncio.run(main())
