INDICATORS API
================

.. contents::
   :depth: 3

indicators > list
-------------------

GET ``/api/v1/indicators/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Indicators list for requested user

``Request Parameter``
    The following parameters can be included as
    part of a URL query string.

    ::

        {
            filter:     <str>
        }

    ::

        filter type (
            week,
            month
        )

``SUCCESS``
    ``STATUS 200``::

        [
            {
                "id": 2,
                "dyspnea": 1,
                "position_bed": 1,
                "heartbeat": 1,
                "stack": 1,
                "weight": 50.000,
                "arterial_pressure": "120/80",
                "pulse": 1,
                "create_at": "2020-05-01T13:04:38.589070+06:00",
                "patient": 1
                "deviation_count": 0
            },
            ...
        ]

``ERROR``
    ``STATUS 400``


indicators > create
----------------------

GET ``/api/v1/indicators/create/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Indicators create for requested user. `Not more one per day.`


``Request Body``
    The request body should be a "application/json"
    encoded object, containing the following items.

    ::

        {
            dyspnea ``required``:               <choices>
            position_bed ``required``:          <choices>
            heartbeat ``required``:             <choices>
            stack ``required``:                 <choices>
            weight  ``required``:               <decimal>
            arterial_pressure  ``required``:    <str>
            pulse  ``required``:                <int>
        }

    ::

        dyspnea choices: (
            1: '- нет'
            2: '+ при нагрузке',
            3: '++ в покое',
        )

    ::

        position_bed choices: (
            1: '- горизонтально'
            2: '+ высоко на 2х подушках',
            3: '++ сидя',
        )

    ::

        heartbeat choices: (
            1: '- нет'
            2: '+ при нагрузке',
            3: '++ в покое',
        )

    ::

        stack choices: (
            1: '- стопы'
            2: '+ голени',
            3: '++ выше колени',
        )

    ``decimal: decimal places 3``

    exp: `0.001`, `70.110` etc.


``SUCCESS``
    ``STATUS 201``
    ::

        {
            "id": 2,
            "dyspnea": 1,
            "position_bed": 1,
            "heartbeat": 1,
            "stack": 1,
            "weight": 50.000,
            "arterial_pressure": "120/80",
            "pulse": 1,
            "create_at": "2020-05-01T13:04:38.589070+06:00",
            "patient": 1
            "deviation_count": 0
        }


``ERROR``
    ``STATUS 400``
    ::

        {
            "message": "Вы уже заполнили анкету за сегодня."
        }


indicators > detail
--------------------

GET ``/api/v1/indicators/{id}/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Indicators detail for requested user

``SUCCESS``
    ``STATUS 200``::

        {
            "id": 11,
            "patient": 1,
            "create_at": "2020-05-01T16:21:36.538036+06:00",
            "dyspnea": {
                "deviation": false,
                "value": 2,
                "description": ""
            },
            "position_bed": {
                "deviation": false,
                "value": 2,
                "description": ""
            },
            "heartbeat": {
                "deviation": false,
                "value": 2,
                "description": ""
            },
            "stack": {
                "deviation": false,
                "value": 1,
                "description": ""
            },
            "weight": {
                "deviation": false,
                "value": 49.986,
                "description": ""
            },
            "arterial_pressure": {
                "deviation": false,
                "value": "140/80",
                "description": ""
            },
            "pulse": {
                "deviation": false,
                "value": 60,
                "desctiption": ""
            },
            "deviation_count": 0
        }

``ERROR``
    ``STATUS 400``



indicators > today
--------------------

GET ``/api/v1/indicators/today/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Get indicator today `id` or `false` for requested user

``SUCCESS``
    ``STATUS 200``
    ::

       {
            "id": 11,
            "isTodaySend": true
        }

    or::

        {
            "id": null,
            "isTodaySend": false
        }

``ERROR``
    ``STATUS 400``
