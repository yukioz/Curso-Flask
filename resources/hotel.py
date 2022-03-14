from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):

    # Compressão de lista python
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left empty.")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left empty.")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return hotel.json()

        return {'message': 'Hotel not found.'}, 404 # Not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 # bad request

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id,  **dados)

        # try catch
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500 # Internal server error

        return hotel.json()

        # hoteis.append(novo_hotel)
        # return novo_hotel, 200


    def put(self, hotel_id):

        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        
        # O **dados contem (nome, cidade, estrelas e diária), e o metodo receberá essas valores.
        hotel = HotelModel(hotel_id,  **dados)

        hotel.save_hotel()
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:

            try:
                hotel.delete_hotel()
            except:
                return {"message": "An internal error ocurred trying to delete hotel."}, 500 # Internal server error
            return {"message": 'Hotel deleted.'}
        
        return {'message': 'Hotel not found.'}, 404