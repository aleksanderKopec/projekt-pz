import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Chat from './Chat';
import Login from './Login';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { themeOptions } from './ThemeOptions';



//setup axios global config
const axios = require('axios').default;
const API_HOST = "chatapp.westeurope.cloudapp.azure.com"
const API_PORT = 80
axios.defaults.baseURL = `http://${API_HOST}:${API_PORT}/api`

const theme = createTheme(themeOptions)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Login></Login>} />
          <Route path='/login' element={<Login></Login>} />
          <Route path='/chat/:roomId' element={<Chat></Chat>} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);

