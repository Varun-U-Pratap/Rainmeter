import json
import urllib.request
import urllib.error
import re
import datetime
import os
import time

# --- CONFIGURATION ---
# Loaded from config.json (next to this script).
# base_dir in config = folder for history, output, log (default = script folder).
# output_format = "rainmeter" (default) | "json" (also writes stats.json for other apps).
# ---------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Content-Type': 'application/json'
}

# Set after _paths(); safe for log_message() when config is loaded before paths
DEBUG_LOG = None

def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    print(formatted_msg)
    try:
        if DEBUG_LOG is not None:
            with open(DEBUG_LOG, "a", encoding="utf-8") as f:
                f.write(formatted_msg + "\n")
    except (OSError, NameError):
        pass

def load_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        log_message("Config file not found. Copy config.example.json to config.json and set your usernames.")
        return {"leetcode_username": "your_leetcode_username", "gfg_username": "your_gfg_username"}
    except json.JSONDecodeError as e:
        log_message(f"Config file invalid JSON: {e}. Using placeholders; set config.json for your usernames.")
        return {"leetcode_username": "your_leetcode_username", "gfg_username": "your_gfg_username"}

config = load_config()
LEETCODE_USER = config.get("leetcode_username", "your_leetcode_username")
GFG_USER = config.get("gfg_username", "your_gfg_username")

def _base_dir():
    """Folder for history, variables, log. From config base_dir (relative to script or absolute)."""
    b = config.get("base_dir") or ""
    if not b:
        return SCRIPT_DIR
    p = os.path.join(SCRIPT_DIR, b) if not os.path.isabs(b) else b
    return os.path.abspath(p)

def _paths():
    base = _base_dir()
    return {
        "history": os.path.join(base, "history.json"),
        "variables": os.path.join(base, "variables.inc"),
        "debug_log": os.path.join(base, "debug.log"),
        "stats_json": os.path.join(base, "stats.json"),
    }

_paths = _paths()
HISTORY_FILE = _paths["history"]
VARIABLES_FILE = _paths["variables"]
DEBUG_LOG = _paths["debug_log"]  # overwrites None set above
STATS_JSON = _paths["stats_json"]

def get_leetcode_stats():
    """
    Fetches LeetCode total solved count using GraphQL.
    """
    log_message(f"Fetching LeetCode stats for {LEETCODE_USER}...")
    query = """
    query userProblemsSolved($username: String!) {
        allQuestionsCount {
            difficulty
            count
        }
        matchedUser(username: $username) {
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                    submissions
                }
            }
        }
    }
    """
    data = {
        "query": query,
        "variables": {"username": LEETCODE_USER}
    }
    
    try:
        req = urllib.request.Request(
            "https://leetcode.com/graphql", 
            data=json.dumps(data).encode('utf-8'), 
            headers=HEADERS
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            resp_json = json.loads(response.read().decode('utf-8'))
            if resp_json.get('errors'):
                log_message(f"LeetCode API errors: {resp_json['errors']}")
                return None
            data = resp_json.get('data')
            if not data:
                return None
            matched = data.get('matchedUser')
            if not matched or not isinstance(matched.get('submitStats'), dict):
                log_message("LeetCode: user not found or no submit stats.")
                return None
            ac_submissions = matched['submitStats'].get('acSubmissionNum') or []
            for item in ac_submissions:
                if isinstance(item, dict) and item.get('difficulty') == 'All':
                    return int(item['count'])
    except urllib.error.URLError as e:
        log_message(f"LeetCode network error: {e}")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        log_message(f"LeetCode parse error: {e}")
    except Exception as e:
        log_message(f"Error fetching LeetCode: {e}")
    return None

def get_gfg_stats():
    """
    Fetches GFG total solved count by scraping the profile page.
    Fallback: Vercel API.
    """
    log_message(f"Fetching GFG stats for {GFG_USER}...")
    # Method 1: Scrape Profile
    try:
        url = f"https://www.geeksforgeeks.org/user/{GFG_USER}/"
        # We need to accept text/html
        headers_html = HEADERS.copy()
        del headers_html['Content-Type']
        
        req = urllib.request.Request(url, headers=headers_html)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Look for the "Problem Solved" stats. 
            # The structure often changes, but usually the number is near the text.
            # Pattern: "Problem Solved" ... >21<
            # Trying a few patterns
            
            # Pattern 1: New Profile Design
            # <div class="...">Problem Solved</div> ... <div class="...">21</div>
            match = re.search(r"Problem Solved.*?(\d+)\s*<", html, re.IGNORECASE | re.DOTALL)
            if match:
                return int(match.group(1))
            
            # Pattern 2: Search for raw number if it follows specific class (riskier)
            # Let's try the Vercel API if scraping direct text fails, 
            # as GFG classes are randomized (e.g. scoreCard_head_left--score__3_M_E)
            
    except urllib.error.URLError as e:
        log_message(f"GFG profile network error: {e}")
    except Exception as e:
        log_message(f"Error scraping GFG profile: {e}")

    # Method 2: Vercel API (Fallback)
    try:
        url = f"https://geeks-for-geeks-stats-card.vercel.app/?username={GFG_USER}"
        req = urllib.request.Request(url, headers={'User-Agent': HEADERS['User-Agent']})
        with urllib.request.urlopen(req, timeout=10) as response:
            svg_text = response.read().decode('utf-8')
            
            # Try to find total solved directly
            match = re.search(r"Problem Solved.*?>(\d+)<", svg_text, re.IGNORECASE | re.DOTALL)
            if match:
                return int(match.group(1))
            
            # Summation fallback: Find counts for each difficulty
            total = 0
            # Regex to find count for a label: Label ... >123<
            # Optimized to look for specific difficulty patterns
            for diff in ["School", "Basic", "Easy", "Medium", "Hard"]:
                m = re.search(f"{diff}.*?>(\\d+)<", svg_text, re.IGNORECASE | re.DOTALL)
                if m:
                    total += int(m.group(1))
            
            if total > 0: 
                return total
    except urllib.error.URLError as e:
        log_message(f"GFG API network error: {e}")
    except Exception as e:
        log_message(f"Error fetching GFG via API: {e}")
    return None

def load_history():
    default = {
        "streak": 0,
        "last_lc_total": 0,
        "last_gfg_total": 0,
        "last_total": 0,
        "last_date": None,
        "daily_history": {},
        "last_activity_timestamp": 0,
        "last_streak_timestamp": 0,
    }
    if not os.path.exists(HISTORY_FILE):
        return default
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            log_message("History file invalid (not a dict). Using defaults.")
            return default
        return data
    except json.JSONDecodeError as e:
        log_message(f"History file corrupt: {e}. Using defaults.")
        return default
    except Exception as e:
        log_message(f"Error loading history: {e}. Using defaults.")
        return default

def save_history(data):
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        log_message(f"Error saving history: {e}")

def get_current_week_dates():
    """Returns a list of 7 dates (YYYY-MM-DD) for the current week (Mon-Sun)."""
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday()) # Monday
    dates = []
    for i in range(7):
        day = start_of_week + datetime.timedelta(days=i)
        dates.append(day.strftime("%Y-%m-%d"))
    return dates

