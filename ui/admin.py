from django.contrib import admin
from .filters import *
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from django.db.models import Q
# Register your models here.
from .models import Productcategories,Typesofproduct, Typesofparameter,Products,Country,Authorities,Officialdefinitionsofproduct,Officialdefinitionsofparameter,Parameters, Priorities, Maintable, Limit_types
from django.contrib.auth.models import Permission
# admin.site.register(Permission)
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from django.contrib.admin.sites import site as default_site

from related_admin import RelatedFieldAdmin
from related_admin import getter_for_related_field


admin.site.site_header = "ITC's Global Regulatory Database Admin Portal| KITES PROJECT"


class OfficialdefinitionsofproductInline(admin.TabularInline):
    model = Officialdefinitionsofproduct

class OfficialdefinitionsofparameterInline(admin.TabularInline):
    model = Officialdefinitionsofparameter

class MaintableInline(admin.TabularInline):
    model = Maintable

class ProductsInline(admin.TabularInline):
    model = Products

class ParametersInline(admin.TabularInline):
    model = Parameters




class CustomModelAdminMixin(object):
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        
        # def index(self, request, extra_context=None):
        #     """
        #     Display the main admin index page, which lists all of the installed
        #     apps that have been registered in this site.
        #     """
        #     # app_list = self.get_app_list(request)
        #     app_list=['User Control', 'REgulatory Tables']
        #     context = {
        #         **self.each_context(request),
        #         'title': self.index_title,
        #         'app_list': app_list,
        #         **(extra_context or {}),
        #     }

        #     request.current_app = self.name

        #     return TemplateResponse(request, self.index_template or
        #         'admin/index.html', context)
        self.search_fields=[]
        for i in model._meta.fields:
            
            if(i.name!='id'):
                if i.__class__.__name__=='ForeignKey':
                    self.search_fields.append(i.name+'__name')    
                else:
                    self.search_fields.append(i.name)
            print(self.search_fields)
        # self.search_fields= [field.name for field in model._meta.fields if ((field.name != "id") and (field.__class__.__name__ != 'ForeignKey'))]
        # print(self.search_fields)
        super(CustomModelAdminMixin, self).__init__(model, admin_site)

class Limit_typesResource(resources.ModelResource):
        
    class Meta:
        model = Limit_types
        import_id_fields=['name']
        exclude=('id',)

class Limit_typesAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    inlines=[MaintableInline]
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    resource_class=Limit_types
    class Meta:
        pass
    pass
admin.site.register(Limit_types,Limit_typesAdmin)


class PrioritiesResource(resources.ModelResource):
    
    class Meta:
        model = Priorities
        import_id_fields=['name']
        exclude=('id',)

class PrioritiesAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    inlines=[MaintableInline]
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    resource_class=PrioritiesResource
    class Meta:
        pass
    pass
admin.site.register(Priorities,PrioritiesAdmin)



class MaintableResource(resources.ModelResource):
    country_name=fields.Field(column_name='country_name', attribute='country_name', widget=ForeignKeyWidget(Country,'name'))
    product_name=fields.Field(column_name='product_name', attribute='product_name', widget=ForeignKeyWidget(Products,'name'))
    parameter_name=fields.Field(column_name='parameter_name', attribute='parameter_name', widget=ForeignKeyWidget(Parameters,'name'))
    authority_name=fields.Field(column_name='authority_name', attribute='authority_name', widget=ForeignKeyWidget(Authorities,'name'))
    priority=fields.Field(column_name='priority', attribute='priority', widget=ForeignKeyWidget(Priorities,'name'))
    limit_type=fields.Field(column_name='limit_type', attribute='limit_type', widget=ForeignKeyWidget(Limit_types,'name'))


    class Meta:
        model = Maintable
        import_id_fields=['country_name','product_name','parameter_name','authority_name','priority','principal_entry']
        exclude=('id',)

class MaintableAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    list_filter=('product_name__categoryofproduct','priority__name','parameter_name__typeofparameter','authority_name',)
    resource_class=MaintableResource
    list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    # def get_readonly_fields(self, request, obj=None):
    #     if obj and obj.product_name=="Wheat grain":
    #         return self.readonly_fields+('maximum_limit',)
    #     return self.readonly_fields

    class Meta:
        pass
admin.site.register(Maintable,MaintableAdmin)



