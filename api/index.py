from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

app.add_middleware(CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

@app.get("/api/test")
async def get_test():
    return "test message"


@app.get("/api/stations")
async def get_stations():
    '''
    Get all stations
    '''
    stations = get_stations_csv()
    stations_json = stations.to_json(orient='records')

    return Response(stations_json, media_type="application/json")


@app.get("/api/stations/{station_type}/")
async def get_stations(station_type):
    '''
    Get all stations by type
    '''
    stations=pd.read_csv(fr"api\data\{station_type}\stations.csv")
    stations_json = stations.to_json(orient='records')

    return Response(stations_json, media_type="application/json")


@app.get("/api/snow/station/{station}")
async def get_snow(station, year: int | None = None):
    '''
    Get snow data by station
    '''
    stations =  get_stations_csv()
    if not stations["station_code"].eq(station).any():
        raise HTTPException(status_code=404, detail="Station not found")

    snow = get_snow_csv()
    snow = snow.loc[(snow["station_code"] == station)]
    
    if year:
        snow["measure_datetime"] = pd.to_datetime(snow["measure_date"])
        snow_filtered = snow.loc[(snow["measure_datetime"].dt.year == year)] 
        del snow_filtered["measure_datetime"]
        snow = snow_filtered
        
    snow_json = snow.to_json(orient='records')
    return Response(snow_json, media_type="application/json")

@app.get("/api/snow/year/{year}")
async def get_snow(year, month: int | None = None, day: int | None = None):
    '''
    Get snow data by year
    '''
    snow = get_snow_csv()
    
    snow["measure_datetime"] = pd.to_datetime(snow["measure_date"])
    snow_filtered = snow.loc[(snow["measure_datetime"].dt.year == int(year))] 
    
    if month:
        snow_filtered = snow_filtered.loc[(snow_filtered["measure_datetime"].dt.month == month)] 
        
    if day:
        snow_filtered = snow_filtered.loc[(snow_filtered["measure_datetime"].dt.day == day)] 
    
    del snow_filtered["measure_datetime"]
    snow = snow_filtered
    
    snow_json = snow.to_json(orient='records')
    return Response(snow_json, media_type="application/json")


def get_stations_csv():
    print(os.getcwd())
    print(os.path.dirname(os.path.abspath(__file__)))
    imis_stations=pd.read_csv(fr"data\imis\stations.csv")
    beob_stations=pd.read_csv(fr"data\beob\stations.csv")
    
    return pd.concat([imis_stations, beob_stations])

def get_snow_csv():
    imis_snow=pd.read_csv(fr"data\imis\daily_snow.csv")
    beob_snow=pd.read_csv(fr"data\beob\daily_snow.csv")
    del beob_snow["HNW_1D"]
    
    return pd.concat([imis_snow, beob_snow])
