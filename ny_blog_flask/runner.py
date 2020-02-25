from app import app, db

if __name__ == '__main__':
    db.create_all()
    print('app run')
    app.run(host='localhost', port=5000, debug=True, use_reloader=False)
