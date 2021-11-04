
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models.fields import TextField
from django.http import request, response
from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse



 
#login
def user_login(request):
    form = form_login(request.POST)
    if form.is_valid():
        user = authenticate(request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
        if user is not None:
            p = profile.objects.get(user=user)
            if p.type=='Administrateur':
                login(request,user)
                return redirect("../../Administrateur/admin_user")
            else:
                login(request,user)
                return redirect("pre_proposition_budgetaire")   
        
    context = {
        'form':form_login
    }
    return render(request,'login.html' , context)

#cette fonction traite la page logout
def logout_page(request):
    logout(request)
    return redirect('login')

###################################################################
###### proposition ############
#page principale de proposition
def pre_proposition_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type =="Administrateur"):
        return render(request, '404.html')  
    name = str(p.nom) + '     ' + str(p.prenom)
    up = unite_profile.objects.filter(pro=p)
    notifications = get_notifications(p)   
    currentYear = datetime.now().year+1
    pe= proposition_etat.objects.get(annee=currentYear)
    context = {
        "notifications":notifications,
        "user": name,
        "poste": p.type,
        'unite':up,
        "etat": pe.etat,
    
    }
    return render(request,'pre_proposition_budgetaire.html',context)



def consultation_proposition(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type=="Administrateur"):
        return render(request, '404.html')
    request.session["unite"]=request.POST.get("id")   
    name = str(p.nom) + '     ' + str(p.prenom)

    u = unite.objects.get(pk=request.session["unite"])
    
    pro = entete_pv.objects.filter(type="proposition",unite=u)
   
    user =  profile.objects.get(user=request.user)
    notifications = get_notifications(user)
    
    context = {
            'notifications':notifications,
            "user": name,
            "unite": u,
            "poste": "Cadre Budgetaire",
            "pv":pro 
        
    }   

    return render(request, "consultation_proposition.html", context )
   

###############################################
###consultation des propositions budget - pv proposition
def intermed_pv_proposition(request):
    request.session["annee3"]=int(request.POST.get("annee"))
    return redirect("pv_proposition")


def get_max_historique(annee,type,type1):

    h = historique.objects.filter(annee=annee,type=type,type_1=type1)
    return h[len(h)-1]

def get_min_historique(annee,type,type1):

    h = historique.objects.filter(annee=annee,type=type,type_1=type1)
    return h[0]

## consultation du pv proposition ####
def pv_proposition(request):

    request.session["annee3"]=int(request.POST.get("annee"))
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type=="Administrateur"):
        return render(request, '404.html')
    u = unite.objects.get(pk=request.session["unite"])
    pv = entete_pv.objects.get(annee=request.session["annee3"],unite=u,type="proposition")
    pro = proposition.objects.filter(type="trafic",pv=pv)
    usert_max=""
    usert_min=""
    dusert_max=""
    dusert_min=""

    userr_max=""
    userr_min=""
    duserr_max=""
    duserr_min=""

    usere_max=""
    usere_min=""
    dusere_max=""
    dusere_min=""

    userf_max=""
    userf_min=""
    duserf_max=""
    duserf_min=""

    userx_max=""
    userx_min=""
    duserx_max=""
    duserx_min=""
    trafic= False
    recette=False
    emission=False
    fonct=False
    expl=False

    if pro.exists():
        trafic=True
        print(get_max_historique(request.session["annee3"],'proposition','trafic'))
        usert_max=get_max_historique(request.session["annee3"],'proposition','trafic').user
        usert_min=get_min_historique(request.session["annee3"],'proposition','trafic').user
        dusert_max=get_max_historique(request.session["annee3"],'proposition','trafic').date_h
        dusert_min=get_min_historique(request.session["annee3"],'proposition','trafic').date_h
    


    pro1 = proposition.objects.filter(type="recette",pv=pv)
    if pro1.exists():
        recette=True

        userr_max=get_max_historique(request.session["annee3"],'proposition','recette').user
        userr_min=get_min_historique(request.session["annee3"],'proposition','recette').user
        duserr_max=get_max_historique(request.session["annee3"],'proposition','recette').date_h
        duserr_min=get_min_historique(request.session["annee3"],'proposition','recette').date_h

    
    pro2 = proposition.objects.filter(type="emission",pv=pv)
    if pro2.exists():
        emission= True
        usere_max=get_max_historique(request.session["annee3"],'proposition','emission').user
        usere_min=get_min_historique(request.session["annee3"],'proposition','emission').user
        dusere_max=get_max_historique(request.session["annee3"],'proposition','emission').date_h
        dusere_min=get_min_historique(request.session["annee3"],'proposition','emission').date_h

    


    pro3 = proposition.objects.filter(type1="FONCTIONNEMENT",pv=pv)
    if pro3.exists():
        fonct=True

        userf_max=get_max_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').user
        userf_min=get_min_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').user
        duserf_max=get_max_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').date_h
        duserf_min=get_min_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').date_h

    pro4 = proposition.objects.filter(type1="EXPLOITATION",pv=pv)
    if pro4.exists():
        expl=True
        userx_max=get_max_historique(request.session["annee3"],'proposition','EXPLOITATION').user
        userx_min=get_min_historique(request.session["annee3"],'proposition','EXPLOITATION').user
        duserx_max=get_max_historique(request.session["annee3"],'proposition','EXPLOITATION').date_h
        duserx_min=get_min_historique(request.session["annee3"],'proposition','EXPLOITATION').date_h



    name = str(p.nom) + '     ' + str(p.prenom)
  

    
    user =  profile.objects.get(user=request.user)
    notifications = get_notifications(user)
    
    context = {
        'notifications':notifications,
        
       "user": name,
       "poste": "Cadre Budgetaire",
       "pro":pro,
       "pro1":pro1,
       "pro2":pro2,
       "pro3":pro3,
       "pro4":pro4,

       "unite":u,
        "usert_max": usert_max,
        "usert_min": usert_min,
        "dusert_max": dusert_max,
        "dusert_min": dusert_min,
        
       "userr_max": userr_max,
        "userr_min": userr_min,
        "duserr_max": duserr_max,
        "duserr_min": duserr_min,
        

        "usere_max": usere_max,
        "usere_min": usere_min,
        "dusere_max": dusere_max,
        "dusere_min": dusere_min,
        
        
       "userf_max": userf_max,
        "userf_min": userf_min,
        "duserf_max": duserf_max,
        "duserf_min": duserf_min,

        "userx_max": userx_max,
        "userx_min": userx_min,
        "duserx_max": duserx_max,
        "duserx_min": duserx_min,
        "trafic":trafic,
        "recette":recette,
        "emission":emission,
        "fonct":fonct,
        "expl":expl
        


        

        
     }   

    return render(request, "pv_proposition.html", context   )

