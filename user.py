from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = (db.UniqueConstraint(
        'slack_username', 'slack_uid',
        name='unique_constraint_slack_id_name'),
    )

    id = db.Column(db.Integer(), primary_key=True)
    slack_username = db.Column(db.String(32), index=True, nullable=False)
    slack_uid = db.Column(db.String(32), unique=True, index=True,
                          nullable=False)
    token = db.Column(db.String(128), unique=True, index=True,
                      nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(),
        onupdate=datetime.now(), nullable=False)

    def to_json(self):
        """
        Display the object properties as a json object.

        Mold up all the properties of BucketList object into
        an object for display.
        """
        return {
            'id': self.id,
            'slack_username': self.slack_username,
            'slack_uid': self.slack_uid
        }

    def save(self):
        """
        Save to database.

        Save instance of the object to database and commit.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except (exc.IntegrityError, exc.InvalidRequestError):
            db.session().rollback()

    def delete(self):
        """
        Delete from database.

        Deletes instance of an object from database
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the BucketList object.
        """
        return '<Slack Handle: {} - {}>'.format(self.slack_username,
                                                self.slack_uid)
