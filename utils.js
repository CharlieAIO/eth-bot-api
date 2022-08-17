const { Pool } = require('pg')
require('dotenv').config();

const pool = new Pool({
    user: process.env.DB_USERNAME,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: 25060,
    host: process.env.DB_HOST,
    idleTimeoutMillis: 10000,
    connectionTimeoutMillis: 10000,
    ssl: true
})

const generateKey = (prefix, length) => {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let key = new Array(length).fill("").map(e => characters.charAt(Math.floor(Math.random() * characters.length))).join('')
    return `${(prefix ? `${prefix}-` : '')}${key}`
}


module.exports = { pool, generateKey }