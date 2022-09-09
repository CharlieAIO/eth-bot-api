const { Router } = require('express')
const { pool, generateKey } = require('./utils')
const { uuid } = require('uuidv4');

const router = Router();

router.get('/raffles/reversed', async (req, res) => {
    let results;
    try {
        results = await pool.query(`SELECT * FROM raffles`)
        results = results.rows;
    } catch { results = [] }

    return res.status(200).json(results.reverse())
})


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

router.put('/raffles/:id/:roleId', async (req, res) => {
    let updated = false;
    let results;
    try {
        results = await pool.query(`SELECT * FROM raffles WHERE "id" = '${req.params.id.trim()}'`)
    } catch { results = [] }


    if (results.rows.length > 0) {
        if (results.rows[0].discord?.role) {
            let discordJSON = results.rows[0].discord
            discordJSON.roleId = req.params.roleId.trim()
            updated = true;
            await pool.query(`UPDATE raffles SET "discord" = '${JSON.stringify(discordJSON)}' WHERE "id" = '${req.params.id.trim()}'`)
        }
    }
    return res.status(200).json({ updated, id: req.params.id })
})



router.post('/license/create/:amount', async (req, res) => {
    for (var i = 0; i < parseInt(req.params.amount); i++) {
        let key;
        await pool.query(`INSERT INTO licenses VALUES ($1,$2,$3,$4)`, [
            uuid(),
            generateKey(null, 30),
            false,
            null
        ])
    }
})

module.exports = router