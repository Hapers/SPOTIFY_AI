const API_URL = "https://bradley-semifine-amada.ngrok-free.dev";

const headers = {
  "Content-Type": "application/json",
  "ngrok-skip-browser-warning": "69420"
};

export async function searchTracks(query) {
  if (!query) return [];

  const res = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`, {
    headers: headers
  });
  if (!res.ok) throw new Error("Search failed");
  return res.json();
}

export async function fetchRecommendations(trackId, topK = 10, mode = "base", userId = "demo_user") {
  if (!trackId || trackId === "undefined") throw new Error("Invalid trackId");

  const res = await fetch(`${API_URL}/recommend`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({ 
      track_id: trackId, 
      top_k: topK, 
      mode, 
      user_id: userId 
    }),
  });

  if (!res.ok) throw new Error("Recommend failed");
  return res.json();
}

export async function fetchTrack(trackId) {
  if (!trackId || trackId === "undefined") return null;
  const res = await fetch(`${API_URL}/track/${trackId}`, {
    headers: headers
  });
  if (!res.ok) throw new Error("Track fetch failed");
  return res.json();
}

export async function fetchHistory(userId = "demo_user") {
  const res = await fetch(`${API_URL}/history?user_id=${encodeURIComponent(userId)}`, {
    headers: headers
  });
  if (!res.ok) throw new Error("History failed");
  return res.json();
}