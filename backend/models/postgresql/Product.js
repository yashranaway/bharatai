import BaseModel from './BaseModel.js';
import db from '../../config/database.js';

class Product extends BaseModel {
  constructor() {
    super(db);
  }

  async create(productData) {
    const data = {
      retailer_id: productData.retailerId,
      supplier_id: productData.supplierId,
      name: productData.name,
      description: productData.description,
      category: productData.category,
      price: productData.price,
      quantity: productData.quantity,
      unit: productData.unit || 'pcs'
    };
    
    return super.create('products', data);
  }
  
  async findByRetailerId(retailerId) {
    return super.findAll('products', { retailer_id: retailerId });
  }
  
  async findBySupplierId(supplierId) {
    return super.findAll('products', { supplier_id: supplierId });
  }
  
  async updateStock(productId, quantity) {
    const sql = 'UPDATE products SET quantity = quantity + $1, updated_at = NOW() WHERE id = $2 RETURNING *';
    const result = await this.query(sql, [quantity, productId]);
    return result.rows[0] || null;
  }
  
  async getStockLevel(productId) {
    const sql = 'SELECT id, name, quantity FROM products WHERE id = $1';
    const result = await this.query(sql, [productId]);
    return result.rows[0] || null;
  }
}

export default Product;