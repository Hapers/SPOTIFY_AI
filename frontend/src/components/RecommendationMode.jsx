import { useState, useRef, useEffect } from "react";
import "../styles/ModeSelect.css";

const MODES = [
  {
    value: "base",
    label: "Base (similar)",
    icon: "🎯",
    info: "Pure similarity — tracks that sound most alike",
  },
  {
    value: "energy",
    label: "Energy",
    icon: "⚡",
    info: "More dynamic, powerful and energetic tracks",
  },
  {
    value: "chill",
    label: "Chill",
    icon: "🌙",
    info: "Calm, acoustic, slow and relaxing vibes",
  },
  {
    value: "popular",
    label: "Popular",
    icon: "🔥",
    info: "More popular and trending tracks",
  },
];

export default function ModeSelect({ mode, setMode }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  const current = MODES.find((m) => m.value === mode);

  useEffect(() => {
    function handleClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () =>
      document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="mode-box" ref={ref}>
      <span className="mode-label">
        Recommendation mode
        <span className="mode-info">
          <svg
            className="info-icon"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
        >
            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="1.5"/>
            <line x1="12" y1="10" x2="12" y2="16" stroke="currentColor" strokeWidth="1.5"/>
            <circle cx="12" cy="7" r="1" fill="currentColor"/>
        </svg>
          <span className="mode-tooltip">
            <strong>Base</strong> — most similar tracks<br />
            <strong>Energy</strong> — dynamic & powerful<br />
            <strong>Chill</strong> — calm & relaxing<br />
            <strong>Popular</strong> — trending & popular
          </span>
        </span>
      </span>

      <div
        className={`mode-trigger ${open ? "open" : ""}`}
        onClick={() => setOpen(!open)}
      >
        <span className="mode-icon">{current.icon}</span>
        <span>{current.label}</span>
        <span className="mode-arrow">▾</span>
      </div>

      {open && (
        <div className="mode-dropdown">
          {MODES.map((m) => (
            <div
              key={m.value}
              className={`mode-item ${
                m.value === mode ? "active" : ""
              }`}
              onClick={() => {
                setMode(m.value);
                localStorage.setItem("recommend_mode", m.value); // 💾
                setOpen(false);
              }}
            >
              <span className="mode-icon">{m.icon}</span>

              <div className="mode-text">
                <div className="mode-name">{m.label}</div>
                <div className="mode-desc">{m.info}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
