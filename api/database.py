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
     @classmethod
     def update_isSuperUser(self, name):
          user = self.query.filter_by(name = name).first()
          if user:
               user.isSuperUser = True
               db.session.commit()
               return user
          


class TODO(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     isSuperUser = db.Column(db.Boolean)
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
          todo = self(user_id = user_id, title = title, isSuperUser = isSuperUser,description=description, time= str(time), image=image)
          db.session.add(todo)
          db.session.commit()
          return todo
     @classmethod
     def delete(self, id):
          todo = self.query.filter_by(id = id).first()
          if todo:
               db.session.delete(todo)
               db.session.commit()
          return todo
     @classmethod
     def create_todo_su_meth(self, id, image):
          todo = self.query.filter_by(id=id).first()
          if todo:
               todo.isSuperUser = True
               todo.image = image
               db.session.commit()
          return todo
     @classmethod
     def update_todo_meth(self, id, title, description, time):
          todo = self.query.filter_by(id=id).first()
          if todo:
               todo.title = title
               todo.description = description
               todo.time = time
               db.session.commit()
          return todo
     
if __name__ == "__main__":
     with app.app_context():
          db.create_all()