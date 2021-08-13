from django.utils.translation import gettext_lazy as _

DYSPNEA_NOT = 1
DYSPNEA_UNDER_LOAD = 2
DYSPNEA_IN_REST = 3
DYSPNEA_CHOICE = (
    (DYSPNEA_NOT, _('Нет')),
    (DYSPNEA_UNDER_LOAD, _('При нагрузке')),
    (DYSPNEA_IN_REST, _('В покое')),
)

POSITION_BED_HORIZONTALLY = 1
POSITION_BED_TWO_PILLOW = 2
POSITION_BED_SIT = 3
POSITION_BED_CHOICES = (
    (POSITION_BED_HORIZONTALLY, _('Горизонтально')),
    (POSITION_BED_TWO_PILLOW, _('Высоко на 2х подушках')),
    (POSITION_BED_SIT, _('Сидя')),
)

HEARTBEAT_NOT = 1
HEARTBEAT_UNDER_LOAD = 2
HEARTBEAT_IN_REST = 3
HEARTBEAT_CHOICES = (
    (HEARTBEAT_NOT, _('Нет')),
    (HEARTBEAT_UNDER_LOAD, _('При нагрузке')),
    (HEARTBEAT_IN_REST, _('В покое')),
)

STACK_NOT = 1
STACK_FOOT = 2
STACK_SHINS = 3
STACK_ABOVE_SHINE = 4
STACK_CHOICES = (
    (STACK_NOT, _('Нет')),
    (STACK_FOOT, _('Стопы')),
    (STACK_SHINS, _('Голени')),
    (STACK_ABOVE_SHINE, _('Выше колени')),
)
