order.py
========

Generate `orders.json` from neighborhoods data `city-data.json` and road coordinates data `roads.json`.

    ./orders.py city-data.json roads.json orders.json

`orders.json` consists of an array of orders:

    [
        <order>,
        <order>,
        <order>,
        ...
    ]

Each order is an object,

    {
        'time': '<order time in 24-hour format>',
        'location': [
            <order latitude in degrees>,
            <order longitude in degrees>
        ]
    }

For example,

    {
        'time': '12:34:56.789',
        'location': [
            39.1,
            84.5167
        ]
    }
