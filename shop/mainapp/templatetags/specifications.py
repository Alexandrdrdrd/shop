from django import template
from django.utils.safestring import mark_safe
register = template.Library()

TABLE_HEAD = """
                <table class="table">
                    <tbody>
  
                    """

TABLE_TAIL = """
                </tbody>
                    </table>  
                """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                    """

PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Частота процессора': 'processor_freq',
        'Оперативная память': 'ram',
        'Видеокарта': 'video',
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение экрана': 'resolution',
        'Заряд аккумулятора': 'accum_volume',
        'Оперативная память': 'ram',

        'Максимальный объем SD карты': 'sd_volume_max',
        'Главная камера ': 'main_cum_mp',
        'Фронтальная камера ': 'frontal_cum_mp'
    }
}


def get_product_spec(product, model_name): # берет информацию для создания таблицы
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):  # создает таблицу которая отображает характеристики продукта
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
