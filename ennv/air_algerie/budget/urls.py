from django.urls import path
from .views import * 


urlpatterns = [
    path('login/' , user_login , name='login'), 
    path('logout_page/' , logout_page , name='logout_page'), 

    path('pre_proposition_budgetaire/' , pre_proposition_budgetaire , name='pre_proposition_budgetaire'),
    path('consultation_proposition/' , consultation_proposition , name='consultation_proposition'),       
    path('pv_proposition/' , pv_proposition , name='pv_proposition'),     
  

    path('redirect_notif/',redirect_notif,name="redirect_notif"),
    path('exporter/',export_lettre,name="exporter"),

]