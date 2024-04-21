import { BrowserRouter, Route, Routes } from 'react-router-dom'
import EventsSection from './components/EventCardsSection'
import { NavbarSimple } from './components/Header'
import './style.css'
import EventPage from './pages/EventPage'

function App() {
  return (
    <>
      <NavbarSimple />
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<EventsSection />} />
          <Route path='/events/:id' element={<EventPage />} />
        </Routes>
      </BrowserRouter>

    </>
  )
}

export default App