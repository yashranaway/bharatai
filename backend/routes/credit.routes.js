import express from 'express';
import creditController from '../controllers/credit.controller.js';

const router = express.Router();

// Verify retailer
router.get('/retailers/:id', creditController.verifyRetailer);

// Add new retailer
router.post('/retailers', creditController.addRetailer);

// Update retailer information
router.put('/retailers/:id', creditController.updateRetailer);

// Perform credit risk assessment
router.post('/assessment/:retailerId', creditController.assessCreditRisk);

// Get retailer credit information
router.get('/retailers/:retailerId/credit-info', creditController.getRetailerCreditInfo);

export default router;