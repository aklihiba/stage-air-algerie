from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model, ModelState
from django.db.models.deletion import CASCADE
from django.db.models.fields import NullBooleanField
from django.db.models.fields.related import ForeignKey

# Create your models here.


### new version ###

class profile(models.Model):
    nom = models.CharField(max_length=100,null=True,blank=True)
    prenom = models.CharField(max_length=100,null=True,blank=True)
    type= models.CharField(max_length=100,null=True,blank=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    


    def __str__(self):
        return '{} {}'.format(self.nom , self.prenom)

  


class monnaie(models.Model):
    code_monnaie=models.CharField(max_length=3,null=True, blank=True)
    lib_monnaie=models.CharField(max_length=10,null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.code_monnaie, self.lib_monnaie)





class unite(models.Model):
    code_unite=models.CharField(max_length=50,null=True, blank=True)
    reseau = models.CharField(max_length=50,null=True, blank=True)
    pays = models.CharField(max_length=50,null=True, blank=True)
    monnaie=models.ForeignKey(monnaie,on_delete=models.CASCADE,default=None)
    commerciale=models.CharField(max_length=1,null=True, blank=True)
    etranger=models.CharField(max_length=1,null=True, blank=True)
    tresorie=models.CharField(max_length=1,null=True, blank=True)
    Trafic_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    Emission_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    Recette_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    Exploitation_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    def __str__(self):
        return self.code_unite


class unite_profile(models.Model):
    unite = models.ForeignKey(unite,on_delete=models.CASCADE,default=None)
    pro =  models.ForeignKey(profile,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return'{} {}'.format(self.unite,self.pro)

class entete_pv(models.Model):
    annee = models.IntegerField(null=True,blank=True)
    unite = models.ForeignKey(unite,on_delete=models.CASCADE,default=None)
    rempli=models.BooleanField(default=False,blank=True)  
    type = models.CharField(max_length=20,null=True,blank=True)
    
    def __str__(self):
        return '{} {} {}'.format(self.type,str(self.annee),self.unite)

class runion(models.Model):
    annee = models.IntegerField(null=True,blank=True)
    unite = models.ForeignKey(unite,on_delete=models.CASCADE,default=None)
    etat = models.CharField(max_length=20,  default="fermé",blank=False) 
    ## False: reunion fermee, True: reunion ouverte
    def __str__(self):
        return str(self.annee)

class proposition_etat(models.Model):
    annee = models.IntegerField(null=True,blank=True)
    etat = models.BooleanField(default=False,blank=False) 
#TODO: in the administrative app: ouvrir/fermer les propositions : le droit de remplir les froms

##TODO: a revoir and see how it works
class historique(models.Model):
    annee=models.IntegerField(blank=True,null=True)
    type = models.CharField(max_length=20,null=True,blank=True) # proposition/realisation/controle/reunion...
    type_1 =models.CharField(max_length=20,null=True,blank=True) # trafic/recette/ca/depenses
    user = models.CharField(max_length=100,null=True,blank=True)
    date_h = models.CharField(max_length=100,null=True,blank=True)

#table comptes
class Pos1(models.Model):
    scf = models.IntegerField(blank=True,unique=True)
    lib =  models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.scf)


class Pos2(models.Model):
    scf = models.IntegerField(blank=True,unique=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos1,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.scf)

        
class Pos3(models.Model):
    scf = models.IntegerField(blank=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos2,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.scf)

class Pos6(models.Model):
    scf = models.IntegerField(blank=True,unique=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos3,on_delete=models.CASCADE,default=None)
    type = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return '{} {} {}'.format( str(self.scf), self.type, self.lib)

class unite_pos6(models.Model):
    unite = models.ForeignKey(unite,on_delete=models.CASCADE,default=None)
    pos6 =  models.ForeignKey(Pos6,on_delete=models.CASCADE,default=None)
    user = models.CharField(max_length=20, null=False, blank=False, default='admin') 
    def __str__(self):
          return'{} {}'.format(self.unite,self.pos6)

class Pos7(models.Model):
    scf = models.IntegerField(blank=True,unique=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos6,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.scf)

class unite_pos7(models.Model):
    unite = models.ForeignKey(unite,on_delete=models.CASCADE,default=None)
    pos7 =  models.ForeignKey(Pos7,on_delete=models.CASCADE,default=None)
    user = models.CharField(max_length=20, null=False, blank=False, default='admin')
    def __str__(self):
          return'{} {}'.format(self.unite,self.pos7)


# proposition (type : trafic / recette / ca / depenses  !!!! type 1 : fonctionnement ou exploitation )
class proposition(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)
    cloture = models.FloatField(null=True,blank=True, default=0)
    prevision = models.FloatField(null=True,blank=True, default=0)
    regler_par = models.CharField(max_length=20,null=True,blank=True)
    # {unite, siege, autre}
    monnaie = models.ForeignKey(monnaie,on_delete=CASCADE ,blank=False)
    rempli=models.BooleanField(default=False,blank=True)  
    commentaire = models.CharField(max_length=256,null=True,blank=True)
    commentaire_degre = models.IntegerField(null=True, blank=True)
    reseau = models.CharField(max_length=20,null=True,blank=True)
    # {international, domestique, autre}
    

    def __str__(self):
     
        return '{} {} {}'.format(self.pv,self.pos6)

class proposition_source(models.Model):
    pv= models.ForeignKey(entete_pv, on_delete=CASCADE, blank=True, null=True)
    date_reception= models.CharField(max_length=30,null=True,blank=True)
    moyen_reception = models.CharField(max_length=30, null=True, blank=True)
    # {mail, courrier, fax, telex}
    source_commentaire= models.CharField(max_length=256,null=True,blank=True)
    source_degre = models.IntegerField(null=True, blank=True)
    
    
   
class realisation(models.Model):
   
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)
    realisation = models.FloatField(null=True,blank=True) 
    rempli=models.BooleanField(default=False,blank=True)  
    commentaire = models.CharField(max_length=256,null=True,blank=True)
    commentaire_degre = models.IntegerField(null=True, blank=True)
    regler_par = models.CharField(max_length=20,null=True,blank=True)
    # {unite, siege, autre}
    monnaie = models.ForeignKey(monnaie,on_delete=CASCADE ,blank=False)
    def __str__(self):
     
        return '{} {}'.format(self.pv,self.pos6)




