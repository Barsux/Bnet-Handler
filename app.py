from ALCU import app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port="9579",debug = True ,ssl_context=('cerr.crt','private.key'))
