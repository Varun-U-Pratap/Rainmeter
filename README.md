# DSATracker 🔥

![DSATracker Banner](https://placehold.co/1200x400/FF9600/141414?text=DSATracker&font=inter)

A sleek, desktop-integrated performance tracker for LeetCode and GeeksForGeeks built with Python and Rainmeter. DSATracker helps users maintain their coding consistency by bringing real-time streak data and problem-solving stats directly to their Windows desktop. This project was developed to gamify the DSA preparation process.

---

## ✨ Features

DSATracker is packed with features designed to provide a seamless and motivational coding track experience.

### Core Functionality
- **Dual-Platform Tracking**: Syncs data from both LeetCode (via GraphQL) and GeeksForGeeks (via optimized Web Scraping) to provide a unified view of your progress.
- **Smart Streak System**: Automatically calculates daily streaks based on calendar activity, ensuring your hard work is visually recognized.
- **Real-Time Problem Counter**: Displays the total number of problems solved across platforms, updated dynamically.
- **Activity "Fire" Indicator**: A Duolingo-inspired visual logic that "lights up" only if you have remained active within the last 24 hours.
- **Local Data Persistence**: Saves all history, streaks, and timestamps locally in `history.json` to reduce API overhead and allow for offline viewing of last-known stats.

### Engineering & Optimization
- **Stability Engine**: Utilizes a Direct Stdout Parser to pass data from Python to Rainmeter instantly, preventing the "UI Jumping" effect found in standard file-based skins.
- **Custom Geometry Drag Handle**: Includes a specialized "hitbox" at the bottom of the widget that follows the curved UI border, allowing for easy repositioning without interfering with click actions.
- **Automated Update Cycle**: A background timer refreshes your stats every 10 minutes, with a manual "click-to-sync" override for instant updates.
- **Low Resource Footprint**: Built to run silently in the background using `pythonw`, consuming negligible CPU and RAM.
- **Logging System**: A robust `debug.log` tracks network requests and script execution to assist in rapid troubleshooting.

### Polished User Experience
- **Sleek & Animated UI**: Modern dark-theme aesthetic with rounded corners and high-contrast typography designed for developer setups.
- **Syncing Visuals**: Clear "Syncing..." status indicators to let the user know when data is being fetched.
- **App Installer Bypass**: Custom environment handling in `local.inc` prevents the Windows Store from interrupting the user when the system is offline.
- **Haptic-Style Visual Cues**: Immediate UI feedback on refresh and interaction.

---

## 🛠️ Tech Stack & Architecture

- **Logic Engine**: Python 3
- **UI Framework**: Rainmeter (Skin DSL)
- **Data Retrieval**: 
  - LeetCode API (GraphQL)
  - GFG Scraper (Regex-based HTML Parsing)
- **Key Python Components**:
  - `urllib.request`: For dependency-free API communication.
  - `json`: For local state management and configuration.
  - `re`: For scraping dynamic web content.
- **Architecture**: A modular system separating UI (Rainmeter), Logic (Python), and User Overrides (Include files).

---

## 🚀 Getting Started

Follow these instructions to get the tracker running on your local machine.

### Prerequisites

- [Rainmeter](https://www.rainmeter.net/) (Windows only).
- [Python 3.x](https://www.python.org/downloads/) (Ensure it is added to your System PATH).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    https://github.com/Varun-U-Pratap/Rainmeter.git
    ```

2.  **Configure your handles:**
    Open `config.json` and enter your platform usernames:
    ```json
    {
        "leetcode_username": "YOUR_LEETCODE_ID",
        "gfg_username": "YOUR_GFG_ID"
    }
    ```

3.  **Configure Python Path:**
    This project uses a direct path to prevent Windows App Store popups.
    - Run `where pythonw` in your command prompt.
    - Open `local.inc` and paste your path:
    ```ini
    [Variables]
    PythonPath="C:\Users\YourName\AppData\Local\Programs\Python\Python312\pythonw.exe"
    ```

4.  **Load the Widget:**
    - Copy the project folder to `Documents\Rainmeter\Skins`.
    - Right-click Rainmeter → Illustro → DSATracker → `DSATracker.ini` -> **Load**.

---

## 🧑‍💻 About the Developer

This project was created by:

- **Varun U Pratap**
  - **LinkedIn**: [https://www.linkedin.com/in/varun-u-pratap-856826340](https://www.linkedin.com/in/varun-u-pratap-856826340)
