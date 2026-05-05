const express = require('express')
const app = express()

app.get('/biens', (req, res) => {
    res.json([
        { nom: "Appartement Montpellier", prix: 200000 },
        { nom: "Maison Toulouse", prix: 350000 }
    ])
})

app.listen(3000, () => {
    console.log("Serveur lancé sur http://localhost:3000")
})