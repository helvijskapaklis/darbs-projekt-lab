from app import db, Couriers, Routes

def get_all_couriers():
    results = []
    couriers = Couriers.query.all()
    for co in couriers:
        route = Routes.query.filter_by(courierID=co.courierID).first()
        route_id = route.routeID if route else None
        results.append({
            'courierID': co.courierID,
            'name': co.name,
            'surname': co.surname,
            'email': co.email,
            'phoneNumber': co.phoneNumber,
            'routeID': route_id
        })
    return results

def add_courier(data):
    e = Couriers.query.filter_by(email=data['email']).first()
    if e:
        return {'message': 'Šāds e-pasts jau eksistē'}, 400
    p = Couriers.query.filter_by(phoneNumber=data['phoneNumber']).first()
    if p:
        return {'message': 'Šāds telefona numurs jau eksistē'}, 400

    new_co = Couriers(
        name=data['name'],
        surname=data['surname'],
        email=data['email'],
        phoneNumber=data['phoneNumber']
    )
    db.session.add(new_co)
    db.session.commit()
    return {'message': 'Kurjers pievienots', 'courierID': new_co.courierID}

def update_courier(courierID, data):
    co = Couriers.query.get(courierID)
    if not co:
        return {'message': 'Kurjers nav atrasts'}, 404

    if 'name' in data:
        co.name = data['name']
    if 'surname' in data:
        co.surname = data['surname']
    if 'email' in data and data['email'] != co.email:
        e2 = Couriers.query.filter_by(email=data['email']).first()
        if e2:
            return {'message': 'Šāds e-pasts jau tiek izmantots'}, 400
        co.email = data['email']
    if 'phoneNumber' in data and data['phoneNumber'] != co.phoneNumber:
        p2 = Couriers.query.filter_by(phoneNumber=data['phoneNumber']).first()
        if p2:
            return {'message': 'Šāds telefona numurs jau tiek izmantots'}, 400
        co.phoneNumber = data['phoneNumber']

    db.session.commit()
    return {'message': 'Kurjera dati atjaunoti'}

def delete_courier(courierID):
    co = Couriers.query.get(courierID)
    if not co:
        return {'message': 'Kurjers nav atrasts'}, 404

    db.session.delete(co)
    db.session.commit()
    return {'message': 'Kurjers dzēsts'}
