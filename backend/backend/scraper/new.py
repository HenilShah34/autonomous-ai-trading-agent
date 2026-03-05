import json
import re
import os
from playwright.sync_api import sync_playwright
from backend.db.insert_data import insert_silver_data

COOKIES_FILE = "mycookie.json"
USER_DATA_DIR = "user_data"
URL = "https://www.investing.com/commodities/silver-streaming-chart"


# -------------------------------------------------
# FIND TRADINGVIEW FRAME
# -------------------------------------------------
def find_tradingview_frame(page, timeout=30000):
    end = page.context._loop.time() + timeout / 1000
    while page.context._loop.time() < end:
        for frame in page.frames:
            try:
                if frame.locator("a.indicators").count() > 0:
                    print("✅ TradingView frame detected")
                    return frame
            except:
                pass
        page.wait_for_timeout(500)
    raise Exception("❌ TradingView frame not found")


# -------------------------------------------------
# BASIC UI SETUP
# -------------------------------------------------
def click_candle_button(tv):
    tv.locator(
        "div.header-group-bars-style span.apply-common-tooltip"
    ).first.click()
    tv.page.wait_for_timeout(1000)


def add_multiple_mas(tv, lengths):
    tv.locator("a.indicators").click()
    tv.page.wait_for_timeout(1000)

    search_box = (
        tv.locator("div")
        .filter(has_text="IndicatorsTechnical")
        .get_by_role("textbox")
    )
    search_box.fill("ma")

    ma_item = (
        tv.locator("div")
        .filter(has_text=re.compile(r"^Moving Average$"))
        .nth(1)
    )

    for _ in lengths:
        ma_item.click(force=True)
        tv.page.wait_for_timeout(300)

    tv.locator(".tv-dialog__close").click()
    tv.page.wait_for_timeout(1000)

    for i, length in enumerate(lengths):
        gear = tv.locator(
            f"div:nth-child({i + 2}) "
            "> .pane-legend-icon-container "
            "> .pane-legend-icon.apply-common-tooltip.format"
        )
        gear.click(force=True)

        length_box = tv.get_by_role("row", name="Length").get_by_role("textbox")
        length_box.fill(str(length))
        tv.get_by_text("OK").click()
        tv.page.wait_for_timeout(700)


def change_timeframe(tv, label):
    caret = tv.locator("span.submenu.apply-common-tooltip").first
    caret.click(force=True)
    tv.page.wait_for_timeout(500)

    tv.locator(
        "div.charts-popup-list.intervals-list.favored-list span.item",
        has_text=label
    ).first.click(force=True)

    tv.page.wait_for_timeout(5000)
    print(f"\n⏱ Timeframe changed to {label}")


# -------------------------------------------------
# READ + INSERT INTO DATABASE
# -------------------------------------------------
def read_and_store(tv, timeframe):
    values = tv.evaluate(
        """() => {
            const out = {};
            document
              .querySelectorAll('.pane-legend-line.pane-legend-wrap.study')
              .forEach(row => {
                const name = row.querySelector(
                    '.pane-legend-line.apply-overflow-tooltip'
                );
                const val = row.querySelector(
                    '.pane-legend-item-value-container'
                );
                if (!name || !val) return;
                out[name.textContent.trim()] =
                    val.textContent.trim();
              });
            return out;
        }"""
    )

    def clean(v):
        if not v or v == "n/a":
            return None
        return float(v.replace(",", ""))

    data = {
        "timeframe": timeframe,
        "open": None,
        "high": None,
        "low": None,
        "close": None,
        "ma20": clean(values.get("MA (20, close, 0)")),
        "ma50": clean(values.get("MA (50, close, 0)")),
        "ma100": clean(values.get("MA (100, close, 0)")),
        "ma200": clean(values.get("MA (200, close, 0)")),
    }

    insert_silver_data(data)
    print("📥 Inserted into DB:", data)


# -------------------------------------------------
# MAIN
# -------------------------------------------------
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        viewport=None,
        locale="en-US",
        timezone_id="Asia/Kolkata",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process"
        ]
    )

    try:
        with open(COOKIES_FILE, "r", encoding="utf-8") as f:
            context.add_cookies(json.load(f))
            print("🍪 Cookies injected")
    except:
        pass

    page = context.new_page()

    # 1️⃣ Open base domain FIRST
    page.goto("https://www.investing.com", wait_until="domcontentloaded")

    # 2️⃣ Inject login cookie
    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        context.add_cookies(json.load(f))
        print("🍪 accessToken injected")

    # 3️⃣ Reload so frontend detects login
    page.reload(wait_until="domcontentloaded")

    # 4️⃣ Now open chart page
    page.goto(URL, wait_until="domcontentloaded")

    tv = find_tradingview_frame(page)
    click_candle_button(tv)
    add_multiple_mas(tv, [20, 50, 100, 200])

    timeframes = ["5 minute", "15 minute", "30 minute", "1 hour", "1 day"]

    print("\n🔁 Starting continuous MA collection loop...\n")

    while True:
        for tf in timeframes:
            change_timeframe(tv, tf)
            read_and_store(tv, tf)

        print("\n⏸ Cycle completed — restarting...\n")
        page.wait_for_timeout(5000)
