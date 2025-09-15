class BaseModel {
  constructor(db) {
    this.db = db;
  }

  async query(sql, params = []) {
    try {
      const result = await this.db.query(sql, params);
      return result;
    } catch (error) {
      throw new Error(`Database query error: ${error.message}`);
    }
  }

  async findById(table, id) {
    const sql = `SELECT * FROM ${table} WHERE id = $1`;
    const result = await this.query(sql, [id]);
    return result.rows[0] || null;
  }

  async findAll(table, conditions = {}, orderBy = 'created_at DESC') {
    let sql = `SELECT * FROM ${table}`;
    const params = [];
    
    if (Object.keys(conditions).length > 0) {
      const whereClause = Object.keys(conditions)
        .map((key, index) => `${key} = $${index + 1}`)
        .join(' AND ');
      
      sql += ` WHERE ${whereClause}`;
      params.push(...Object.values(conditions));
    }
    
    sql += ` ORDER BY ${orderBy}`;
    
    const result = await this.query(sql, params);
    return result.rows;
  }

  async create(table, data) {
    const keys = Object.keys(data);
    const values = Object.values(data);
    const placeholders = keys.map((_, index) => `$${index + 1}`).join(', ');
    
    const sql = `
      INSERT INTO ${table} (${keys.join(', ')}) 
      VALUES (${placeholders}) 
      RETURNING *
    `;
    
    const result = await this.query(sql, values);
    return result.rows[0];
  }

  async update(table, id, data) {
    const keys = Object.keys(data);
    const values = Object.values(data);
    const setClause = keys.map((key, index) => `${key} = $${index + 1}`).join(', ');
    
    const sql = `
      UPDATE ${table} 
      SET ${setClause}, updated_at = NOW() 
      WHERE id = $${keys.length + 1} 
      RETURNING *
    `;
    
    const result = await this.query(sql, [...values, id]);
    return result.rows[0];
  }

  async delete(table, id) {
    const sql = `DELETE FROM ${table} WHERE id = $1 RETURNING *`;
    const result = await this.query(sql, [id]);
    return result.rows[0] || null;
  }
}

export default BaseModel;