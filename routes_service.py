from app import db, Routes, Clients, Couriers, Locations

def get_all_routes():
    routes = Routes.query.all()
    results = []
    for r in routes:
        cl = Clients.query.get(r.clientID)
        co = Couriers.query.get(r.courierID)
        c_name = f"{cl.name} {cl.surname}" if cl else "???"
        co_name = f"{co.name} {co.surname}" if co else "???"
        results.append({
            'routeID': r.routeID,
            'clientName': c_name,
            'courierName': co_name
        })
    return results

def add_route(data):
    """
    data => { "clientID": X }
    Algoritms:
      1) Pārbaudām, vai klients eksistē
      2) Meklējam brīvu kurjeru (kurš nav iekļauts nevienā maršrutā)
      3) Ja atrasts, izveidojam maršrutu
      4) Ja nav, atgriežam kļūdu
    """
    c = Clients.query.get(data['clientID'])
    if not c:
        return {'message': 'Klients nav atrasts'}, 400

    assigned_couriers = [r.courierID for r in Routes.query.all()]
    free_courier = Couriers.query.filter(~Couriers.courierID.in_(assigned_couriers)).first()
    if not free_courier:
        return {'message': 'Nav brīvu kurjeru'}, 400

    new_r = Routes(clientID=c.clientID, courierID=free_courier.courierID)
    db.session.add(new_r)
    db.session.commit()
    return {
        'message': f'Maršruts izveidots, kurjeris = {free_courier.name} {free_courier.surname}',
        'routeID': new_r.routeID
    }

def update_route(routeID, data):
    rt = Routes.query.get(routeID)
    if not rt:
        return {'message': 'Maršruts nav atrasts'}, 404

    if 'clientID' in data:
        c = Clients.query.get(data['clientID'])
        if not c:
            return {'message': 'Klients nav atrasts'}, 400
        rt.clientID = c.clientID

    if 'courierID' in data:
        co = Couriers.query.get(data['courierID'])
        if not co:
            return {'message': 'Kurjers nav atrasts'}, 400
        rt.courierID = co.courierID

    db.session.commit()
    return {'message': 'Maršruts atjaunots'}

def delete_route(routeID):
    rt = Routes.query.get(routeID)
    if not rt:
        return {'message': 'Maršruts nav atrasts'}, 404

    Locations.query.filter_by(routeID=routeID).delete()
    db.session.delete(rt)
    db.session.commit()
    return {'message': 'Maršruts dzēsts'}

def get_locations(routeID):
    r = Routes.query.get(routeID)
    if not r:
        return {'message': 'Maršruts nav atrasts'}
    locs = Locations.query.filter_by(routeID=routeID).all()
    res = []
    for l in locs:
        res.append({
            'locationID': l.locationID,
            'country': l.country,
            'city': l.city,
            'address': l.address
        })
    return res

def add_location(routeID, data):
    r = Routes.query.get(routeID)
    if not r:
        return {'message': 'Maršruts nav atrasts'}, 404

    new_loc = Locations(
        routeID=routeID,
        country=data['country'],
        city=data['city'],
        address=data['address']
    )
    db.session.add(new_loc)
    db.session.commit()
    return {'message': 'Lokācija pievienota'}

def update_location(routeID, locationID, data):
    loc = Locations.query.filter_by(routeID=routeID, locationID=locationID).first()
    if not loc:
        return {'message': 'Lokācija nav atrasta'}, 404

    if 'country' in data:
        loc.country = data['country']
    if 'city' in data:
        loc.city = data['city']
    if 'address' in data:
        loc.address = data['address']

    db.session.commit()
    return {'message': 'Lokācija atjaunota'}

def delete_location(routeID, locationID):
    loc = Locations.query.filter_by(routeID=routeID, locationID=locationID).first()
    if not loc:
        return {'message': 'Lokācija nav atrasta'}, 404

    db.session.delete(loc)
    db.session.commit()
    return {'message': 'Lokācija dzēsta'}
