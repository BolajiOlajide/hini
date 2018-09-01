from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'Users'

    __table_args__ = (db.UniqueConstraint(
        'slack_uid', 'team_id',
        name='unique_constraint_slack_id_team'),
    )

    id = db.Column(db.Integer(), primary_key=True)
    slack_username = db.Column(db.String(32), nullable=False)
    slack_uid = db.Column(db.String(32), nullable=False)
    google_token = db.Column(db.String(512), unique=True, index=True,
                             nullable=True)
    email = db.Column(db.String(64), nullable=False)
    tz = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    team_id = db.Column(db.String(32), nullable=False)
    refresh_token = db.Column(db.String(128), nullable=True)
    state = db.Column(db.String(128), nullable=True)
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


class Team(db.Model):
    __tablename__ = 'Teams'

    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(512), nullable=False)
    team_name = db.Column(db.String(128), nullable=True)
    team_id = db.Column(db.String(128), nullable=False)
    bot_token = db.Column(db.String(128), nullable=False)
    user_token = db.Column(db.String(128), nullable=False)
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
            'id': self.id
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
        return '<Team ID: {}>'.format(self.id)
