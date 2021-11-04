from django.shortcuts import render,redirect
from .forms import *
from budget.models import *
from .forms import *
from .filters import *

from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import authenticate,login, logout

def admin_user(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  

    profiles = profile.objects.all()
    for p in profiles :
        if p.type == "Administrateur":
            profiles = profiles.exclude(id = p.id)




    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",
        "profile":profiles

    }
    return render(request,"admin_user.html",context)


def add_user(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  
    name = str(p.nom) + '     ' + str(p.prenom)

    #set_password
    form1 = form_edit_user(request.POST)
    if form1.is_valid():
        
        if form1.cleaned_data["password"] == form1.cleaned_data["password2"]:
            u = User(username = form1.cleaned_data["user_name"],is_staff=False)
            u.set_password(form1.cleaned_data["password"])
            u.save()
            p1 = profile(nom = form1.cleaned_data["nom"],prenom = form1.cleaned_data["prenom"],type = form1.cleaned_data["type_u"],user=u)
            p1.save()
        else:
            print("gerer cette exception")
        return redirect("admin_user")
    
    context = {
        "user": name,
        "poste": "ADMIN",
        
        "form":form_edit_user

    }
    return render(request,"add_user.html",context)

def inter_edit(request):
    request.session["profile"]=request.POST.get("id")

    return redirect ("edit_user")
def edit_user(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  
    name = str(p.nom) + '     ' + str(p.prenom)

    id = request.session["profile"]
    p1 = profile.objects.get (id=id)
    #set_password
    form1 = form_edit_user(request.POST)
    if form1.is_valid():
        if form1.cleaned_data["password"] == "" or form1.cleaned_data["password2"] == "" :
            p1.nom = form1.cleaned_data["nom"]
            p1.prenom = form1.cleaned_data["prenom"]
            p1.type = form1.cleaned_data["type_u"]
            u = User.objects.get(id=p1.user.id)
            u.username = form1.cleaned_data["user_name"]
            u.save()
            p1.user=u
            p1.save()
        else:
            if form1.cleaned_data["password"] == form1.cleaned_data["password2"]:
                p1.nom = form1.cleaned_data["nom"]
                p1.prenom = form1.cleaned_data["prenom"]
                p1.type = form1.cleaned_data["type_u"]
                u = User.objects.get(id=p1.user.id)
                u.username = form1.cleaned_data["user_name"]
                u.set_password(form1.cleaned_data["password"])
                u.save()
                p1.user=u
                p1.save()
            else:
                print("gerer cette exception")
        return redirect("admin_user")
    
    form = form_edit_user(initial={'nom': p1.nom,'prenom':p1.prenom,'type_u':p1.type,'user_name':p1.user.username})
    context = {
        "user": name,
        "poste": "ADMIN",
        "profile":p1,
        "form":form

    }
    return render(request,"edit_user.html",context)


def edit_user1(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"edit1_user.html",context)



def delete_user(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  
    id = request.POST.get("id")
    print(id)
    p1 = profile.objects.get(id=id)
    u = User.objects.get(id=p1.user.id)
    p1.delete()
    u.delete()
    return redirect ("admin_user")


def admin_unite(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  

    u = unite.objects.all()
    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",
        "unite":u
        

    }
    return render(request,"admin_unite.html",context)

def add_unite(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  

    name = str(p.nom) + '     ' + str(p.prenom)
    form1 = form_unite(request.POST)
    if form1.is_valid():
        u1 = unite()
        u1.code_unite = form1.cleaned_data["code"]
        u1.reseau = form1.cleaned_data["reseau"]
        u1.pays = form1.cleaned_data["pays"]
        u1.commeriale = form1.cleaned_data["comercial"]
        u1.etranger = form1.cleaned_data["etranger"]
        u1.tresorie = form1.cleaned_data["tresorie"]
        u1.Trafic_Indicateur = form1.cleaned_data["trafic"]
        u1.Emission_Indicateur = form1.cleaned_data["emission"]
        u1.Recette_Indicateur = form1.cleaned_data["recette"]
        u1.Exploitation_Indicateur = form1.cleaned_data["exploitation"]
        u1.lib_monnaie=monnaie.objects.get(code_monnaie=form1.cleaned_data["monnaies"])
        u1.save()

        return redirect("admin_unite")

    context = {
        "user": name,
        "poste": "ADMIN",
        "form": form1

    }
    return render(request,"add_unite.html",context)


def interu_edit(request):
    request.session["unite"]=request.POST.get("id")
    return redirect ("edit_unite")

def edit_unite(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  

    id = request.session["unite"]
    u1 = unite.objects.get (id=id)

    name = str(p.nom) + '     ' + str(p.prenom)
    form = form_unite(initial={'monnaies':u1.lib_monnaie,'comercial':u1.commeriale,'etranger':u1.etranger,'tresorie':u1.tresorie,'trafic':u1.Trafic_Indicateur,'emission':u1.Emission_Indicateur,'recette':u1.Recette_Indicateur,'exploitation':u1.Exploitation_Indicateur})
    form1 = form_unite(request.POST)
    if form1.is_valid():
        u1.commeriale = form1.cleaned_data["comercial"]
        u1.etranger = form1.cleaned_data["etranger"]
        u1.tresorie = form1.cleaned_data["tresorie"]
        u1.Trafic_Indicateur = form1.cleaned_data["trafic"]
        u1.Emission_Indicateur = form1.cleaned_data["emission"]
        u1.Recette_Indicateur = form1.cleaned_data["recette"]
        u1.Exploitation_Indicateur = form1.cleaned_data["exploitation"]
        u1.lib_monnaie=monnaie.objects.get(code_monnaie=form1.cleaned_data["monnaies"])
        u1.save()

        return redirect("admin_unite")

    context = {
        "user": name,
        "poste": "ADMIN",
        "unite":u1,
        "form": form

    }
    return render(request,"edit_unite.html",context)


def edit_unite1(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"edit_unite1.html",context)


def delete_unite(request):
    if (not request.user.is_authenticated):
     return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')
    print()  
    id = request.POST.get("id")
    u = unite.objects.get(id=id)
    u.delete()
    return redirect ("admin_unite")


def admin_compte(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)

    pos = Pos6.objects.all()
    pos_filters=pos_filter(request.GET,pos)
    context = {
        "user": name,
        "poste": "ADMIN",
        "pos":pos_filters

    }
    return render(request,"admin_compte.html",context)


def interc_edit(request):
    request.session["compte"]=request.POST.get("id")
    return redirect ("edit_compte")

def edit_compte(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)

    id = request.session["compte"]
    c1 = Pos6.objects.get(id=id)
    form1=form_compte(initial={'lib':c1.lib})

    form2 = form_compte(request.POST)
    if form2.is_valid():
        c1.lib = form2.cleaned_data["lib"]
        c1.save()

        return redirect("admin_compte")

    context = {
        "user": name,
        "poste": "ADMIN",
        "compte":c1,
        "form":form1

    }
    return render(request,"edit_compte.html",context)




def add_compte(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"add_compte.html",context)


def add_pos1(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"add_pos1.html",context)


def add_pos2(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"add_pos2.html",context)


def add_pos3(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"add_pos3.html",context)


def add_pos6(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)

    form2 = form_compte(request.POST)
    if form2.is_valid():
        c1=Pos6()
        c1.scf = form2.cleaned_data["scf"]
        x= str(c1.scf)
        x=x[0:3]
        pos33 = Pos3.objects.get(scf=x)
        c1.ref=pos33
        c1.lib = form2.cleaned_data["lib"]
        c1.save()

        return redirect("admin_compte")

    context = {
        "user": name,
        "poste": "ADMIN",
        "form":form_compte

    }
    return render(request,"add_pos6.html",context)


def add_pos7(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"add_pos7.html",context)


def delete_compte(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"delete_compte.html",context)



def admin_affectation(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)


    context = {
        "user": name,
        "poste": "ADMIN",

    }
    return render(request,"admin_affectation.html",context)
# affectation unite a un utilisateur

def add_unite_user(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)

    form= form_unite_user
    form1 = form_unite_user(request.POST)
    if form1.is_valid():
        u1 = unite_profile()
        u1.unite=unite.objects.get(code_unite=form1.cleaned_data["unite"])  
        x = str(form1.cleaned_data["profile"])
        x=x.split()     
        u1.pro=profile.objects.get(nom=x[0],prenom=x[1])
        u1.save()

        return redirect("admin_affectation")
    
    context = {
        "user": name,
        "poste": "ADMIN",
        "form":form
    }
    return render(request,"add_unite_user.html",context)



def delete_unite_user(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  

    
    
    name = str(p.nom) + '     ' + str(p.prenom)
    up=unite_profile.objects.all()

    context = {
        "user": name,
        "poste": "ADMIN",
        "up":up
    }
    return render(request,"delete_unite_user.html",context)

def delete_up(request):
    if (not request.user.is_authenticated):
     return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')
    id = request.POST.get("id")

    u = unite_profile.objects.get(id=id)

    u.delete()
    return redirect ("delete_unite_user")


# add un compte a une unite
def add_unite_pos(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)

    form= form_unite_pos
    form1 = form_unite_pos(request.POST)
    if form1.is_valid():
        u1 = unite_pos6()
        u1.unite=unite.objects.get(code_unite=form1.cleaned_data["unite"])   
        u1.pos6=Pos6.objects.get(scf=form1.cleaned_data["compte"].scf)  
        u1.type=form1.cleaned_data["type"]           
        u1.save()

        return redirect("admin_affectation")
    
    context = {
        "user": name,
        "poste": "ADMIN",
        "form":form
    }
    return render(request,"add_unite_pos.html",context)

# suprrimer un commpte depense d' une unite 

def delete_unite_pos(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  

    name = str(p.nom) + '     ' + str(p.prenom)
    upos=unite_pos6.objects.order_by("unite")

    context = {
        "user": name,
        "poste": "ADMIN",
        "up":upos
    }
    return render(request,"delete_unite_pos.html",context)

def delete_up_pos(request):
    if (not request.user.is_authenticated):
     return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')
    id = request.POST.get("id")
    u = unite_pos6.objects.get(id=id)
    u.delete()
    return redirect ("delete_unite_pos")



def affectation_date_reunion(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)
    currentYear = datetime.now().year+1
    r = runion.objects.all()
    u = unite.objects.all()
    for ue in u:
        for re in r:
            if ue == re.unite:
                u = u.exclude(id=ue.id)
    context = {
        "user": name,
        "poste": "ADMIN",
        "r":r,
        "unite":u

    }
    return render(request,"affectation_date_reunion.html",context)

def ouvrir(request):
    id = request.POST.get("unite")
    u = unite.objects.get(id=id)
    
    p = entete_pv.objects.filter(unite=u,annee=datetime.now().year+1,type="proposition")
    
    if not p.exists():
         e =entete_pv(unite=u,annee=datetime.now().year+1,type="proposition")
         e.save()
    c = entete_pv.objects.filter(unite=u,annee=datetime.now().year,type="controle")
    if not c.exists():
         c =entete_pv(unite=u,annee=datetime.now().year,type="controle")
         c.save()
    r = entete_pv.objects.filter(unite=u,annee=datetime.now().year-1,type="realisation")
    if not r.exists():
         r =entete_pv(unite=u,annee=datetime.now().year-1,type="realisation")
         r.save()
    rr = entete_pv.objects.filter(unite=u,annee=datetime.now().year-2,type="realisation")
    if not rr.exists():
         rr =entete_pv(unite=u,annee=datetime.now().year-2,type="realisation")
         rr.save()
         
    r = runion(etat='ouvert',annee=datetime.now().year+1,unite=u)
    r.save()

    return redirect('affectation_date_reunion')
def fermer(request):
    id = request.POST.get("id")
    r = runion.objects.get(id=id)
    if r.etat =="ouvert":
        r.etat= "fermé"
    else:
        r.etat="ouvert"
    r.save()
    return redirect('affectation_date_reunion')    



def importer(request):
    form= DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context = {
        "form":form
    }
    return render(request,'importer.html',context) 



def gestion_proposition(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type!="Administrateur"):
        return render(request, '404.html')  


    name = str(p.nom) + '     ' + str(p.prenom)
    currentYear = datetime.now().year+1
    r = proposition_etat.objects.filter(annee=currentYear)
    if not r.exists():
        r = proposition_etat(annee=currentYear,etat=False)
        r.save()
    r = proposition_etat.objects.get(annee=currentYear)
    context = {
        "user": name,
        "poste": "ADMIN",
        "r":r

    }
    return render(request,"gestion_proposition.html",context)

def ouvrir_proposition(request):
    id = request.POST.get("id")
    r = proposition_etat.objects.get(id=id)
    r.etat=True
    r.save()
    return redirect('gestion_proposition')

def fermer_proposition(request):
    id = request.POST.get("id")
    r = proposition_etat.objects.get(id=id)
    r.etat=False
    r.save()
    return redirect('gestion_proposition')    



