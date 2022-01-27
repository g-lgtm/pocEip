const express = require('express');
const bodyParser = require('body-parser');
require('dotenv').config({path: './config/.env'});
require('./config/db'); 
const userRoutes = require('./routes/user.routes');
const cors = require('cors');

const app = express();

const corsOptions = {
    origin: process.env.CLIENT_URL,
    credentials: true,
    'allowedHeaders': ['sessionId', 'Content-Type'],
    'exposedHeaders': ['sessionId'],
    'methods': 'GET,HEAD,PUT,PATCH,POST,DELETE',
    'preflightContinue': false
}
app.use(cors(corsOptions));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.use('/api/field', userRoutes);

//server
app.listen(process.env.PORT, () => console.log('serveur started :' + process.env.PORT));
