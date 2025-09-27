import React, { useState } from 'react'
import { HashRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Detector from './pages/Detector'
import Weather from './pages/Weather'
import History from './pages/History'
import About from './pages/About'
import Contact from './pages/Contact'
import { useTranslation } from 'react-i18next'
import './i18n/i18n'
import './App.css' // optional, if you want component-specific styles

function App() {
  const { i18n } = useTranslation()
  const [language, setLanguage] = useState('en')

  const toggleLanguage = (lang) => {
    i18n.changeLanguage(lang)
    setLanguage(lang)
  }

  return (
    <Router>
      <header>
        <h1>AI Crop Doctor</h1>
        <nav>
          <Link to="/">{i18n.t('home')}</Link>
          <Link to="/detector">{i18n.t('predict')}</Link>
          <Link to="/weather">{i18n.t('weather')}</Link>
          <Link to="/history">{i18n.t('history')}</Link>
          <Link to="/about">{i18n.t('about')}</Link>
          <Link to="/contact">{i18n.t('contact')}</Link>
          <select value={language} onChange={(e) => toggleLanguage(e.target.value)}>
            <option value="en">English</option>
            <option value="ta">தமிழ்</option>
          </select>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/detector" element={<Detector />} />
          <Route path="/weather" element={<Weather />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </main>
    </Router>
  )
}

export default App
