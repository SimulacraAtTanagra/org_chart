# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 19:00:47 2021

@author: shane
"""

from pydot import Dot, Node, Edge
from src.admin import newest,rehead,colclean
import pandas as pd


def get_reports(df):
    #[df.dept_descr_job=='Human Resources'][df.comp_freq_job_id=='A']
    df=df[df.hr_status=='Active'][['empl_id','person_nm','hr_status','reports_to_emplid','dept_descr_job']]
    firstlist=list(df[['empl_id','person_nm']].itertuples(index=False,name=None))
    secondlist=list(df[['empl_id','reports_to_emplid']].itertuples(index=False,name=None))
    deptlist=list(df[['empl_id','dept_descr_job']].itertuples(index=False,name=None))
    deptdict={i[0]:i[1] for i in deptlist}
    firstdict={i[0]:i[1] for i in firstlist}
    final=[]
    for i,o in secondlist:
        try:
            final.append((firstdict[i],firstdict[o]))
        except:
            print(i)
    return(final,deptdict)
    
def leveler(df):
    thislist,deptlist=get_reports(df)
    newdict={"Berenecea Johnson-Eanes":1}
    newdict.update({x[0]:0 for x in thislist})
    while True:
        if len([value for value in newdict.values() if value==0])==0:
            break
        for person in newdict.keys():
            if newdict[person]==0:
                try:
                    if newdict[[x[1] for x in thislist if x[0]==person][0]]==0:
                        pass
                    else:
                        newnum=newdict[[x[1] for x in thislist if x[0]==person][0]]+1
                        newdict.update({person:newnum})
                except:
                    print(f'{person} not found')
            else:
                pass
    for i in range(max([value for value in newdict.values()])):    
        graph=Dot(graph_type='graph',ratio='.3',size=150,dpi = 150,splines='ortho')
        #graph.set_node_defaults(style="filled", fillcolor="grey")
        graph.set_edge_defaults(color="blue", arrowhead="vee", weight="1")
        for report_to,report in thislist:
            try:
                if newdict[report_to] in [i,i+1,i+2] or newdict[report] in [i,i+1,i+2]:
                    graph.add_edge(Edge(report,report_to))
            except:
                print(report_to,report)
        #graph.write("c:\\users\\shane\\desktop\\out.dot")
        graph.write_png(f"c:\\users\\shane\\desktop\\orgcharts\\level{i}.png")

def indiv_with_sub(df,outfolder):
    thislist,deptlist=get_reports(df)
    for x in list(set([i[1] for i in thislist])):
        graph=Dot(graph_type='graph',ratio='auto',size=150,dpi = 150,splines='ortho')
        #people who report to x
        reports=[y for y in thislist if y[1]==x]
        #and the people they report to
        reports2=[y for y in thislist if y[1] in [z[0] for z in reports]]
        reporting=reports+reports2
        reporting=list(set(reporting))
        for report_to,report in reporting:
            graph.add_edge(Edge(report,report_to))
        print(f"Now writing file for {x}")
        graph.write_png(f"{outfolder}\\{x}.png")
            
if __name__=="__main__":
    path="c:\\users\\shane\\downloads"
    fname="FULL_FILE"
    df=colclean(pd.read_excel(newest(path,fname)))
    outfolder='c:\\users\\shane\\desktop\\orgcharts'
    indiv_with_sub(df,outfolder)