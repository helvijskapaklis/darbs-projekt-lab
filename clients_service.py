from app import db, Clients, Routes

def get_all_clients():
    results = []
    clients = Clients.query.all()
    for c in clients:
        route = Routes.query.filter_by(clientID=c.clientID).first()
        route_id = route.routeID if route else None
        results.append({
            'clientID': c.clientID,
            'name': c.name,
            'surname': c.surname,
            'email': c.email,
            'phoneNumber': c.phoneNumber,
            'routeID': route_id
        })
    return results

def add_client(data):
    e = Clients.query.filter_by(email=data['email']).first()
    if e:
        return {'message': 'Šāds e-pasts jau eksistē'}, 400
    p = Clients.query.filter_by(phoneNumber=data['phoneNumber']).first()
    if p:
        return {'message': 'Šāds telefona numurs jau eksistē'}, 400

    new_c = Clients(
        name=data['name'],
        surname=data['surname'],
        email=data['email'],
        phoneNumber=data['phoneNumber']
    )
    db.session.add(new_c)
    db.session.commit()
    return {'message': 'Klients pievienots', 'clientID': new_c.clientID}

def update_client(clientID, data):
    c = Clients.query.get(clientID)
    if not c:
        return {'message': 'Klients nav atrasts'}, 404

    if 'name' in data:
        c.name = data['name']
    if 'surname' in data:
        c.surname = data['surname']
    if 'email' in data and data['email'] != c.email:
        e2 = Clients.query.filter_by(email=data['email']).first()
        if e2:
            return {'message': 'Šāds e-pasts jau tiek izmantots'}, 400
        c.email = data['email']
    if 'phoneNumber' in data and data['phoneNumber'] != c.phoneNumber:
        p2 = Clients.query.filter_by(phoneNumber=data['phoneNumber']).first()
        if p2:
            return {'message': 'Šāds telefona numurs jau tiek izmantots'}, 400
        c.phoneNumber = data['phoneNumber']

    db.session.commit()
    return {'message': 'Klienta dati atjaunoti'}

def delete_client(clientID):
    c = Clients.query.get(clientID)
    if not c:
        return {'message': 'Klients nav atrasts'}, 404

    db.session.delete(c)
    db.session.commit()
    return {'message': 'Klients dzēsts'}
