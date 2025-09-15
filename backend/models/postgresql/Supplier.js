import BaseModel from './BaseModel.js';
import db from '../../config/database.js';

class Supplier extends BaseModel {
  constructor() {
    super(db);
  }

  async create(supplierData) {
    const data = {
      name: supplierData.name,
      contact_person: supplierData.contactPerson,
      email: supplierData.email,
      phone: supplierData.phone,
      address: supplierData.address,
      city: supplierData.city,
      state: supplierData.state,
      pincode: supplierData.pincode
    };
    
    return super.create('suppliers', data);
  }
}

export default Supplier;