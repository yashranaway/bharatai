import BaseModel from './BaseModel.js';
import db from '../../config/database.js';

class CreditAssessment extends BaseModel {
  constructor() {
    super(db);
  }

  async create(assessmentData) {
    const data = {
      retailer_id: assessmentData.retailerId,
      credit_score: assessmentData.creditScore,
      risk_level: assessmentData.riskLevel,
      recommended_credit_limit: assessmentData.recommendedCreditLimit,
      assessment_date: assessmentData.assessmentDate || new Date()
    };
    
    return super.create('credit_assessments', data);
  }
  
  async findByRetailerId(retailerId) {
    return super.findAll('credit_assessments', { retailer_id: retailerId }, 'assessment_date DESC');
  }
  
  async getLatestAssessment(retailerId) {
    const sql = `
      SELECT * FROM credit_assessments 
      WHERE retailer_id = $1 
      ORDER BY assessment_date DESC 
      LIMIT 1
    `;
    const result = await this.query(sql, [retailerId]);
    return result.rows[0] || null;
  }
}

export default CreditAssessment;