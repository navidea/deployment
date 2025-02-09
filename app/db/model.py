from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Post(Base) :
    """
    Represents a post in the database.

    Attributes:
        id (int): The unique identifier for the post.
        content (str): The content of the post.
        published (bool): Indicates whether the post is published or not.
        created_time (datetime): The timestamp when the post was created.
    """
    #table name
    __tablename__ = "post"
    #id
    id = Column(Integer, primary_key=True,nullable=False)

    #title
    title = Column(String)
    #content
    content = Column(String, nullable=True)
    #published
    published = Column(Boolean, default=True, nullable=False)
    #created
    created_time = Column(TIMESTAMP(timezone=True),
                    server_default= text("NOW()"),nullable=False)
