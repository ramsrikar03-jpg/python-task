#=======================================================================
# 📝 FastAPI TODO App (CRUD) - SQLite Database Version
#=======================================================================

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


#=======================================================================
#🚀 Create FastAPI App
#=======================================================================
app = FastAPI()

#=======================================================================
#Database Configuration
#=======================================================================
DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()

#=======================================================================
# 🧱 Database Model (Table)
#=======================================================================
class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)

#Create table 
Base.metadata.create_all(bind=engine)

#=======================================================================
# 📋 Pydantic Schema
#=======================================================================
class Todo(BaseModel):
    id : int
    title : str
    completed : bool = False

    class Config:
        orm_mode = True
    
#=======================================================================
# Dependency (DB Session)
#=======================================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#=======================================================================
# 🛠️ Home Route
#=======================================================================
@app.get("/")
def home():
    return {"message": "FastAPI TODO with DB!"}

#=======================================================================
# 🆕 Create TODO
#=======================================================================    
@app.post("/todos")
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    existing = db.query(TodoDB).filter(TodoDB.id == todo.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")
    
    new_todo = TodoDB(
        id = todo.id,
        title = todo.title,
        completed = todo.completed
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {"message": "TODO created", "data": new_todo}

#=======================================================================
# 🔍 Read All TODOs
#=======================================================================
@app.get("/todos")
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoDB).all()
    return {"count": len(todos), "data": todos}

#=======================================================================
# 🔍 Read Single TODO
#=======================================================================
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="TODO not found")
    return todo

#=======================================================================
# ✏️ Update TODO
#=======================================================================
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="TODO not found")
    
    todo.title = updated_todo.title
    todo.completed = updated_todo.completed
    db.commit()
    db.refresh(todo)

    return {"message": "Updated Successfully", "data": todo}

#=======================================================================
# 🗑️ Delete TODO
#=======================================================================
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="TODO not found")
    
    db.delete(todo)
    db.commit()

    return {"message": "Deleted Successfully"}