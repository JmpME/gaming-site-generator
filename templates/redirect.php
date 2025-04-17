<?php
require_once 'config.php';
require_once 'jmpDG.php'; // Подключаем файл палладиума

// Получаем параметры
$platform = $_GET['platform'] ?? '';

// Проверяем существование платформы
if (!isset($OFFERS[$platform])) {
    header('Location: index.php');
    exit();
}

// Собираем параметры трекинга
$tracking_params = [];
foreach($TRACK_PARAMS as $param) {
    if(isset($_GET[$param])) {
        $tracking_params[$param] = $_GET[$param];
    }
}

// Добавляем source к параметрам трекинга
$tracking_params['source'] = $platform;

// Проверяем через Palladium
$isTarget = (new RequestHandlerClient())->run();

if(!$isTarget) {
    // Для ботов показываем белую страницу
    header('Location: ' . $OFFERS[$platform]['white']);
} else {
    // Для реальных пользователей - оффер со всеми метками
    $target_url = buildUrl($OFFERS[$platform]['real'], $tracking_params);
    header('Location: ' . $target_url);
}

// Функция для построения URL с параметрами
function buildUrl($base_url, $params) {
    if(empty($params)) return $base_url;
    
    $url = $base_url;
    $separator = (strpos($base_url, '?') === false) ? '?' : '&';
    
    foreach($params as $key => $value) {
        $url .= $separator . urlencode($key) . '=' . urlencode($value);
        $separator = '&';
    }
    
    return $url;
}

exit();
?> 