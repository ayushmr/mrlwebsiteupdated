from django.shortcuts import render
from .models import Productcategories,Typesofproduct, Typesofparameter,Products,Country,Authorities,Officialdefinitionsofproduct,Officialdefinitionsofparameter,Parameters, Priorities, Maintable

# from .models import Master,Countries,ComCountryRelation,RegulatoryParameters,TypeOfParameters,Profile,Commodities
# Create your views here.
import io
import xlsxwriter
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect
import xlwt
import csv
from operator import itemgetter
from itertools import groupby
from .forms import gdata
# from .forms import Getdata
def index(request):
    countrieslist=request.session['col']
    commoditylist=request.session['coml']
    parameterlist=request.session['parl']
    master=Master.objects.filter(Q(country__in=countrieslist)&Q(product__in=commoditylist)&Q(parameter__in=parameterlist)).all()
    

    
    # master_by_countries=Master.objects.values('country')
    # master_by_commodities=Master.objects.values('product')
    # master_by_country_commodity=master.filter()
    # master_by_parameters=Master.objects.values('parameter')
    # for country in master_by_countries:
    #     for commodity in master_by_commodities:
    #         for parameter in master_by_parameters:
    #             master.filter()
    countries=Countries.objects.all()
    com=Commodities.objects.all()
    comcon=ComCountryRelation.objects.all()
    params=RegulatoryParameters.objects.all()
    paramtype=TypeOfParameters.objects.all()
    prof=Profile.objects.all()
    
    
    return render(request,'report.html',{'master': master,'countries':countries,'com':com,'comcon':comcon,'params':params,'paramtype':paramtype,'prof':prof})


# def new_report(request):
#     form=Getdata(request.POST or None)
#     if request.POST:
#         data=request.POST.copy()
#         countrylist=data.getlist('countries')
#         comlist=data.getlist('commodities')
#         paramlist=data.getlist('parameters')

def compute_rows(text, width):
    if len(text) < width:
        return 1
    phrases = text.replace('\r', '').split('\n')
 
    rows = 0
    for phrase in phrases:
        if len(phrase) < width:
            rows = rows + 1
        else:
            words = phrase.split(' ')
            temp = ''
            for idx, word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows = rows + 1
                    temp = '' + word + ' '
                # check if it is not the last word
                if idx == len(words) - 1 and len(temp) > 0:
                    rows = rows + 1
    return rows


