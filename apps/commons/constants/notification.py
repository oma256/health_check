from apps.commons.constants.users import KY, RU

DEVIATION = 'deviation'
INDICATOR = 'indicator'

NOTIFICATION_TYPE = (
    (DEVIATION, 'Отклонение'),
    (INDICATOR, 'Индикатор')
)

NOTIFICATION_TITLES_LN = {
    RU: 'Уведомление',
    KY: 'Кабарлоо',
}

NOTIFICATION_MESSAGE_LN = {
    DEVIATION: {
        RU: 'У вас отклонение на: {deviation_count}',
        KY: 'Сиздегиле болгон озгоруулор: {deviation_count}'
    },
    INDICATOR: {
        RU: 'Заполните индикатор',
        KY: 'Индикоторду толуктагыла'
    }
}