class CountriesResource(resources.ModelResource):
    authorities=fields.Field(column_name='authorities', attribute='authorities', widget=ManyToManyWidget(Authorities,'name'))
    class Meta:
        model = Country
        import_id_fields=['name']
        exclude=('id',)

# @admin.register(Country)
class CountriesAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    # pass
    resource_class=CountriesResource
    class Meta:
        pass
admin.site.register(Country,CountriesAdmin)



class ProductsResource(resources.ModelResource):
    categoryofproduct=fields.Field(column_name='categoryofproduct', attribute='categoryofproduct', widget=ForeignKeyWidget(Productcategories,'name'))
    typeofproduct=fields.Field(column_name='typeofproduct', attribute='typeofproduct', widget=ForeignKeyWidget(Typesofproduct,'name'))
    class Meta:
        model = Products
        import_id_fields=['name']
        exclude=('id',)

# @admin.register(Products)
class ProductsAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    inlines=[OfficialdefinitionsofproductInline]
    resource_class=ProductsResource
    list_filter=('categoryofproduct',)
    class Meta:
        pass
admin.site.register(Products,ProductsAdmin)



class ParametersResource(resources.ModelResource):
    typeofparameter=fields.Field(column_name='typeofparameter', attribute='typeofparameter', widget=ForeignKeyWidget(Typesofparameter,'name'))
    class Meta:
        model = Parameters
        import_id_fields=['name']
        exclude=('id',)

# @admin.register(Parameters)
class ParametersAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    inlines=[OfficialdefinitionsofparameterInline]
    resource_class = ParametersResource
    list_filter=('typeofparameter',)
    class Meta:
        pass
    pass
admin.site.register(Parameters,ParametersAdmin)



class AuthoritiesResource(resources.ModelResource):
    products=fields.Field(column_name='products', attribute='products', widget=ManyToManyWidget(Products,'name'))
    parameters=fields.Field(column_name='parameters', attribute='parameters', widget=ForeignKeyWidget(Parameters,'name'))
    class Meta:
        model = Authorities
        import_id_fields=['name']
        exclude=('id',)

# @admin.register(Authorities)
class AuthoritiesAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    resource_class=AuthoritiesResource
    class Meta:
        pass        
    pass    
admin.site.register(Authorities,AuthoritiesAdmin)



class ProductcategoriesResource(resources.ModelResource):    
    class Meta:
        model = Productcategories
        import_id_fields=['name']
        exclude=('id',)

# @admin.register(Productcategories)
class ProductcategoriesAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    inlines=[ProductsInline]
    resource_class=ProductcategoriesResource
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    class Meta:
        pass
    pass
admin.site.register(Productcategories,ProductcategoriesAdmin)


class TypesofproductResource(resources.ModelResource):
    
    class Meta:
        model = Typesofproduct
        import_id_fields=['name']
        exclude=('id',)

# @admin.register(Typesofproduct)
class TypesofproductAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    inlines=[ProductsInline]
    resource_class=TypesofproductResource
    class Meta:
        pass
    pass
admin.site.register(Typesofproduct,TypesofproductAdmin)


class TypesofparameterResource(resources.ModelResource):
    
    class Meta:
        model = Typesofparameter
        import_id_fields=['name']
        exclude=('id',)

# @admin.register(Typesofparameter)
class TypesofparameterAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)    
    inlines=[ParametersInline]
    resource_class=TypesofparameterResource
    class Meta:
        pass
    pass
admin.site.register(Typesofparameter,TypesofparameterAdmin)



class OfficialdefinitionsofproductResource(resources.ModelResource):
    authority=fields.Field(column_name='authority', attribute='authority', widget=ForeignKeyWidget(Authorities,'name'))
    product=fields.Field(column_name='product', attribute='product', widget=ForeignKeyWidget(Products,'name'))
    class Meta:
        model = Officialdefinitionsofproduct
        import_id_fields=['product','authority']
        exclude=('id',)

# @admin.register(Officialdefinitionsofproduct)
class OfficialdefinitionsofproductAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    # inlines=[MaintableInline]
    resource_class=OfficialdefinitionsofproductResource
    class Meta:
        search_fields=['product__name','authority__name']
    pass
admin.site.register(Officialdefinitionsofproduct,OfficialdefinitionsofproductAdmin)



