import pymysql

def get_conn():
    """ Get a connection to the RDS database

    Returns:
        pymysql.connect: Connection to the RDS database
    """
    return pymysql.connect(
        host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
        db='predimmo',
        user='admin',
        password='N8XR3u#m9[5Mk6UK',
        port=3306)

def make_request(conn, sql):
    """Execute a SQL request and commit, returning the raw result

    Args:
        conn (pymysql.connect): Connection to the RDS database
        sql (String): Query

    Returns:
        String: result in string
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
    return result

def create_query_search(formSearch):
    """Create a query search for the SearchForm after the user click on the 'submit' button for a search

    Args:
        formSearch (Forms.form): The POST form of the request

    Returns:
        String: SQL statement
    """
    departement = formSearch.cleaned_data['departement']
    price = formSearch.cleaned_data['price']
    type_local = formSearch.cleaned_data['type_local']
    superficie = int(formSearch.cleaned_data['superficie'])
    nb_pieces = int(formSearch.cleaned_data['nb_pieces'])
    price_low = price - 10 / 100 * price
    price_up = price + 10 / 100 * price
    superficie_low = superficie - 10 / 100 * superficie
    superficie_up = superficie + 10 / 100 * superficie
    nb_pieces_low = nb_pieces - 1
    nb_pieces_up = nb_pieces + 1
    # return "select * from data_django WHERE code_postal = " + str(departement) + " limit 5"
    return "SELECT * FROM data_django WHERE valeur_fonciere BETWEEN " + str(price_low) + " AND " + str(price_up) + \
                " AND code_type_local = " + str(type_local) + \
                " AND surface_terrain BETWEEN " + str(superficie_low) + " AND " + str(superficie_up) + \
                " AND nombre_pieces_principales BETWEEN " + str(nb_pieces_low) + " AND " + str(nb_pieces_up) + \
                " AND code_postal = " + str(departement) + \
                " LIMIT 5"
                                    