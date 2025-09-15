import Order from '../models/postgresql/Order.js';
import DeliveryTracking from '../models/postgresql/DeliveryTracking.js';

// Place a new delivery order
export const placeOrder = async (req, res) => {
  try {
    const orderData = req.body;
    const orderModel = new Order();
    const newOrder = await orderModel.create(orderData);
    
    res.status(201).json({
      success: true,
      data: newOrder,
      message: 'Order placed successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to place order',
      error: error.message
    });
  }
};

// Get order by ID
export const getOrderById = async (req, res) => {
  try {
    const { id } = req.params;
    const orderModel = new Order();
    const order = await orderModel.findById('orders', id);
    
    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }
    
    res.json({
      success: true,
      data: order
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to fetch order',
      error: error.message
    });
  }
};

// Get all orders for a customer (retailer)
export const getOrdersByCustomer = async (req, res) => {
  try {
    const { customerId } = req.params;
    const orderModel = new Order();
    const orders = await orderModel.findByRetailerId(customerId);
    
    res.json({
      success: true,
      data: orders,
      count: orders.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to fetch orders',
      error: error.message
    });
  }
};

// Update order status
export const updateOrderStatus = async (req, res) => {
  try {
    const { orderId } = req.params;
    const { status } = req.body;
    const orderModel = new Order();
    const updatedOrder = await orderModel.updateStatus(orderId, status);
    
    if (!updatedOrder) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }
    
    // Also add tracking entry
    const trackingModel = new DeliveryTracking();
    await trackingModel.create({
      orderId,
      status,
      location: req.body.location,
      notes: req.body.notes
    });
    
    res.json({
      success: true,
      data: updatedOrder,
      message: 'Order status updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to update order status',
      error: error.message
    });
  }
};

// Get delivery tracking information
export const getTrackingInfo = async (req, res) => {
  try {
    const { orderId } = req.params;
    const trackingModel = new DeliveryTracking();
    const trackingInfo = await trackingModel.findByOrderId(orderId);
    
    res.json({
      success: true,
      data: trackingInfo,
      count: trackingInfo.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to fetch tracking information',
      error: error.message
    });
  }
};

// Cancel an order
export const cancelOrder = async (req, res) => {
  try {
    const { orderId } = req.params;
    const orderModel = new Order();
    const cancelledOrder = await orderModel.updateStatus(orderId, 'cancelled');
    
    if (!cancelledOrder) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }
    
    // Also add tracking entry
    const trackingModel = new DeliveryTracking();
    await trackingModel.create({
      orderId,
      status: 'cancelled',
      notes: 'Order cancelled by user'
    });
    
    res.json({
      success: true,
      data: cancelledOrder,
      message: 'Order cancelled successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to cancel order',
      error: error.message
    });
  }
};

export default {
  placeOrder,
  getOrderById,
  getOrdersByCustomer,
  updateOrderStatus,
  getTrackingInfo,
  cancelOrder
};