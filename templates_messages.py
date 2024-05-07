temp_mes = """
Активные заявки:
{% for pr in problems %}
    {{loop.index}}: ID problems: {{pr.id}}
    Author: {{pr.fio}}
    Problem: {{pr.content}}
    Place: {{pr.adress}}
{% endfor %}
"""

temp_mes_edit = """
Введите id выполненой заявки:
{% for pr in problems %}
    {{loop.index}}: ID problems: {{pr.id}}
    Problem: {{pr.content}}
{% endfor %}
"""

temp_mes_user = """
Введите id заявки, автору которой хотите послать сообщение:
{% for pr in problems %}
    {{loop.index}}: ID problems: {{pr.id}}
    Problem: {{pr.content}}
{% endfor %}
"""