class OfficialdefinitionsofparameterResource(resources.ModelResource):
    authority=fields.Field(column_name='authority', attribute='authority', widget=ForeignKeyWidget(Authorities,'name'))
    parameter=fields.Field(column_name='parameter', attribute='parameter', widget=ForeignKeyWidget(Parameters,'name'))
    class Meta:
        model = Officialdefinitionsofparameter
        import_id_fields=['parameter','authority']
        exclude=('id',)

# @admin.register(Officialdefinitionsofparameter)
class OfficialdefinitionsofparameterAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    # list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)
    # inlines=[MaintableInline]
    resource_class=OfficialdefinitionsofparameterResource
    class Meta:
        pass
    pass
admin.site.register(Officialdefinitionsofparameter,OfficialdefinitionsofparameterAdmin)



















# @admin.register(Profile)
# class ProfilesAdmin(admin.ModelAdmin):
#     list_display = ('user', 'Countries_of_interest','Products_of_interest','Parameters_of_interest','Parameter_types_of_interest',)


# #admin.site.register(Master)
# #admin.site.register(RegulatoryParameters)
# #admin.site.register(TypeOfParameters)
# #admin.site.register(Countries)
# #admin.site.register(Commodities)
# #admin.site.register(ComCountryRelation)
# class ComCountryRelationInline(admin.TabularInline):
#     model = ComCountryRelation

# # class StatusListFilter(MultipleChoiceListFilter):
# #     title = 'Priority'
# #     parameter_name = 'criticality_of_maintaining'

# #     def lookups(self, request, model_admin):
# #         return Master.criticality_of_maintaining_choices


# # # Define the admin class

# # class countriesListFilter(admin.SimpleListFilter):
    
# #     """
# #     This filter will always return a subset of the instances in a Model, either filtering by the
# #     user choice or by a default value.
# #     """
# #     # Human-readable title which will be displayed in the
# #     # right admin sidebar just above the filter options.
# #     title = 'Countries'

# #     # Parameter for the filter that will be used in the URL query.
# #     parameter_name = 'country'

# #     default_value = None

# #     def lookups(self, request, model_admin):
# #         """
# #         Returns a list of tuples. The first element in each
# #         tuple is the coded value for the option that will
# #         appear in the URL query. The second element is the
# #         human-readable name for the option that will appear
# #         in the right sidebar.
# #         """
# #         list_of_countries = []
# #         queryset = Countries.objects.all()
# #         for countries in queryset:
# #             list_of_countries.append(
# #                 (str(countries.country_name), countries.country_name)
# #             )
# #         return sorted(list_of_countries, key=lambda tp: tp[1])

# #     def queryset(self, request, queryset):
# #         """
# #         Returns the filtered queryset based on the value
# #         provided in the query string and retrievable via
# #         `self.value()`.
# #         """
# #         # Compare the requested value to decide how to filter the queryset.
# #         if self.value():
# #             return queryset.filter(country__country_name=self.value())
# #         return queryset

# #     def value(self):
# #         """
# #         Overriding this method will allow us to always have a default value.
# #         """
# #         value = super(countriesListFilter, self).value()
# #         if value is None:
# #             if self.default_value is None:
# #                 # If there is at least one Species, return the first by name. Otherwise, None.
# #                 first_countries = Countries.objects.order_by('country_name').first()
# #                 value = None if first_countries is None else first_countries.country_name
# #                 self.default_value = value
# #             else:
# #                 value = self.default_value
# #         return str(value)
# class RegulatoryParametersResource(resources.ModelResource):
    
#     class Meta:
#         model = RegulatoryParameters
#         import_id_fields=['name_of_parameter']


# class CountryResource(resources.ModelResource):
    
#     class Meta:
#         model = Countries
#         import_id_fields=['country_name']

# class MasterResource(resources.ModelResource):
    
