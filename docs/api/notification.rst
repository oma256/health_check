NOTIFICATION API
================

.. contents::
   :depth: 3



notification > list > today
-----------------------------

GET ``/api/v1/notification/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``Authorisation``
    Authorisation token
    Accept-Language

``Content-Type:``
    application/json

``Description:``
    Get list notifications `today`

    types::

        (
            'deviation',
            'indicator'
        )

``SUCCESS``
    ``STATUS 200``::

        [
            {
                "id": 2,
                "type": "deviation",
                "deviation_count": 0,
                "is_viewed": false,
                "create_at": "2020-05-02T15:48:14.021413+06:00"
            },
            {
                "id": 3,
                "type": "indicator",
                "deviation_count": 0,
                "is_viewed": false,
                "create_at": "2020-05-02T15:48:21.321764+06:00"
            }
        ]

``ERROR``
    ``STATUS 400``



notification > viewed > update
-------------------------------

PATCH ``/api/v1/notification/viewed/update/{id}/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Authorisation``
    Authorisation token

``Content-Type:``
    application/json

``Description:``
    Update notification viewed status as True

``Path Parameters``
    The following parameters should be included in the URL path.
    ::

        {
            id ``required`` A unique integer value identifying this Notification.
        }

``Request Body``
    The request body should be a "application/json"
    encoded object, containing the following items.

    ::

        {
            is_viewed ``required``: <bool>
        }


``SUCCESS``
    ``STATUS 200``::

        {
            "id": 3,
            "type": "indicator",
            "deviation_count": 0,
            "is_viewed": true,
            "create_at": "2020-05-02T15:48:21.321764+06:00"
        }

``ERROR``
    ``STATUS 404``::

        {
            "detail": "Не найдено."
        }

