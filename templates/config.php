<?php
// Настройки Palladium
define('PALLADIUM_TOKEN', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiZDBiM2Y3YjJmOTlhMzU3ZDg4ZjM3MmIxZmFhOThiZjFmNGMwMzJkOGFhMjZiNjA3NjE1NmNiN2FiNWYxN2E1MDJhYWM4Mzk5MjU4ZTA0MjciLCJpYXQiOjE3NDQ4OTM4NjYuNjQxODU3LCJuYmYiOjE3NDQ4OTM4NjYuNjQxODYsImV4cCI6MTc3NjQyOTg2Ni42Mjc5OCwic3ViIjoiNDcyMCIsInNjb3BlcyI6W119.bDJYISa_hs9PjRV1SytoMfaYihRVOsvgE-vT3Hyre_v6GDr77FOk_tCkRt5VGa4SbphZ6IvmJpavySbT7lEuhio3f_xzoGsn78bd1N6OTFyF-uL8ptQjLZvanxdf4jzW083yb-v05lYSOkSAY6rMpn2sw5ZHAJWJe59uhmB5t9E8bcjXlc6PDgwiwhFYTM5_5hv3k5IdBFFHYEF9P2RQ6iqH-LMCqcpbhxN5tN_QBCqocyTBaUIhUQUuc4f9H4wmT8CWrE6CQS1jJPF7JKF-EuEEpqwkfN4gwj00ibqXdbx89w7vhH4_RQ_yaT2m-dmNbPQuXwsstmFTZWC0XFrIYhqI8j7rblauYQX-1c5wZSHIvLM_Q26lPonQJhigW5adnaeOl--zvg44sPlVi7Y21lrp_uxaJbhwdV3UWoItfwFVewkvn3gcEsapJLyuozXPpYP-7lI2wXAFMMxsPS65Z6HhG6smtUUYx8GFqbL0LJ3XaJtkvU_S1287b6RHqn7HuDZrP01XvCdnuGPKSuKHpDyNH4AnAghZ9MPXn9hHC6c092YeKWxxTKV1gop1MYCFYAZnYO9NVaOHTvhKQCQ7tnosB9OXhyL1vSMeLIOcIr6BU6Y1zV5qOh4hvFCXhpSg5SBATzaljo7h4wVNp9K4wU0Op--Z2jULWa4SejrFzMQ');
define('PALLADIUM_URL', 'https://api.palladium.expert/');

// Базовый URL оффера
define('OFFER_BASE_URL', 'https://mytreck.monster/jRBjNfWT');

// Настройки редиректов
$OFFERS = [
    'GameNova' => [
        'white' => 'https://www.kongregate.com',
        'real' => OFFER_BASE_URL . '?source=gamenova'
    ],
    'QuickJoy' => [
        'white' => 'https://www.miniclip.com',
        'real' => OFFER_BASE_URL . '?source=quickjoy'
    ],
    'PlaySphere' => [
        'white' => 'https://www.addictinggames.com',
        'real' => OFFER_BASE_URL . '?source=playsphere'
    ],
    'FunHub' => [
        'white' => 'https://www.crazygames.com',
        'real' => OFFER_BASE_URL . '?source=funhub'
    ],
    'PuzzleLand' => [
        'white' => 'https://www.coolmathgames.com',
        'real' => OFFER_BASE_URL . '?source=puzzleland'
    ],
    'SportZone' => [
        'white' => 'https://www.gamesgames.com/games/sports',
        'real' => OFFER_BASE_URL . '?source=sportzone'
    ]
];

// Параметры для передачи
$TRACK_PARAMS = [
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_content',
    'utm_term',
    'click_id',
    'source',
    'sub1',
    'sub2',
    'sub3',
    'sub4',
    'sub5'
];

// Настройки фильтрации
$ALLOWED_COUNTRIES = ['RU', 'BY', 'UA'];
$ALLOWED_DEVICES = ['desktop', 'mobile'];
?> 