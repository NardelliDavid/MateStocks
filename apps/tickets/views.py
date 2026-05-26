#from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return redirect('crud_productos')