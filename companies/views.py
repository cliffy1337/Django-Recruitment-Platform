from django.shortcuts import render

def company_list(request):
    return render(request, 'companies/company_list.html')