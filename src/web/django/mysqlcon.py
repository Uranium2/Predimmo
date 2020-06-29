import pymysql

def get_conn():
    return pymysql.connect(
        host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
        db='predimmo',
        user='admin',
        password='N8XR3u#m9[5Mk6UK',
        port=3306)
