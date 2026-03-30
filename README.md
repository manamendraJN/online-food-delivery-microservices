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

### 2. Restaurant Service
- Purpose: Manages restaurant details such as name, cuisine, and city.
- Base API: /api/restaurants
- Typical operations: Create restaurant, list restaurants, get by id, update, delete.

### 3. Order Service
- Purpose: Manages food orders placed by users to restaurants.
- Base API: /api/orders
- Typical operations: Create order, track status, update order status, delete order.

### 4. Payment Service
- Purpose: Manages payment records for orders.
- Base API: /api/payments
- Typical operations: Create payment, check payment status, update payment status, delete payment.

### 5. Delivery Service
- Purpose: Manages delivery assignments and delivery tracking status.
- Base API: /api/deliveries
- Typical operations: Create delivery, update rider/location/status, get by id, delete.

## API Gateway

- Service: gateway-food-delivery
- Purpose: Single entry point for all domains.
- Gateway routes: /gateway/users, /gateway/restaurants, /gateway/orders, /gateway/payments, /gateway/deliveries
- Behavior: Forwards requests to the matching backend microservice and returns the same response.

## Ports

- Gateway: 8020
- User: 8021
- Restaurant: 8022
- Order: 8023
- Payment: 8024
- Delivery: 8025