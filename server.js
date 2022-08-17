const express = require('express')
const http = require('http')
const bodyParser = require('body-parser')
require('dotenv').config();

const routes = require('./routes')

const setupServer = () => {
    const app = express();
    const server = http.createServer(app)

    app.disable('x-powered-by')
    app.use(bodyParser.urlencoded({ extended: true }))
    app.use(express.json())
    app.use((req, res, next) => {
        if (req.url.includes('/raffles')) {
            if (req.headers['x-api-key'] !== process.env.API_KEY) {
                return res.status(403).json({
                    response: 'ACCESS DENIED',
                    reason: 'INVALID API KEY'
                })
            }
        }
        if (req.url.includes('/raffles')) {
            if (req.headers['x-api-key'] !== process.env.API_KEY) {
                return res.status(403).json({
                    response: 'ACCESS DENIED',
                    reason: 'INVALID API KEY'
                })
            }
        }
        return next()
    })

    app.use(routes)
    app.get('/test', (req, res) => {
        return res.status(200).send('test')
    })

    app.use((req, res) => {
        res.status(404).json({
            error: true,
            reason: "Not Found"
        })
    })



    server.on("listening", () => {
        console.log(`Server Listening on Port:${process.env.SERVER_PORT}`)
    })
    server.listen(process.env.SERVER_PORT)
}

setupServer()