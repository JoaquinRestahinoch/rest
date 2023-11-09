from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import random
from productos import productos
app = Flask(__name__, template_folder='templates')

# Ruta para servir los archivos estáticos generados por Vue (asegúrate de que la carpeta 'static' esté en el mismo directorio que este archivo)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Ruta para servir el archivo index.html de Vue
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# Tus rutas de Flask
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(productos)

@app.route('/api/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    productos.append(new_product)
    return jsonify({'message': 'Producto agregado correctamente'})

@app.route('/api/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def get_update_or_delete_product(product_id):
    if request.method == 'GET':
        if product_id < 0 or product_id >= len(productos):
            return jsonify({'error': 'Producto no encontrado'}), 404
        return jsonify(productos[product_id])
    elif request.method == 'PUT':
        if product_id < 0 or product_id >= len(productos):
            return jsonify({'error': 'Producto no encontrado'}), 404
        updated_data = request.get_json()

        existing_product = productos[product_id]
        existing_product.update(updated_data)

        return jsonify({'message': 'Producto actualizado correctamente'})
    elif request.method == 'DELETE':
        if product_id < 0 or product_id >= len(productos):
            return jsonify({'error': 'Producto no encontrado'}), 404
        del productos[product_id]
        return jsonify({'message': 'Producto eliminado correctamente'})

if __name__ == '__main__':
    app.run(port=8080, debug=True)
