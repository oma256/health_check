AUTH API
=========

.. contents::
   :depth: 3



device > create
----------------------

POST ``/api/v1/device/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Register device to send FCM notification

``Request Body``
    The request body should be a "application/json"
    encoded object, containing the following items.

    ::

        {
            name:                               <str>
            registration_id ``required``:       <str>
            device_id:                          <str>
            active:                             <bool>
            type  ``required``:                 <choices>
        }

    ::

        type choices: (
            ios,
            android,
            web,
        )

``SUCCESS``
    ``STATUS 200``

``ERROR``
    ``STATUS 400``


device > delete
----------------------

DELETE ``/api/v1/device/{registration_id}/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    DELETE device by registration id

``SUCCESS``
    ``STATUS 204``

``ERROR``
    ``STATUS 404``


login > single
----------------------


POST ``/api/v1/auth/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    None

``Content-Type:``
    application/json

``Description:``
    Get account token, type, profile fields for given phone if registered before and is active

``Request Body``
    The request body should be a "application/json"
    encoded object, containing the following items.

    ::

        {
            phone  ``required``:  <phone>
        }

    `phone format: +996777000123`

``SUCCESS``
    ``STATUS 200``

    doctor::

        {
            "token": "8a8a4ffa805db4c06e2b3c1055348feca05d1c32",
            "type": "doctor",
            "profile": {
                "id": 4,
                "last_name": "Admin",
                "first_name": "Admin",
                "middle_name": "",
                "phone": "+111222111",
                "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
                "positions": [
                    "asdasd"
                ]
            }
        }

    patient::

        {
            "token": "8a8a4ffa805db4c06e2b3c1055348feca05d1c32",
            "type": "patient",
            "profile": {
                "id": 4,
                "last_name": "Admin",
                "first_name": "Admin",
                "middle_name": "",
                "phone": "+111222111",
                "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
                "doctor": {
                    "id": 4,
                    "last_name": "Admin",
                    "first_name": "Admin",
                    "middle_name": "",
                    "phone": "+111222111",
                    "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
                    "positions": [
                        "asdasd"
                    ]
                },
                "date_of_birth": "2020-05-01",
                "documents": [
                    {
                        "name": "Ruslan Tolkun uulu",
                        "image": "http://localhost:8000/media/CACHE/images/uploads/PatientDocument/5/ee5a3140-0554-4a49-9800-cb14e46eec6c/b45d75e41d880d533729146aee7a07e7.png"
                    }
                ],
                "address": "Bishkek",
                "unread_notifications_exists": false
            }
        }

``ERROR``
    ``STATUS 400``::

        {
            'detail': 'user not found'
        }





profile > single
----------------------


GET ``/api/v1/profile/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Get profile

``SUCCESS``
    ``STATUS 200``
    doctor::

        {
            "id": 4,
            "last_name": "Admin",
            "first_name": "Admin",
            "middle_name": "",
            "phone": "+111222111",
            "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
            "positions": [
                "asdasd"
            ]
        }

    patient::

        {
            "id": 4,
            "last_name": "Admin",
            "first_name": "Admin",
            "middle_name": "",
            "phone": "+111222111",
            "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
            "doctor": {
                "id": 4,
                "last_name": "Admin",
                "first_name": "Admin",
                "middle_name": "",
                "phone": "+111222111",
                "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
                "positions": [
                    "asdasd"
                ]
            },
            "date_of_birth": "2020-05-01",
            "documents": [
                {
                    "id": 8,
                    "name": "NEw on",
                    "image": "http://localhost:8000/media/uploads/PatientDocument/b/75b6e122-2ac4-4d48-b110-1c4fad288c6c.png",
                    "preview": "http://localhost:8000/media/CACHE/images/uploads/PatientDocument/b/75b6e122-2ac4-4d48-b110-1c4fad288c6c/49a876101a4e55ee1dd20b80d72cdbf6.png"
                }
            ],
            "address": "Bishkek",
            "unread_notifications_exists": false
        }

``ERROR``
    ``STATUS 400``



patient > list
----------------------


GET ``/api/v1/doctor/patients/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Get patient profile list

``SUCCESS``
    ``STATUS 200``::

        [
            {
                "id": 4,
                "first_name": "Admin",
                "last_name": "Admin",
                "middle_name": "",
                "deviation": false
            }
        ]

``ERROR``
    ``STATUS 400``



patient > single
----------------------


GET ``/api/v1/doctor/patients/{id}/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Get patient profile detail

