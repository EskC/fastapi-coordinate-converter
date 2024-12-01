from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyproj import Transformer

app = FastAPI()

# CORS middleware'ini ekleyin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Koordinat dönüşümü için kullanıcıdan veri alacak model
class CoordinateRequest(BaseModel):
    x: float
    y: float
    from_epsg: int
    to_epsg: int

# POST endpoint'i tanımlayın
@app.post("/convert")
async def convert_coordinates(data: CoordinateRequest):
    transformer = Transformer.from_crs(f"epsg:{data.from_epsg}", f"epsg:{data.to_epsg}", always_xy=True)
    x2, y2 = transformer.transform(data.x, data.y)
    return {"x": x2, "y": y2}
