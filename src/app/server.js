const express = require("express");
const axios = require('axios');
const path = require("path");
const app = new express()

app.use(express.static(path.join(__dirname, "/public")));

const url = "http://ml-api:5000"; // substitua por sua URL da API

app.get('/api/data', async (req, res) => {
    try {
        const response = await axios.get(url);
        res.send(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send('Ocorreu um erro ao buscar os dados da API.');
    }
});

app.listen(3000, () => {
    console.log("Server runing on port 3000");
});