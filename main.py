from flask import request, jsonify, render_template
from app import app
from clients_service import get_all_clients, add_client, update_client, delete_client
from couriers_service import get_all_couriers, add_courier, update_courier, delete_courier
from routes_service import (
    get_all_routes, add_route, update_route, delete_route,
    get_locations, add_location, update_location, delete_location
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        return jsonify(add_client(request.json))
    return jsonify(get_all_clients())

@app.route('/api/clients/<int:clientID>', methods=['PUT', 'DELETE'])
def client_detail(clientID):
    if request.method == 'PUT':
        return jsonify(update_client(clientID, request.json))
    return jsonify(delete_client(clientID))

@app.route('/api/couriers', methods=['GET', 'POST'])
def couriers():
    if request.method == 'POST':
        return jsonify(add_courier(request.json))
    return jsonify(get_all_couriers())

@app.route('/api/couriers/<int:courierID>', methods=['PUT', 'DELETE'])
def courier_detail(courierID):
    if request.method == 'PUT':
        return jsonify(update_courier(courierID, request.json))
    return jsonify(delete_courier(courierID))

@app.route('/api/routes', methods=['GET', 'POST'])
def routes():
    if request.method == 'POST':
        return jsonify(add_route(request.json))
    return jsonify(get_all_routes())

@app.route('/api/routes/<int:routeID>', methods=['PUT', 'DELETE'])
def route_detail(routeID):
    if request.method == 'PUT':
        return jsonify(update_route(routeID, request.json))
    return jsonify(delete_route(routeID))

@app.route('/api/routes/<int:routeID>/locations', methods=['GET', 'POST'])
def route_locations(routeID):
    if request.method == 'POST':
        return jsonify(add_location(routeID, request.json))
    locs = get_locations(routeID)
    if isinstance(locs, dict):
        return jsonify(locs), 404
    return jsonify(locs)

@app.route('/api/routes/<int:routeID>/locations/<int:locationID>', methods=['PUT', 'DELETE'])
def route_location_detail(routeID, locationID):
    if request.method == 'PUT':
        return jsonify(update_location(routeID, locationID, request.json))
    return jsonify(delete_location(routeID, locationID))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
