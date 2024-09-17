from django.urls import path
from  main.views import home, create_product, show_xml_data, show_json_data, show_xml_by_id, show_json_by_id

app_name = 'main'
urlpatterns = [
    path('', home, name='home'),
    path('create_product/', create_product, name='create_product'),
    path('xml_data/', show_xml_data, name='show_xml_data'),
    path('json_data/', show_json_data, name='show_json_data'),
    path('xml_data/<id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json_data/<id>/', show_json_by_id, name='show_json_by_id'),
]
