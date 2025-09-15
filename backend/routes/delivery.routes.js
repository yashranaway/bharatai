import express from 'express';
import deliveryController from '../controllers/delivery.controller.js';

const router = express.Router();

// Place a new delivery order
router.post('/orders', deliveryController.placeOrder);

// Get order by ID
router.get('/orders/:id', deliveryController.getOrderById);

// Get all orders for a customer
router.get('/orders/customer/:customerId', deliveryController.getOrdersByCustomer);

// Update order status
router.put('/orders/:orderId/status', deliveryController.updateOrderStatus);

// Get delivery tracking information
router.get('/orders/:orderId/tracking', deliveryController.getTrackingInfo);

// Cancel an order
router.delete('/orders/:orderId', deliveryController.cancelOrder);

export default router;