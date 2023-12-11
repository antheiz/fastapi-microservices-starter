from app.models.users import User
from app.models.customers import Customer
from sqlalchemy.orm import Session


def create_customer(session: Session, user_obj: User):
    if not user_obj.is_superuser:
        customer = Customer(user_id=user_obj.user_id, email=user_obj.email)
        session.add(customer)
        session.commit()
