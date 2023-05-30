from website import create_app #import create_app function to create flask app 

app = create_app() #create app from __init__.py
if __name__ == '__main__': #only if we run this file, it will run (import would not work)
    app.run(debug=True)#make debug work so it is easier to debug during process
