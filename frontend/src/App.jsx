import { useState } from 'react'
import axios from 'axios'
import './App.css'
import { BrowserRouter,Routes,Route } from 'react-router-dom'
import CrawlPage from './pages/crawlPage.jsx'
import ChatPage from './pages/chatPage.jsx'

function App() {
  return(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<CrawlPage/>}></Route>
      <Route path='/chat' element={<ChatPage/>}></Route>
    </Routes>
  </BrowserRouter>
  )
}


export default App
