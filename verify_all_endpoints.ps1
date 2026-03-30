$report = 'ALL_ENDPOINTS_VERIFICATION.txt'
Remove-Item $report -ErrorAction SilentlyContinue

function W($t) {
    Add-Content -Path $report -Value $t
}

function Test-CrudEndpoint($scope, $service, $baseUrl, $createBody, $updateBody, $readField) {
    W("[$scope][$service]")

    try {
        $list = Invoke-RestMethod -Uri $baseUrl -Method Get
        W("GET list: PASS (count=$($list.Count))")
    }
    catch {
        W("GET list: FAIL ($($_.Exception.Message))")
        W("")
        return
    }

    try {
        $created = Invoke-RestMethod -Uri $baseUrl -Method Post -ContentType 'application/json' -Body ($createBody | ConvertTo-Json)
        $id = $created.id
        W("POST create: PASS (id=$id)")
    }
    catch {
        W("POST create: FAIL ($($_.Exception.Message))")
        W("")
        return
    }

    try {
        $single = Invoke-RestMethod -Uri ($baseUrl + '/' + $id) -Method Get
        W("GET by id: PASS ($readField=$($single.$readField))")
    }
    catch {
        W("GET by id: FAIL ($($_.Exception.Message))")
    }

    try {
        $updated = Invoke-RestMethod -Uri ($baseUrl + '/' + $id) -Method Put -ContentType 'application/json' -Body ($updateBody | ConvertTo-Json)
        W("PUT update: PASS ($readField=$($updated.$readField))")
    }
    catch {
        W("PUT update: FAIL ($($_.Exception.Message))")
    }

    try {
        Invoke-RestMethod -Uri ($baseUrl + '/' + $id) -Method Delete | Out-Null
        W('DELETE: PASS')
    }
    catch {
        W("DELETE: FAIL ($($_.Exception.Message))")
    }

    try {
        Invoke-RestMethod -Uri ($baseUrl + '/' + $id) -Method Get | Out-Null
        W('GET after delete: FAIL (still exists)')
    }
    catch {
        W('GET after delete: PASS (not found)')
    }

    W("")
}

W('Full Endpoint Verification Report')
W('Generated: ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))
W('')

# Direct microservice endpoints
Test-CrudEndpoint 'Direct' 'Users' 'http://127.0.0.1:8021/api/users' @{name='Verify User';email='verify.user@example.com';phone='0701234567'} @{name='Verify User Updated'} 'name'
Test-CrudEndpoint 'Direct' 'Restaurants' 'http://127.0.0.1:8022/api/restaurants' @{name='Verify Restaurant';cuisine='Fusion';city='Colombo'} @{city='Kandy'} 'city'
Test-CrudEndpoint 'Direct' 'Orders' 'http://127.0.0.1:8023/api/orders' @{user_id=1;restaurant_id=1;total_amount=1500.0;status='PLACED'} @{status='PREPARING'} 'status'
Test-CrudEndpoint 'Direct' 'Payments' 'http://127.0.0.1:8024/api/payments' @{order_id=1;amount=1500.0;method='CARD';status='PENDING'} @{status='PAID'} 'status'
Test-CrudEndpoint 'Direct' 'Deliveries' 'http://127.0.0.1:8025/api/deliveries' @{order_id=1;rider_name='Verify Rider';current_location='Colombo';status='ASSIGNED'} @{status='PICKED'} 'status'

# Gateway endpoints
Test-CrudEndpoint 'Gateway' 'Users' 'http://127.0.0.1:8020/gateway/users' @{name='Verify User';email='verify.user@example.com';phone='0701234567'} @{name='Verify User Updated'} 'name'
Test-CrudEndpoint 'Gateway' 'Restaurants' 'http://127.0.0.1:8020/gateway/restaurants' @{name='Verify Restaurant';cuisine='Fusion';city='Colombo'} @{city='Kandy'} 'city'
Test-CrudEndpoint 'Gateway' 'Orders' 'http://127.0.0.1:8020/gateway/orders' @{user_id=1;restaurant_id=1;total_amount=1500.0;status='PLACED'} @{status='PREPARING'} 'status'
Test-CrudEndpoint 'Gateway' 'Payments' 'http://127.0.0.1:8020/gateway/payments' @{order_id=1;amount=1500.0;method='CARD';status='PENDING'} @{status='PAID'} 'status'
Test-CrudEndpoint 'Gateway' 'Deliveries' 'http://127.0.0.1:8020/gateway/deliveries' @{order_id=1;rider_name='Verify Rider';current_location='Colombo';status='ASSIGNED'} @{status='PICKED'} 'status'

Get-Content $report
