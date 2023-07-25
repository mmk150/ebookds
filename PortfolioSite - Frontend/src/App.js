import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './App.css';
import Home from './pages/Home.js';
import { BrowserRouter as Router, Routes,Route } from 'react-router-dom';


import { PrimeReactProvider, PrimeReactContext } from 'primereact/api';
        
import "primereact/resources/primereact.min.css";

import NotFound from './pages/NotFound';


function App() {

  return (
    <>
    <PrimeReactProvider>
    <Navbar/>
    <Routes>
      <Route path='/' element={<Home />}/>
      <Route path='*' element = {<NotFound />} />
    </Routes>
    <Footer/>
    </PrimeReactProvider>
   </>
  );
}

export default App;
