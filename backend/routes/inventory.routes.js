import express from 'express';
import inventoryController from '../controllers/inventory.controller.js';

const router = express.Router();

// Get all products
router.get('/products', inventoryController.getAllProducts);

// Get product by ID
router.get('/products/:id', inventoryController.getProductById);

// Add new product
router.post('/products', inventoryController.addProduct);

// Update product
router.put('/products/:id', inventoryController.updateProduct);

// Delete product
router.delete('/products/:id', inventoryController.deleteProduct);

// Auto add stock
router.post('/products/:productId/add-stock', inventoryController.addStock);

// Auto deduct stock
router.post('/products/:productId/deduct-stock', inventoryController.deductStock);

// Get stock level
router.get('/products/:productId/stock-level', inventoryController.getStockLevel);

export default router;