temp_mes = """
Активные заявки:
{% for pr in problems %}
    {{loop.index}}: ID problems: {{pr.id}}
    Author: {{pr.fio}}
    Problem: {{pr.content}}
    Place: {{pr.adress}}
{% endfor %}
"""