def _build_output_from_history(history):
    """Build variables.inc lines and RAINMETER line from history (for last-known display)."""
    current_timestamp = time.time()
    last_activity_ts = history.get("last_activity_timestamp", 0)
    time_since_activity = current_timestamp - last_activity_ts if last_activity_ts else 999999
    is_fire_on = time_since_activity < 86400  # 24 hours
    COLOR_ACCENT = "255,150,0,255"
    COLOR_TEXT_SUB = "150,150,150,255"
    streak_color = COLOR_ACCENT if is_fire_on else COLOR_TEXT_SUB
    fire_img = "fireon.png" if is_fire_on else "fireoff.png"
    output_lines = [
        f"Streak={history.get('streak', 0)}",
        f"TotalSolved={history.get('last_total', 0)}",
        f"LC_Count={history.get('last_lc_total', 0)}",
        f"GFG_Count={history.get('last_gfg_total', 0)}",
        f"FireImg={fire_img}",
        f"StreakColor={streak_color}",
    ]
    week_dates = get_current_week_dates()
    COLOR_ACTIVE = "255,255,255,255"
    COLOR_INACTIVE = "60,60,60,255"
    for i, date_str in enumerate(week_dates):
        status = history.get("daily_history", {}).get(date_str, False)
        color = COLOR_ACTIVE if status else COLOR_INACTIVE
        output_lines.append(f"Day{i+1}Color={color}")
    rainmeter_line = (
        f"RAINMETER:Streak={history.get('streak', 0)}|TotalSolved={history.get('last_total', 0)}|"
        f"LC_Count={history.get('last_lc_total', 0)}|GFG_Count={history.get('last_gfg_total', 0)}|"
        f"FireImg={fire_img}|StreakColor={streak_color}"
    )
    return output_lines, rainmeter_line

def _write_variables_and_rainmeter(output_lines, rainmeter_line):
    """Write variables.inc and print RAINMETER line for RunCommand to capture."""
    try:
        with open(VARIABLES_FILE, "w", encoding="utf-8") as f:
            f.write("[Variables]\n")
            f.write("\n".join(output_lines))
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
    except OSError as e:
        log_message(f"Error writing variables.inc: {e}")
    print(rainmeter_line)

