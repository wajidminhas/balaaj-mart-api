

from sqlmodel import Session, select
from app.product_db.model import Product
from app.product_db.schema import ProductCreate, ProductUpdate

def create_product(session: Session, product_create: ProductCreate) -> Product:
    product = Product.obj.model(product_create)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_product(session: Session, product_id: int) -> Product:
    return session.get(Product, product_id)

def get_products(session: Session) -> list[Product]:
    statement = select(Product)
    return session.exec(statement).all()

def update_product(session: Session, product_id: int, product_update: ProductUpdate) -> Product:
    product = session.get(Product, product_id)
    if not product:
        return None
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)
    session.commit()
    session.refresh(product)
    return product

def delete_product(session: Session, product_id: int) -> Product:
    product = session.get(Product, product_id)
    if not product:
        return None
    session.delete(product)
    session.commit()
    return product
