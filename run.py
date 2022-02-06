from salt import create_app
import os

app = create_app()

#check and run
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 6000))