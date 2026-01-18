import { useState } from "react";
import { searchTracks } from "../api/backend";

export default function SearchBar({ onSelect }) {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);

  async function handleSearch(e) {
    setQ(e.target.value);
    if (e.target.value.length < 3) return;

    const data = await searchTracks(e.target.value);
    setResults(data);
  }

  return (
    <div>
      <input
        className="search"
        placeholder="Search track..."
        value={q}
        onChange={handleSearch}
      />

      {results.map(track => (
        <div
          key={track.id}
          className="result-item"
          onClick={() => onSelect(track)}
        >
          🎵 {track.name} — {track.artist}
        </div>
      ))}
    </div>
  );
}
