from flask import Flask,render_template,request
from waitress import serve
import pandas as pd
import pyodbc
import io 
import matplotlib.pyplot as plt
import base64


def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
   return render_template('result.html')


@app.route('/process',methods=['POST'])
def process():
    user_input=request.form['user_input']
    
  
    f= "select ccal from  bdrie.dbo.cobranza_universo where cnudoci='"+user_input+"' "
    sql_con = pyodbc.connect('driver={SQL Server};SERVER=OF00SRVBDH;Trusted_Connection=True;DATABASE=MIS1')
    query = f
    print(query)
    base  = pd.read_sql(query, sql_con)
    print(base.head())
    respuesta=base['ccal'].values
    
    f2="select mes,sum(deuda) as deuda\
    from bdrie.dbo.rcc_cobranza\
    where cnudoci='"+user_input+"'\
    group by mes "
    
    base2  = pd.read_sql(f2, sql_con)

    graph1_url = build_graph(base2['mes'],base2['deuda']);
        
    return render_template('result.html',user_input=respuesta,graph1=graph1_url,\
                           cliente=user_input)


if __name__ == "__main__":
 #app.run()
 #app.run(debug = False)
 serve(app, host='0.0.0.0', port=5000)


