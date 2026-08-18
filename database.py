from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./inventario.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PuntoAcopio(Base):
    __tablename__ = "puntos_acopio"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(200))
    responsable = Column(String(100))
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)

    inventarios = relationship("InventarioPunto", back_populates="punto")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(30), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50))
    unidad_medida = Column(String(20))
    requiere_vencimiento = Column(Boolean, default=False)

    inventarios = relationship("InventarioPunto", back_populates="producto")

class InventarioPunto(Base):
    __tablename__ = "inventarios_punto"

    id = Column(Integer, primary_key=True, index=True)
    punto_id = Column(Integer, ForeignKey("puntos_acopio.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    
    cantidad_actual = Column(Float, default=0.0)
    stock_minimo = Column(Float, default=10.0)
    stock_maximo = Column(Float, default=100.0)

    punto = relationship("PuntoAcopio", back_populates="inventarios")
    producto = relationship("Producto", back_populates="inventarios")

def init_db():
    Base.metadata.create_all(bind=engine)
    print("¡Base de datos local iniciada correctamente!")

if __name__ == "__main__":
    init_db()
