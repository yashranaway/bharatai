import BaseModel from './BaseModel.js';
import bcrypt from 'bcrypt';
import db from '../../config/database.js';

class User extends BaseModel {
  constructor() {
    super(db);
  }

  async create(userData) {
    // Hash password before saving
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(userData.password, saltRounds);
    
    const data = {
      username: userData.username,
      email: userData.email,
      password_hash: hashedPassword,
      role: userData.role || 'retailer'
    };
    
    return super.create('users', data);
  }
  
  async findByEmail(email) {
    const sql = 'SELECT * FROM users WHERE email = $1';
    const result = await this.query(sql, [email]);
    return result.rows[0] || null;
  }
  
  async findByUsername(username) {
    const sql = 'SELECT * FROM users WHERE username = $1';
    const result = await this.query(sql, [username]);
    return result.rows[0] || null;
  }
  
  async comparePassword(plainPassword, hashedPassword) {
    return bcrypt.compare(plainPassword, hashedPassword);
  }
  
  async updatePassword(userId, newPassword) {
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(newPassword, saltRounds);
    
    const sql = 'UPDATE users SET password_hash = $1, updated_at = NOW() WHERE id = $2 RETURNING *';
    const result = await this.query(sql, [hashedPassword, userId]);
    return result.rows[0] || null;
  }
}

export default User;