const express = require("express");
const axios = require('axios');
const path = require("path");
const app = new express()

app.use(express.static(path.join(__dirname, "/public")));

app.get('/api', async (req, res) => {
    const url = "http://ml-api:5000";
    try {
        const response = await axios.get(url);
        res.send(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send('Ocorreu um erro ao buscar os dados da API.');
    }
});

app.post('/api/data', async (req, res) => {
    const url = "http://ml-api:5000/api";
    const data = req.body; // Dados recebidos na requisição POST
    try {
        const response = await axios.post(url, data); // Passa os dados para a função axios.post
        res.send(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send('Ocorreu um erro ao buscar os dados da API.');
    }
});

app.listen(3000, () => {
    console.log("Server runing on port 3000");
});