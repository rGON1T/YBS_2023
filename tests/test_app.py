from httpx import AsyncClient


async def test_courier_post(ac: AsyncClient):
    response = await ac.post("/couriers", json={
        "couriers": [
            {
                "courier_type": "AUTO",
                "regions": [
                    1,
                    2,
                    3
                ],
                "working_hours": [
                    "12:00-15:00"
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "couriers": [
            {
                "courier_type": "AUTO",
                "regions": [
                    1,
                    2,
                    3
                ],
                "working_hours": [
                    "12:00-15:00"
                ]
            }
        ]
    }


async def test_several_courier_post(ac: AsyncClient):
    response = await ac.post("/couriers", json={
        "couriers": [
            {
                "courier_type": "AUTO",
                "regions": [
                    1,
                    2,
                    3
                ],
                "working_hours": [
                    "12:00-15:00"
                ]
            },
            {
                "courier_type": "BIKE",
                "regions": [
                    2,
                    4,
                    6
                ],
                "working_hours": [
                    "12:00-15:00",
                    "20:00-23:00"
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "couriers": [
            {
                "courier_type": "AUTO",
                "regions": [
                    1,
                    2,
                    3
                ],
                "working_hours": [
                    "12:00-15:00"
                ]
            },
            {
                "courier_type": "BIKE",
                "regions": [
                    2,
                    4,
                    6
                ],
                "working_hours": [
                    "12:00-15:00",
                    "20:00-23:00"
                ]
            }
        ]
    }


async def test_courier_post_incorrect_type(ac: AsyncClient):
    response = await ac.post("/couriers", json={
        "couriers": [
            {
                "courier_type": "LIKE",
                "regions": [
                    1,
                    2,
                    3
                ],
                "working_hours": [
                    "12:00-15:00"
                ]
            }
        ]
    })
    assert response.status_code == 422


async def test_courier_post_incorrect_time_format(ac: AsyncClient):
    response = await ac.post("/couriers", json={
        "couriers": [
            {
                "courier_type": "LIKE",
                "regions": [
                    1,
                    2,
                    3
                ],
                "working_hours": [
                    "25:00-15:00"
                ]
            }
        ]
    })
    assert response.status_code == 422


async def test_courier_get_by_id_2(ac: AsyncClient):
    response = await ac.get("/couriers/2")
    assert response.status_code == 200
    assert response.json() == {
        "courier_id": 2,
        "courier_type": "AUTO",
        "regions": [
            1,
            2,
            3
        ],
        "working_hours": [
            "12:00-15:00"
        ]
    }


async def test_courier_get_by_id(ac: AsyncClient):
    response = await ac.get("/couriers/1")
    assert response.status_code == 200


async def test_not_exists_courier_get_by_id(ac: AsyncClient):
    response = await ac.get("/couriers/5")
    assert response.status_code == 400
    assert response.json() == {'detail': 'courier 5 not found'}


async def test_courier_get(ac: AsyncClient):
    response = await ac.get("/couriers", params={'limit': 2, 'offset': 1})
    assert response.status_code == 200
    assert response.json() == {
        'couriers': [
            {
                'courier_id': 2,
                'courier_type': 'AUTO',
                'regions': [
                    1,
                    2,
                    3
                ],
                'working_hours': [
                    '12:00-15:00'
                ]
            },
            {
                'courier_id': 3,
                'courier_type': 'BIKE',
                'regions': [
                    2,
                    4,
                    6
                ],
                'working_hours': [
                    '12:00-15:00',
                    '20:00-23:00'
                ]
            }
        ],
        'limit': 2,
        'offset': 1}


async def test_courier_get_without_params(ac: AsyncClient):
    response = await ac.get("/couriers")
    assert response.status_code == 200
    assert response.json() == {"couriers": [(await ac.get("/couriers/1")).json()], 'limit': 1, 'offset': 0}


async def test_courier_get_empty_list(ac: AsyncClient):
    response = await ac.get("/couriers", params={'limit': 2, 'offset': 10})
    assert response.status_code == 200
    assert response.json() == {'couriers': [], 'limit': 2, 'offset': 10}


async def test_courier_get_empty_list_2(ac: AsyncClient):
    response = await ac.get("/couriers", params={'limit': 0, 'offset': 1})
    assert response.status_code == 200
    assert response.json() == {'couriers': [], 'limit': 0, 'offset': 1}


async def test_order_post(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "orders": [
            {
                "weight": 25.5,
                "regions": 1,
                "delivery_hours": [
                    "10:00-15:00"
                ],
                "cost": 40
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "orders": [
            {
                "weight": 25.5,
                "regions": 1,
                "delivery_hours": [
                    "10:00-15:00"
                ],
                "cost": 40
            }
        ]
    }


async def test_several_orders_post(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "orders": [
            {
                "weight": 35.5,
                "regions": 2,
                "delivery_hours": [
                    "9:00-13:00"
                ],
                "cost": 80
            },
            {
                "weight": 20,
                "regions": 3,
                "delivery_hours": [
                    "15:00-16:00"
                ],
                "cost": 45
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "orders": [
            {
                "weight": 35.5,
                "regions": 2,
                "delivery_hours": [
                    "9:00-13:00"
                ],
                "cost": 80
            },
            {
                "weight": 20,
                "regions": 3,
                "delivery_hours": [
                    "15:00-16:00"
                ],
                "cost": 45
            }
        ]
    }


async def test_several_orders_post_2(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "orders": [
            {
                "weight": 10,
                "regions": 4,
                "delivery_hours": [
                    "15:00-15:15"
                ],
                "cost": 100
            },
            {
                "weight": 70,
                "regions": 6,
                "delivery_hours": [
                    "20:00-23:00"
                ],
                "cost": 75
            }
        ]
    })
    assert response.status_code == 200


async def test_order_post_field_required(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "orders": [
            {
                "weight": 25.5,
                "delivery_hours": [
                    "10:00-15:00"
                ],
                "cost": 40
            }
        ]
    })
    assert response.status_code == 422


async def test_order_post_incorrect_value(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "orders": [
            {
                "weight": -5,
                "regions": 1,
                "delivery_hours": [
                    "10:00-15:00"
                ],
                "cost": 40.5
            }
        ]
    })
    assert response.status_code == 422


async def test_order_post_incorrect_time_format(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "orders": [
            {
                "weight": 25.5,
                "regions": 1,
                "delivery_hours": [
                    "001:00-15:00"
                ],
                "cost": 40
            }
        ]
    })
    assert response.status_code == 422


async def test_order_get(ac: AsyncClient):
    response = await ac.get("/orders", params={'limit': 2, 'offset': 1})
    assert response.status_code == 200
    assert response.json() == [(await ac.get("/orders/2")).json(), (await ac.get("/orders/3")).json(), ]


async def test_order_get_by_id(ac: AsyncClient):
    response = await ac.get("/orders/2")
    assert response.status_code == 200
    assert response.json() == {
        "order_id": 2,
        "weight": 35.5,
        "regions": 2,
        "delivery_hours": [
            "9:00-13:00"
        ],
        "cost": 80,
        "complete_time": None
    }


async def test_not_exists_order_get_by_id(ac: AsyncClient):
    response = await ac.get("/orders/6")
    assert response.status_code == 400
    assert response.json() == {'detail': 'order 6 not found'}


async def test_order_get_without_params(ac: AsyncClient):
    response = await ac.get("/orders")
    assert response.status_code == 200
    assert response.json() == [(await ac.get("/orders/1")).json()]


async def test_order_get_empty_list(ac: AsyncClient):
    response = await ac.get("/orders", params={'limit': 2, 'offset': 100})
    assert response.status_code == 200
    assert response.json() == []


async def test_order_get_empty_list_2(ac: AsyncClient):
    response = await ac.get("/orders", params={'limit': 0, 'offset': 0})
    assert response.status_code == 200
    assert response.json() == []


async def test_complete_order(ac: AsyncClient):
    response = await ac.post("/orders/complete", json={
        "complete_info": [
            {
                "courier_id": 1,
                "order_id": 1,
                "complete_time": "2023-05-15T14:49:28.119Z"
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [(await ac.get("/orders/1")).json()]


async def test_complete_several_orders(ac: AsyncClient):
    response = await ac.post("/orders/complete", json={
        "complete_info": [
            {
                "courier_id": 1,
                "order_id": 2,
                "complete_time": "2023-05-15T14:49:28.119Z"
            },
            {
                "courier_id": 2,
                "order_id": 3,
                "complete_time": "2023-05-15T14:49:28.119Z"
            },
            {
                "courier_id": 1,
                "order_id": 4,
                "complete_time": "2023-05-15T14:49:28.119Z"
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [(await ac.get("/orders/2")).json(), (await ac.get("/orders/3")).json(),
                               (await ac.get("/orders/4")).json()]


async def test_complete_order_courier_not_found(ac: AsyncClient):
    response = await ac.post("/orders/complete", json={
        "complete_info": [
            {
                "courier_id": 20,
                "order_id": 1,
                "complete_time": "2023-05-15T14:49:28.119Z"
            }
        ]
    })
    assert response.status_code == 400


async def test_complete_order_order_not_found(ac: AsyncClient):
    response = await ac.post("/orders/complete", json={
        "complete_info": [
            {
                "courier_id": 1,
                "order_id": 20,
                "complete_time": "2023-05-15T14:49:28.119Z"
            }
        ]
    })
    assert response.status_code == 400


async def test_complete_order_already_completed(ac: AsyncClient):
    response = await ac.post("/orders/complete", json={
        "complete_info": [
            {
                "courier_id": 1,
                "order_id": 1,
                "complete_time": "2023-05-15T14:49:28.119Z"
            }
        ]
    })
    assert response.status_code == 400


async def test_get_couriers_metainfo(ac: AsyncClient):
    response = await ac.get("/couriers/meta-info/1?startDate=2023-05-15&endDate=2023-05-16")
    assert response.status_code == 200
    assert response.json() == {'courier_id': 1, 'courier_type': 'AUTO', 'regions': [1, 2, 3],
                               'working_hours': ['12:00-15:00'], 'rating': 0, 'earnings': 880}
