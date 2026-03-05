import json
import re
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
from backend.db.insert_data import insert_market_data

COOKIES_FILE = "mycookie.json"
USER_DATA_DIR = "user_data_sp500"
URL = "https://www.investing.com/indices/us-spx-500-chart"


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
# UI SETUP
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

        length_box = (
            tv.get_by_role("row", name="Length")
            .get_by_role("textbox")
        )
        length_box.fill(str(length))
        tv.get_by_text("OK").click()
        tv.page.wait_for_timeout(700)

        print(f"✅ MA {length} configured")


def change_timeframe(tv, label):
    caret = tv.locator("span.submenu.apply-common-tooltip").first
    caret.click(force=True)
    tv.page.wait_for_timeout(500)

    item = tv.locator(
        "div.charts-popup-list.intervals-list.favored-list span.item",
        has_text=label
    ).first
    item.click(force=True)

    tv.page.wait_for_timeout(5000)
    print(f"\n⏱ Timeframe changed to {label}")


# -------------------------------------------------
# READ OHLC VALUES (TradingView Legend)
# -------------------------------------------------
def read_ohlc_values(tv):
    ohlc = tv.evaluate(
        """() => {
            const out = {};
            const legend = document.querySelector(
                '.pane-legend:not(.hidden)'
            );
            if (!legend) return null;

            const values = legend.querySelectorAll(
                '.pane-legend-item-value'
            );

            if (values.length >= 4) {
                out.open  = values[0].textContent.trim();
                out.high  = values[1].textContent.trim();
                out.low   = values[2].textContent.trim();
                out.close = values[3].textContent.trim();
            }

            return out;
        }"""
    )

    if not ohlc:
        print("⚠️ OHLC not available")
        return None

    print(
        f"📊 OHLC → "
        f"O={ohlc['open']} | "
        f"H={ohlc['high']} | "
        f"L={ohlc['low']} | "
        f"C={ohlc['close']}"
    )

    return ohlc


# -------------------------------------------------
# READ MA VALUES
# -------------------------------------------------
def read_ma_values(tv):
    return tv.evaluate(
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
                    val.textContent.trim() || 'n/a';
              });
            return out;
        }"""
    )


def clean(v):
    if not v or v == "n/a":
        return None
    return float(v.replace(",", ""))


# -------------------------------------------------
# READ + INSERT OHLC + MA (CANDLE ROW)
# -------------------------------------------------
def read_and_store_candle(tv, timeframe, ts):
    ohlc = read_ohlc_values(tv)
    ma = read_ma_values(tv)

    if not ohlc:
        return

    data = {
        "time": ts,
        "timeframe": timeframe,
        "open":  clean(ohlc.get("open")),
        "high":  clean(ohlc.get("high")),
        "low":   clean(ohlc.get("low")),
        "close": clean(ohlc.get("close")),
        "ma20":  clean(ma.get("MA (20, close, 0)")),
        "ma50":  clean(ma.get("MA (50, close, 0)")),
        "ma100": clean(ma.get("MA (100, close, 0)")),
        "ma200": clean(ma.get("MA (200, close, 0)")),
    }

    insert_market_data("sp500", data)
    print("📥 Candle inserted:", data)


# -------------------------------------------------
# READ + INSERT LIVE SP500 PRICE (SEPARATE ROW)
# -------------------------------------------------
def read_and_store_sp500_price(page, ts):
    try:
        page.wait_for_selector(
            '[data-test="instrument-price-last"]',
            timeout=15000
        )

        price_text = page.locator(
            '[data-test="instrument-price-last"]'
        ).first.inner_text().strip()

        price = float(price_text.replace(",", ""))

        data = {
            "time": ts,
            "timeframe": "SP500 Price",
            "open": None,
            "high": None,
            "low": None,
            "close": price,   # live price stored as close
            "ma20": None,
            "ma50": None,
            "ma100": None,
            "ma200": None,
        }

        insert_market_data("sp500", data)
        print(f"💰 SP500 Price inserted: {price}")

    except Exception:
        print("⚠️ SP500 price unavailable")


# -------------------------------------------------
# MAIN
# -------------------------------------------------
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        viewport=None,
        args=["--disable-blink-features=AutomationControlled"]
    )

    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        context.add_cookies(json.load(f))
        print("🍪 Cookies injected")

    page = context.new_page()
    page.goto(URL, wait_until="domcontentloaded")

    tv = find_tradingview_frame(page)
    click_candle_button(tv)
    add_multiple_mas(tv, [20, 50, 100, 200])

    timeframes = ["5 minute", "15 minute", "30 minute", "1 hour", "1 day"]

    print("\n🔁 Starting OHLC + MA + SP500 Price loop...\n")

    while True:
        ts = datetime.now(timezone.utc)

        # ✅ LIVE SP500 PRICE ROW
        read_and_store_sp500_price(page, ts)

        # ✅ CANDLE DATA PER TIMEFRAME
        for tf in timeframes:
            change_timeframe(tv, tf)
            read_and_store_candle(tv, tf, ts)

        print("\n⏸ Cycle completed — restarting...\n")
        page.wait_for_timeout(5000)
