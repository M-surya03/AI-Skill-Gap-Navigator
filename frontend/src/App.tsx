import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import HomePage from './pages/HomePage';
import { Sparkles } from 'lucide-react';

const Navbar: React.FC = () => {
  const loc = useLocation();
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <div className="navbar-logo">
          <Sparkles size={18} color="white" />
        </div>
        SkillMap AI
      </Link>
      <ul className="navbar-nav">
        <li>
          <Link to="/" className={`nav-link ${loc.pathname === '/' ? 'active' : ''}`}>
            Analyze
          </Link>
        </li>
        <li>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link"
          >
            API Docs
          </a>
        </li>
      </ul>
    </nav>
  );
};

const App: React.FC = () => (
  <BrowserRouter>
    <Navbar />
    <Routes>
      <Route path="/" element={<HomePage />} />
    </Routes>
  </BrowserRouter>
);

export default App;
