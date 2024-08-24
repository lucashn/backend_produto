from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

PRODUTOS = {
    'p1': {
        'p_id': 'p1',
        'nome': 'Camiseta',
        'quantidade': 10,
        'preco': 29.99
    },
    'p2': {
        'p_id': 'p2',
        'nome': 'Calça',
        'quantidade': 5,
        'preco': 59.99
    },
    'p3': {
        'p_id': 'p3',
        'nome': 'Kit de meias',
        'quantidade': 7,
        'preco': 23.56
    },
}


def abortar_se_nao_existir(p_id):
    if p_id not in PRODUTOS:
        abort(404, message="Produto {} não existe".format(p_id))


parser = reqparse.RequestParser()
parser.add_argument('nome')
parser.add_argument('quantidade')
parser.add_argument('preco')
parser.add_argument('p_id')


def le_produto(args):
    return {
        'nome': args['nome'],
        'quantidade': int(args['quantidade']),
        'preco': float(args['preco'])
    }


class Produto(Resource):
    def get(self, p_id):
        abortar_se_nao_existir(p_id)
        return PRODUTOS[p_id]

    def delete(self, p_id):
        abortar_se_nao_existir(p_id)
        del PRODUTOS[p_id]
        return '', 204

    def put(self, p_id):
        args = parser.parse_args()
        PRODUTOS[p_id] = le_produto(args)
        PRODUTOS[p_id].p_id = p_id
        return PRODUTOS[p_id], 201

class ListaProdutos(Resource):
    def get(self):
        return list(PRODUTOS.values())

    def post(self):
        args = parser.parse_args()
        p_id = int(max(PRODUTOS.keys()).lstrip('p')) + 1
        p_id = f'p{p_id}'
        PRODUTOS[p_id] = le_produto(args)
        PRODUTOS[p_id].p_id = p_id 
        return PRODUTOS[p_id], 201

api.add_resource(ListaProdutos, '/produto')
api.add_resource(Produto, '/produto/<p_id>')

if __name__ == '__main__':
    app.run(debug=True)