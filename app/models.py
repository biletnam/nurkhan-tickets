from app import db
from sqlalchemy.sql import func


event_has_customer = db.Table(
    'event_has_customer', db.Base.metadata,
    db.Column('event_id'), db.Integer, db.ForeignKey('events.id'),
    db.Column('customer_id'), db.Integer, db.ForeignKey('customers.id'))


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    phone = db.Column(db.String(20), index=True)
    name = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True)

    events = db.relationship('Event',
                             secondary=event_has_customer,
                             back_populates='customers')

    def serialize(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'email': self.email,
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_serialized(cls):
        return [event.serialize for event in cls.query.all()]

    @classmethod
    def add_customer(cls, phone, name, email):
        customer = Customer()
        customer.phone = phone
        customer.name = name
        customer.email = email
        db.session.add(customer)
        db.session.commit()


class Event(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.Text, index=True)
    url = db.Column(db.String(128), index=True)

    customers = db.relationship('Customer',
                                secondary=event_has_customer,
                                back_populates='events')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_serialized(cls):
        return [event.serialize for event in cls.query.all()]

    @classmethod
    def get_by_url(cls, url):
        return cls.query.filter(cls.url == url).first()

    @classmethod
    def add_event(cls, name, description):
        event = Event()
        event.name = name
        event.description = description
        db.session.add(event)
        db.session.commit()
