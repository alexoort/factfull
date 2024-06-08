from app import create_app

app = create_app()
app.config['DEBUG'] = True

if __name__ == '__main__':
    print("Running the app...")
    app.run(debug=True)
    



