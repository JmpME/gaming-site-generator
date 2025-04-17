<?php
require_once 'config.php';

function checkPalladium($ip, $userAgent) {
    $data = [
        'token' => PALLADIUM_TOKEN,
        'ip' => $ip,
        'ua' => $userAgent,
        'url' => $_SERVER['HTTP_REFERER'] ?? '',
    ];

    $ch = curl_init(PALLADIUM_URL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    
    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}

function isBot($checkResult) {
    return isset($checkResult['is_bot']) && $checkResult['is_bot'] === true;
}
?> 