#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Filnamn: portfolioserver.py
## 2012-10-22 Per Jonsson & Linda Jansson
## IP1, Linköpings universitet
## Kurs: TDP003 (Anders Fröberg) ##

"""
-------------PRESENTATIONSLAGER-----------------------------------
Samverkar med data.py (datalagret)
----------------------------------------------------------------
"""
## IMPORTERA
import data
from flask import Flask, request, url_for, abort, redirect, render_template

## VARIABLER
app = Flask(__name__)
app.debug=True # för felsökningssyfte

## FUNKTIONER
def data_load():
    """ Anropas varhelst vi vill komma åt databasen (inte enbart en gång) """
    # Skickar användaren till felmeddelande
    if data.load("data.json") == None: abort(400)
    # Om det inte strular
    return data.load("data.json")

## URL:er
@app.route('/')
def start_page():
    """ Laddar startsidan """
    return render_template("index.html", db = data_load())

@app.route("/list/")
def list_projects():
    """ Sidan där vi listar projekten översiktligt """
    db = data_load()
    return render_template("list_projects.html", db = db)#, project_count = data.get_project_count(db))

@app.route("/projects/<project_no>")
def show_project(project_no):
    """ Laddar sidan med detaljerad projektvy """
    db = data_load()
    # Kolla så att vi får ett heltal
    try:
        int(project_no)
    # Skicka tillbaka användaren
    except Exception:
        #return redirect(url_for('start_page'))
        return render_template('404.html', e="404"), 404
    # Kolla att det sökta projektet finns
    if data.get_project(db, int(project_no)) == None:
        # Finns inte, skicka till 404
        #return redirect(url_for('start_page'))
        return render_template('404.html', e="404"), 404
    # Hittat projektet
    return render_template("projects.html", project = data.get_project(db, int(project_no)), db = db)


@app.route("/techniques/")
def techniques():
    """ Sidan som listar tekniker """
    db = data_load()
    return render_template("techniques.html", techniques = data.get_techniques(db), db = db)

@app.route("/techniques/<t>")
def techniques_show(t):
    """ Listar projekt med specifik teknik """
    db = data_load()
    # Kolla statistik
    stats = data.get_technique_stats(db)
    # Kolla om den sökta tekniken finns i databasen
    if not t in stats:
        # Den fanns inte, skicka till 404
        return render_template('404.html', e="404")
    # Ladda teknikvy-sidan
    return render_template("techniques_show.html", namn = t, techniques = data.get_techniques(db),
                            db = db,
                            stats = stats[t],
                            id = [data.get_project(db, x) for x in range (len(db))])

@app.route("/search/")
def search():
    """ Söksidan"""
    db = data_load()
    return render_template("search.html", techniques = data.get_techniques(db),
                            tlen = len(data.get_techniques(db)))

@app.route("/search/results", methods=['POST'])
def search_results():
    """ Visa sökresultat """
    db = data_load()
    # Fånga input från användaren
    search_string = request.form['key']
    search_fields = request.form.getlist("search_fields")
    if search_fields == []: search_fields = None # konvertera så att datalagret förstår
    sort_order = request.form['sort_order']
    sort_by = request.form['sort_by']
    techs = request.form.getlist("techniques")
    # Sammanfatta och sök m.h.a. data.py
    search_res = data.search(db, search=search_string, sort_order = sort_order,
                             sort_by = sort_by,techniques = techs,
                             search_fields = search_fields)
    return render_template("search_results.html", search_res = search_res, db = db, search = search_string)

@app.route("/per/")
def per():
    return render_template("per.html")

@app.route("/cv/")
def cv():
    return render_template("cv.html")

@app.route("/kontakt/")
def kontakt():
    return render_template("kontakt.html")

## FELHANTERING
@app.errorhandler(400)
def no_data(e):
    """ Ingen data i databasen """
    return render_template('data_error.html'), 400

@app.errorhandler(404)
def page_not_found(e):
    """ Fel URL """
    return render_template('404.html', e=e), 404

@app.errorhandler(405)
def not_allowed(e):
    """ The method GET is not allowed for the requested URL. """
    return render_template('405.html', e=e), 405

@app.errorhandler(418)
def teapot(e):
    """ I am a teapot"""
    return render_template('418.html', e=e), 418

@app.errorhandler(500)
def internal_error(e):
    """ Serverfel  """
    return render_template('500.html', e=e), 500

## KÖR ##
if __name__=="__main__":
    app.run()
