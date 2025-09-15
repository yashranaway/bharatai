import BaseModel from './BaseModel.js';
import db from '../../config/database.js';

class Retailer extends BaseModel {
  constructor() {
    super(db);
  }

  async create(retailerData) {
    const data = {
      user_id: retailerData.userId,
      business_name: retailerData.businessName,
      owner_name: retailerData.ownerName,
      email: retailerData.email,
      phone: retailerData.phone,
      address: retailerData.address,
      city: retailerData.city,
      state: retailerData.state,
      pincode: retailerData.pincode,
      annual_revenue: retailerData.annualRevenue,
      years_in_business: retailerData.yearsInBusiness
    };
    
    return super.create('retailers', data);
  }
  
  async findByUserId(userId) {
    const sql = 'SELECT * FROM retailers WHERE user_id = $1';
    const result = await this.query(sql, [userId]);
    return result.rows[0] || null;
  }
  
  async findByEmail(email) {
    const sql = 'SELECT * FROM retailers WHERE email = $1';
    const result = await this.query(sql, [email]);
    return result.rows[0] || null;
  }
}

export default Retailer;