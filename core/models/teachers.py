from core import db
from core.libs import helpers, assertions
from core.models.principals import Principal

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.Sequence('teachers_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Teacher %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)
    
    # @classmethod
    # def get_by_id(cls, _id):
    #     return cls.filter(cls.id == _id).first()
    
    @classmethod
    def get_teachers_by_principal(cls, principal_id):
        principal = Principal.get_by_id(principal_id)
        assertions.assert_valid(principal, 'No Principal with this id was found')
        return cls.filter().all()