from app import create_app
import os
app = create_app()

#start app
if __name__ == '__main__':
    #port = int(os.environ.get('PORT',5000))
    #call the run method
    app.run()