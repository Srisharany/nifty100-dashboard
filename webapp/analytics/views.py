from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from .models import Company, ProfitLoss, BalanceSheet, CashFlow, Analysis
from .serializers import (
    CompanySerializer,
    ProfitLossSerializer,
    BalanceSheetSerializer,
    CashFlowSerializer
)


class CompanyAPI(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ProfitLossAPI(generics.ListAPIView):
    serializer_class = ProfitLossSerializer

    def get_queryset(self):
        return ProfitLoss.objects.filter(company_id=self.kwargs['symbol'])


class BalanceSheetAPI(generics.ListAPIView):
    serializer_class = BalanceSheetSerializer

    def get_queryset(self):
        return BalanceSheet.objects.filter(company_id=self.kwargs['symbol'])


class CashFlowAPI(generics.ListAPIView):
    serializer_class = CashFlowSerializer

    def get_queryset(self):
        return CashFlow.objects.filter(company_id=self.kwargs['symbol'])


def home(request):
    return render(request, 'analytics/home.html')


def company_list(request):
    query = request.GET.get('q')

    companies = Company.objects.all().order_by('company_name')

    if query:
        companies = companies.filter(company_name__icontains=query)

    return render(request, 'analytics/company_list.html', {
        'companies': companies,
        'query': query
    })


def company_detail(request, symbol):
    company = get_object_or_404(Company, symbol=symbol)

    profits = ProfitLoss.objects.filter(company_id=symbol).order_by('year')
    balances = BalanceSheet.objects.filter(company_id=symbol).order_by('year')
    cashflows = CashFlow.objects.filter(company_id=symbol).order_by('year')

    analysis_rows = Analysis.objects.filter(company_id=symbol)

    roe_data = analysis_rows.filter(roe__icontains='Last Year').first()
    sales_growth = analysis_rows.first()
    stock_cagr = analysis_rows.first()

    years = [p.year for p in profits]
    sales = [float(p.sales or 0) for p in profits]
    net_profit = [float(p.net_profit or 0) for p in profits]

    return render(request, 'analytics/company_detail.html', {
        'company': company,
        'profits': profits,
        'balances': balances,
        'cashflows': cashflows,
        'roe_data': roe_data,
        'sales_growth': sales_growth,
        'stock_cagr': stock_cagr,
        'years': years,
        'sales': sales,
        'net_profit': net_profit
    })