``SUCCESS``
    ``STATUS 200``::

        {
            "id": 4,
            "last_name": "Admin",
            "first_name": "Admin",
            "middle_name": "",
            "phone": "+111222111",
            "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
            "doctor": {
                "id": 4,
                "last_name": "Admin",
                "first_name": "Admin",
                "middle_name": "",
                "phone": "+111222111",
                "photo": "http://localhost:8000/media/CACHE/images/uploads/User/d/47d48070-8df8-44c2-b5c2-b4927457cbd7/32f8cb4973e83ffaa3a20b5169758cf3.png",
                "positions": [
                    "asdasd"
                ]
            },
            "date_of_birth": "2020-05-01",
            "documents": [
                {
                    "id": 1,
                    "name": "Ruslan Tolkun uulu",
                    "image": "http://localhost:8000/media/uploads/PatientDocument/5/ee5a3140-0554-4a49-9800-cb14e46eec6c.png",
                    "preview": "http://localhost:8000/media/CACHE/images/uploads/PatientDocument/5/ee5a3140-0554-4a49-9800-cb14e46eec6c/b45d75e41d880d533729146aee7a07e7.png"
                },
                ...

            ],
            "address": "Bishkek"
        }

``ERROR``
    ``STATUS 400``
    ::

        {
            "detail": "Не найдено."
        }




patient > indicators > list
---------------------------


GET ``/api/v1/doctor/patients/{id}/indicators/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Get patient indicators list

``SUCCESS``
    ``STATUS 200``::

        [
            {
                "id": 12,
                "patient": 1,
                "dyspnea": 1,
                "position_bed": 1,
                "heartbeat": 1,
                "stack": 1,
                "weight": "52.000",
                "arterial_pressure": "1",
                "pulse": 1,
                "create_at": "2020-05-01T17:47:32.902976+06:00",
                "deviation_count": 2
            },
            ...
        ]

``ERROR``
    ``STATUS 400``




patient > indicator > detail
------------------------------

GET ``/api/v1/doctor/patients/{patient_id}/indicators/{indicator_id}/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Get patient indicator detail

``SUCCESS``
    ``STATUS 200``::

        {
            "id": 12,
            "patient": 1,
            "create_at": "2020-05-01T17:47:32.902976+06:00",
            "dyspnea": {
                "deviation": false,
                "value": 1,
                "description": "Нен"
            },
            "position_bed": {
                "deviation": false,
                "value": 1,
                "description": "Горизонтально"
            },
            "heartbeat": {
                "deviation": false,
                "value": 1,
                "description": "Нет"
            },
            "stack": {
                "deviation": false,
                "value": 1,
                "description": "Стопы"
            },
            "weight": {
                "deviation": true,
                "value": 52.0,
                "description": "У вас избыточный вес на 1.000 кг"
            },
            "arterial_pressure": {
                "deviation": null,
                "value": "1",
                "description": "1"
            },
            "pulse": {
                "deviation": true,
                "value": 1,
                "description": 1
            },
            "deviation_count": 2
        }

``ERROR``
    ``STATUS 400``
    ::

        {
            "detail": "Не найдено."
        }



patient > documents > list
------------------------------

GET ``/api/v1/doctor/patients/{patient_id}/documents/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Get patient documents list

``SUCCESS``
    ``STATUS 200``::

        [
            {
                "id": 1,
                "name": "Ruslan Tolkun uulu",
                "image": "http://localhost:8000/media/uploads/PatientDocument/5/ee5a3140-0554-4a49-9800-cb14e46eec6c.png",
                "preview": "http://localhost:8000/media/CACHE/images/uploads/PatientDocument/5/ee5a3140-0554-4a49-9800-cb14e46eec6c/b45d75e41d880d533729146aee7a07e7.png"
            },
            ...
        ]

``ERROR``
    ``STATUS 400``


patient > document > create
------------------------------

POST ``/api/v1/doctor/patients/{patient_id}/documents/create/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Create patient document

``Request Body``
    The request body should be a "application/json"
    encoded object, containing the following items.

    ::

        {
            name  ``required``:  <str>
            image  ``required``:  <file>
        }


``SUCCESS``
    ``STATUS 200``::

        {
            "id": 1,
            "name": "Ruslan Tolkun uulu",
            "image": "http://localhost:8000/media/uploads/PatientDocument/5/ee5a3140-0554-4a49-9800-cb14e46eec6c.png",
            "preview": "http://localhost:8000/media/CACHE/images/uploads/PatientDocument/5/ee5a3140-0554-4a49-9800-cb14e46eec6c/b45d75e41d880d533729146aee7a07e7.png"
        }

``ERROR``
    ``STATUS 400``

    ``STATUS 406``::

        {
            "message": "Пациента с данным id не сущестыует или он не активен"
        }



patient > document > delete
------------------------------

DELETE ``/api/v1/doctor/patients/{patient_id}/documents/{document_id}/delete/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Delete patient document

``SUCCESS``
    ``STATUS 204 No Content``

``ERROR``
    ``STATUS 400``

    ``STATUS 404``::

        {
            "detail": "Не найдено."
        }



language > update
-------------------------

PUT ``/api/v1/update/language/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Update account language. Used to get sms to send FCM notification

``Request Body``
    The request body should be a "application/json"
    encoded object, containing the following items.

    ::

        {
            language  ``required``:  <choice>
        }

    ::

        language choice: (
            'ru',
            'ky'
        )

``SUCCESS``
    ``STATUS 200``::

        {
            "language": "ky"
        }

``ERROR``
    ``STATUS 400``