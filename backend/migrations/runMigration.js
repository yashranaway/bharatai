import fs from 'fs';
import db from '../config/database.js';

// Read the SQL file
const sql = fs.readFileSync('./migrations/init_schema.sql', 'utf8');

// Run the migration
db.query(sql)
  .then(res => {
    console.log('Database schema created successfully');
    process.exit(0);
  })
  .catch(err => {
    console.error('Error creating database schema:', err);
    process.exit(1);
  });