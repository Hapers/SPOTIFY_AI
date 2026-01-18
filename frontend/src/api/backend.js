const API_URL = "http://127.0.0.1:8000";

export async function searchTracks(query) {
  const res = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error("Search failed");
  return res.json();
}

export async function fetchRecommendations(trackId, topK = 10) {
  if (!trackId || typeof trackId !== "string") {
    throw new Error("Invalid track_id");
  }

  const res = await fetch(`${API_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      track_id: trackId,
      top_k: topK,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error("Recommend error:", err);
    throw new Error("Recommend failed");
  }

  return res.json();
}

export async function fetchTrack(trackId) {
  const res = await fetch(`${API_URL}/track/${trackId}`);
  if (!res.ok) throw new Error("Track fetch failed");
  return res.json();
}
