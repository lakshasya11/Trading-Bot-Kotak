# Trading Bot Kotak - API Documentation

---

## Base URL
```
http://localhost:8000
```

---

## Authentication Endpoints

### 1. Login
```
GET /login
```
**Description**: Initiates login process for the trading bot

**Response**: Redirects to login page or returns session information

---

### 2. Authenticate
```
POST /api/authenticate
```
**Description**: Authenticates user with credentials

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Authentication successful",
  "session_id": "string"
}
```

---

## Status & Information Endpoints

### 3. Bot Status
```
GET /api/status
```
**Description**: Get current trading bot status

**Response**:
```json
{
  "bot_running": true,
  "bot_paused": false,
  "active_trades": 0,
  "total_trades_today": 0,
  "pnl_today": 0.0,
  "capital_available": 0.0
}
```

---

### 4. Debug Information
```
GET /api/debug_info
```
**Description**: Get debug information for troubleshooting

**Response**:
```json
{
  "timestamp": "2026-03-13T10:30:00Z",
  "version": "1.0.0",
  "broker": "kotak",
  "debug_mode": true
}
```

---

### 5. Diagnostics
```
GET /api/diagnostics
```
**Description**: Get detailed diagnostics of bot health and system status

**Response**:
```json
{
  "system_health": "healthy",
  "database_status": "connected",
  "websocket_status": "connected",
  "market_feed": "active",
  "issues": []
}
```

---

## Trade Information Endpoints

### 6. Trade History (Today)
```
GET /api/trade_history
```
**Description**: Get all trades executed today

**Query Parameters**:
- `limit` (optional): Max number of trades to return (default: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response**:
```json
{
  "trades": [
    {
      "trade_id": "12345",
      "symbol": "BANKNIFTY",
      "entry_price": 45000.00,
      "exit_price": 45050.00,
      "quantity": 1,
      "pnl": 50.00,
      "entry_time": "2026-03-13T09:30:00Z",
      "exit_time": "2026-03-13T10:00:00Z"
    }
  ],
  "total": 1,
  "count": 1
}
```

---

### 7. Trade History (All Time)
```
GET /api/trade_history_all
```
**Description**: Get all historical trades from database

**Query Parameters**:
- `limit` (optional): Max number of trades to return
- `offset` (optional): Pagination offset
- `from_date` (optional): Filter from date (YYYY-MM-DD)
- `to_date` (optional): Filter to date (YYYY-MM-DD)

**Response**: Similar to `/api/trade_history`

---

### 8. Performance Metrics
```
GET /api/performance
```
**Description**: Get performance statistics and metrics

**Response**:
```json
{
  "total_trades": 50,
  "winning_trades": 35,
  "losing_trades": 15,
  "win_rate": 70.0,
  "total_pnl": 5000.00,
  "avg_win": 200.00,
  "avg_loss": -100.00,
  "max_drawdown": -500.00,
  "sharpe_ratio": 1.5
}
```

---

## Strategy & Parameters Endpoints

### 9. Update Strategy Parameters
```
POST /api/update_strategy_params
```
**Description**: Update trading strategy parameters

**Request Body**:
```json
{
  "supertrend_period": 10,
  "supertrend_multiplier": 3.0,
  "atr_period": 14,
  "rsi_period": 14,
  "rsi_threshold": 30,
  "sl_percent": 2.0,
  "tp_percent": 5.0
}
```

**Response**:
```json
{
  "success": true,
  "message": "Parameters updated successfully",
  "new_params": {}
}
```

---

### 10. Reset Parameters to Default
```
POST /api/reset_params
```
**Description**: Reset all strategy parameters to default values

**Response**:
```json
{
  "success": true,
  "message": "Parameters reset to default",
  "params": {}
}
```

---

### 11. Update UOA Watchlist
```
POST /api/reset_uoa_watchlist
```
**Description**: Update the Underlying On Arrival (UOA) watchlist

**Request Body**:
```json
{
  "symbols": ["BANKNIFTY", "NIFTY", "FINNIFTY"]
}
```

**Response**:
```json
{
  "success": true,
  "message": "Watchlist updated",
  "watchlist": []
}
```

---

## Bot Control Endpoints

### 12. Start Bot
```
POST /api/start
```
**Description**: Start the trading bot

**Response**:
```json
{
  "success": true,
  "message": "Bot started successfully"
}
```

---

### 13. Stop Bot
```
POST /api/stop
```
**Description**: Stop the trading bot

**Response**:
```json
{
  "success": true,
  "message": "Bot stopped successfully"
}
```

---

### 14. Pause Bot
```
POST /api/pause
```
**Description**: Pause trading (don't enter new trades, but manage existing ones)

**Response**:
```json
{
  "success": true,
  "message": "Bot paused"
}
```

---

### 15. Unpause Bot
```
POST /api/unpause
```
**Description**: Resume trading after pause

**Response**:
```json
{
  "success": true,
  "message": "Bot resumed"
}
```

---

### 16. Manual Exit
```
POST /api/manual_exit
```
**Description**: Manually exit a specific trade

**Request Body**:
```json
{
  "trade_id": "12345"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Trade exited successfully",
  "exit_price": 45050.00,
  "pnl": 50.00
}
```

---

## Optimization Endpoints

### 17. Optimize Strategy
```
POST /api/optimize
```
**Description**: Run strategy optimization process

**Request Body**:
```json
{
  "optimization_type": "grid_search",
  "iterations": 100,
  "parameters": []
}
```

**Response**:
```json
{
  "success": true,
  "message": "Optimization started",
  "job_id": "opt_12345",
  "status": "running"
}
```

---

## Expiry Information Endpoints

### 18. Get Expiries
```
GET /api/expiries/{index_name}
```
**Description**: Get available expiry dates for a given index

**Parameters**:
- `index_name` (path): Index name (e.g., BANKNIFTY, NIFTY, FINNIFTY)

**Response**:
```json
{
  "index": "BANKNIFTY",
  "expiries": [
    "2026-03-19",
    "2026-03-26",
    "2026-04-16"
  ]
}
```

---

## User Management Endpoints

### 19. Get Users
```
GET /api/users
```
**Description**: Get list of configured users

**Response**:
```json
{
  "users": [
    {
      "id": "user1",
      "name": "User One",
      "active": true,
      "broker": "kotak"
    },
    {
      "id": "user2",
      "name": "User Two",
      "active": false,
      "broker": "kotak"
    }
  ]
}
```

---

### 20. Switch User
```
POST /api/users/switch/{user_id}
```
**Description**: Switch active trading user

**Parameters**:
- `user_id` (path): User ID to switch to

**Response**:
```json
{
  "success": true,
  "message": "Switched to user2",
  "active_user": "user2"
}
```

---

## WebSocket Endpoints

### 21. WebSocket Connection
```
WS /ws
```
**Description**: Real-time WebSocket connection for live data streaming

**Connection**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

**Incoming Messages**:
```json
{
  "type": "trade_update",
  "data": {
    "trade_id": "12345",
    "status": "active",
    "current_price": 45050.00
  }
}
```

**Outgoing Messages**:
```json
{
  "action": "get_status",
  "data": {}
}
```

---

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "detail": "Error message description",
  "status_code": 400
}
```

### Common Error Codes:
- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Authentication required
- `404`: Not Found - Endpoint or resource not found
- `500`: Internal Server Error - Server error

---

## Rate Limiting

- No current rate limiting implemented
- Recommended: Implement rate limiting for production

---

## Authentication

Currently supported authentication methods:
- Bearer Token (in development)
- Session-based authentication

---

## CORS Configuration

CORS is enabled for:
- `http://localhost:3000` (Frontend)
- `http://localhost:8000` (Backend)

---

## Examples

### Get Bot Status
```bash
curl -X GET http://localhost:8000/api/status
```

### Start Bot
```bash
curl -X POST http://localhost:8000/api/start
```

### Update Parameters
```bash
curl -X POST http://localhost:8000/api/update_strategy_params \
  -H "Content-Type: application/json" \
  -d '{
    "supertrend_period": 10,
    "supertrend_multiplier": 3.0
  }'
```

---

## Notes

- All timestamps are in UTC (ISO 8601 format)
- Prices and PnL are in INR (Indian Rupees)
- Bot runs Monday-Friday during market hours (9:15 AM - 3:30 PM IST)

---

**Last Updated**: March 13, 2026  
**API Version**: 1.0.0  
**Broker**: Kotak Neo Trading

---
