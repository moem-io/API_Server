from  my_server.app import app

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000)
    app.run(port=5000, debug=True)