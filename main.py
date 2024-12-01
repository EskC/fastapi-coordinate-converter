from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyproj import Transformer

# FastAPI uygulamasını başlat
app = FastAPI()

# Kullanıcıdan veri almak için bir model oluşturun
class CoordinateRequest(BaseModel):
    x: float
    y: float
    from_epsg: int
    to_epsg: int

# POST /convert endpoint'i
@app.post("/convert")
async def convert_coordinates(data: CoordinateRequest):
    try:
        # EPSG kodlarına göre bir Transformer oluşturun
        transformer = Transformer.from_crs(f"epsg:{data.from_epsg}", f"epsg:{data.to_epsg}", always_xy=True)
        
        # Koordinatları dönüştür
        x2, y2 = transformer.transform(data.x, data.y)
        
        return {"x": x2, "y": y2}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
