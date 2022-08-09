const { Router } = require('express')
const { pool } = require('./utils')

const router = Router();

router.get('/raffles', async (req, res) => {
    let results;
    try {
        results = await pool.query(`SELECT * FROM raffles`)
        results = results.rows;
    } catch { results = [] }

    return res.status(200).json(results)
})

router.get('/raffles/:id', async (req, res) => {
    let results;
    try {
        results = await pool.query(`SELECT * FROM raffles WHERE "id" = '${req.params.id.trim()}'`)
        results = results.rows;
    } catch { results = [] }

    return res.status(200).json(results)
})

router.post('/raffles', async (req, res) => {
    added = false
    let data = req.body
    console.log(data)
    for (var i = 0; i < data.length; i++) {
        results = await pool.query(`SELECT * FROM raffles WHERE "id" = '${data[i].id.trim()}'`)
        if (results.rows.length < 1) {
            await pool.query(`INSERT INTO raffles VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)`, [
                data[i].id,
                data[i].date,
                data[i].winners,
                data[i].eth,
                data[i].image,
                data[i].name,
                data[i].twitter,
                data[i].discord,
                data[i].extra
            ])
            added = true;
        }
    }

    return res.status(200).json({ added, amount: data.length })
})

router.delete('/raffles', async (req, res) => {
    await pool.query(`DELETE FROM raffles`)

    return res.status(200).json({ deleted: true, id: req.params.id })
})

router.delete('/raffles/:id', async (req, res) => {
    await pool.query(`DELETE FROM raffles WHERE "id" = '${req.params.id.trim()}'`)

    return res.status(200).json({ deleted: true, id: req.params.id })
})

module.exports = router