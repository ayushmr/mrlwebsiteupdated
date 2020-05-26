from django import forms
from .models import Productcategories,Typesofproduct, Typesofparameter,Products,Country,Authorities,Officialdefinitionsofproduct,Officialdefinitionsofparameter,Parameters, Priorities, Maintable
# from django_select2.forms import  (HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
#     ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
#     Select2Widget )
# from . import views
# # DEMO_CHOICES =( 
# #     ("1", "Naveen"), 
# #     ("2", "Pranav"), 
# #     ("3", "Isha"), 
# #     ("4", "Saloni"), 
# # )   
# # x=profile()

# # print(choice)
class gdata(forms.Form):
    choicec=Country.objects.all()
    country=forms.ModelChoiceField(help_text="Select Desired Country", queryset=choicec, to_field_name='name', widget=forms.Select(attrs={'class':'selectpicker countries','data-live-search':'true'}))
    choicep=Products.objects.all()
    product = forms.ModelChoiceField(help_text="Select Desired Product", queryset=choicep,to_field_name='name',widget=forms.Select(attrs={'class':'selectpicker countries','data-live-search':'true'}))

# class Getdata(forms.Form):
#     # choice=Countries.objects.values_list('country_name',)
    
#     choicec=Countries.objects.all()
#     choicep=Commodities.objects.all()
#     choiceparam=RegulatoryParameters.objects.all()
#     prof=Profile.objects.all()
#     countries = forms.ModelMultipleChoiceField(help_text="Select Desired Countries", queryset=choicec,widget=forms.SelectMultiple(attrs={'class':'selectpicker countries','multiple data-live-search':'true'}))
#     commodities = forms.ModelMultipleChoiceField(help_text="Select Desired Products", queryset=choicep,widget=forms.SelectMultiple(attrs={'class':'selectpicker commodities','multiple data-live-search':'true'}),to_field_name="com_name")
#     parameters = forms.ModelMultipleChoiceField(help_text="Select Desired Parameters", queryset=choiceparam,widget=forms.SelectMultiple(attrs={'class':'selectpicker params','multiple data-live-search':'true'}))
    
#     # def __init__(self,request,*args,**kwargs):
#     #     super (Getdata,self).__init__(*args,**kwargs)
#     #     self.fields['countries'] = forms.CharField(label='Username',max_length=100,initial=request.session['some_var'])
    
#     # def label_from_instance(self, obj):
#         # return "%s | %s" % (obj.country_name, obj.country_name)
#     def clean(self):
#         cleaned_data = super(Getdata, self).clean()
#         countries = cleaned_data.get('countries')
#         commodities = cleaned_data.get('commodities')
#         parameters = cleaned_data.get('parameters')
#         if not countries and not commodities and not parameters:
#             raise forms.ValidationError('You have to write something!')