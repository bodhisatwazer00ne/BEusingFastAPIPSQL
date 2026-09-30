from fastapi import FastAPI,HTTPException, status, Depends
from models import Product
from database import SessionLocal,engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

products=[
    Product(id="1",name="phone",description="budget phone",price="1000",quantity="10"),
    Product(id="2",name="Laptop",description="Asus",price="10000",quantity="5"),
    Product(id="3",name="Earphones",description="bass boosted",price="100",quantity="15"),
    Product(id="4",name="Watch",description="Smart Watch",price="2000",quantity="40"),
]

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()        


def init_db():
    db = SessionLocal()

    existing_count = db.query(database_models.Product).count()

    if existing_count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
        print("Database initialized with sample products.")
        
    db.close()

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    db_products=db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product  
    return "No product found"

@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    db.refresh(db_product)
    return {"message": "Product created successfully", "product": product}

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "product": db_product}


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
