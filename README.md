# 3050-abschlussarbeit-backend

## Start development
uvicorn api.index:app --reload

## Start deployment 
uvicorn api.index:app --host 0.0.0.0 --port $PORT
