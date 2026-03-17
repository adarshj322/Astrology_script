import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP

from vedic_calculator import calculate_vedic_chart, calculate_transit

mcp = FastMCP("vedic-astrology", instructions="Vedic Astrology chart calculator using Swiss Ephemeris (Sidereal Lahiri)")


@mcp.tool()
def cast_vedic_chart(
    dob: str,
    time: str,
    lat: float,
    lon: float,
    timezone: str,
    query_date: str = "",
) -> str:
    """
    Calculate a complete Vedic birth chart (Sidereal Lahiri ayanamsha).

    Returns planetary positions with sign, house, nakshatra, pada, dignity,
    combustion, retrograde status, Navamsha (D9), Dashamsha (D10), aspects,
    Vimshottari Dasha periods, detected yogas, and Panchang elements.

    Parameters:
        dob: Date of birth as "YYYY-MM-DD" (e.g. "1990-04-15")
        time: Time of birth as "HH:MM" in 24-hour format (e.g. "14:30")
        lat: Birth latitude as decimal degrees (e.g. 28.6139 for New Delhi)
        lon: Birth longitude as decimal degrees (e.g. 77.2090 for New Delhi)
        timezone: IANA timezone string (e.g. "Asia/Kolkata", "America/New_York")
        query_date: Optional date for Dasha lookup as "YYYY-MM-DD". Defaults to today.
    """
    try:
        result = calculate_vedic_chart(
            dob_str=dob,
            time_str=time,
            lat=lat,
            lon=lon,
            timezone_str=timezone,
            query_date_str=query_date if query_date else None,
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def cast_transit_chart(
    transit_date: str,
    natal_chart_json: str,
    timezone: str = "Asia/Kolkata",
) -> str:
    """
    Calculate planetary transits for a given date overlaid on a natal chart.

    Returns each transit planet's current sign, nakshatra, house from natal Lagna,
    house from natal Moon, Sade Sati status, and Rahu-Ketu transit axis.

    IMPORTANT: You must call cast_vedic_chart first and pass its FULL JSON output
    as the natal_chart_json parameter.

    Parameters:
        transit_date: The date to compute transits for as "YYYY-MM-DD" (e.g. "2026-02-28")
        natal_chart_json: The FULL JSON string output from a previous cast_vedic_chart call
        timezone: IANA timezone string (defaults to "Asia/Kolkata")
    """
    try:
        natal_chart = json.loads(natal_chart_json)
        result = calculate_transit(
            transit_date_str=transit_date,
            natal_chart=natal_chart,
            timezone_str=timezone,
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run()
