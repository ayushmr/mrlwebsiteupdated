from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the 
#desired behavior
#   * Remove ` ` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Productcategories(models.Model):
    ht='It is the name of product category for example Fruit, Grains etc.'
    name=models.CharField(verbose_name='Category Name',max_length=255, unique=True,help_text=ht)

    def __str__(self):
        return self.name

    class Meta:
        # 
#         db_table = 'master'
        verbose_name_plural = "Product Categories"
        verbose_name = "Product Category"
#     

class Typesofproduct(models.Model):
    ht='It is the name of type of product on the basis of its finishing for example Proprietory, Processed etc.'
    name=models.CharField(verbose_name='Product Type',max_length=255, unique=True,help_text=ht)

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name_plural = "Product Types"
        verbose_name = "Type of Product"




class Typesofparameter(models.Model):
    ht='It is the name of type of parameter for example Pesticide, General etc.'
    name=models.CharField(verbose_name='Parameter Type',max_length=255, unique=True,help_text=ht)

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name_plural = "Parameter Types"
        verbose_name = "Type of Parameter"


class Products(models.Model):
    ht='It is the name of product for example Wheat, Chilli etc.'
    name=models.CharField(verbose_name='Product Name',max_length=255, unique=True,help_text=ht)
    typeofproduct=models.ForeignKey(verbose_name='Type of Product',to=Typesofproduct, to_field='name',on_delete=models.PROTECT,related_query_name='Type of Product')
    categoryofproduct=models.ForeignKey(verbose_name='Food category of Product',to=Productcategories, to_field='name',on_delete=models.PROTECT,related_query_name='Category of Product')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"


class Country(models.Model):
    ht='It is the name of country or geographical location for example India, European Union etc.'
    name=models.CharField(verbose_name='Country Name',max_length=255, unique=True,help_text=ht)
    note= models.TextField(null=True,blank=True, verbose_name='Note defining country regulation',help_text='Put any information here that you could not put inside the pdf report.')  
    pdf = models.FileField(blank=True, null=True,upload_to='pdf',verbose_name='Country Report',help_text='Put here a brief document defining country regulations.')
    authorities=models.ManyToManyField(to='Authorities',related_query_name='Regulatory authorities')    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        verbose_name = "Country"


class Authorities(models.Model):
    ht='It is the name of Regulatory Authority preferably full name with short form in brackets for example Food Safety Standards Institue(FSSI), Beaureau of Indian Standards(BIS) etc.'
    name=models.CharField(verbose_name='Authority Name',max_length=255, unique=True,help_text=ht)
    pdf = models.FileField(blank=True, null=True,upload_to='pdf',verbose_name='Authority Report',help_text='Put here a brief document defining Authority regulations.')
    products=models.ManyToManyField(to=Products, through='Officialdefinitionsofproduct')
    parameters=models.ManyToManyField(to='Parameters',through='Officialdefinitionsofparameter')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authorities"
        verbose_name = "Regulatroy Authority"


class Officialdefinitionsofproduct(models.Model):
    product=models.ForeignKey(to=Products, on_delete=models.PROTECT)
    authority=models.ForeignKey(to=Authorities,on_delete=models.PROTECT)
    definition=models.TextField(null=True,blank=True, verbose_name='Definition product by authority',help_text='Put the offical definition or any other descriptive qualities if defined by Authority for this product.')
    publishedcommodity=models.TextField(null=True,blank=True, verbose_name='Published name of product',help_text='Put the published name of product defined by Authority for this product. Try to involve categories and subcategories as well if given.')

    def __str__(self):
        return ("%s as defined by %s" %(self.product,self.authority))

    class Meta:
        verbose_name_plural = "Product Definitions by Authorities"
        verbose_name = "Product as defined by authority"


class Officialdefinitionsofparameter(models.Model):
    parameter=models.ForeignKey(to='Parameters',on_delete=models.PROTECT)
    authority=models.ForeignKey(to=Authorities,on_delete=models.PROTECT)
    definition=models.TextField(null=True,blank=True, verbose_name='Parameter Definition by authority',help_text='Put the offical definition or any other descriptive qualities if defined by Authority for this parameter. Any scientific family can also be mentioned if defined by the authority.')

    def __str__(self):
        return ("%s as defined by %s" %(self.parameter,self.authority))

    class Meta:
        verbose_name_plural = "Parameter definitions by Authorities"
        verbose_name = "Parameter as defined by authority"


