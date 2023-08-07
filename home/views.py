from django.shortcuts import render,redirect
from .forms import loginForm,signupForm
from django.contrib.auth import authenticate,login,logout

import pickle
import pandas as pd
import numpy as np

from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

from .models import User,Product,Billing,fpRecord,Fp,associationRecord,association

from rich import print

# Create your views here.
def model(data):
    values=data
    pro = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
           ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
           ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]
    
    # values=pro
       
    with open('fpgrowth-model.pkl', 'rb') as f:
        fp_model = pickle.load(f)
        
    transaction = values 
    
    te = TransactionEncoder()
    te_ary = te.fit(values).transform(values)
    
    dataset = pd.DataFrame(te_ary, columns=te.columns_)
     
    recommendations = fpgrowth(dataset, min_support=0.6, use_colnames=True)
     
    obj=fpRecord()
    # obj.save()
    lastRecord=fpRecord.objects.all().last()
    
    for i  in recommendations.index:
        support=recommendations.iloc[i]['support']
        str=pickle.dumps(recommendations.iloc[i]['itemsets'])
        
        object=Fp(support=support,itemsets=str,key_id=lastRecord.id)
        # object.save()
   
    # Create a dictionary to store itemsets and their related items

    # res=set()
    # d=[]
    # for i  in recommendations.index:
    #     # print(recommendations.iloc[i]['itemsets'])  
    #     y=list(recommendations.iloc[i]['itemsets'])
    #     if len(y)>1:
    #         for j in y:
    #         #    res.add(j)
    #             pass    
    #         print(y)
               
               
    recommendations = association_rules(recommendations, metric='lift', min_threshold=1)
    recommendationns = recommendations.sort_values('confidence', ascending=False)
    print(recommendationns.to_string())
    
    associationObj=associationRecord(fpKey_id=lastRecord.id)
    # associationObj.save()
    
    last=associationRecord.objects.all().last()
    
    for i  in recommendationns.index:
        support=recommendations.iloc[i]['support']
        confidence=recommendations.iloc[i]['confidence']
        lift=recommendations.iloc[i]['lift']
        antecedents=pickle.dumps(recommendations.iloc[i]['antecedents'])
        consequents=pickle.dumps(recommendations.iloc[i]['consequents'])
        
        instance=association(antecedents=antecedents,consequents=consequents,support=support,confidence=confidence,lift=lift,key_id=last.id)
        # instance.save()
        
        
        
def home(request):
    return render(request,'home.html')


def auth_login(request):
    form=loginForm(request.POST or None)
    msg=None
    if request.method=='POST':
        if form.is_valid():
            
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            
            if user is not None:
                
                login(request,user)
                return redirect('home')
            else:
                msg="invalid credentials"
        else:
            msg="ERROR  validating form"

        
    return render(request,'login.html',{"form":form,"msg":msg})

def signup(request):
    
    msg=None
    if request.method =='POST':
        form=signupForm(request.POST)
        
        if form.is_valid():
            
            user=form.save()
            msg="user created"
            return redirect('login')
        else:
            msg="form is not valid"
    else:
        form=signupForm()
    
    return render(request,'signup.html',{"form":form,"msg":msg})

def logout_request(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    record=fpRecord.objects.all().last()
    data=Fp.objects.filter(key_id=record.id)
    itemsets=[]
    support=[]
    
    for i in data:
        unpickle=pickle.loads(i.itemsets)
        temp=[]
        for a in unpickle:
            temp.append(a)    
        itemsets.append(temp)    
        support.append(i.support) 
       
    info=zip(itemsets,support)  
    
    asso=associationRecord.objects.get(fpKey_id=record.id)
    
    associationData=association.objects.filter(key_id=asso.id)
    antecedents=[]
    consequents=[]
    
    for c in associationData:
        antecedentsUnpickle=pickle.loads(c.antecedents)
        consequentsUnpickle=pickle.loads(c.consequents)
        temp=[]
        for a in antecedentsUnpickle:
            temp.append(a)    
        antecedents.append(temp)
        temp2=[]
        for a in consequentsUnpickle:
            temp2.append(a)    
        consequents.append(temp2)
        
        table2=zip(antecedents,consequents,associationData)
        
    

       
      
    return render(request,'dashboard.html',{"info":info,"table2":table2})

def runModel(request):
    bills=Billing.objects.all()
    list=[]
     
    for bill in bills:
        str=bill.bill
        unpickle=pickle.loads(str)
        list.append(unpickle)   
    model(list)     
    return redirect('dashboard')

def bills(list):
    bill=list 
    
    str=pickle.dumps(bill)
    
    obj=Billing(bill=str)
    obj.save()
    
    
    

def product(request):
    productList=Product.objects.all()
    list=[]
    
    if request.method=="POST":
        for product in productList:
            pro=request.POST.get(product.productName)
            if pro:
                list.append(pro)
            
        
        bills(list)
        
    return render(request,'product.html',{"productList":productList})