import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'

import Navegación from './componentes/Navegacion.jsx';
import Resultados from './componentes/Resultados.jsx';

function App() {
  return (
    <>
    <Navegación />
    <Router>
      <div>
        <Routes>
          <Route path="*" element={<Resultados />} />
        </Routes>
      </div>
    </Router>
    </>
  );
}

export default App
