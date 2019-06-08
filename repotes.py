
from flask import Flask,render_template,request
from waitress import serve
import pandas as pd
import pyodbc
from cStringIO import StringIO
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)


@app.route('/',methods = ['POST', 'GET'])
def index():
   return render_template('result.html')


@app.route('/process',methods=['POST'])
def process():
    user_input=request.form['user_input']
    
    
#10270891     
    
    f= "select ccal from  bdrie.dbo.cobranza_universo where cnudoci='"+user_input+"' "
    sql_con = pyodbc.connect('driver={SQL Server};SERVER=OF00SRVBDH;Trusted_Connection=True;DATABASE=MIS1')
    query = f
    print(query)
    base  = pd.read_sql(query, sql_con)
    print(base.head())
    respuesta=base['ccal'].values
    
    f2="select mes,sum(deuda) as deuda\
    from bdrie.dbo.rcc_cobranza\
    where cnudoci='42219420'\
    group by mes "
    
    base2  = pd.read_sql(f2, sql_con)

    fig = plt.figure()
    base2.plot()
    io = StringIO()
    fig.savefig(io, format='png')
    data = base64.encodestring(io.getvalue())
    
    
    return render_template('result.html',user_input=respuesta,data=data)



if __name__ == "__main__":
 #app.run()
 #app.run(debug = False)
 serve(app, host='0.0.0.0', port=5000)
