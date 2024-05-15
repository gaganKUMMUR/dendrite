from core import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    isSuperUser = db.Column(db.Boolean)

    def __repr__(self):
         return f"User <{self.name} {self.isSuperUser}>"
    
    @classmethod
    def create(self, name):
         user = self(name = name, isSuperUser= False)
         db.session.add(user)
         db.session.commit()
         return user
    @classmethod
    def delete(self, id):
       
          user = self.query.filter_by(id = id)
          if user:
               db.session.delete(user)
               db.session.commit()
               return user
          

    
class TODO(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     title = db.Column(db.String)
     description = db.Column(db.String)
     time = db.Column(db.String)
     image = db.Column(db.String)

     @classmethod
     def create(self, user_id, isSuperUser,title, description, time, image="None"):
          if (isSuperUser):
               image = image
          else:
               image = "None"
          todo = self(user_id = user_id, title = title, description=description, time= str(time), image=image)
          db.session.add(todo)
          db.session.commit()
          return todo
     @classmethod
     def delete(self, id):
          todo = self.query.filter_by(id = id)
          if todo:
              db.session.delete(todo)
              db.session.commit()
          return todo
     
if __name__ == "__main__":
     with app.app_context():
          db.create_all()