# DSA Tracker for Rainmeter

A modular, Rainmeter-based tracker for LeetCode and GeeksForGeeks progress.
Features a **Duolingo-inspired streak system** that tracks your daily coding activity.

![Preview](fireon.png)

## Features

- **Streak System**: 
  - Tracks consecutive days of coding.
  - **Duolingo Style**: Streak increments based on time (15h cooldown), not just calendar days.
  - **Strict Reset**: Resets if no problem is solved within 24 hours of the last solve.
  - **Visual Feedback**: Fire icon glows orange when active, turns grey/off when streak is at risk or broken.
- **Multi-Platform**: Tracks LeetCode (GraphQL) and GeeksForGeeks (Scraping/API).
- **Modular**: Python script can be used standalone or with other widgets.
- **Robust**: Handles network failures and API changes gracefully.

## Installation

1. **Install Rainmeter**: [https://www.rainmeter.net/](https://www.rainmeter.net/)
2. **Clone this repo** into your Rainmeter Skins folder:
   ```bash
   cd ~/Documents/Rainmeter/Skins
   git clone https://github.com/yourusername/DSATracker.git
   ```
3. **Configuration**:
   - Rename `config.example.json` to `config.json`.
   - Edit `config.json` and enter your usernames:
     ```json
     {
         "leetcode_username": "your_username",
         "gfg_username": "your_username",
         "output_format": "rainmeter"
     }
     ```
4. **Python Setup**:
   - Ensure Python 3 is installed.
   - If `pythonw` is in your system PATH, it should work out of the box.
   - **Custom Python Path**: If the skin doesn't load stats:
     - Rename `local.inc.example` to `local.inc`.
     - Edit `local.inc` and set `PythonPath` to your `pythonw.exe` location.
5. **Load Skin**: Open Rainmeter, find **DSATracker**, and load `DSATracker.ini`.

## Usage

- **Refresh**: Click the widget area to manually refresh stats.
- **Auto-Update**: Updates automatically every 10 minutes.
- **Streak Rules**:
  - Solve at least one problem every 24 hours to keep the fire burning.
  - Streak increases only once per 15-hour window (prevents farming).

## Files Structure

- `DSATracker.ini`: The Rainmeter skin definition.
- `stats.py`: The core logic (fetches data, calculates streak).
- `config.json`: User configuration (ignored by git).
- `history.json`: Local storage for streak data (generated automatically).
- `variables.inc`: Dynamic variables for the skin (generated automatically).

## License

Creative Commons Attribution-Non-Commercial-Share Alike 3.0
