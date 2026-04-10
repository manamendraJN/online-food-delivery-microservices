# Online Food Delivery Microservices - How To Run

This guide shows the cleanest way to run the full project on Windows and test all API endpoints.

## Architecture

Services and ports:
- API Gateway: 8020
- User Service: 8021
- Restaurant Service: 8022
- Order Service: 8023
- Payment Service: 8024
- Delivery Service: 8025

You can test APIs in two modes:
- Direct mode: Call each microservice directly on ports 8021-8025.
- Gateway mode: Call through the gateway on port 8020.

## Prerequisites

- Windows with PowerShell
- Python 3.10 or newer

Optional:
- VS Code

## 1. Open the project root

Open PowerShell and go to the folder that contains requirements.txt:

```powershell
cd <path-to-online-food-delivery-microservices>
```

## 2. Set up Python (recommended: virtual environment)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If your machine does not recognize python, use the full python.exe path in all commands.

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Start all services

Open 6 terminals from the project root and run one command in each terminal.

Terminal 1 (User Service):
```powershell
cd user-service
python -m uvicorn main:app --host 127.0.0.1 --port 8021
```

Terminal 2 (Restaurant Service):
```powershell
cd restaurant-service
python -m uvicorn main:app --host 127.0.0.1 --port 8022
```

Terminal 3 (Order Service):
```powershell
cd order-service
python -m uvicorn main:app --host 127.0.0.1 --port 8023
```

Terminal 4 (Payment Service):
```powershell
cd payment-service
python -m uvicorn main:app --host 127.0.0.1 --port 8024
```

Terminal 5 (Delivery Service):
```powershell
cd delivery-service
python -m uvicorn main:app --host 127.0.0.1 --port 8025
```

Terminal 6 (Gateway Service):
```powershell
cd gateway-food-delivery
python -m uvicorn main:app --host 127.0.0.1 --port 8020
```

Each terminal should show startup messages similar to:
- Application startup complete.
- Uvicorn running on http://127.0.0.1:<port>

## 5. Quick health checks

Open in browser:
- http://127.0.0.1:8020/
- http://127.0.0.1:8021/
- http://127.0.0.1:8022/
- http://127.0.0.1:8023/
- http://127.0.0.1:8024/
- http://127.0.0.1:8025/

Swagger docs:
- Gateway: http://127.0.0.1:8020/docs
- User: http://127.0.0.1:8021/docs
- Restaurant: http://127.0.0.1:8022/docs
- Order: http://127.0.0.1:8023/docs
- Payment: http://127.0.0.1:8024/docs
- Delivery: http://127.0.0.1:8025/docs

## 6. Run full API verification (recommended)

From project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_all_endpoints.ps1
```

What this script verifies:
- CRUD flow for all 5 domains
- Direct endpoints (ports 8021-8025)
- Gateway endpoints (port 8020)

Output report:
- ALL_ENDPOINTS_VERIFICATION.txt

## 7. Manual quick checks (optional)

Direct mode:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8021/api/users/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8022/api/restaurants/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8023/api/orders/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8024/api/payments/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8025/api/deliveries/read-all" -Method Get
```

Gateway mode:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8020/gateway/users/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8020/gateway/restaurants/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8020/gateway/orders/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8020/gateway/payments/read-all" -Method Get
Invoke-RestMethod -Uri "http://127.0.0.1:8020/gateway/deliveries/read-all" -Method Get
```

## 8. Troubleshooting

### Port already in use

Error example:
- only one usage of each socket address is normally permitted

Find process using a port:
```powershell
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -eq 8021 }
```

Kill by process id (replace <PID>):
```powershell
Stop-Process -Id <PID> -Force
```

### Gateway returns 503

Cause:
- One or more backend services are not running.

Fix:
- Start all microservices first (8021-8025), then start or retry gateway requests.

### Module import errors

```powershell
python -m pip install -r requirements.txt
```

## 9. Stop the project

In each service terminal, press Ctrl + C.
