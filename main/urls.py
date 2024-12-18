from django.urls import path
from main.views import home, create_product, show_xml_data, show_json_data, show_xml_by_id, show_json_by_id
from main.views import register, login_user, logout_user, edit_product, delete_product, create_product_ajax, create_product_flutter
app_name = 'main'
urlpatterns = [
    path('', home, name='home'),
    path('create_product/', create_product, name='create_product'),
    path('xml_data/', show_xml_data, name='show_xml_data'),
    path('json_data/', show_json_data, name='show_json_data'),
    path('xml_data/<id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json_data/<id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('delete/<uuid:id>', delete_product, name='delete_product'),
    path('create_product_ajax/', create_product_ajax, name='create_product_ajax'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),

]
