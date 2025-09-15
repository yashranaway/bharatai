import jwt from 'jsonwebtoken';
import User from '../models/postgresql/User.js';

// Generate JWT token
const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: '30d',
  });
};

// Register user
export const registerUser = async (req, res) => {
  try {
    const { username, email, password, role } = req.body;

    // Create user instance
    const userModel = new User();

    // Check if user already exists
    const [existingUserByEmail, existingUserByUsername] = await Promise.all([
      userModel.findByEmail(email),
      userModel.findByUsername(username)
    ]);
    
    if (existingUserByEmail || existingUserByUsername) {
      return res.status(400).json({
        success: false,
        message: 'User already exists with this email or username'
      });
    }

    // Create user
    const userData = {
      username,
      email,
      password,
      role: role || 'retailer'
    };
    
    const user = await userModel.create(userData);

    // Generate token
    const token = generateToken(user.id);

    // Remove password hash from response
    delete user.password_hash;

    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      data: {
        _id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        token
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to register user',
      error: error.message
    });
  }
};

// Login user
export const loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Create user instance
    const userModel = new User();

    // Check for user
    const user = await userModel.findByEmail(email);
    
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password'
      });
    }

    // Check password
    const isMatch = await userModel.comparePassword(password, user.password_hash);
    
    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password'
      });
    }

    // Generate token
    const token = generateToken(user.id);

    // Remove password hash from response
    delete user.password_hash;

    res.json({
      success: true,
      message: 'Login successful',
      data: {
        _id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        token
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to login',
      error: error.message
    });
  }
};

// Get user profile
export const getUserProfile = async (req, res) => {
  try {
    // Create user instance
    const userModel = new User();
    const user = await userModel.findById('users', req.user.id);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }
    
    // Remove password hash from response
    delete user.password_hash;
    
    res.json({
      success: true,
      data: user
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to fetch user profile',
      error: error.message
    });
  }
};

// Update user role (admin only)
export const updateUserRole = async (req, res) => {
  try {
    const { userId, role } = req.body;

    // Validate role
    if (!['admin', 'retailer', 'supplier'].includes(role)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid role'
      });
    }

    // Create user instance
    const userModel = new User();
    
    // Update user role
    const user = await userModel.update('users', userId, { role });

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }

    // Remove password hash from response
    delete user.password_hash;

    res.json({
      success: true,
      message: 'User role updated successfully',
      data: user
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to update user role',
      error: error.message
    });
  }
};

export default {
  registerUser,
  loginUser,
  getUserProfile,
  updateUserRole
};