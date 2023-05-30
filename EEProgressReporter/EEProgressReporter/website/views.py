from flask import Blueprint, render_template, request 
#import for flask app to work
#blueprint: make it nicely organized, can be accessed in different files
#render_template: display template (aka website pages)
#request: fetch variable from html

import process_pdf
#process_pdf programed by me

views = Blueprint('views', __name__)#define blueprint
percentage_overall = 'error'
percent_individual = 'error'
value_presence = 'error'
toc = 'error'
tocroi = 'error'
wordCount = 'error'
wcroi = 'error'
titlePage = 'error'
tproi = 'error'
bibliography = 'error'
broi = 'error'
#set global variable to error to show the user an error has occur 

@views.route('/') #default: direct to home
@views.route('/home')#run when require to go to home page as well
def home():
    return render_template("index.html")#get index html when at home

@views.route('/help')
def help():
    return render_template("help.html")#get help page

@views.route('/uploadFiles', methods=["POST", "GET"])#POST for form 
def uploadFiles():
    return render_template("uploadFiles.html")#get uploadFiles page

@views.route('/loading')
def loading():
    return render_template("loading.html")#display loading

@views.route('/pastReports')
def pastReports():
    return render_template("pastReports.html")#get past Reports page

@views.route('/upload', methods=["POST", "GET"])
def upload():
    global toc, tocroi, wordCount, wcroi, titlePage, tproi, bibliography, broi, percentage_overall, percent_individual, value_presence
    #get global variable
    if request.method == "POST":
        path = request.form.get("file")
        toc = request.form.get("tableOfContent")
        tocroi = request.form.get("tocRateOfImportance")
        wordCount = request.form.get("wordCount")
        wcroi = request.form.get("wcRateOfImportance")
        titlePage = request.form.get("titlePage")
        tproi = request.form.get("tpRateOfImportance")
        bibliography = request.form.get("bibliography")
        broi = request.form.get("bRateOfImportance")
        #get all the variables from html 

        try: 
            #send all the data to process_pdf for process
            percentage_overall, percent_individual, value_presence = process_pdf.the_main(path, toc, tocroi, wordCount, wcroi, titlePage, tproi, bibliography, broi)
            #return percentage_overall, percentage_individual and value_presence and change data of the global variables 
            #order: total_words, toc_presence, titlePage_presence, bibliography_presence
            return render_template('loading.html')
        except:
            return render_template('error.html')#render template for error for error handling and ask the user to go back and check

@views.route('report')
def reports():
    global toc, tocroi, wordCount, wcroi, titlePage, tproi, bibliography, broi, percentage_overall, percent_individual, value_presence
    #get global variable 
    try: 
            return render_template("report.html", 
            want_wordcount = wordCount, word_count_importance = wcroi, vp_wc = value_presence[0],
            want_toc = toc, toc_importance = tocroi, vp_toc = value_presence[1],
            want_titlepage = titlePage, titlepage_importance = tproi, vp_tp = value_presence[2],
            want_bibliography = bibliography, bibliography_importance = broi, vp_b = value_presence[3],
            all = percentage_overall)
            #render template with all variable send to display 
    except:
        return render_template("error.html")
        #render error template for error handling and ask the user to go back and change up settings