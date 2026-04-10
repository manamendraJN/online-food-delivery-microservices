$report = 'ALL_ENDPOINTS_VERIFICATION.txt'
Remove-Item $report -ErrorAction SilentlyContinue

function W($t) {
    Add-Content -Path $report -Value $t
}

function Test-CrudEndpoint($scope, $service, $listUrl, $createUrl, $readUrlPrefix, $updateUrlPrefix, $deleteUrlPrefix, $createBody, $updateBody, $readField) {
    W("[$scope][$service]")

    try {
        $list = Invoke-RestMethod -Uri $listUrl -Method Get
        W("GET list: PASS (count=$($list.Count))")
    }
    catch {
        W("GET list: FAIL ($($_.Exception.Message))")
        W("")
        return
    }

    try {
        $created = Invoke-RestMethod -Uri $createUrl -Method Post -ContentType 'application/json' -Body ($createBody | ConvertTo-Json)
        $id = $created.id
        W("POST create: PASS (id=$id)")
    }
    catch {
        W("POST create: FAIL ($($_.Exception.Message))")
        W("")
        return
    }

    try {
        $single = Invoke-RestMethod -Uri ($readUrlPrefix + '/' + $id) -Method Get
        W("GET by id: PASS ($readField=$($single.$readField))")
    }
    catch {
        W("GET by id: FAIL ($($_.Exception.Message))")
    }

    try {
        $updated = Invoke-RestMethod -Uri ($updateUrlPrefix + '/' + $id) -Method Put -ContentType 'application/json' -Body ($updateBody | ConvertTo-Json)
        W("PUT update: PASS ($readField=$($updated.$readField))")
    }
    catch {
        W("PUT update: FAIL ($($_.Exception.Message))")
    }

    try {
        Invoke-RestMethod -Uri ($deleteUrlPrefix + '/' + $id) -Method Delete | Out-Null
        W('DELETE: PASS')
    }
    catch {
        W("DELETE: FAIL ($($_.Exception.Message))")
    }

    try {
        Invoke-RestMethod -Uri ($readUrlPrefix + '/' + $id) -Method Get | Out-Null
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
Test-CrudEndpoint 'Direct' 'Users' 'http://127.0.0.1:8021/api/users/read-all' 'http://127.0.0.1:8021/api/users/create' 'http://127.0.0.1:8021/api/users/read' 'http://127.0.0.1:8021/api/users/update' 'http://127.0.0.1:8021/api/users/delete' @{name='Verify User';email='verify.user@example.com';phone='0701234567'} @{name='Verify User Updated'} 'name'
Test-CrudEndpoint 'Direct' 'Restaurants' 'http://127.0.0.1:8022/api/restaurants/read-all' 'http://127.0.0.1:8022/api/restaurants/create' 'http://127.0.0.1:8022/api/restaurants/read' 'http://127.0.0.1:8022/api/restaurants/update' 'http://127.0.0.1:8022/api/restaurants/delete' @{name='Verify Restaurant';cuisine='Fusion';city='Colombo'} @{city='Kandy'} 'city'
Test-CrudEndpoint 'Direct' 'Orders' 'http://127.0.0.1:8023/api/orders/read-all' 'http://127.0.0.1:8023/api/orders/create' 'http://127.0.0.1:8023/api/orders/read' 'http://127.0.0.1:8023/api/orders/update' 'http://127.0.0.1:8023/api/orders/delete' @{user_id=1;restaurant_id=1;total_amount=1500.0;status='PLACED'} @{status='PREPARING'} 'status'
Test-CrudEndpoint 'Direct' 'Payments' 'http://127.0.0.1:8024/api/payments/read-all' 'http://127.0.0.1:8024/api/payments/create' 'http://127.0.0.1:8024/api/payments/read' 'http://127.0.0.1:8024/api/payments/update' 'http://127.0.0.1:8024/api/payments/delete' @{order_id=1;amount=1500.0;method='CARD';status='PENDING'} @{status='PAID'} 'status'
Test-CrudEndpoint 'Direct' 'Deliveries' 'http://127.0.0.1:8025/api/deliveries/read-all' 'http://127.0.0.1:8025/api/deliveries/create' 'http://127.0.0.1:8025/api/deliveries/read' 'http://127.0.0.1:8025/api/deliveries/update' 'http://127.0.0.1:8025/api/deliveries/delete' @{order_id=1;rider_name='Verify Rider';current_location='Colombo';status='ASSIGNED'} @{status='PICKED'} 'status'

# Gateway endpoints
Test-CrudEndpoint 'Gateway' 'Users' 'http://127.0.0.1:8020/gateway/users/read-all' 'http://127.0.0.1:8020/gateway/users/create' 'http://127.0.0.1:8020/gateway/users/read' 'http://127.0.0.1:8020/gateway/users/update' 'http://127.0.0.1:8020/gateway/users/delete' @{name='Verify User';email='verify.user@example.com';phone='0701234567'} @{name='Verify User Updated'} 'name'
Test-CrudEndpoint 'Gateway' 'Restaurants' 'http://127.0.0.1:8020/gateway/restaurants/read-all' 'http://127.0.0.1:8020/gateway/restaurants/create' 'http://127.0.0.1:8020/gateway/restaurants/read' 'http://127.0.0.1:8020/gateway/restaurants/update' 'http://127.0.0.1:8020/gateway/restaurants/delete' @{name='Verify Restaurant';cuisine='Fusion';city='Colombo'} @{city='Kandy'} 'city'
Test-CrudEndpoint 'Gateway' 'Orders' 'http://127.0.0.1:8020/gateway/orders/read-all' 'http://127.0.0.1:8020/gateway/orders/create' 'http://127.0.0.1:8020/gateway/orders/read' 'http://127.0.0.1:8020/gateway/orders/update' 'http://127.0.0.1:8020/gateway/orders/delete' @{user_id=1;restaurant_id=1;total_amount=1500.0;status='PLACED'} @{status='PREPARING'} 'status'
Test-CrudEndpoint 'Gateway' 'Payments' 'http://127.0.0.1:8020/gateway/payments/read-all' 'http://127.0.0.1:8020/gateway/payments/create' 'http://127.0.0.1:8020/gateway/payments/read' 'http://127.0.0.1:8020/gateway/payments/update' 'http://127.0.0.1:8020/gateway/payments/delete' @{order_id=1;amount=1500.0;method='CARD';status='PENDING'} @{status='PAID'} 'status'
Test-CrudEndpoint 'Gateway' 'Deliveries' 'http://127.0.0.1:8020/gateway/deliveries/read-all' 'http://127.0.0.1:8020/gateway/deliveries/create' 'http://127.0.0.1:8020/gateway/deliveries/read' 'http://127.0.0.1:8020/gateway/deliveries/update' 'http://127.0.0.1:8020/gateway/deliveries/delete' @{order_id=1;rider_name='Verify Rider';current_location='Colombo';status='ASSIGNED'} @{status='PICKED'} 'status'

Get-Content $report
