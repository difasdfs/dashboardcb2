from django.urls import path

from . import views

app_name = 'layermanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:layer_id>/', views.view_layer, name='detail'),
    path('add_layer/', views.add_layer, name='add_layer'),
    path('add_layer/post', views.add_layer_post, name='add_layer_post'),
    path('<int:layer_id>/update_layer', views.update_layer, name='update_layer'),
    path('<int:layer_id>/add_cabang/', views.add_cabang, name='add_cabang'),
    path('<int:layer_id>/add_cabang/post', views.add_cabang_post, name='add_cabang_post'),
    path('add_kategori', views.add_kategori, name="add_kategori"),
    path('add_kategori/post', views.add_kategori_post, name="add_kategori_post"),
    path('add_item', views.add_item, name="add_item"),
    path('add_item/post', views.add_item_post, name="add_item_post"),
    path('list_item', views.list_item, name="list_item"),
    path('add_modifier', views.add_modifier, name="add_modifier"),
    path('add_modifier/post', views.add_modifier_post, name="add_modifier_post"),
    path('add_modifier_varian', views.add_modifier_varian, name="add_modifier_varian"),
    path('add_modifier_varian/post', views.add_modifier_varian_post, name="add_modifier_varian_post"),
    path('add_modifier_item', views.add_modifier_item, name="add_modifier_item"),
    path('add_modifier_item/post', views.add_modifier_item_post, name="add_modifier_item_post"),
    path('remove_modifier_item/<int:item_id>/<int:modifier_id>', views.remove_modifier_item, name="remove_modifier_item"),
    path('edit_modifier_varian/<int:varian_id>', views.edit_modifier_varian, name="edit_modifier_varian"),
    path('edit_modifier_varian/<int:varian_id>/post', views.edit_modifier_varian_post, name="edit_modifier_varian_post"),
    path('<int:layer_id>/add_harga', views.add_harga, name="add_harga"),
    path('<int:layer_id>/add_harga/post', views.add_harga_post, name="add_harga_post"),
    path('edit_harga/<harga_id>', views.edit_harga, name="edit_harga"),
    path('edit_harga/<harga_id>/post', views.edit_harga_post, name="edit_harga_post"),
    path('uploadfile', views.uploadfile, name="uploadfile"),
]