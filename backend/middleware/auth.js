import jwt from 'jsonwebtoken';
import User from '../models/postgresql/User.js';

const auth = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({ 
        success: false, 
        message: 'Access denied. No token provided.' 
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Create user model instance
    const userModel = new User();
    const user = await userModel.findById('users', decoded.id);
    
    if (!user) {
      return res.status(401).json({ 
        success: false, 
        message: 'Access denied. Invalid token.' 
      });
    }

    // Format user data to match expected structure
    req.user = {
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role
    };
    
    next();
  } catch (error) {
    res.status(401).json({ 
      success: false, 
      message: 'Access denied. Invalid token.' 
    });
  }
};

export default auth;