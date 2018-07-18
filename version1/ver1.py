# -*- coding: utf-8 -*-
"""
Created on Wed May 31 17:59:42 2017

@author: UDAY KUMAR
"""
import plotly
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='udayu1111', api_key='Fp3Qsz4JNIEV8R37PD6N')
import lasio

l = lasio.read("sample.las") 

print("------------------------------------------------------------------------------------------")

for curve in l.curves:
    print("%s\t[%s]\t%s\t%s" % (
            curve.mnemonic, curve.unit, curve.value, curve.descr))
print("------------------------------------------------------------------------------------------")
print("No. of attributes :",len(curve.value))
print("------------------------------------------------------------------------------------------")
print("1.DEPT vs AT60")
print("2.DEPT vs AT90")
print("3.DEPT vs GR")
print("4.DEPT vs HCAL")
print("5.DEPT vs HCGR")
print("6.DEPT vs HFK")
print("7.DEPT vs HTHO")
print("8.DEPT vs HURA")
print("9.DEPT vs NPHI")
print("10.DEPT vs PEFZ")
print("11.DEPT vs PHID")
print("12.DEPT vs RHOZ")
print("------------------------------------------------------------------------------------------")

          
trace0 = go.Scatter(
    x=l["AT60"],
    y=l["DEPT"],
    name = 'Resistivity AT60'
)
trace1 = go.Scatter(
    x=l["AT90"],
    y=l["DEPT"],
    name = 'Resistivity AT90'
)
trace2 = go.Scatter(
    x=l["GR"],
    y=l["DEPT"],
    name = 'Gamma Ray',
)

n = int(input("Enter the no. of subplots :"))
fig = tools.make_subplots(rows=1, cols= n , shared_yaxes=True)

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace2, 1, 3)


fig['layout']['xaxis1'].update(title='xaxis 1 title')
fig['layout']['xaxis2'].update(title='Res AT90', type='log')
fig['layout']['xaxis3'].update(title='xaxis 3 title')

fig['layout'].update(height=2000, width=1100,
                     title='Multiple Subplots with Shared DEPTH(Y-Axis)', plot_bgcolor='#d9e6fc', yaxis= dict(autorange="reversed"))
plotly.offline.plot(fig)