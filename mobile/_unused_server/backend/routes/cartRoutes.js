const express = require('express');
const router = express.Router();
const cartController = require('../controllers/cartController');

// /api/cart
router.get('/:customerId', cartController.getCart);
router.post('/add', cartController.addToCart);
router.delete('/:cartId', cartController.removeFromCart);

module.exports = router;