def newform(request):
    form=gdata(request.POST or None)
    if request.POST:
        data=request.POST.copy()
        

        output=io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet_s = workbook.add_worksheet("General Information")
        title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter',
        'color':'white',
        'bg_color':'black'
        
        })
        header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
        })
        text_format = workbook.add_format({'text_wrap': True})

        
        country=(data.getlist('country'))[0]
        product=(data.getlist('product'))[0]

        title_text = u"Specification Sheet for Country: {0}; For Product: {1}".format(country, product)
        worksheet_s.merge_range('B2:H2', title_text, title)

        all_maintable=Maintable.objects.filter(Q(country_name=country),Q(product_name=product))
        principal_maintable=all_maintable.filter(Q(principal_entry='Yes'))
        principal_maintable=principal_maintable.order_by('priority')
        all_priorities=principal_maintable.values_list('priority', flat=True).distinct()
        authoritiesforpe=set(principal_maintable.values_list('authority_name',flat=True).distinct())
        # print(authoritiesforpe)
        datawhole={'country':country,'product':product, }
        officialdefns={}

        # the rest of the headers from the HTML file

        c=0
        x=3
        description_col_width=20
        observations_col_width = 20
        for i in authoritiesforpe:
            
            worksheet_s.write(4+c,x , "Regulatory Authority", header)
            worksheet_s.write(4+c, x+1, i)
            if(len(i)>description_col_width):
                description_col_width=len(i)
            
            c=c+1
            # worksheet_s.write(4, 3, ugettext(u"Max T. (℃)"), header)
            
            officialdefns[i]={}
            try:
                obj=Officialdefinitionsofproduct.objects.get(authority__name=i,product__name=product)
                officialdefns[i]['publishedcommodity']=obj.publishedcommodity
                # officialdefns[i]['publishedcommodity'] = officialdefns[i]['publishedcommodity'].replace('\r', '')
                worksheet_s.write(4+c, x, "Published Commodity", header)
                worksheet_s.write(4+c, x+1, officialdefns[i]['publishedcommodity'],text_format)
                # observations_rows = compute_rows(officialdefns[i]['publishedcommodity'], observations_col_width)
                # print(observations_rows)
                # worksheet_s.set_row(4+c, 15 * observations_rows)
                c=c+1
                officialdefns[i]['definition']=obj.definition
                # officialdefns[i]['definition'] = officialdefns[i]['definition'].replace('\r', '')
                worksheet_s.write(4+c, x, "Definition", header)
                worksheet_s.write(4+c, x+1, officialdefns[i]['definition'], text_format)
                # observations_rows = compute_rows(officialdefns[i]['definition'], observations_col_width)
                # print(observations_rows)
                # worksheet_s.set_row(4+c, 15 * observations_rows)
                worksheet_s.set_column('D:E', description_col_width)
                c=c+3
            except Exception as e:
                print(e)
                c=c+1
                continue
            
        par_col_width=25
        range_col_width=25
        limits_col_width=10
        unit_col_width=20
        regulation_col_width=20
        remarks_col_width=50
        source_col_width=35
        for i in all_priorities:
            worksheet_s = workbook.add_worksheet("%s Regulations"%(i))
            rin,cin=0,1
            r,c=rin,cin
            prmnbypr=principal_maintable.filter(priority__name=i)
            prmnbypr=prmnbypr.order_by('parameter_name__typeofparameter')
            typesofparam=prmnbypr.values_list('parameter_name__typeofparameter__name', flat=True).distinct()
            datawhole[i]={}
            for j in typesofparam:
                datawhole[i][j]={}
                
                title_text = u"{0}".format(j)
                r+=1
                worksheet_s.merge_range('A{0}:I{0}'.format(r), title_text, title)
                r+=1

                prmnbyprandt=prmnbypr.filter(parameter_name__typeofparameter__name=j)
                prmnbyprandt=prmnbyprandt.order_by('parameter_name')
                worksheet_s.set_column('%s:%s'%(chr(c+65),chr(c+65)), par_col_width)
                worksheet_s.write(r, c, "Parameter Name", header)
                c+=1
                worksheet_s.set_column('%s:%s'%(chr(c+65),chr(c+65)), range_col_width)
                worksheet_s.write(r, c, "Range", header)
                c+=1
                worksheet_s.set_column('%s:%s'%(chr(c+65),chr(c+65)), limits_col_width)
                worksheet_s.write(r, c, "Limits", header)
                c+=1
                worksheet_s.set_column('%s:%s'%(chr(c+65),chr(c+65)), unit_col_width)
                worksheet_s.write(r, c, "Unit", header)
                c+=1
                worksheet_s.set_column('%s:%s'%(chr(c+65),chr(c+65)), remarks_col_width)
                worksheet_s.write(r, c, "Remarks", header)
                c+=1
                worksheet_s.set_column('%s:%s'%(chr(c+65),chr(c+65)), source_col_width)
                worksheet_s.write(r, c, "Source Information", header)
                c+=1
                worksheet_s.set_column('%s:%s'%(chr(c+65),chr(c+65)), regulation_col_width)
                worksheet_s.write(r, c, "Official Communication", header)
                c=cin
                r+=1
                for k in prmnbyprandt:
                    kn=k.parameter_name.name
                    worksheet_s.write(r, c, kn,text_format)
                    c+=1
                    datawhole[i][j][kn]={}
                    if(k.minimum_limit==None):
                        if(k.maximum_limit==None):
                            datawhole[i][j][kn]['Range']='Not defined'
                            datawhole[i][j][kn]['Limits']='Not defined'
                        else:
                            datawhole[i][j][kn]['Range']='Should be Less than'
                            datawhole[i][j][kn]['Limits']=k.maximum_limit
                    else:
                        if(k.maximum_limit==None):
                            datawhole[i][j][kn]['Range']='Should be More than'
                            datawhole[i][j][kn]['Limits']=k.minimum_limit
                        else:
                            datawhole[i][j][kn]['Range']='In between'
                            datawhole[i][j][kn]['Limits']="{0}-{1}".format(k.minimum_limit,k.maximum_limit)
                    datawhole[i][j][kn]['Official Communication']=k.info_on_regulations
                    datawhole[i][j][kn]['Unit']=k.unit
                    datawhole[i][j][kn]['Remarks']=k.remarks
                    datawhole[i][j][kn]['Source']=k.source_document
                    worksheet_s.write(r, c, datawhole[i][j][kn]['Range'],text_format)
                    c+=1
                    worksheet_s.write(r, c, datawhole[i][j][kn]['Limits'],text_format)
                    c+=1
                    worksheet_s.write(r, c, datawhole[i][j][kn]['Unit'],text_format)
                    c+=1
                    worksheet_s.write(r, c, datawhole[i][j][kn]['Remarks'],text_format)
                    c+=1
                    worksheet_s.write(r, c, datawhole[i][j][kn]['Source'],text_format)
                    c+=1
                    worksheet_s.write(r, c, datawhole[i][j][kn]['Official Communication'],text_format)
                    c=cin
                    r+=1
                r+=1









        # print(datawhole)            
        workbook.close()
        xlsx_data = output.getvalue()
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        response.write(xlsx_data)
        return response
        


    return render(request,"newform.html",{'form':form,})



def form(request):
    # context={'form':}
    form=Getdata(request.POST or None)
    # context['form']= Getdata()
    if request.POST:
        # if form.is_valid():
            data = request.POST.copy()
            request.session['col']=data.getlist('countries')
            request.session['coml']=data.getlist('commodities')
            request.session['parl']=data.getlist('parameters')
            return redirect('/ui')
            # temp=form.cleaned_data.get()
            # print(temp)
    return render(request,"form.html",{'form':form,})

def excel_view(request):
    normal_style = xlwt.easyxf("""
     font:
         name Verdana
     """) 
    response = HttpResponse(content_type='ui/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="data.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Username', 'First name', 'Last name', 'Email address'])

    # print(request.GET.copy())
    wb = xlwt.Workbook()
    ws0 = wb.add_sheet('Worksheet')
    ws0.write(0, 0, "something", normal_style)
    wb.save(response)
    return response

