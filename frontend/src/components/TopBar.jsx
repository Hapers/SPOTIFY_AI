import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

const MoonIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
  </svg>
);

const SunIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="5" fill="currentColor"/>
    <line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" />
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" />
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
  </svg>
);

export default function TopBar() {
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "dark");
  const [token, setToken] = useState(localStorage.getItem("spotify_token"));
  const [userAvatar, setUserAvatar] = useState(null);
  
  // Хук location нужен, чтобы ловить момент возвращения пользователя после логина
  const location = useLocation();

  // 1. Следим за изменением URL. Если URL сменился, проверяем токен в localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem("spotify_token");
    if (storedToken !== token) {
      setToken(storedToken);
    }
  }, [location]); // Срабатывает при каждом переходе по страницам

  // 2. Управление темой
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  // 3. Загрузка данных профиля при наличии токена
  useEffect(() => {
    if (token) {
      fetch("https://api.spotify.com/v1/me", { // Исправил URL на правильный Spotify API
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => {
          if (!res.ok) throw new Error("Unauthorized");
          return res.json();
        })
        .then((data) => {
          if (data.images && data.images.length > 0) {
            setUserAvatar(data.images[0].url);
          }
        })
        .catch(() => {
          // Если токен протух — очищаем его
          localStorage.removeItem("spotify_token");
          setToken(null);
          setUserAvatar(null);
        });
    } else {
      setUserAvatar(null);
    }
  }, [token]);

  return (
    <header className="topbar">
      <Link to="/" className="logo">Spotify AI</Link>

      <div className="topbar-right">
        {/* Кнопка переключения темы */}
        <button 
          className="theme-toggle-v2" 
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          title="Toggle Theme"
        >
          {theme === "dark" ? <SunIcon /> : <MoonIcon />}
        </button>

        {/* Условный рендеринг: Аватарка или Кнопка входа */}
        {token ? (
          <Link to="/profile" className="avatar-link">
            {userAvatar ? (
              <img src={userAvatar} alt="Profile" className="topbar-avatar" />
            ) : (
              <div className="topbar-avatar placeholder-circle">
                {/* Буква-заглушка */}
                U
              </div>
            )}
          </Link>
        ) : (
          <a href="http://localhost:8000/auth/login" className="account-btn">
            Login
          </a>
        )}
      </div>
    </header>
  );
}