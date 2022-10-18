from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import imageio as iio
import datetime
dt=datetime.datetime.now()
dp = pickle.load(open('dpprod.pkl','rb'))

data=pd.read_csv('prod_.csv')

app = Flask(__name__,template_folder='Template')

@app.route('/', methods=['GET','POST'])
def man():
    product=sorted(data['product'].unique())
    return render_template('aac.html',product = product)

k=data['product'].unique().tolist()
p=0
q=36
e=[]
for i in range(0,6):
    s=data.iloc[p:q,[2]]
    e.append(float(s['expiri duretion in years'].unique()))
    p=q
    q=q+41
print(e[0]-int(e[0]))
@app.route('/predict',methods=['POST'])
def prediction():
    d1= request.form['product']
    d2= dt.year
    d3= request.form['month']
    d4= request.form['prodleft']
    arr= np.array([[d1, d2, d3]])
    print(d1)
    pred= dp.predict(arr)

    d4=np.array(d4).astype(int)
    l2=np.array(d2).astype(int)
    l3=np.array(d3).astype(int)
    pred=pred-d4
    for i in range(0,6):
        if k[i]==str(d1):
            flot_month=e[i]-int(e[i])
            exp_month=l3+flot_month*10
            if exp_month > 12:
                exp_month=l3+flot_month*10-12
                exp_year=int(e[i]+int(l2)+1)
            elif exp_month==12:
                exp_month=1
                exp_year= int(e[i]+l2+1)  
            else:
                exp_month=l3+flot_month*10
                exp_year=int(e[i]+l2)
    if (dt.month>exp_month):
        months_left=12-dt.month+int(exp_month)
        years_left=exp_year-dt.year-1
    elif(dt.month==exp_month):
        months_left=0
        years_left=exp_year-dt.year
    else:
        years_left=exp_year-dt.year
        months_left=int(exp_month)-dt.month

    return render_template('after.html',data=int(pred),d = d1,d2= d2,d3= d3,prodleft= d4, exp_year=exp_year,exp_month= int(exp_month),years_left=years_left,months_left=months_left)
        
if __name__ == '__main__':
    app.run(debug=True)