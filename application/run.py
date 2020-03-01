from flask import Flask,render_template,abort
from entitie.entities import Create_entities
import datetime

app = Flask(__name__)

entitie = Create_entities()
entitie.create_user()

@app.route('/')
def home():
    return render_template('pages/index.html')

@app.route('/notes')
def notes():
    return render_template('pages/notes.html')
      
# #<id> c'est un parametre qui va etre reçu par la fonction
# @app.route('/blog/posts/<int:id>')
# def posts_show(id):
#     try: 
#         return render_template('posts/show.html')
#     except:
#         abort(404)

@app.context_processor
def inject_now():
    #l'année dispolnible sur toutes l'application
    return dict({'now': datetime.datetime.now().year})


# @app.context_processor
# def utility_processor():
#     def pluralize(count,singular,plural=None):
#         if not isinstance(count,int):
#             raise ValueError(f'{count} must be an integer')
#         if plural is None :
#             plural = singular +'s'
#         if count == 1:
#             res = singular
#         else:
#             res = plural
#         return f'{count} {res}'
#     return dict(nom_dans_vue = pluralize)

""" gestion d'erreur 404 """
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    entitie.db.create_all()
    app.run(debug = True,host = '0.0.0.0',port = '5001')
