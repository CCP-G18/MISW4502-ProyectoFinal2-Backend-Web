import uuid
from app.repositories.product_repository import ProductRepository, Product
from app.exceptions.http_exceptions import BadRequestError
from typing import IO
from app.models.manufacturer_model import Manufacturer
from app.models.category_model import Category
import pandas as pd

REQUIRED_COLUMNS = [
    "Nombre del producto",
    "Descripción",
    "Cantidad inicial",
    "Precio unitario",
    "Nombre del fabricante",
    "Nombre de la categoría"
]

def validate_uuid(id):
  try:
    uuid.UUID(id, version=4)
    return True
  except ValueError:
    return False
    
class ProductService:
    
  @staticmethod
  def get_all():
    products = ProductRepository.get_all()
    
    return products
    
  @staticmethod
  def create(product_data):
    if not product_data.get("name"):
      raise BadRequestError("El nombre es requerido")
    if not product_data.get("description"):
      raise BadRequestError("La descripción es requerida")
    if not product_data.get("unit_amount"):
      raise BadRequestError("El monto es requerido")
    if not product_data.get("quantity"):
      raise BadRequestError("La cantidad es requerida")
    if not product_data.get("image_url"):
      raise BadRequestError("La url de la imagen es requerida")
    if not product_data.get("manufacturer_id"):
      raise BadRequestError("El fabricante es requerido")
    if not product_data.get("category_id"):
      raise BadRequestError("La categoría es requerida")
    if not validate_uuid(product_data.get("manufacturer_id")):
      raise BadRequestError("El fabricante no es válido")
    if not validate_uuid(product_data.get("category_id")):
      raise BadRequestError("La categoría no es válida")
      
    product = Product(
      name=product_data.get("name"),
      description=product_data.get("description"),
      unit_amount=product_data.get("unit_amount"),
      quantity=product_data.get("quantity"),
      image_url=product_data.get("image_url"),
      manufacturer_id=product_data.get("manufacturer_id"),
      category_id=product_data.get("category_id"),
    )
      
    return ProductRepository.create(product)
  
  @staticmethod
  def get_product_by_id(product_id):
    if not validate_uuid(product_id):
      raise BadRequestError("El id no es válido")   
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
      raise BadRequestError("El producto no existe")    
    return product
  
  @staticmethod
  def update_quantity(product_id, product_data):
    if not validate_uuid(product_id):
        raise BadRequestError("El ID del producto no es válido")    
    
    if "quantity" not in product_data:
      raise BadRequestError("La cantidad es requerida")                 
    if not isinstance(product_data.get("quantity"), int) or product_data.get("quantity") < 0:
        raise BadRequestError("La cantidad debe ser un número entero no negativo")    
    
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
        raise BadRequestError("El producto no existe")

    product.quantity = product_data.get("quantity")
    updated_product = ProductRepository.update(product)
    
    return updated_product
  
  @staticmethod
  def get_products_by_category(category_id):
    if not validate_uuid(category_id):
      raise BadRequestError("El id de la categoría no es válido")   
    
    products = ProductRepository.get_products_by_category(category_id)
   
    if products is None or len(products) == 0:
        raise BadRequestError("No hay productos en esta categoría")       
    return products
  
  @staticmethod
  def parse_and_validate_file(file):
    extension_file = file.filename.split('.')[-1].lower()
    if extension_file not in ['csv', 'xlsx']:
      raise BadRequestError("Formato no soportado. Solo se permite CSV o Excel")
    
    manufacturer_map = {
      m.name.strip().lower(): m.id for m in Manufacturer.query.all()
    }

    category_map = {
      c.name.strip().lower(): c.id for c in Category.query.all()
    }

    chunksize = 100
    reader = pd.read_csv(file, chunksize=chunksize) if extension_file == 'csv' else pd.read_excel(file, chunksize=chunksize)

    validos = []
    errores = []

    for chunk in reader:
      chunk.fillna('', inplace=True)
      for _, row in chunk.iterrows():
        item = row.to_dict()
        item['errores'] = []
        for col in REQUIRED_COLUMNS:
          if str(row.get(col)).strip() == '':
            item['errores'].append(f"Columna '{col}' vacía")

        name_manufacturer = str(row.get("Nombre del fabricante")).strip().lower()
        manufacturer_id = manufacturer_map.get(name_manufacturer)
        if not manufacturer_id:
          item['errores'].append("Fabricante no encontrado")
        else:
          item['manufacturer_id'] = manufacturer_id

        name_category = str(row.get("Nombre de la categoría")).strip().lower()
        category_id = category_map.get(name_category)

        if not category_id:
          item['errores'].append("Categoría no encontrada")
        else:
          item['category_id'] = category_id

        if not item['errores']:
          validos.append({
            "Nombre del producto": row["Nombre del producto"],
            "Descripción": row["Descripción"],
            "Cantidad inicial": int(row["Cantidad inicial"]),
            "Precio unitario": float(row["Precio unitario"]),
            "manufacturer_id": manufacturer_id,
            "category_id": category_id,
            "image_url": None
          })
        else:
          errores.append(item)
    return {
      "validos": validos,
      "errores": errores,
      "cantidad_validos": len(validos),
      "cantidad_errores": len(errores)
    }

  @staticmethod
  def get_categories():
    categories = ProductRepository.get_categories()
    return categories  