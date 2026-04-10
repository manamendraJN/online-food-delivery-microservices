# Online Food Delivery Microservices

## Project Overview

This project is a simple microservices-based food delivery backend built with FastAPI.
It demonstrates how to split a domain into independent services and expose them through an API Gateway.

Main goals of this project:
- Keep each domain isolated in its own service.
- Provide standard CRUD APIs for each domain.
- Route all domains through one gateway endpoint layer.
- Support both direct service testing and gateway testing.

## Microservices (Small Explanation)

### 1. User Service
- Purpose: Manages customer profile data.
- Base API: /api/users
- Typical operations: Create user, list users, get user by id, update user, delete user.

endpoints:
- GET /api/users/read-all
- GET /api/users/read/{user_id}
- POST /api/users/create
- PUT /api/users/update/{user_id}
- DELETE /api/users/delete/{user_id}

### 2. Restaurant Service
- Purpose: Manages restaurant details such as name, cuisine, and city.
- Base API: /api/restaurants
- Typical operations: Create restaurant, list restaurants, get by id, update, delete.

endpoints:
- GET /api/restaurants/read-all
- GET /api/restaurants/read/{restaurant_id}
- POST /api/restaurants/create
- PUT /api/restaurants/update/{restaurant_id}
- DELETE /api/restaurants/delete/{restaurant_id}

### 3. Order Service
- Purpose: Manages food orders placed by users to restaurants.
- Base API: /api/orders
- Typical operations: Create order, track status, update order status, delete order.

endpoints:
- GET /api/orders/read-all
- GET /api/orders/read/{order_id}
- POST /api/orders/create
- PUT /api/orders/update/{order_id}
- DELETE /api/orders/delete/{order_id}

### 4. Payment Service
- Purpose: Manages payment records for orders.
- Base API: /api/payments
- Typical operations: Create payment, check payment status, update payment status, delete payment.

endpoints:
- GET /api/payments/read-all
- GET /api/payments/read/{payment_id}
- POST /api/payments/create
- PUT /api/payments/update/{payment_id}
- DELETE /api/payments/delete/{payment_id}

### 5. Delivery Service
- Purpose: Manages delivery assignments and delivery tracking status.
- Base API: /api/deliveries
- Typical operations: Create delivery, update rider/location/status, get by id, delete.

endpoints:
- GET /api/deliveries/read-all
- GET /api/deliveries/read/{delivery_id}
- POST /api/deliveries/create
- PUT /api/deliveries/update/{delivery_id}
- DELETE /api/deliveries/delete/{delivery_id}

## API Gateway

- Service: gateway-food-delivery
- Purpose: Single entry point for all domains.
- Gateway route groups: /gateway/users, /gateway/restaurants, /gateway/orders, /gateway/payments, /gateway/deliveries
- Behavior: Forwards requests to the matching backend microservice and returns the same response.

### Gateway Endpoints

Users:
- GET /gateway/users/read-all
- GET /gateway/users/read/{user_id}
- POST /gateway/users/create
- PUT /gateway/users/update/{user_id}
- DELETE /gateway/users/delete/{user_id}

Restaurants:
- GET /gateway/restaurants/read-all
- GET /gateway/restaurants/read/{restaurant_id}
- POST /gateway/restaurants/create
- PUT /gateway/restaurants/update/{restaurant_id}
- DELETE /gateway/restaurants/delete/{restaurant_id}

Orders:
- GET /gateway/orders/read-all
- GET /gateway/orders/read/{order_id}
- POST /gateway/orders/create
- PUT /gateway/orders/update/{order_id}
- DELETE /gateway/orders/delete/{order_id}

Payments:
- GET /gateway/payments/read-all
- GET /gateway/payments/read/{payment_id}
- POST /gateway/payments/create
- PUT /gateway/payments/update/{payment_id}
- DELETE /gateway/payments/delete/{payment_id}

Deliveries:
- GET /gateway/deliveries/read-all
- GET /gateway/deliveries/read/{delivery_id}
- POST /gateway/deliveries/create
- PUT /gateway/deliveries/update/{delivery_id}
- DELETE /gateway/deliveries/delete/{delivery_id}

## Ports

- Gateway: 8020
- User: 8021
- Restaurant: 8022
- Order: 8023
- Payment: 8024
- Delivery: 8025

