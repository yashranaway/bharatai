import Product from '../models/postgresql/Product.js';

// Get all products
export const getAllProducts = async (req, res) => {
  try {
    const productModel = new Product();
    const products = await productModel.findAll('products');
    
    res.json({
      success: true,
      data: products,
      count: products.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to fetch products',
      error: error.message
    });
  }
};

// Get product by ID
export const getProductById = async (req, res) => {
  try {
    const { id } = req.params;
    const productModel = new Product();
    const product = await productModel.findById('products', id);
    
    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }
    
    res.json({
      success: true,
      data: product
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to fetch product',
      error: error.message
    });
  }
};

// Add new product
export const addProduct = async (req, res) => {
  try {
    const productData = req.body;
    const productModel = new Product();
    const newProduct = await productModel.create(productData);
    
    res.status(201).json({
      success: true,
      data: newProduct,
      message: 'Product added successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to add product',
      error: error.message
    });
  }
};

// Update product
export const updateProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    const productModel = new Product();
    const updatedProduct = await productModel.update('products', id, updates);
    
    if (!updatedProduct) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }
    
    res.json({
      success: true,
      data: updatedProduct,
      message: 'Product updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to update product',
      error: error.message
    });
  }
};

// Delete product
export const deleteProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const productModel = new Product();
    const deleted = await productModel.delete('products', id);
    
    if (!deleted) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Product deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to delete product',
      error: error.message
    });
  }
};

// Auto add stock
export const addStock = async (req, res) => {
  try {
    const { productId } = req.params;
    const { quantity } = req.body;
    
    if (typeof quantity !== 'number' || quantity <= 0) {
      return res.status(400).json({
        success: false,
        message: 'Invalid quantity'
      });
    }
    
    const productModel = new Product();
    const updatedProduct = await productModel.updateStock(productId, quantity);
    
    if (!updatedProduct) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }
    
    res.json({
      success: true,
      data: updatedProduct,
      message: `Added ${quantity} units to stock`
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to add stock',
      error: error.message
    });
  }
};

// Auto deduct stock
export const deductStock = async (req, res) => {
  try {
    const { productId } = req.params;
    const { quantity } = req.body;
    
    if (typeof quantity !== 'number' || quantity <= 0) {
      return res.status(400).json({
        success: false,
        message: 'Invalid quantity'
      });
    }
    
    const productModel = new Product();
    const updatedProduct = await productModel.updateStock(productId, -quantity);
    
    if (!updatedProduct) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }
    
    res.json({
      success: true,
      data: updatedProduct,
      message: `Deducted ${quantity} units from stock`
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to deduct stock',
      error: error.message
    });
  }
};

// Get stock level
export const getStockLevel = async (req, res) => {
  try {
    const { productId } = req.params;
    const productModel = new Product();
    const stockInfo = await productModel.getStockLevel(productId);
    
    if (!stockInfo) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }
    
    res.json({
      success: true,
      data: {
        productId: stockInfo.id,
        productName: stockInfo.name,
        currentStock: stockInfo.quantity,
        lowStockThreshold: 10
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to get stock level',
      error: error.message
    });
  }
};

export default {
  getAllProducts,
  getProductById,
  addProduct,
  updateProduct,
  deleteProduct,
  addStock,
  deductStock,
  getStockLevel
};