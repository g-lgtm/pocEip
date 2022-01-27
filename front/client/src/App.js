import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./routes/Home";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route exact path='/' element={<Home />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
