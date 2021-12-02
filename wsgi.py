from app import create_app
import os
app = create_app()

#start app
if __name__ == '__main__':
    app.run()