#     class Meta:
#         model = Master
#         import_id_fields=['country','product','parameter','criticality_of_maintaining']
#         exclude=('ID',)
#         fieldsets = (
#         (None, {
#             'fields': ('country', 'product', 'parameter',('Maximum_Limit','Minimum_Limit','Unit','criticality_of_maintaining','parameter_definition','import_tolerance'))
#         }),
#         ('Additional Details about timeline of rule', {
#             'fields': ('effective_date', 'expire_date','status_of_expire_date')
#         }),
#         ('Information on source and rules', {
#             'fields': ('info_on_regulations','Limit_type','source_document','date_of_publishing_source','remarks')
#         }),
#     )

    
# # class MasterAdmin(admin.ModelAdmin):
#     # list_display = ('country', 'product', 'parameter', 'mrl','criticality_of_maintaining','mrl_type','effective_date','expire_date','status_of_expire_date','import_tolerance','date_of_publishing_source','info_on_regulations','residue_definition','source_document','remarks')
#     # list_filter = (('product', admin.RelatedOnlyFieldListFilter),('parameter', admin.RelatedOnlyFieldListFilter),('country', admin.RelatedOnlyFieldListFilter),'criticality_of_maintaining',)
#     # search_fields=('country__country_name','parameter__name_of_parameter','product__com_name',)
#     # def get_ordering(self, request):
#     #     if request.user.is_superuser:
#     #         return ['country', 'product','parameter']
#     #     else:
#     #         return ['country']

#     # blog_list = Master.objects.filter( country__country_name = 'Canada' ).order_by( '-id' )
#     # list_select_related=('product','parameter',)
    
#     # def country(self,obj):
#     #     return obj.country.country_name
#     # country.admin_order_field='country'
#     # # multiple_selection_list_filter = ('country', 'product','parameter','criticality_of_maintaining',)
#     # fields=['country','product', ('parameter', 'mrl','residue_definition','criticality_of_maintaining'),('info_on_regulations','source_document'),'remarks']    
# # Register the admin class with the associated model
#     # fieldsets = (
#     #     (None, {
#     #         'fields': ('country', 'product', 'parameter',('mrl','criticality_of_maintaining','residue_definition','import_tolerance'))
#     #     }),
#     #     ('Additional Details about timeline of rule', {
#     #         'fields': ('effective_date', 'expire_date','status_of_expire_date')
#     #     }),
#     #     ('Information on source and rules', {
#     #         'fields': ('info_on_regulations','mrl_type','source_document','date_of_publishing_source','remarks')
#     #     }),
#     # )
#     # def get_readonly_fields(self, request, obj=None):
#     #     if not request.user.is_superuser and request.user.has_perm('master.read_master'):
#     #         return [(f.product,f.country,f.parameter,f.mrl,f.mrl_type) for f in self.model._meta.fields]        
#     #     return super(MasterAdmin, self).get_readonly_fields(
#     #         request, obj=obj
#     #     )

# class MasterAdmin(ImportExportModelAdmin,RelatedFieldAdmin):
#     resource_class = MasterResource
#     list_display = ('country', 'product', 'parameter','parameter__type_of_parameter', 'Maximum_Limit','Minimum_Limit','Unit','criticality_of_maintaining','Limit_type','effective_date','expire_date','status_of_expire_date','import_tolerance','source_document','date_of_publishing_source','info_on_regulations','parameter_definition','remarks')
#     # list_display = ('country', 'product', 'parameter', 'mrl','criticality_of_maintaining','mrl_type','effective_date','expire_date','status_of_expire_date','import_tolerance','date_of_publishing_source','info_on_regulations','residue_definition','source_document','remarks')
#     list_filter = (('product', admin.RelatedOnlyFieldListFilter),'parameter__type_of_parameter',('country', admin.RelatedOnlyFieldListFilter),'criticality_of_maintaining',)
#     search_fields=('country__country_name','parameter__name_of_parameter','product__com_name','parameter__type_of_parameter','info_on_regulations','parameter_definition','Limit_type','effective_date','expire_date','status_of_expire_date' ,'source_document','date_of_publishing_source','info_on_regulations','remarks')
    
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         master_instance=Profile.objects.filter(user=request.user)
#         # print(qs.filter(parameter__type_of_parameter='Physico-chemical'))
#         Final=Q()
#         for i in master_instance:
#             Temp=Q()
            
