from . import app
from .views import index, position_create, employee_create, employee_delete, \
    employee_update, register, login, logout

app.add_url_rule('/', view_func=index)
app.add_url_rule('/position/create', view_func=position_create, methods=['POST', 'GET'])
app.add_url_rule('/employee/create', view_func=employee_create, methods=['POST', 'GET'])
app.add_url_rule('/employee/delete/<int:id>', view_func=employee_delete, methods=['POST', 'GET'])
app.add_url_rule('/employee/update/<int:id>', view_func=employee_update, methods=['POST', 'GET'])
app.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])
app.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=logout)
