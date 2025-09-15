import Retailer from '../models/postgresql/Retailer.js';
import CreditAssessment from '../models/postgresql/CreditAssessment.js';

// Verify retailer
export const verifyRetailer = async (req, res) => {
  try {
    const { id } = req.params;
    const retailerModel = new Retailer();
    const retailer = await retailerModel.findById('retailers', id);
    
    if (!retailer) {
      return res.status(404).json({
        success: false,
        message: 'Retailer not found'
      });
    }
    
    res.json({
      success: true,
      data: retailer
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to verify retailer',
      error: error.message
    });
  }
};

// Add new retailer
export const addRetailer = async (req, res) => {
  try {
    const retailerData = req.body;
    const retailerModel = new Retailer();
    const newRetailer = await retailerModel.create(retailerData);
    
    res.status(201).json({
      success: true,
      data: newRetailer,
      message: 'Retailer added successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to add retailer',
      error: error.message
    });
  }
};

// Update retailer information
export const updateRetailer = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    const retailerModel = new Retailer();
    const updatedRetailer = await retailerModel.update('retailers', id, updates);
    
    if (!updatedRetailer) {
      return res.status(404).json({
        success: false,
        message: 'Retailer not found'
      });
    }
    
    res.json({
      success: true,
      data: updatedRetailer,
      message: 'Retailer updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to update retailer',
      error: error.message
    });
  }
};

// Perform credit risk assessment
export const assessCreditRisk = async (req, res) => {
  try {
    const { retailerId } = req.params;
    const retailerModel = new Retailer();
    const retailer = await retailerModel.findById('retailers', retailerId);
    
    if (!retailer) {
      return res.status(404).json({
        success: false,
        message: 'Retailer not found'
      });
    }
    
    // Simple credit scoring algorithm based on business factors
    let score = 0;
    const factors = [];
    
    // Years in business factor (max 30 points)
    const yearsFactor = Math.min(retailer.years_in_business * 5, 30);
    factors.push({
      name: 'Years in Business',
      weight: 0.3,
      score: yearsFactor,
      description: `${retailer.years_in_business} years in business`
    });
    score += yearsFactor;
    
    // Annual revenue factor (max 40 points)
    const revenueScore = Math.min(retailer.annual_revenue / 100000, 40);
    factors.push({
      name: 'Annual Revenue',
      weight: 0.4,
      score: revenueScore,
      description: `₹${retailer.annual_revenue.toLocaleString()} annual revenue`
    });
    score += revenueScore;
    
    // Business stability factor (max 30 points)
    const stabilityScore = Math.min(retailer.years_in_business * 6, 30);
    factors.push({
      name: 'Business Stability',
      weight: 0.3,
      score: stabilityScore,
      description: 'Business stability based on years of operation'
    });
    score += stabilityScore;
    
    // Normalize score to 100
    score = Math.min(score, 100);
    
    // Determine risk level
    let riskLevel;
    if (score >= 70) {
      riskLevel = 'low';
    } else if (score >= 40) {
      riskLevel = 'medium';
    } else {
      riskLevel = 'high';
    }
    
    // Calculate recommended credit limit (in rupees)
    const recommendedCreditLimit = retailer.annual_revenue * 0.1; // 10% of annual revenue
    
    const assessmentData = {
      retailerId,
      creditScore: Math.round(score),
      riskLevel,
      recommendedCreditLimit,
      assessmentDate: new Date()
    };
    
    // Save assessment
    const assessmentModel = new CreditAssessment();
    const assessment = await assessmentModel.create(assessmentData);
    
    // Update retailer with credit score
    await retailerModel.update('retailers', retailerId, {
      credit_score: Math.round(score),
      risk_level: riskLevel
    });
    
    res.json({
      success: true,
      data: {
        ...assessment,
        factors
      },
      message: 'Credit risk assessment completed'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to perform credit risk assessment',
      error: error.message
    });
  }
};

// Get retailer credit information
export const getRetailerCreditInfo = async (req, res) => {
  try {
    const { retailerId } = req.params;
    const retailerModel = new Retailer();
    const retailer = await retailerModel.findById('retailers', retailerId);
    
    if (!retailer) {
      return res.status(404).json({
        success: false,
        message: 'Retailer not found'
      });
    }
    
    res.json({
      success: true,
      data: {
        id: retailer.id,
        businessName: retailer.business_name,
        creditScore: retailer.credit_score,
        riskLevel: retailer.risk_level,
        yearsInBusiness: retailer.years_in_business,
        annualRevenue: retailer.annual_revenue
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to fetch retailer credit information',
      error: error.message
    });
  }
};

export default {
  verifyRetailer,
  addRetailer,
  updateRetailer,
  assessCreditRisk,
  getRetailerCreditInfo
};