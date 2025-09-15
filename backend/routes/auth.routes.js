import express from 'express';
import { registerUser, loginUser, getUserProfile, updateUserRole } from '../controllers/auth.controller.js';
import auth from '../middleware/auth.js';
import checkRole from '../middleware/role.js';

const router = express.Router();

// Register user
router.post('/register', registerUser);

// Login user
router.post('/login', loginUser);

// Get user profile (protected)
router.get('/profile', auth, getUserProfile);

// Update user role (admin only)
router.put('/role', auth, checkRole('admin'), updateUserRole);

export default router;