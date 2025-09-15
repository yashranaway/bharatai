import BaseModel from './BaseModel.js';
import db from '../../config/database.js';

class Order extends BaseModel {
  constructor() {
    super(db);
  }

  async create(orderData) {
    const data = {
      retailer_id: orderData.retailerId,
      customer_name: orderData.customerName,
      customer_phone: orderData.customerPhone,
      shipping_address: orderData.shippingAddress,
      total_amount: orderData.totalAmount,
      status: orderData.status || 'pending',
      estimated_delivery: orderData.estimatedDelivery
    };
    
    return super.create('orders', data);
  }
  
  async findByRetailerId(retailerId) {
    return super.findAll('orders', { retailer_id: retailerId });
  }
  
  async updateStatus(orderId, status) {
    const sql = 'UPDATE orders SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING *';
    const result = await this.query(sql, [status, orderId]);
    return result.rows[0] || null;
  }
  
  async addOrderItem(orderItemData) {
    const data = {
      order_id: orderItemData.orderId,
      product_id: orderItemData.productId,
      quantity: orderItemData.quantity,
      price: orderItemData.price,
      total: orderItemData.total
    };
    
    return super.create('order_items', data);
  }
}

export default Order;