class Parameters(models.Model):
    ht='It is the name of Parameter given by ITC system. Do not put any general names or parameter defintions here. Ex: Moisture, Ash etc.'
    name=models.CharField(verbose_name='Parameter Name',max_length=255, unique=True,help_text=ht)
    typeofparameter=models.ForeignKey(verbose_name='Type of Parameter',to=Typesofparameter, to_field='name',on_delete=models.CASCADE,related_query_name='Type of Parameter')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Parameters"
        verbose_name = "Parameter"

class Priorities(models.Model):
    ht='It is the Priority Keyword given by ITC system. ex: Mandatory, Monitoring'
    name=models.CharField(verbose_name='Priority',max_length=255, unique=True,help_text=ht) 
    definition=models.TextField(null=True,blank=True, verbose_name='Definition of the keyword',help_text='Put what exactly do you mean by this keyword')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Priority Keywords defined by research team"
        verbose_name = "Priority Keyword"

class Limit_types(models.Model):
    ht='It is the Limit type for classification of rules as per ITC staff. ex: General, Organic Limit, Residue Limits etc'
    name=models.CharField(verbose_name='Limit type',max_length=255, unique=True,help_text=ht) 
    definition=models.TextField(null=True,blank=True, verbose_name='Definition of the Limit type',help_text='Put what exactly do you mean by this Limit type')

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name_plural = "Limit Types"
        verbose_name = "Limit type"


