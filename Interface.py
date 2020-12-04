#!/usr/bin/env python
# coding: utf-8

# In[13]:


import rdflib
import rdflib.plugins.sparql as sparql
import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import webbrowser
#This Scrollable class reference to https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame 
class Scrollable(tk.Frame):

    def __init__(self, frame, width=800):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set, background='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        tk.Frame.__init__(self, frame)         

        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)        

    def update(self):
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
        
def callback(url):
    webbrowser.open_new(url)

def search(id):
    for widget in scrollable_body.winfo_children():
        widget.destroy()
    try:
        val = int(id)
        OTO = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/untitled-ontology-45#")
        XMLNS = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/ser531#")
        PRO = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/ser531#")
        XSD = rdflib.URIRef("http://www.w3.org/2001/XMLSchema#")
        RDF = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        q = sparql.prepareQuery(
            'SELECT ?a ?title ?content ?topic WHERE { ?a xmlns:hasID ?v . ?a oto:hasTitle ?label . ?label xmlns:TitleContent ?title . ?a oto:hasBody ?body . ?body rdfs:label ?content. ?a pro:hasTopic ?topic}', 
            initNs = {"oto":OTO, "xmlns": XMLNS,"xsd":XSD,"pro":PRO})
        g = rdflib.Graph()
        g.parse("Coffee.owl")
        v = rdflib.term.Literal(id)
        qres = g.query(q,initBindings = {'v' : v})
        
        topic = ''
        if len(qres) == 0:
            error_label = tk.Label(scrollable_body,background='white',width=800)
            error_label.configure(text='There is no this id. Please enter another one')
            error_label.pack()
            
        for row in qres:           
            result_label = tk.Label(scrollable_body,fg='blue',cursor='hand2',background='white')
            result_label.configure(text=row[1])
            url1 = "https://coffee.meta.stackexchange.com/questions/" + id + "/" + row[1]
            result_label.bind("<Button-1>", lambda e: callback(url1))
            result_label.pack()
            topic = row[3]
            contentLabel = tk.Label(scrollable_body,width=800,wraplength=800,justify='left',background='white')
            contentLabel.configure(text=row[2])
            contentLabel.pack()
            
        q = sparql.prepareQuery(
            'SELECT ?id ?title ?content WHERE { ?a pro:hasTopic ?v. ?a xmlns:hasID ?id FILTER(?id != ?oid). ?a oto:hasTitle ?label . ?label xmlns:TitleContent ?title . ?a oto:hasBody ?body . ?body rdfs:label ?content}', 
            initNs = {"oto":OTO, "xmlns": XMLNS,"xsd":XSD,"pro":PRO})
        g = rdflib.Graph()
        g.parse("Coffee.owl")
        oid = rdflib.term.Literal(id)
        qres = g.query(q,initBindings = {'v' : topic, 'oid' : oid})
        index = 1
        for i in qres:
            blank = tk.Label(scrollable_body,background='white',width=800)
            blank.pack()
            url = "https://coffee.meta.stackexchange.com/questions/" + i[0] + "/" + i[1]
            newB = tk.Button(scrollable_body, text="Recommand "+ str(index)+" url", command=lambda x=url: callback(x))
            newB.pack()
            resultlabel = tk.Label(scrollable_body,background='white',width=800)
            resultlabel.configure(text='Recommand' + str(index))
            resultlabel.pack()
            result1 = tk.Label(scrollable_body,background='white',width=800)
            result1.configure(text=i[1])
            result1.pack()
            contentLabel = tk.Label(scrollable_body,width=800,wraplength=800,justify='left',background='white')
            contentLabel.configure(text=i[2])
            contentLabel.pack()
            index += 1
        scrollable_body.update()
    except ValueError:
        print("value error")
        
def searchK(s):
    for widget in scrollable_body.winfo_children():
        widget.destroy()
    try:
        OTO = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/untitled-ontology-45#")
        XMLNS = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/ser531#")
        PRO = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/ser531#")
        XSD = rdflib.URIRef("http://www.w3.org/2001/XMLSchema#")
        RDF = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        q = sparql.prepareQuery(
            'SELECT ?id ?title WHERE { ?t rdf:type pro:Keyword. ?t rdfs:label ?v. ?topic pro:hasKeyword ?t. ?document pro:hasTopic ?topic. ?document pro:hasID ?id . ?document oto:hasTitle ?label . ?label xmlns:TitleContent ?title .}', 
            initNs = {"oto":OTO, "xmlns": XMLNS,"xsd":XSD,"pro":PRO})
        g = rdflib.Graph()
        g.parse("Coffee.owl")
        h = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/ser531#OWLNamedIndividual_0fa8cf3f_ab95_4e68_a468_b9424c4249d8")
        v = rdflib.term.Literal(s)
        qres = g.query(q,initBindings = {'v' : v})
        

        for row in qres:  
            newB = tk.Button(scrollable_body, text=row[1], command=lambda x=row[0]: search(x))
            newB.pack()
        scrollable_body.update()
    except ValueError:
        print("value error")

win = tk.Tk()
win.title('Ser531 Project')
win.geometry('800x800')
win.configure(background='white')


search_panel = tk.Frame(win)
search_panel.pack(side=tk.TOP)
search_label = tk.Label(search_panel, text='ID',background='white')
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(search_panel)
search_entry.pack(side=tk.LEFT)

search_btn = tk.Button(win, text='search by id', command= lambda: search(search_entry.get()))
search_btn.pack()

search_label = tk.Label(win, text='Or',background='white')
search_label.pack(side=tk.TOP)

search_key_panel = tk.Frame(win)
search_key_panel.pack(side=tk.TOP)
search_key_label = tk.Label(search_key_panel, text='Key',background='white')
search_key_label.pack(side=tk.LEFT)
OTO = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/untitled-ontology-45#")
XMLNS = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/ser531#")
PRO = rdflib.URIRef("http://www.semanticweb.org/marcushsu/ontologies/2020/10/ser531#")
XSD = rdflib.URIRef("http://www.w3.org/2001/XMLSchema#")
RDF = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
q = sparql.prepareQuery(
    'SELECT ?keyword WHERE { ?a rdf:type pro:Keyword . ?a rdfs:label ?keyword}', 
    initNs = {"oto":OTO, "xmlns": XMLNS,"xsd":XSD,"pro":PRO})
g = rdflib.Graph()
g.parse("Coffee.owl")

qres = g.query(q)

key_value=[]
for row in qres:
    key_value.append(row[0])

            
combo = ttk.Combobox(win,value=key_value)
combo.pack()

search_key_btn = tk.Button(win, text='search by key', command= lambda: searchK(combo.get()))
search_key_btn.pack()


scrollable_body = Scrollable(win, width = 15)
scrollable_body.update()
win.mainloop()
   


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




