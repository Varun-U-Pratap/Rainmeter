# DSA Tracker for Rainmeter

![DSATracker Banner](https://placehold.co/1200x400/FF9600/141414?text=DSATracker&font=inter)
![DSA Tracker Preview](fireon.png)
![DSA Tracker Preview](fireoff.png)

A **modular Rainmeter-based DSA progress tracker** for **LeetCode** and **GeeksForGeeks**, built around a **strict, time-based activity validation system** to reflect genuine problem-solving consistency.

Designed for developers who value **discipline, visibility, and engineering rigor** over inflated metrics.

---

## ✨ Features

### 🔥 Time-Based Streak Validation
- Tracks **consecutive coding activity using timestamps**, not calendar days
- **15-hour cooldown window** prevents artificial or repeated streak increments
- **Hard 24-hour expiry rule** resets streak on inactivity
- Eliminates timezone manipulation and date-based loopholes

### 🎯 Real-Time Visual Feedback
- 🔥 Fire indicator turns **active (orange)** when streak conditions are met
- 🌫️ Indicator switches **inactive (grey)** when streak expires
- Immediate on-desktop feedback without opening a browser or app

### 🌐 Multi-Platform Support
- **LeetCode** — GraphQL-based data retrieval
- **GeeksForGeeks** — Scraping with structured fallback logic
- Designed to tolerate minor API, schema, or layout changes

### 🧩 Modular & Extensible Architecture
- Python backend can operate:
  - Independently (CLI / scripts)
  - Integrated with Rainmeter
  - As a base layer for additional coding platforms
- Clean separation between:
  - Data fetching
  - Validation logic
  - UI rendering

### 🛡️ Fault-Tolerant by Design
- Graceful handling of:
  - Network outages
  - Partial or delayed responses
  - Platform downtime
- Prevents UI crashes or corrupted state in Rainmeter

---

## 🧠 Why This Project?

While preparing Data Structures and Algorithms, I found it difficult to **consistently track progress and stay accountable** while focusing on *actually understanding* DSA concepts rather than just solving problems.

I explored existing tools and trackers, but most were:
- Date-based and easy to manipulate
- Focused on raw counts instead of consistency
- Detached from the development environment

To address this gap, I designed and built my own solution.

This project:
- Enforces **time-based activity validation**
- Provides **always-visible feedback** directly on the desktop
- Removes reliance on self-reporting or manual updates
- Encourages sustained, disciplined practice through system constraints

By building the tool myself, I solved both problems:
1. Creating a **reliable way to track real DSA practice**
2. Improving my own **consistency and understanding** through enforced structure

The result is a lightweight monitoring system that reflects genuine effort, not inflated statistics.

---

## Setup Instructions

### Download and Install RainMeter:

from https://www.rainmeter.net/ download the .exe file and install it by double left click

### Clone the repository into your Rainmeter skins directory by running the following command in any bash terminal:

```bash
cd ~/Documents/Rainmeter/Skins
git clone https://github.com/Varun-U-Pratap/DSA_Widget.git
cd ~/Documents/Rainmeter/Skins/DSA_Widget/
mv config.example.json config.json
mv local.inc.example local.inc
```

### Edit config.json and add your LeetCode and GFG usernames:
Replace the placeholders with your actual usernames.
```json
{
  "leetcode_username": "your_leetcode_username",
  "gfg_username": "your_gfg_username",
  "output_format": "rainmeter"
}
```
**Note:** `config.json`, `local.inc`, `history.json`, `variables.inc`, and `debug.log` are gitignored—your data and paths are never committed.

### If Python is not detected automatically or the widget is blank, configure it manually or else skip this step:
open CMD and run
```script
where pythonw
```
copy the last path and paste it into `local.inc` (see `local.inc.example`). Use `PythonPath=...` with no leading space.

### Loading the .ini file
Click ^ from the taskbar.
Right click and open manage from the rainmeter running.
Navigate into the DSA_Widget and find ini file and load it.
Now you are good to go.

---

## 🧑‍💻 About the Developer

- **Varun U Pratap**
  - **LinkedIn**: [https://www.linkedin.com/in/varun-u-pratap-856826340](https://www.linkedin.com/in/varun-u-pratap-856826340)

## 📞 Contact Me

For any inquiries, feedback, or collaborations regarding DSA Tracker, please reach out to me on LinkedIn.
