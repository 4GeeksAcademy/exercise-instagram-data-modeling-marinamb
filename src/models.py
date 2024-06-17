import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class UserPrivate(Base):
    __tablename__ = 'user_private'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(15), nullable=False, unique=True)
    password = Column(String(128), nullable=False)  
    email = Column(String(50), nullable=False, unique=True)
    public_profile = relationship('UserPublic', back_populates='private_profile', uselist=False)


class UserPublic (Base):
    __tablename__='user_public'
    id= Column(Integer, primary_key=True)
    user_name=Column(String(15), nullable=False, unique= True)
    description = Column(String(250), nullable=True, unique=True)
    user_private_id = Column(Integer, ForeignKey("user_private.id"))
    images = relationship("Images", back_populates="user_public")
    user_private = relationship("UserPrivate", back_populates="user_public")
    post = relationship("Post", back_populates="user_public")
    likes = relationship("Likes", back_populates="user_public")

class Images (Base):
    __tablename__='images'
    id = Column(Integer, primary_key=True)
    profile_photo = Column(Boolean) 
    user_public_id=Column(Integer, ForeignKey("user_public.id"))
    post_id=Column(Integer, ForeignKey("post.id"))
    user_public = relationship("UserPublic", back_populates="images")
    post = relationship("Post", back_populates="images")

class Post (Base):
    __tablename__='post'
    id= Column(Integer, primary_key=True)
    user_public_id=Column(Integer, ForeignKey("user_public.id"))
    image_id = Column(Integer, ForeignKey("Images.id")) 
    user_public = relationship("UserPublic", back_populates="post")
    images = relationship("Images", back_populates="post")
    likes = relationship("Likes", back_populates="post")

class Likes(Base):
    __tablename__='likes'
    id=Column(Integer, primary_key=True)
    likes= Column(Integer, nullable=True)
    post_id = Column(Integer, ForeignKey("Post.id"))
    user_public_id=Column(Integer, ForeignKey("user_public.id"))
    user_public = relationship("UserPublic", back_populates="likes")
    post = relationship("Post", back_populates="likes")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