def main():
    log_message("--- Starting Update ---")
    
    # Load history FIRST so we can show last-known values even when offline or on timeout
    history = load_history()
    
    # Migration: ensure all keys exist (old history files may be missing some)
    if "last_lc_total" not in history: history["last_lc_total"] = 0
    if "last_gfg_total" not in history: history["last_gfg_total"] = 0
    if "last_activity_timestamp" not in history: history["last_activity_timestamp"] = 0
    if "last_streak_timestamp" not in history: history["last_streak_timestamp"] = 0
    if "streak" not in history: history["streak"] = 0
    if "last_total" not in history: history["last_total"] = history["last_lc_total"] + history["last_gfg_total"]
    if "last_date" not in history: history["last_date"] = None
    if "daily_history" not in history: history["daily_history"] = {}
    
    # Output last-known values immediately so Rainmeter always gets parseable data
    # (fixes blank widget after reboot or when offline/timeout)
    output_lines, rainmeter_line = _build_output_from_history(history)
    _write_variables_and_rainmeter(output_lines, rainmeter_line)
    
    # 1. Get Totals (may hang or fail when offline)
    lc_count = get_leetcode_stats()
    if lc_count: log_message(f"LeetCode Success: {lc_count}")
    
    gfg_count = get_gfg_stats()
    if gfg_count: log_message(f"GFG Success: {gfg_count}")
    
    last_lc = history.get("last_lc_total", 0)
    last_gfg = history.get("last_gfg_total", 0)
    
    # Use last known values if API fails
    final_lc = lc_count if lc_count is not None else last_lc
    final_gfg = gfg_count if gfg_count is not None else last_gfg
    
    # Calculate total
    total_now = final_lc + final_gfg
    
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    yesterday = today - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    # 2. Activity & Streak Logic (Time-Based Duolingo Style)
    
    # Check if we have solved anything NEW
    lc_increased = (lc_count is not None) and (lc_count > last_lc)
    gfg_increased = (gfg_count is not None) and (gfg_count > last_gfg)
    
    current_timestamp = time.time()
    last_activity_ts = history.get("last_activity_timestamp", 0)
    last_streak_ts = history.get("last_streak_timestamp", 0)
    
    # STRICT 24H RULE: Check if streak is broken BEFORE processing new activity
    # If more than 24 hours have passed since the LAST SOLVE, reset to 0.
    time_gap = current_timestamp - last_activity_ts if last_activity_ts else 9999999
    
    current_streak = history.get("streak", 0)
    if time_gap > 86400: # 24 Hours
        current_streak = 0
        # If broken, reset streak timestamp too so next solve counts as 1 immediately
        last_streak_ts = 0 
        
    # Update timestamp if we have NEW activity
    if lc_increased or gfg_increased:
        history["last_activity_timestamp"] = current_timestamp
        
        # Streak Increment Logic:
        # 1. If streak was 0, it becomes 1.
        # 2. If streak > 0, we need a cooldown to prevent spamming.
        #    "Duolingo style" means roughly once per "day".
        #    Since we are NOT using calendar, we use a 15-hour cooldown from the LAST STREAK INCREMENT.
        
        streak_gap = current_timestamp - last_streak_ts
        
        if current_streak == 0:
            current_streak = 1
            history["last_streak_timestamp"] = current_timestamp
        elif streak_gap > 54000: # 15 Hours (15 * 3600)
            current_streak += 1
            history["last_streak_timestamp"] = current_timestamp
        
        # Note: If streak > 0 and gap < 15h, we do NOTHING to streak, 
        # but we DID update last_activity_ts above, so the 24h timer resets.

    # Update stored totals if they increased
    if lc_count is not None and lc_count > last_lc:
        history["last_lc_total"] = lc_count
    if gfg_count is not None and gfg_count > last_gfg:
        history["last_gfg_total"] = gfg_count
    
    # Recalculate Total based on stored bests (to avoid drops)
    history["last_total"] = history["last_lc_total"] + history["last_gfg_total"]
    
    # Save the strictly calculated streak
    history["streak"] = current_streak
    
    # Maintain daily_history only for the visual graph (approximate)
    was_active_today = history.get("daily_history", {}).get(today_str, False)
    if lc_increased or gfg_increased:
        was_active_today = True
        
    if "daily_history" not in history:
        history["daily_history"] = {}
    history["daily_history"][today_str] = was_active_today
    
    if was_active_today:
        history["last_date"] = today_str
        
    save_history(history)
    
    # 3. Generate variables.inc and RAINMETER line (updated values)
    output_lines, rainmeter_line = _build_output_from_history(history)
    _write_variables_and_rainmeter(output_lines, rainmeter_line)
    
    is_fire_on = (time.time() - history.get("last_activity_timestamp", 0) or 999999) < 86400
    log_message(f"Stats updated successfully. Streak={history['streak']} Fire={'ON' if is_fire_on else 'OFF'}")

    # Optional JSON output for other apps (config: output_format = "json")
    payload = {
        "streak": history["streak"],
        "total_solved": history["last_total"],
        "lc_count": history["last_lc_total"],
        "gfg_count": history["last_gfg_total"],
        "fire_on": is_fire_on,
        "fire_img": "fireon.png" if is_fire_on else "fireoff.png",
    }
    if config.get("output_format") == "json":
        try:
            with open(STATS_JSON, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            print(json.dumps(payload))
        except OSError as e:
            log_message(f"Error writing stats.json: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"CRITICAL ERROR: {e}")
        # Fallback: output last-known so Rainmeter still gets parseable data (no blank widget)
        try:
            history = load_history()
            output_lines, rainmeter_line = _build_output_from_history(history)
            _write_variables_and_rainmeter(output_lines, rainmeter_line)
        except Exception:
            pass
