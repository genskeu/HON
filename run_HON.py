from HON import create_app

#start app
if __name__ == '__main__':
    #call the run method
    app = create_app()
    app.run(host="0.0.0.0")