#             if(i.Parameter_types_of_interest==None):
#                 if(i.Countries_of_interest==None):
#                     if(i.Products_of_interest==None):
#                         if(i.Parameters_of_interest==None):
#                             Final=Final|(Temp)
#                             continue
#                         else:
#                             Temp=Temp|Q(parameter=i.Parameters_of_interest)
#                     else:
#                         Temp=Temp|Q(product=i.Products_of_interest)
#                         if(i.Parameters_of_interest==None):
#                             Final=Final|(Temp)
#                             continue
#                         else:
#                             Temp=(Temp&Q(parameter=i.Parameters_of_interest))
#                 else:
#                     Temp=Temp|Q(country=i.Countries_of_interest)
#                     if(i.Products_of_interest==None):
#                         if(i.Parameters_of_interest==None):
#                             Final=Final|(Temp)
#                             continue
#                         else:
#                             Temp=(Temp&Q(parameter=i.Parameters_of_interest))
#                     else:
#                         Temp=(Temp&Q(product=i.Products_of_interest))
#                         if(i.Parameters_of_interest==None):
#                             Final=Final|(Temp)
#                             continue
#                         else:
#                             Temp=(Temp&Q(parameter=i.Parameters_of_interest))
#             else:
#                 Temp=Temp|Q(parameter__type_of_parameter=i.Parameter_types_of_interest)
             
#             Final=Final|(Temp)
           
#         return qs.filter(Final)


#     def get_ordering(self, request):
#         if request.user.is_superuser:
#             return ['country', 'product','parameter']
#         else:
#             return ['country']
#     fieldsets = (
#         (None, {
#             'fields': ('country', 'product', 'parameter',('Minimum_Limit','Maximum_Limit','Unit','criticality_of_maintaining','parameter_definition','import_tolerance'))
#         }),
#         ('Additional Details about timeline of rule', {
#             'fields': ('effective_date', 'expire_date','status_of_expire_date')
#         }),
#         ('Information on source and rules', {
#             'fields': ('info_on_regulations','Compliance_Authority','Limit_type','source_document','date_of_publishing_source','remarks')
#         }),
#     )
    
# # admin.site.unregister(Master)
# admin.site.register(Master, MasterAdmin)

# class RegulatoryParametersInline(admin.TabularInline):
#     model = RegulatoryParameters


# # @admin.register(RegulatoryParameters)
# class RegulatoryParametersAdmin(ImportExportModelAdmin):
#     list_display = ('name_of_parameter', 'type_of_parameter')
#     resource_class = RegulatoryParametersResource
#     list_filter=('type_of_parameter',)
# admin.site.register(RegulatoryParameters,RegulatoryParametersAdmin)

# # Register the Admin classes for BookInstance using the decorator
# @admin.register(TypeOfParameters) 
# class TypeOfParametersAdmin(admin.ModelAdmin):
#     list_display = ('type',)
#     inlines=[RegulatoryParametersInline]

# #@admin.register(Countries) 
# # class CountriesAdmin(admin.ModelAdmin):
# #     list_display = ('country_name','note_for_country_regulations')
# #     inlines = [ComCountryRelationInline]

# class AuthoritiesAdmin(ImportExportModelAdmin):
#     list_display = ('Authority_Name','country','info_note')
#     # inlines = [MasterInline]
#     list_filter=('country',)
#     resource_class = CountryResource
#     # def get_queryset(self, request):
#     #     qs = super().get_queryset(request)
#     #     if request.user.is_superuser:
#     #         return qs
#     #     return qs.filter(country_name__in=Profile.objects.filter(user=request.user).values_list('Countries_of_interest',flat=True))

# admin.site.register(Authorities,AuthoritiesAdmin)

# class CountriesAdmin(ImportExportModelAdmin):
#     list_display = ('country_name','note_for_country_regulations','pdf_note')
#     inlines = [ComCountryRelationInline]
#     resource_class = CountryResource
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(country_name__in=Profile.objects.filter(user=request.user).values_list('Countries_of_interest',flat=True))

# admin.site.register(Countries,CountriesAdmin)

# @admin.register(Commodities) 
# class CommoditiesAdmin(admin.ModelAdmin):
#     list_display = ('com_name', 'com_type')
#     inlines = [ComCountryRelationInline]


# # @admin.register(ComCountryRelation) 
# class ComCountryRelationAdmin(ImportExportModelAdmin):
#     list_display = ('commodity', 'country', 'published_commodity', 'definition_commodity_field')
#     list_filter=('country',)
# admin.site.register(ComCountryRelation, ComCountryRelationAdmin)


# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin

# Unregister the provided model admin
# admin.site.unregister(User)

# # Register out own model admin, based on the default UserAdmin
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     pass

