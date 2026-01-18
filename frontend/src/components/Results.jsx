export default function Results({ items = [] }) {
  if (items.length === 0) return <p>No results</p>;

  return (
    <div className="results">
      {items.map((t, i) => (
        <div key={i} className="card">
          🎵 {t.track_id}
        </div>
      ))}
    </div>
  );
}
