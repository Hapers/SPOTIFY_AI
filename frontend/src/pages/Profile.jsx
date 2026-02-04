import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchHistory } from "../api/backend";
import "../styles/profile.css";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [history, setHistory] = useState([]);
  const [expandedId, setExpandedId] = useState(null);
  const navigate = useNavigate();
  const token = localStorage.getItem("spotify_token");
  const [loading, setLoading] = useState(!!token);

  const currentMode = localStorage.getItem("recommend_mode") || "base";

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetch("https://api.spotify.com/v1/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("401");
        return res.json();
      })
      .then((data) => {
        const spotifyUser = {
          id: data.id,
          name: data.display_name,
          email: data.email || "Not provided",
          country: data.country,
          avatar: data.images?.[0]?.url || "",
        };
        setUser(spotifyUser);

        return fetchHistory(spotifyUser.id); 
      })
      .then((historyData) => {
        setHistory(Array.isArray(historyData) ? historyData : []);
      })
      .catch((err) => {
        console.error("Profile load error:", err);
        if (err.message === "401") {
          localStorage.removeItem("spotify_token");
          navigate("/");
        }
      })
      .finally(() => setLoading(false));
  }, [token, navigate]);

  const formatDate = (isoString) => {
    if (!isoString) return "";
    try {
      const date = new Date(isoString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' • ' + 
             date.toLocaleDateString([], { day: '2-digit', month: 'short' });
    } catch (e) {
      return "";
    }
  };

  if (loading) return <div className="profile-container"><p>Loading profile...</p></div>;
  if (!user) return <div className="profile-container"><button onClick={() => navigate("/")}>Please Login</button></div>;

  return (
    <div className="profile-container">
      <div className="profile-hero">
        <h1>Welcome, {user.name}</h1>
      </div>

      <div className="profile-card">
        <div className="profile-header">
          <img src={user.avatar || "/default-avatar.png"} alt="avatar" className="profile-avatar-img" />
          <div className="profile-header-info">
            <strong>{user.name}</strong>
          </div>
          <button className="logout-btn" onClick={() => { localStorage.clear(); navigate("/"); }}>Logout</button>
        </div>
        
        <div className="profile-grid">
          <div className="info-box">
            <label>Email</label>
            <div className="info-field">{user.email}</div>
          </div>
          <div className="info-box">
            <label>Country</label>
            <div className="info-field">{user.country}</div>
          </div>
          <div className="info-box">
            <label>Current Mode</label>
            <div className="info-field" style={{ textTransform: 'capitalize' }}>{currentMode}</div>
          </div>
          <div className="info-box">
            <label>History items</label>
            <div className="info-field">{history.length}</div>
          </div>
        </div>
      </div>

      <div className="profile-card" style={{ marginTop: "30px" }}>
        <h3>Search History</h3>
        <div className="history-list">
          {history.length === 0 ? (
            <p style={{textAlign: 'center', opacity: 0.5, padding: '20px'}}>
              No history yet. Go to Home and recommend some tracks!
            </p>
          ) : (
            history.map((group, index) => (
              <div key={group._id || index} className={`history-group ${expandedId === index ? 'expanded' : ''}`}>
                <div className="history-main-row" onClick={() => setExpandedId(expandedId === index ? null : index)}>
                  {/* Защита от отсутствия картинки */}
                  <img src={group.source_track_image || "/music-placeholder.png"} className="history-thumb" alt="" onError={(e) => e.target.src="/music-placeholder.png"} />
                  <div className="history-meta">
                    <strong>{group.source_track_name || "Unknown Track"}</strong>
                    <div className="meta-sub">
                      <span className="mode-badge">{group.mode || "Base"}</span>
                      <span className="time-stamp">{formatDate(group.timestamp)}</span>
                    </div>
                  </div>
                  <button className="expand-indicator">{expandedId === index ? "✕" : "Open"}</button>
                </div>

                {expandedId === index && (
                  <div className="tracks-dropdown">
                    {group.recommended && group.recommended.length > 0 ? (
                      group.recommended.map((track, i) => (
                        <div key={i} className="track-mini-item">
                          <img src={track.image || "/music-placeholder.png"} alt="" onError={(e) => e.target.src="/music-placeholder.png"} />
                          <div className="track-names">
                            <p>{track.name || "Unknown"}</p>
                            <span>{track.artist || "Unknown"}</span>
                          </div>
                          {track.spotify_url && (
                             <a href={track.spotify_url} target="_blank" rel="noreferrer" className="play-mini-btn">Play</a>
                          )}
                        </div>
                      ))
                    ) : (
                        <p style={{padding: '10px', fontSize: '0.9rem', color: '#888'}}>No recommendations saved for this item.</p>
                    )}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}