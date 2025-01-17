# 3050-abschlussarbeit-backend

## Data Source
https://www.slf.ch/de/services-und-produkte/slf-datenservice/

## Start development
pip install -r requirements.txt
uvicorn api.index:app --reload

## Start deployment 
uvicorn api.index:app --host 0.0.0.0 --port $PORT
