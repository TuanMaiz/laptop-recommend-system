# Tracking API Examples

Based on the TrackingContext code, here are examples of the actual API requests that get sent to the tracking API:

## 1. Immediate Product Interest Event (High Priority)

```json
POST /api/tracking
Content-Type: application/json

[
  {
    "type": "product_interest",
    "trigger": "click",
    "timestamp": 1703123456789,
    "product": {
      "id": "laptop-123",
      "name": "MacBook Pro 16\"",
      "brand": "Apple",
      "category": "Laptops",
      "price": 2499
    },
    "timeOnPage": 45000,
    "scrollDepth": 75,
    "url": "/products/laptop-123",
    "userId": "user-456",
    "sessionId": "session-xyz789",
    "fingerprint": "fp-abc123def456",
    "priority": "high"
  }
]
```

## 2. Batch Events Request (Multiple Events)

```json
POST /api/tracking
Content-Type: application/json

[
  {
    "type": "page_view",
    "timestamp": 1703123400000,
    "url": "/products/laptops",
    "referrer": "https://google.com",
    "title": "Gaming Laptops - TechStore",
    "userId": "user-456",
    "sessionId": "session-xyz789",
    "fingerprint": "fp-abc123def456"
  },
  {
    "type": "product_view",
    "timestamp": 1703123410000,
    "product": {
      "id": "gaming-laptop-789",
      "name": "ASUS ROG Strix G15",
      "brand": "ASUS",
      "model": "G15",
      "category": "Gaming Laptops",
      "price": 1899,
      "specifications": {
        "processor": "AMD Ryzen 9",
        "gpu": "RTX 4070",
        "ram": "32GB",
        "storage": "1TB SSD"
      }
    },
    "url": "/products/gaming-laptop-789",
    "userId": "user-456",
    "sessionId": "session-xyz789",
    "fingerprint": "fp-abc123def456"
  },
  {
    "type": "click",
    "timestamp": 1703123420000,
    "element": {
      "tagName": "BUTTON",
      "className": "btn btn-primary add-to-cart",
      "id": "add-to-cart-btn",
      "text": "Add to Cart"
    },
    "url": "/products/gaming-laptop-789",
    "userId": "user-456",
    "sessionId": "session-xyz789",
    "fingerprint": "fp-abc123def456",
    "action": "add_to_cart",
    "productId": "gaming-laptop-789",
    "value": 1899
  },
  {
    "type": "time_spent",
    "timestamp": 1703123450000,
    "timeSpent": 120,
    "scrollDepth": 85,
    "url": "/products/gaming-laptop-789",
    "currentProduct": {
      "id": "gaming-laptop-789",
      "name": "ASUS ROG Strix G15",
      "brand": "ASUS",
      "category": "Gaming Laptops",
      "price": 1899
    },
    "userId": "user-456",
    "sessionId": "session-xyz789",
    "fingerprint": "fp-abc123def456"
  }
]
```

## 3. Anonymous User Request

```json
POST /api/tracking
Content-Type: application/json

[
  {
    "type": "product_interest",
    "trigger": "time_spent",
    "timestamp": 1703123456789,
    "product": {
      "id": "laptop-456",
      "name": "Dell XPS 13",
      "brand": "Dell",
      "category": "Ultrabooks",
      "price": 1299
    },
    "timeOnPage": 15000,
    "scrollDepth": 60,
    "url": "/products/laptop-456",
    "userId": null,
    "sessionId": "session-anonymous-123",
    "fingerprint": "fp-anonymous-789abc",
    "priority": "high"
  }
]
```

## 4. Click Event with Additional Data

```json
POST /api/tracking
Content-Type: application/json

[
  {
    "type": "click",
    "timestamp": 1703123456789,
    "element": {
      "tagName": "A",
      "className": "product-link",
      "id": "product-link-123",
      "text": "View Details"
    },
    "url": "/products/category/laptops",
    "userId": "user-789",
    "sessionId": "session-def456",
    "fingerprint": "fp-ghi789jkl012",
    "action": "view_details",
    "productId": "laptop-123",
    "productName": "MacBook Pro 16\"",
    "productCategory": "Laptops"
  }
]
```

## 5. Navigation Click Event

```json
POST /api/tracking
Content-Type: application/json

[
  {
    "type": "click",
    "timestamp": 1703123456789,
    "element": {
      "tagName": "A",
      "className": "nav-link",
      "id": "nav-laptops",
      "text": "Laptops"
    },
    "url": "/",
    "userId": "user-123",
    "sessionId": "session-abc123",
    "fingerprint": "fp-def456ghi789",
    "action": "navigation",
    "section": "header",
    "destination": "/laptops"
  }
]
```

## Key Points About the API Requests

- **Single Array Format**: All requests send events as an array, even for single events
- **Immediate vs Batch**: Product interest events are sent immediately, others are batched
- **User Context**: Always includes userId (null for anonymous), sessionId, and fingerprint
- **Timestamps**: All events include Unix timestamp in milliseconds
- **URL Context**: Current page URL is included with each event
- **Flexible Data**: Additional properties can be added to events (like action, value, etc.)
- **Product Data**: Product events include comprehensive product information
- **Element Details**: Click events capture detailed element information

The `trackingApi.sendTrack()` method handles the actual HTTP POST request to your tracking endpoint with these JSON payloads.

# Get hybrid recommendations
GET /laptops/recommendations/hybrid?fingerprint=fp-abc123&limit=10&collaborative_weight=0.7&content_weight=0.3

# Track interaction
POST /laptops/track-interaction?laptop_id=laptop-123&interaction_type=product_view&fingerprint=fp-abc123&session_id=session-xyz