class Maintable(models.Model):
    country_name=models.ForeignKey(verbose_name='Country',to=Country,on_delete=models.PROTECT,to_field='name')
    authority_name=models.ForeignKey(verbose_name='Regulatory Authority',to=Authorities,on_delete=models.PROTECT,to_field='name')
    product_name=models.ForeignKey(verbose_name='Product',to=Products, on_delete=models.PROTECT, to_field='name')
    parameter_name=models.ForeignKey(verbose_name='Parameter',to=Parameters, on_delete=models.PROTECT, to_field='name')

    priority = models.ForeignKey(verbose_name='Priority',to=Priorities, on_delete=models.PROTECT, to_field='name')  # Field name made lowercase.

    maximum_limit = models.FloatField(verbose_name='Maximum Limit', max_length=10,blank=True,null=True)  # Field name made lowercase.
    minimum_limit = models.FloatField(verbose_name='Minimum Limit', max_length=10, blank=True, null=True)
    unit = models.CharField(verbose_name='Unit', max_length=20, blank=True, null=True)

    effective_date = models.DateField(verbose_name='Effective Date', blank=True, null=True)  # Field name made lowercase.
    expire_date = models.DateField(verbose_name='Expire Date', blank=True, null=True)  # Field name made lowercase.
    Proposed='Proposed'
    Fixed='Fixed'
    status_of_expire_date_choices=((Proposed,'Proposed'),(Fixed,'Fixed'),)
    status_of_expire_date = models.CharField(verbose_name='Is Expire date "Fixed" or "Proposed"', max_length=8, blank=True, null=True,choices=status_of_expire_date_choices,default=None)  # Field name made lowercase.        

    Yes='YES'
    No='NO'
    import_tolerance_choices=((Yes,'YES'),(No,'NO'),)
    import_tolerance = models.CharField(verbose_name='Import Tolerance?',max_length=3,choices=import_tolerance_choices,default=No)
    limit_type = models.ForeignKey(verbose_name='Limit type',to=Limit_types, on_delete=models.PROTECT, to_field='name', blank=True, default='General')  # Field name made lowercase.
    principal_entry=models.CharField(verbose_name='Is this a Principal entry?',max_length=3,choices=import_tolerance_choices,default=Yes,help_text='Mark Yes if you think that this limit is very commonly followed for given country and product and should be shown to users by default.')

    info_on_regulations = models.TextField(verbose_name='Regulation information for given limit', blank=True, null=True, help_text='Put any official rule, article number, document name, where you think the change will occur so you could directly search and track its entries. ')  # Field name made lowercase.
    source_document = models.TextField(verbose_name='Source Document information(or Link)',blank=True, null=True)
    date_of_publishing_source = models.DateField(verbose_name='Date of Publishing Source', blank=True, null=True)  # Field name made lowercase.
    
    remarks = models.TextField(verbose_name='Remarks', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return ("Limits of %s for %s defined by %s in country %s" %(self.parameter_name,self.product_name,self.authority_name, self.country_name))

    class Meta:
        verbose_name_plural = "Main Table"
        verbose_name = "Main table entry"
        unique_together=(('country_name','product_name','parameter_name','authority_name','priority'))


# class ComCountryRelation(models.Model):
#     commodity = models.OneToOneField('Commodities', models.DO_NOTHING, db_column='commodity', primary_key=True)
#     country = models.ForeignKey('Countries', models.DO_NOTHING, db_column='country')
#     published_commodity = models.TextField(db_column='Published_commodity', blank=True, null=True)  # Field name made lowercase.
#     definition_commodity_field = models.TextField(db_column='Definition_commodity_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
#     Yes='YES'
#     No='NO'
#     undefined_published_commodity_choices=((Yes,'YES'),(No,'NO'),)
    
#     undefined_published_commodity = models.CharField(db_column='Undefined_published_commodity', max_length=3,choices=undefined_published_commodity_choices,default=No)  # Field name made lowercase.

#     class Meta:
         
#         db_table = 'com_country_relation'
#         unique_together = (('commodity', 'country'),)
#         verbose_name_plural = "Rules Associated with country and products"
#         verbose_name = "Country-Product Relationship"
#         # permissions=(
#         #     ('read_Country_product_relationships','Can read specific information related to any product with any country'),
#         # )



# class Commodities(models.Model):
#     com_name = models.CharField(primary_key=True, max_length=255)
#     Ra='RAW AGRICULTURAL'
#     Proc='PROCESSED'
#     com_type_choices=((Ra,'RAW AGRICULTURAL'),(Proc,'PROCESSED'),)
#     com_type = models.CharField(db_column='com-type', max_length=16,choices=com_type_choices,null=True)  # Field renamed to remove unsuitable characters.

#     def __str__(self):
#         return self.com_name

#     class Meta:
         
#         db_table = 'commodities'
#         verbose_name_plural = "List of Commodities"
#         verbose_name = "Commodity"
#         # permissions=(
#         #     ('read_commodities','Can read commodities supported by platform'),
#         # )



# class Countries(models.Model):
#     country_name = models.CharField(primary_key=True, max_length=45)
#     note_for_country_regulations = models.TextField(db_column='Note_for_country_regulations')  # Field name made lowercase.
#     pdf_note = models.FileField(upload_to='pdf', blank=True, null=True)
#     def __str__(self):
#         return self.country_name

#     class Meta:
         
#         db_table = 'countries'
#         verbose_name_plural = "List of Countries"
#         verbose_name = "Country"
#         # permissions=(
#         #     ('read_countries','Can read countries supported by platform'),
#         # )



# class Master(models.Model):
#     ID= models.IntegerField(db_column='IDX',primary_key=True, editable=False)
#     country = models.ForeignKey(Countries, models.DO_NOTHING, db_column='Country')  # Field name made lowercase.
#     product = models.ForeignKey(Commodities, models.DO_NOTHING, db_column='Product')  # Field name made lowercase.
#     parameter = models.ForeignKey('RegulatoryParameters', models.DO_NOTHING, 
# db_column='Parameter')  # Field name made lowercase.
#     Maximum_Limit = models.FloatField(db_column='Maximum_Limit', max_length=10,blank=True,null=True)  # Field name made lowercase.
#     Minimum_Limit = models.FloatField(db_column='Minimum_Limit', max_length=10, default=0)
#     Unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)
#     # Constants in Model class
#     Default='Default'
#     General='General'
#     Organic_MRLs='Organic MRLs'
#     Not_defined='Not defined'

#     mrl_type_choices = (
#         (Default, 'Default'),
#         (General, 'General'),
#         (Organic_MRLs,'Organic MRLs'),
#         (Not_defined,'Not defined')
#         )
    
#     Limit_type = models.CharField(db_column='MRL_type', max_length=20,choices=mrl_type_choices,default=Default)  # Field 
# #name made lowercase.
#     effective_date = models.DateField(db_column='Effective_Date', blank=True, null=True)  # Field name made lowercase.
#     expire_date = models.DateField(db_column='Expire_Date', blank=True, null=True)  # Field name made lowercase.
#     Proposed='Proposed'
#     Fixed='Fixed'
#     status_of_expire_date_choices=((Proposed,'Proposed'),(Fixed,'Fixed'),)
    
#     status_of_expire_date = models.CharField(db_column='Status_of_expire_date', max_length=8, blank=True, null=True,choices=status_of_expire_date_choices,default=None)  # Field name made lowercase.        
#     Yes='YES'
#     No='NO'
#     import_tolerance_choices=((Yes,'YES'),(No,'NO'),)
#     import_tolerance = models.CharField(max_length=3,choices=import_tolerance_choices,default=No)
#     info_on_regulations = models.CharField(db_column='Info_on_regulations', max_length=255, blank=True, null=True)  # Field name made lowercase.
#     Compliance_Authority= models.ForeignKey(Authorities, models.DO_NOTHING, db_column='Authority_Name', null=True, blank=True)
#     parameter_definition = models.CharField(db_column='Residue_definititon', max_length=255, blank=True, null=True)  # Field name made lowercase.
#     source_document = models.TextField(blank=True, null=True)
#     date_of_publishing_source = models.DateField(db_column='Date_of_publishing_source', blank=True, null=True)  # Field name made lowercase.
#     Ma='MANDATORY'
#     Mo='MONITORING'
#     pd='PROPOSED DRAFT'
#     criticality_of_maintaining_choices=((Ma,'MANDATORY'),(Mo,'MONITORING'),(pd,'PROPOSED DRAFT'),)
#     criticality_of_maintaining = models.CharField(db_column='Criticality_of_maintaining', max_length=20,choices=criticality_of_maintaining_choices,default=Ma)  # Field name made lowercase.
#     remarks = models.TextField(db_column='Remarks', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
         
#         db_table = 'master'
#         verbose_name_plural = "Main Table"
#         verbose_name = "Regulation Detail"
#         unique_together = (('country', 'product', 'parameter','criticality_of_maintaining',))
#         ordering = ['country', 'product','criticality_of_maintaining', 'parameter']
#         # permissions=(
#         #     ('read_master','Can read specific MRL related to various countries and commodities supported by platform'),
#         # )


# class RegulatoryParameters(models.Model):
#     name_of_parameter = models.CharField(db_column='Name_of_parameter', primary_key=True, max_length=255)  # Field name made lowercase.
#     type_of_parameter = models.ForeignKey('TypeOfParameters', models.DO_NOTHING, db_column='Type_of_parameter')  # Field name made lowercase.

#     def __str__(self):
#         return self.name_of_parameter

#     class Meta:
         
#         db_table = 'regulatory_parameters'
#         verbose_name = "PARAMETER"
#         verbose_name_plural = "List of Parameters"
        
#         # permissions=(
#         #     ('read_parameters','Can read parameters supported by platform'),
#         # )


# # class Authorities(models.Model):
# #     Authority_Name = models.CharField(primary_key=True, max_length=20)
# #     country = models.ForeignKey(Countries, models.DO_NOTHING, db_column='Country', blank=True, null=True)

# #     def __str__(self):
# #         return self.type

# #     class Meta:
# #         verbose_name = "Authority"
# #         verbose_name_plural = "Authorities"
# #         # permissions=(
#         #     ('read_parameter_types','Can read parameter types supported by platform'),
#         # )

# class TypeOfParameters(models.Model):
#     type = models.CharField(primary_key=True, max_length=40)

#     def __str__(self):
#         return self.type

#     class Meta:
#         db_table = 'type_of_parameters'
#         verbose_name = "TYPE OF PARAMETER"
#         verbose_name_plural = "List of TYPES OF PARAMETERS"
#         # permissions=(
#         #     ('read_parameter_types','Can read parameter types supported by platform'),
#         # )