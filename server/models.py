from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Failed simple name validation")
        author = Author.query.filter_by(name=value).first()
        if author is not None:
            raise ValueError("Failed name validation")
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit():
            raise ValueError("Phone number should only contain digits")
        if not len(value) == 10:
            raise ValueError("Number not exactly 10 digits")
        return value 
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Post must have a title")
        if 'Won\'t Believe' not in value and 'Secret' not in value and 'Top' not in value and 'Guess' not in value:
            raise ValueError("Post title not sufficiently clickbait-y")
        return value 
        
    @validates('content')
    def validate_content(self, key, value):
        if not len(value) >= 250:
            raise ValueError("Content must be at least 250 characters long")
        return value 
    
    @validates('summary')
    def validate_summary(self, key, value):
        if not len(value) <= 250:
            raise ValueError("Summary must be less than 250 characters")
        return value 
    
    @validates('category')
    def validate_category(self, key, value):
        if value != 'Fiction' and value != 'Non-Fiction':
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return value 



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
