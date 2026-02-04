import { useState, useEffect } from "react";
import { searchTracks, fetchRecommendations } from "../api/backend";
import RecommendationMode from "../components/RecommendationMode";

const API_URL = "https://bradley-semifine-amada.ngrok-free.dev";
const NGROK_HEADERS = { "ngrok-skip-browser-warning": "true" };

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [recLoading, setRecLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [userId, setUserId] = useState("guest");
  const [limit, setLimit] = useState(10); 
  const [searchTime, setSearchTime] = useState(null);
  const [mode, setMode] = useState(localStorage.getItem("recommend_mode") || "base");

  useEffect(() => {
    const token = localStorage.getItem("spotify_token");
    if (!token) return;

    fetch("https://api.spotify.com/v1/me", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        if (data.id) setUserId(data.id);
      })
      .catch(err => console.error("User fetch error:", err));
  }, []);

  async function handleSearch() {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await searchTracks(query);
      setResults(data);
    } catch (err) {
      console.error("Search error:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRecommend(track) {
    const tid = track.track_id || track.id;
    if (!tid) return;
    
    const startTime = Date.now();
    setRecLoading(true);
    setRecommendations([]);
    setSearchTime(null);

    try {
      const data = await fetchRecommendations(tid, limit, mode, userId); 
      setRecommendations(data.recommendations || []);
      setSearchTime(((Date.now() - startTime) / 1000).toFixed(1));
      console.log("BACKEND RESPONSE DATA:", data);
    } catch (err) {
      console.error("Rec error:", err);
    } finally {
      setRecLoading(false);
    }
  }

  async function handleSavePlaylist() {
    const token = localStorage.getItem("spotify_token");
    if (!token) return alert("Please log in to save playlists!");
    setIsSaving(true);
    try {
      const trackIds = recommendations.map(r => r.track_id || r.id);
      const res = await fetch(`${API_URL}/create-playlist`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            ...NGROK_HEADERS
        },
        body: JSON.stringify({
          name: `AI ${mode.toUpperCase()} Mix`,
          track_ids: trackIds,
          token: token
        })
      });
      if (!res.ok) throw new Error("Failed to create playlist");
      const data = await res.json();
      alert("Playlist created successfully!");
      window.open(data.playlist_url, "_blank");
    } catch (err) {
      alert("Error saving playlist. Try to Logout and Login again.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="container">
      <div className="search-bar">
        <input 
          placeholder="Search track..." 
          value={query} 
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()} 
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <div className="controls-row" style={{ display: 'flex', alignItems: 'center', gap: '40px', margin: '20px 0' }}>
        <RecommendationMode mode={mode} setMode={setMode} />
        <div className="limit-control" style={{ flex: 1 }}>
          <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: '#b3b3b3' }}>
            Tracks to find: <strong style={{ color: '#1DB954' }}>{limit}</strong>
          </label>
          <input 
            type="range" 
            min="1" max="50" step="1" 
            value={limit} 
            onChange={(e) => setLimit(parseInt(e.target.value))}
            style={{ width: '100%', accentColor: '#1DB954', cursor: 'pointer' }}
          />
        </div>
      </div>

      <div className="list">
        {results.map((track) => (
          <div className="card" key={track.track_id || track.id}>
            <div className="card-info">
              <img src={track.image} alt="" />
              <div><strong>{track.name}</strong><span>{track.artist}</span></div>
            </div>
            <button onClick={() => handleRecommend(track)}>Recommend</button>
          </div>
        ))}
      </div>

      {recLoading && <p>AI is thinking...</p>}

      {recommendations.length > 0 && (
        <div className="recommendations-section">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
                <h2>Recommended ({mode})</h2>
                {searchTime && <span style={{fontSize: '12px', color: '#666'}}>Found in {searchTime}s</span>}
            </div>
            <button onClick={handleSavePlaylist} disabled={isSaving} className="save-btn">
              {isSaving ? "Saving..." : "💾 Save to Spotify"}
            </button>
          </div>
          <div className="list fade-in">
            {recommendations.map((track, idx) => (
              <div className="card highlight" key={`${track.track_id}-${idx}`}>
                <div className="card-info">
                  <img src={track.image || "/music-placeholder.png"} alt="" />
                  <div><strong>{track.name}</strong><span>{track.artist}</span></div>
                </div>
                <a href={track.spotify_url} target="_blank" rel="noreferrer" className="spotify-link">Open</a>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}