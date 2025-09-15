import BaseModel from './BaseModel.js';
import db from '../../config/database.js';

class DeliveryTracking extends BaseModel {
  constructor() {
    super(db);
  }

  async create(trackingData) {
    const data = {
      order_id: trackingData.orderId,
      status: trackingData.status,
      location: trackingData.location,
      notes: trackingData.notes
    };
    
    return super.create('delivery_tracking', data);
  }
  
  async findByOrderId(orderId) {
    return super.findAll('delivery_tracking', { order_id: orderId }, 'created_at ASC');
  }
  
  async updateStatus(trackingId, status, location, notes) {
    const data = {
      status,
      location,
      notes
    };
    
    return super.update('delivery_tracking', trackingId, data);
  }
}

export default DeliveryTracking;