import pymysql

def get_conn():
    return pymysql.connect(
        host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
        db='predimmo',
        user='admin',
        password='N8XR3u#m9[5Mk6UK',
        port=3306)

def create_query_search(formSearch):
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
                                    