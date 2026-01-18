import { useState } from "react";
import {
  searchTracks,
  fetchRecommendations,
  fetchTrack,
} from "../api/backend";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [recLoading, setRecLoading] = useState(false);

  async function handleSearch() {
    if (!query.trim()) return;
    setLoading(true);
    setResults([]);
    setRecommendations([]);
    try {
      const data = await searchTracks(query);
      setResults(data);
    } finally {
      setLoading(false);
    }
  }

  async function handleRecommend(track) {
    console.log("RECOMMEND CLICK:", track);

  if (!track.track_id) {
    console.error("Track ID missing:", track);
    return;
  }

  setLoading(true);
    setRecommendations([]);

    const rec = await fetchRecommendations(track.track_id);


    // 🔥 подтягиваем полные данные треков
    const fullTracks = await Promise.all(
      rec.recommendations.map((r) => fetchTrack(r.track_id))
    );

    setRecommendations(fullTracks.filter(Boolean));
    setRecLoading(false);
  }

  return (
    <div className="container">
      <h1 className="title">🎧 Spotify AI</h1>
      <p className="subtitle">
        Search a track and generate AI-based recommendations
      </p>

      <div className="search-bar">
        <input
          placeholder="Search track..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && <p className="loading">Searching…</p>}

      {/* SEARCH RESULTS */}
      <div className="list">
        {results.map((track) => (
          <div className="card" key={track.id}>
            <div className="card-info">
              <img src={track.image} alt="" />
              <div>
                <strong>{track.name}</strong>
                <span>{track.artist}</span>
              </div>
            </div>
            <button onClick={() => handleRecommend(track)}>
              Recommend
            </button>
          </div>
        ))}
      </div>

      {/* RECOMMENDATIONS */}
      {recLoading && <p className="loading">Generating recommendations…</p>}

      {recommendations.length > 0 && (
        <>
          <h2 className="section-title">Recommended tracks</h2>
          <div className="list">
            {recommendations.map((track) => (
              <div className="card highlight" key={track.id}>
                <div className="card-info">
                  <img src={track.image} alt="" />
                  <div>
                    <strong>{track.name}</strong>
                    <span>{track.artist}</span>
                  </div>
                </div>
                <a
                  href={track.url}
                  target="_blank"
                  rel="noreferrer"
                  className="spotify-link"
                >
                  Open
                </a>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