class lettre(models.Model):
    pdf = models.FileField(upload_to='lettre')
   
class notification(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    notified_user = models.ForeignKey(profile, on_delete=models.CASCADE,default=None)
    modifier_user = models.ForeignKey(profile,related_name="cadre5",on_delete=models.CASCADE,default=None,null=True)
    date = models.DateTimeField()
    type = models.CharField(max_length=30 ,null=False)
    controle_mois=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.pv,self.notified_user,self.modifier_user)


class controle(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)
    mois =  models.CharField(max_length=20,null=True,blank=True)
    montant = models.FloatField(null=True,blank=True)
    rempli=models.BooleanField(default=False,blank=True) 

    def __str__(self):
     
        return '{} {}'.format(self.pv, self.pos6)

class reunion(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)
    cloture = models.FloatField(null=True,blank=True, default=0)
    prevision = models.FloatField(null=True,blank=True, default=0)
    proposition =  models.ForeignKey(proposition, on_delete=CASCADE, null=True)
    realisation_1 = models.ForeignKey(realisation, on_delete=CASCADE, related_name="realisation_1",null=True, blank=True)
    realisation_2 = models.ForeignKey(realisation, on_delete=CASCADE, related_name="realisation_2",null=True, blank=True)
    controle_budgetaire = models.FloatField(null=True,blank=True)
    mois_controle = models.CharField(max_length=20,null=True,blank=True)
    cadre =  models.ForeignKey(profile,related_name="cadre",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd",on_delete=models.CASCADE,default=None,null=True)
    date_cadre=models.CharField(max_length=20,null=True,blank=True)
    date_cdd=models.CharField(max_length=20,null=True,blank=True)
    date_sd=models.CharField(max_length=20,null=True,blank=True)
    valide=models.BooleanField(default=False,blank=True) 

    def __str__(self):
        return str(self.pv)

class notifie(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)
    prevision = models.FloatField(null=True,blank=True)
    monnaie = models.ForeignKey(monnaie,on_delete=CASCADE ,blank=False)
    cadre =  models.ForeignKey(profile,related_name="cadre2",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd2",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd2",on_delete=models.CASCADE,default=None,null=True)
    date_cadre=models.CharField(max_length=20,null=True,blank=True)
    date_cdd=models.CharField(max_length=20,null=True,blank=True)
    date_sd=models.CharField(max_length=20,null=True,blank=True)
    valide=models.BooleanField(default=False,blank=True) 

    def __str__(self):
        return str(self.pv)


class notifie_mensuel(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)

    janvier = models.FloatField(default=0,blank=True)
    fevrier = models.FloatField(default=0,blank=True)
    mars = models.FloatField(default=0,blank=True)
    avril = models.FloatField(default=0,blank=True)
    mai = models.FloatField(default=0,blank=True)
    juin = models.FloatField(default=0,blank=True)
    juillet = models.FloatField(default=0,blank=True)
    aout = models.FloatField(default=0,blank=True)
    septembre = models.FloatField(default=0,blank=True)
    octobre = models.FloatField(default=0,blank=True)
    novembre = models.FloatField(default=0,blank=True)
    decembre = models.FloatField(default=0,blank=True)
    monnaie = models.ForeignKey(monnaie,on_delete=CASCADE ,blank=False)
    cadre =  models.ForeignKey(profile,related_name="cadre1",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd1",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd1",on_delete=models.CASCADE,default=None,null=True)
    date_cadre=models.CharField(max_length=20,null=True,blank=True)
    date_cdd=models.CharField(max_length=20,null=True,blank=True)
    date_sd=models.CharField(max_length=20,null=True,blank=True)
    valide=models.BooleanField(default=False,blank=True) 

    def __str__(self):
        return str(self.type)






class modifications(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    type_modif = models.CharField(max_length=20,null=True,blank=True)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)
    notifie =  models.ForeignKey(notifie,on_delete=models.CASCADE,default=None)
    modif = models.FloatField(default=0,blank=True)
    monnaie = models.ForeignKey(monnaie,on_delete=CASCADE ,blank=False)
    cadre =  models.ForeignKey(profile,related_name="cadre3",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd3",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd3",on_delete=models.CASCADE,default=None,null=True)
    date_cadre=models.CharField(max_length=20,null=True,blank=True)
    date_cdd=models.CharField(max_length=20,null=True,blank=True)
    date_sd=models.CharField(max_length=20,null=True,blank=True)
    valide=models.BooleanField(default=False,blank=True) 

    def __str__(self):
        return str(self.type)


class modification_mensuel(models.Model):
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    pos6 = models.ForeignKey(Pos6, on_delete=CASCADE,blank=False, null=False)
    pos7 = models.ForeignKey(Pos7,on_delete=CASCADE, blank=True, default=None)
    type_modif = models.CharField(max_length=20,null=True,blank=True)

    janvier = models.FloatField(default=0,blank=True)
    fevrier = models.FloatField(default=0,blank=True)
    mars = models.FloatField(default=0,blank=True)
    avril = models.FloatField(default=0,blank=True)
    mai = models.FloatField(default=0,blank=True)
    juin = models.FloatField(default=0,blank=True)
    juillet = models.FloatField(default=0,blank=True)
    aout = models.FloatField(default=0,blank=True)
    septembre = models.FloatField(default=0,blank=True)
    octobre = models.FloatField(default=0,blank=True)
    novembre = models.FloatField(default=0,blank=True)
    decembre = models.FloatField(default=0,blank=True)
    cadre =  models.ForeignKey(profile,related_name="cadre4",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd4",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd4",on_delete=models.CASCADE,default=None,null=True)
    date_cadre=models.CharField(max_length=20,null=True,blank=True)
    date_cdd=models.CharField(max_length=20,null=True,blank=True)
    date_sd=models.CharField(max_length=20,null=True,blank=True)
    valide=models.BooleanField(default=False,blank=True) 


    def __str__(self):
        return str(self.pv)


############################################################################################
### not used yet ###

#class taux_change(models.Model):
#    monnaie = models.ForeignKey(monnaie,on_delete=models.CASCADE,default=None)
#    Taux = models.FloatField(null=True,blank=True)
#    mois = models.CharField(max_length=20,null=True,blank=True)
#    annee = models.IntegerField(null=True,blank=True)
#
#    def __str__(self):
#        return str(self.Taux)




####






