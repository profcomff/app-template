import { BrowserRouter, Route, Routes } from 'react-router-dom'
import EventsSection from './components/EventCardsSection'
import { NavbarSimple } from './components/Header'
import './style.css'
import EventPage from './pages/EventPage'
import AddEvent from './pages/AddEvent'
import NotFound from './pages/NotFound'

function App() {
  return (
    <>
      <BrowserRouter>
        <NavbarSimple />
        <Routes>
          <Route path='/' element={<EventsSection />} />
          <Route path='/events/:id' element={<EventPage />} />
          <Route path='/addEvent' element={<AddEvent />} />
          <Route path='/*' element={<NotFound />} />
        </Routes>
      </BrowserRouter>

    </>
  )
}

export default App