from flask import Flask, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adsbd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Ads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    date = db.Column(db.DateTime(), default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            "description": self.description,
            'username': self.username,
            'date': self.date
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)




@app.route('/api/get/<int:advertisement_id>', methods=['GET'])
def get_adv(advertisement_id):
    advertisement = Ads.query.get(advertisement_id)
    return jsonify(advertisement.to_dict())



@app.route('/api/post', methods=['POST'])
def post_adv():
    advertisement = Ads(**request.json)
    try:
        db.session.add(advertisement)
        db.session.commit()
        return jsonify(advertisement.to_dict())
    except:
        return 'Ошибка'


@app.route('/api/delete/<int:ads_id>', methods=['DELETE'])
def delete_adv(advertisement_id):
    advertisement = Ads.query.get(advertisement_id)
    try:
        db.session.delete(advertisement)
        db.session.commit()
        return jsonify(advertisement.to_dict())
    except:
        return 'Ошибка'


@app.route('/api/patch/<int:advertisement_id>', methods=['PATCH'])
def patch_adv(advertisement_id):
    advertisement = Ads.query.get(advertisement_id)
    advertisement.update(**request.json)
    try:
        db.session.commit()
        return jsonify(advertisement.to_dict())
    except:
        return 'Ошибка'




if __name__ == '__main__':
    app.run()