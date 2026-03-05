import { useEffect, useState, useRef } from "react";

function App() {
  const [data, setData] = useState([]);
  const [theme, setTheme] = useState("dark");
  const [selectedSymbol, setSelectedSymbol] = useState("silver");
  const previousValues = useRef({});

  const isDark = theme === "dark";

  const fetchData = async () => {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/latest/${selectedSymbol}`
      );
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("API error:", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, [selectedSymbol]);

  // ✅ UPDATED: Dynamic live price detection
  const liveRow = data.find((row) =>
    row.timeframe?.toLowerCase().includes("price")
  );

  const maRows = data.filter(
    (row) => !row.timeframe?.toLowerCase().includes("price")
  );

  const buildRows = () => {
    const result = [];

    if (liveRow) {
      result.push({
        tf: "LIVE RATE",
        label: "Current Market",
        value: liveRow.close,
        isLive: true,
      });
    }

    maRows.forEach((row) => {
      const tf = row.timeframe;

      if (row.ma200)
        result.push({ tf, label: "MA 200", value: row.ma200 });
      if (row.ma100)
        result.push({ tf, label: "MA 100", value: row.ma100 });
      if (row.ma50)
        result.push({ tf, label: "MA 50", value: row.ma50 });
      if (row.ma20)
        result.push({ tf, label: "MA 20", value: row.ma20 });
    });

    return result.sort((a, b) => b.value - a.value);
  };

  const rows = buildRows();

  const timeframeHueMap = {
    "5 minute": 140,
    "15 minute": 275,
    "30 minute": 185,
    "1 hour": 45,
    "1 day": 10,
  };

  const maLightnessMap = {
    "MA 20": 60,
    "MA 50": 52,
    "MA 100": 44,
    "MA 200": 36,
  };

  const getRowStyle = (row) => {
    if (row.isLive) {
      return {
        background:
          "linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb,#3b82f6)",
        backgroundSize: "300% 300%",
        animation: "liveGradient 8s ease infinite",
        border: "1px solid rgba(59,130,246,0.7)",
        boxShadow:
          "0 0 35px rgba(59,130,246,0.6), inset 0 0 20px rgba(255,255,255,0.06)",
      };
    }

    const baseHue = timeframeHueMap[row.tf] || 200;
    const lightness = maLightnessMap[row.label] || 45;

    return {
      background: `linear-gradient(90deg,
        hsl(${baseHue},75%,${lightness - 5}%),
        hsl(${baseHue},75%,${lightness}%)
      )`,
    };
  };

  const getMovementData = (key, value) => {
    const prev = previousValues.current[key];
    let direction = null;
    let percent = 0;

    if (prev !== undefined && prev !== 0) {
      percent = ((value - prev) / prev) * 100;
      if (value > prev) direction = "up";
      else if (value < prev) direction = "down";
    }

    previousValues.current[key] = value;
    return { direction, percent };
  };

  return (
    <div
      className={`min-h-screen transition-all duration-500 ${
        isDark ? "bg-[#0b1220] text-white" : "bg-gray-100 text-gray-900"
      }`}
    >
      <div className="max-w-5xl mx-auto py-8 px-6 space-y-8">

        {/* HEADER */}
        <div className="flex justify-between items-center">

          {/* LEFT SIDE (Dropdown + Title) */}
          <div className="flex items-center gap-6">

            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className={`px-3 py-2 rounded-lg text-sm font-bold ${
                isDark
                  ? "bg-slate-800 text-white"
                  : "bg-gray-200 text-black"
              }`}
            >
              <option value="silver">Silver</option>
              <option value="gold">Gold</option>
              <option value="crude">Crude</option>
              <option value="sp500">S&P 500</option>
            </select>

            <div>
              <h1 className="text-2xl font-bold">
                📊 Full Color Gradient MA Dashboard
              </h1>
              <p className="text-sm opacity-70">
                {rows.length} sorted indicators based on live market price
              </p>
            </div>

          </div>

          <button
            onClick={() => setTheme(isDark ? "light" : "dark")}
            className={`px-4 py-2 rounded-full text-sm font-bold transition-all ${
              isDark ? "bg-white text-black" : "bg-black text-white"
            }`}
          >
            {isDark ? "☀ Light" : "🌙 Dark"}
          </button>
        </div>

        {/* MAIN TABLE */}
        <div
          className={`rounded-2xl overflow-hidden shadow-2xl border ${
            isDark
              ? "border-slate-800"
              : "border-gray-300 bg-white"
          }`}
        >
          <div
            className={`grid grid-cols-3 py-4 px-6 text-xs font-bold uppercase tracking-widest ${
              isDark
                ? "bg-slate-900 text-slate-400"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            <div>Candle Timeframe</div>
            <div>MA Period</div>
            <div className="text-right">Price</div>
          </div>

          {rows.map((row) => {
            const key = row.isLive
              ? "live-rate"
              : `${row.tf}-${row.label}`;

            const movement = getMovementData(key, row.value);

            return (
              <div
                key={key}
                style={getRowStyle(row)}
                className={`grid grid-cols-3 px-6 ${
                  row.isLive ? "py-6 font-bold" : "py-3"
                }`}
              >
                <div className="uppercase font-bold flex items-center gap-2">
                  {row.isLive && (
                    <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></span>
                  )}
                  {row.tf}
                </div>

                <div className={row.isLive ? "italic text-lg" : "font-black"}>
                  {row.label}
                </div>

                <div className="text-right font-mono font-bold flex justify-end items-center gap-3">

                  {movement.direction === "up" && (
                    <span className="text-green-400">▲</span>
                  )}
                  {movement.direction === "down" && (
                    <span className="text-red-400">▼</span>
                  )}

                  <span className="text-xl">{row.value}</span>

                  {movement.direction && (
                    <span
                      className={`text-xs ${
                        movement.direction === "up"
                          ? "text-green-500"
                          : "text-red-500"
                      }`}
                    >
                      {movement.percent.toFixed(2)}%
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* COLOR SCHEME LEGEND */}
        <div
          className={`rounded-xl p-6 border shadow-xl ${
            isDark
              ? "bg-slate-900/70 border-slate-800 text-slate-300"
              : "bg-white border-gray-300 text-gray-700"
          }`}
        >
          <h3 className="text-sm font-bold mb-6">
            🎨 Color Scheme Legend
          </h3>

          <div className="grid grid-cols-6 gap-6 text-xs">
            <LegendItem title="LIVE RATE" gradient="from-blue-700 to-blue-400" />
            <LegendItem title="5 MIN" gradient="from-green-700 to-green-400" />
            <LegendItem title="15 MIN" gradient="from-purple-700 to-purple-400" />
            <LegendItem title="30 MIN" gradient="from-teal-700 to-teal-400" />
            <LegendItem title="1 HOUR" gradient="from-yellow-600 to-yellow-400" />
            <LegendItem title="1 DAY" gradient="from-red-700 to-red-500" />
          </div>
        </div>

        <div className="relative h-1 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-cyan-400 to-transparent animate-dividerGlow"></div>
        </div>

        <div
          className={`grid grid-cols-3 text-xs uppercase tracking-widest font-semibold ${
            isDark
              ? "text-slate-400"
              : "text-gray-600"
          }`}
        >
          <div className="text-left">
            DATA UPDATED REAL-TIME
          </div>
          <div className="text-center">
            SORTING: PRICE DESCENDING
          </div>
          <div className="text-right">
            FORM FACTOR: DESKTOP OPTIMIZED
          </div>
        </div>

      </div>

      <style>
        {`
        @keyframes liveGradient {
          0% {background-position: 0% 50%}
          50% {background-position: 100% 50%}
          100% {background-position: 0% 50%}
        }

        @keyframes dividerGlow {
          0% {transform: translateX(-100%);}
          100% {transform: translateX(100%);}
        }

        .animate-dividerGlow {
          animation: dividerGlow 4s linear infinite;
        }
        `}
      </style>
    </div>
  );
}

function LegendItem({ title, gradient }) {
  return (
    <div>
      <div className={`h-2 rounded-full bg-gradient-to-r ${gradient} mb-2`}></div>
      <p className="font-bold">{title}</p>
    </div>
  );
}

export default App;