# fastapi_social_media
Social media API using FastAPI
- basic user, posting, voting routes with authentification tokens
- schemas validation & pydantic models
- SQL database ORM with SQLAlchemy + Alembic database migration tool
- Testing w/ pytest + CI/CD w/ Github Actions
- Hosted on : 
  - Heroku: https://social-fastapi-hich.herokuapp.com/docs
  - DigitalOcean Ubuntu VM: https://hichch.xyz/docs
  - Dockerized: https://hub.docker.com/r/hichchou/fastapi_social
  
Run with command line:
uvicorn app.main:app --reload