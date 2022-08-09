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

module.exports = { pool }