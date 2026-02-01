# DSA Tracker for Rainmeter

![DSATracker Banner](https://placehold.co/1200x400/FF9600/141414?text=DSATracker&font=inter)![DSA Tracker Preview](fireon.png)![DSA Tracker Preview](fireoff.png)

A **modular Rainmeter-based DSA progress tracker** for **LeetCode** and **GeeksForGeeks**, featuring a **Duolingo-inspired streak system** that rewards real consistency instead of calendar abuse.

Designed for developers who want **visible discipline**, not vanity stats.

---

## ✨ Features

### 🔥 Duolingo-Style Streak System
- Tracks **consecutive coding activity** using real timestamps
- **15-hour cooldown window** to prevent artificial streak farming
- **Strict 24-hour reset rule** if no problem is solved
- **Time-based streak logic**, not date-based

### 🎯 Visual Feedback
- 🔥 Fire icon glows **orange** when streak is active
- 🌫️ Fire turns **grey/off** when streak is broken or at risk
- Instant motivation directly on your desktop

### 🌐 Multi-Platform Tracking
- **LeetCode** — GraphQL-based data fetching
- **GeeksForGeeks** — Scraping / API fallback logic
- Built to tolerate minor API or layout changes

### 🧩 Modular Architecture
- Python backend works:
  - Standalone
  - With Rainmeter
  - As a base for future platform extensions

### 🛡️ Robust & Fault-Tolerant
- Gracefully handles:
  - Network failures
  - Partial responses
  - API downtime
- No broken skins or crashes

---

## 🖥️ Installation & Setup

### Prerequisites
- Windows
- Rainmeter installed → https://www.rainmeter.net/
- Python 3 installed (`pythonw.exe` recommended)

### Setup Instructions

Clone the repository into your Rainmeter skins directory:

```bash
cd ~/Documents/Rainmeter/Skins
git clone https://github.com/Varun-U-Pratap/DSA_Widget.git
config.example.json → config.json
```

Edit config.json and add your usernames:

```json
{
  "leetcode_username": "your_username",
  "gfg_username": "your_username",
  "output_format": "rainmeter"
}
```

If Python is not detected automatically, configure it manually:

```ini
local.inc.example → local.inc  
PythonPath=C:\Path\To\pythonw.exe
```

Open Rainmeter, locate DSATracker, and load DSATracker.ini.

Click the widget to manually refresh stats.  
Stats auto-update every 10 minutes.  
Solve at least one problem every 24 hours to keep the streak alive.  
Streak increments only once per 15-hour window.