## Status Codes Used In This Project

The API uses these status codes.

- 200 OK
Used when a request succeeds and returns data (for example most GET and successful update calls).

- 201 Created
Used when a new resource is created successfully (POST create endpoints).

- 204 No Content
Used when delete succeeds and there is no response body.

- 404 Not Found
Used when the requested record does not exist (for example user_id, order_id not found) or unknown gateway service key.

- 405 Method Not Allowed
Used in gateway forwarding logic when an unsupported HTTP method is requested.

- 500 Internal Server Error
Used in microservices when unexpected server-side exceptions happen.

- 503 Service Unavailable
Used by the gateway when a backend microservice cannot be reached.

- 504 Gateway Timeout
Used by the gateway when a backend microservice does not respond in time.

Note:
- FastAPI may also return 422 Unprocessable Entity automatically for invalid request body/path/query validation errors.

## Microservices vs Direct API Access

This project uses a microservices architecture.
Each business domain is split into a separate service (User, Restaurant, Order, Payment, Delivery).
Because these services run independently, clients can access APIs in two patterns:

- Direct API access: client calls each microservice directly.
- Gateway API access: client calls only the gateway, and gateway forwards to microservices.

This section explains the difference in architecture, operations, and security.

### 1. Direct API Access

The client calls each service directly on its own port.

Example:
- Read users: http://127.0.0.1:8021/api/users/read-all
- Read orders: http://127.0.0.1:8023/api/orders/read-all

Request flow:
- Client -> Target microservice

Operational behavior:
- Client must know each service address.
- Each service can evolve independently, but clients must track route/port changes.
- Good for internal debugging because there is no proxy layer hiding errors.

Best for:
- Service-level debugging
- Local development of one service
- Internal test scripts

Pros:
- Lower latency (no gateway hop)
- Very clear when debugging one service
- Fewer moving parts for isolated tests

Cons:
- Client must know all ports and service routes
- Hard to apply common policies in one place
- Tight client coupling to service topology

Security impact (important):
- Larger attack surface if every microservice is externally exposed.
- Repeating authentication/authorization logic across services is error-prone.
- Inconsistent security headers, rate limits, and request validation can happen.
- Harder centralized audit logging because requests are spread across services.

### 2. Gateway API Access

The client calls only the gateway, and the gateway forwards the request.

Example:
- Read users: http://127.0.0.1:8020/gateway/users/read-all
- Read orders: http://127.0.0.1:8020/gateway/orders/read-all

Request flow:
- Client -> Gateway -> Target microservice -> Gateway -> Client

Operational behavior:
- Clients integrate with one base URL.
- Internal service topology can change with less client impact.
- Gateway can shape requests/responses and standardize API behavior.

Best for:
- Frontend and external client integration
- Production-like access pattern
- Centralized controls and observability

Pros:
- Single entry point for all clients
- Easier centralized auth, logging, throttling, and monitoring
- Backend service changes can be hidden behind stable gateway routes

Cons:
- Adds one extra network hop
- Gateway must be maintained and monitored
- Gateway can become a bottleneck or single point of failure if not designed for high availability

Security impact (important):
- Better place to enforce authentication, authorization, and API key/JWT checks.
- Centralized rate limiting helps reduce abuse and brute-force attempts.
- Easier to apply standard security headers and input checks consistently.
- Better centralized audit logs and threat monitoring.
- Still requires service-to-service security internally (do not trust internal traffic by default).

### Practical Difference In This Project

- Same business operations are available in both modes.
- URL shape changes:
	- Direct: /api/<resource>/...
	- Gateway: /gateway/<resource>/...
- Gateway mode is usually what client apps should use.
- Direct mode is usually what developers use for internal debugging.

Security recommendation for this project:
- External clients should use gateway routes only.
- Microservice direct ports should be internal/private in production.
- Keep direct access mainly for local development and controlled internal testing.

### Which One Should You Use?

- Use gateway access for frontend/mobile clients and production-style testing.
- Use direct access when developing or troubleshooting a specific microservice quickly.
- Keep both available in development for flexibility.

Quick decision rule:
- Development/debugging of one service -> Direct access.
- Shared environments (QA/UAT/Prod) or public clients -> Gateway access.