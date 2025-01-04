from os import name
from sqlalchemy import Column, Integer, String, Text
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(50))

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        
    def __repr__(self):
        return f'<User {self.username!r}>'
    

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title= Column(String(120), nullable=False)
    text = Column(Text())
    def __unit__(self, title=None, text=None) -> None:
        self.title = title
        self.text = text

    def __repr__(self):
        return f"<Post {self.title!r}>"