const express = require("express");
const axios = require('axios');
const path = require("path");
const app = new express()

// Middleware para analisar o corpo da solicitação em JSON
app.use(express.json());

app.use(express.static(path.join(__dirname, "/public")));

const API_URL = process.env['API_URL']
const API_PORT = process.env['API_PORT']

app.get('/api', async (req, res) => {
    const url = API_URL + ":" + API_PORT;
    console.log(url)
    try {
        const response = await axios.get(url, {
            auth: {
                username: process.env['BASIC_AUTH_USERNAME'],
                password: process.env['BASIC_AUTH_PASSWORD']
              }
        });
        res.status(200).send(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send(`Ocorreu um erro ao buscar os dados da API: ${error}`);
    }
});

app.post('/api/data', async (req, res) => {
    const url = API_URL + ":" + API_PORT + "/api/recommender_movie/";
    const data_json = req.body;
    console.log(url)
    console.log(data_json) // Dados recebidos na requisição POST
    try {
        const response = await axios.post(url, data_json, {
            auth: {
                username: process.env['BASIC_AUTH_USERNAME'],
                password: process.env['BASIC_AUTH_PASSWORD']
              }
        }); // Passa os dados para a função axios.post
        res.status(200).send(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send(error);
    }
});

app.listen(process.env.PORT, () => {
    console.log("Server runing on port 3000");
});