#### remplir la proposition ######
def proposition(request):
    
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Cadre Budgetaire"):
        return render(request, '404.html')
    
    request.session['unite'] = request.POST.get('id')      
    year = datetime.now().year+1
    u = unite.objects.get( id = request.session['unite'])
    # get the pv
    pv = entete_pv.objects.filter(annee=year, unite=u, type='proposition')
    if not pv.exists():
        pv = entete_pv(unite=u, annee=year, type='proposition')
        pv.save()
    else:
        pv = entete_pv.objects.get(annee=year, unite=u, type='proposition')
    # check the indicateurs
    trafic = False
    trafic_dom = False
    if( u.commerciale in {'y','Y'}):
        trafic = True
        if (u.etranger=='N'):
            trafic_dom= True
    
    emission = False
    emission_dom= False
    if(u.Emissision_Indicateur in {'y','Y'}):
        emission = True
        if (u.etranger=='N' and u.commerciale =='Y'):
            emission_dom = True
    
    recette = False
    if (u.Recette_Indicateur in {'y','Y'}):
        recette= True

    dep_exp = False
    if(u.Exploitation_Indicateur in {'y','Y'}):
        dep_exp=True
    
    unit_pos= unite_pos6.objects.filter(unite=u)
    unit_pos7 = unite_pos7.objects.filter(unite = u)
    propositions = proposition.objects.filter(pv=pv)
    pro_trafic = []
    pro_emission = []
    pro_recette = []
    pro_dep_fct = []
    pro_dep_exp = []
    #### parcour des unite_pos6
    # si ca existe dans proposition le mettre dans trafic_props
    # si proposition n'existe pas : creer une nouvelle  prop
    for up in unit_pos :
        if (trafic):
            if up.pos6.type == 'trafic':
                p6 = Pos6.objects.get(id = up.pos6)
                pr = propositions.filter(pos6 = p6)
                if not (pr.exists()):
                    pr = proposition(pv=pv, rempli=False, pos6=p6, monnaie=u.monnaie,reseau='international')
                ####TODO: IMPORTANT: la source concerne le pv et non pas la proposition
                # enleve source de proposition, et rajoute la comme nouvelle table relier avc entete_pv    
                pro_trafic.append(pr)

         
##### notification's fct ######
def create_notif(pv, user, path,mois):

    up = unite_profile.objects.filter(unite= pv.unite)
    if up.exists :
        ## unite_pro = unite_profile.objects.get(unite=pv.unite)
        for unpr in up :
            pro = unpr.pro
            if (pro.type=='Sous Directeur' and not user.type=='Sous Directeur'):
                if not pv.type in {'controle','proposition'}:
                    notif = notification(pv=pv, notified_user=pro, modifier_user=user , date=datetime.now(),type=path,controle_mois=mois)
                    notif.save()       
            if (pro.type== 'Chef de Departement' and user.type=='Cadre Budgetaire'):
                notif = notification(pv=pv, notified_user=pro, modifier_user=user , date=datetime.now(), type=path,controle_mois=mois)
                notif.save()
    
def get_notifications(user):
    n = notification.objects.filter(notified_user=user)
    if n.exists:
        return n


## redirect notification de validation
def redirect_notif(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    id= request.POST.get('notification_id')
    n = notification.objects.get(id=id)
    pv = entete_pv.objects.get(id=n.pv.id)
    u = unite.objects.get(id=pv.unite.id)
    #cas reunion
    if('reunion' in n.type ):
        request.session['unite']=u.id
    #cas notifier
    elif('notifie' in n.type):
        request.session['unite_notif']=u.id
        request.session['annee_notifie']=pv.annee
    #cas actualisation ou reajustement
    elif('actualisation' in n.type or 'reajustement' in n.type):
        request.session['unite_act']=u.id
        request.session['annee_act']=pv.annee
    #cas controle
    elif('controle'  in n.type):
        request.session['unite']=u.id
        request.session['annee']=pv.annee    
        if request.method == 'POST':
            request.POST.update({'mois': [n.controle_mois]})
            #TODO: test if it works!
    elif ("realisation"  in n.type):
        request.session['unite1']=u.id
        request.session['annee1']=pv.annee


    return redirect(n.type)

#### lettre functions ######
def export_lettre(reauest):
    pdf = lettre.objects.last()
    response = HttpResponse(pdf.pdf,content_type='charset=utf-8')
    return response
 