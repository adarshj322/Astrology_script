# RishiAI — Vedic Astrology MCP Server

A Vedic astrology engine exposed as an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server, built on the **Swiss Ephemeris** with **Sidereal Lahiri** ayanamsha. Designed to power AI astrologer agents (like the included **RishiAI** persona) with astronomically precise chart data rooted in *Brihat Parashara Hora Shastra* (BPHS).

## Features

- **Natal Chart Casting** — Ascendant (Lagna), all nine Vedic grahas (Sun through Ketu), whole-sign houses, nakshatras with padas, and planetary dignities
- **Divisional Charts** — Navamsha (D9) and Dashamsha (D10) sign placements for every planet
- **Planetary Strength** — Dignity classification (exalted / mooltrikona / own sign / friend / neutral / enemy / debilitated), combustion detection per BPHS orbs, retrograde status, and directional strength (Digbala)
- **BPHS Aspects** — Standard 7th-house aspects for all planets, plus special aspects for Mars (4th/8th), Jupiter (5th/9th), and Saturn (3rd/10th)
- **Vimshottari Dasha** — Full 120-year Mahadasha timeline, with active Mahadasha, Antardasha, and Pratyantardasha for any query date
- **Yoga Detection** — Pancha Mahapurusha, Gajakesari, Budhaditya, Chandra-Mangal, Kemadruma, Adhi Yoga, Raj Yoga, Viparita Raj Yoga, and Neecha Bhanga Raja Yoga
- **Panchang** — Birth Tithi, Vara (weekday lord), Nakshatra, Panchang Yoga, and Karana
- **Transit Overlay** — Current planetary positions mapped to natal houses (from Lagna and Moon), Sade Sati detection with phase, and Rahu-Ketu transit axis

## Architecture

```
mcp_server.py            MCP entry point — exposes cast_vedic_chart & cast_transit_chart
  └── vedic_calculator.py   Core engine — Swiss Ephemeris computations & chart assembly
        ├── constants.py       Zodiac signs, sign lords, nakshatras, dasha years, dignity tables
        ├── nakshatra.py       Nakshatra lookup from longitude
        ├── panchang.py        Tithi, Vara, Yoga, Karana calculations
        ├── yoga.py            Yoga detection logic
        ├── dasha.py           Vimshottari Dasha period computation
        └── dignity.py         Dignity, combustion, digbala, compound relationships
```

## Prerequisites

- **Python 3.10+**
- **Swiss Ephemeris data files** — The `swisseph` package includes bundled ephemeris files. For extended date ranges, download additional files from [astro.com](https://www.astro.com/swisseph/) and set the path via `swe.set_ephe_path()`.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd Astrology_script

# Install dependencies
pip install swisseph pytz mcp
```

## MCP Tools

### `cast_vedic_chart`

Generates a complete Vedic natal chart.

| Parameter | Type | Description |
|-----------|------|-------------|
| `dob` | string | Date of birth — `"YYYY-MM-DD"` |
| `time` | string | Time of birth — `"HH:MM"` (24-hour) |
| `lat` | float | Birth latitude (e.g. `28.6139` for Delhi) |
| `lon` | float | Birth longitude (e.g. `77.2090` for Delhi) |
| `timezone` | string | IANA timezone (e.g. `"Asia/Kolkata"`) |
| `query_date` | string | Optional — date for Dasha lookup, defaults to today |

**Returns:** JSON with `metadata`, `panchang`, `lagna`, `planets` (with dignity, combustion, D9, D10, aspects), `dashas`, and `yogas`.

### `cast_transit_chart`

Calculates planetary transits overlaid on a natal chart.

| Parameter | Type | Description |
|-----------|------|-------------|
| `transit_date` | string | Date to compute transits — `"YYYY-MM-DD"` |
| `natal_chart_json` | string | Full JSON output from `cast_vedic_chart` |
| `timezone` | string | Optional — defaults to `"Asia/Kolkata"` |

**Returns:** JSON with transit `planets` (sign, house from Lagna/Moon, nakshatra), `sade_sati` status, and `rahu_ketu_axis`.

## Usage with Cursor

The project includes a Cursor MCP configuration at `.cursor/mcp.json` that registers the server locally:

```json
{
  "mcpServers": {
    "vedic-astrology": {
      "command": "python3",
      "args": ["mcp_server.py"]
    }
  }
}
```

The included RishiAI system prompt (`.cursor/rules/rishi-ai.mdc`) turns Cursor's AI agent into a Vedic astrologer that calls these tools to fetch precise chart data, then interprets the results following BPHS principles.

## Running Standalone

```bash
python mcp_server.py
```

This starts the MCP server over stdio, ready to accept tool calls from any MCP-compatible client.

## Ayanamsha

All calculations use the **Lahiri (Chitrapaksha)** ayanamsha, the official standard of the Indian government and the most widely used system in Vedic astrology.

## References

- *Brihat Parashara Hora Shastra* — foundational text for Vedic astrology
- [Swiss Ephemeris](https://www.astro.com/swisseph/) — high-precision astronomical computation library
- [Model Context Protocol](https://modelcontextprotocol.io/) — open protocol for AI tool integration

## License

This project is for personal and educational use.
