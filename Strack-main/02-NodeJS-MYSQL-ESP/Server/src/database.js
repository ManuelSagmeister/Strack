import mysql from 'mysql2'
import dotenv from 'dotenv'

dotenv.config();

const pool = mysql.createPool({//Configuration of our MYSQL Database
    host: 'localhost',
    port: 3306,
    user: 'ESP32',
    password: 'esp32io.com',
    database: 'strack'
}).promise()

export async function getRange(){//Getting our Data from tbl Ranges
const result = await pool.query('Select * FROM Ranges')
const rows = result[0]
return rows
}

export async function getLocation(){//Getting data from tbl location
    const result = await pool.query('Select * FROM location order by l_ID DESC LIMIT 2')
    const rows = result[0]
    return rows
    }

export async function addRange(r_Range, fk_Anchor_MAC, fk_Tag_MAC){//Inserting Data into our tbl Ranges
    const result = await pool.query('INSERT INTO Ranges (r_Range, fk_Anchor_MAC, fk_Tag_MAC) VALUES (?, ?, ?)', [r_Range, fk_Anchor_MAC, fk_Tag_MAC])
    return result
}