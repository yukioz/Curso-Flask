from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
    'hotel_id': 'alpha',
    'nome': 'Alpha Hotel',
    'estrelas': 4.3,
    'diaria': 420.34,
    'cidade': 'São Paulo'
    },
    {
    'hotel_id': 'bravo',
    'nome': 'Bravo Hotel',
    'estrelas': 4.4,
    'diaria': 320.74,
    'cidade': 'Brasília'
    },
    {
    'hotel_id': 'mont',
    'nome': 'Mont Hotel',
    'estrelas': 3.3,
    'diaria': 334.12,
    'cidade': 'Berlim'
    },
]

class HotelModel:
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self. estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            return hotel

        return {'message': 'Hotel not found.'}, 404 # Not found

    def post(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        novo_objeto = HotelModel(hotel_id,  **dados)
        novo_hotel = novo_objeto.json() # converter para json
        # novo_hotel = { 'hotel_id': hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()

        novo_objeto = HotelModel(hotel_id,  **dados)
        novo_hotel = novo_objeto.json() # converter para json
        # novo_hotel = { 'hotel_id': hotel_id, **dados}

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
        else:
            return {'message': 'Hotel not found.'}, 404
        
        return novo_hotel, 200

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]

        return {'message': 'Hotel deleted.'}