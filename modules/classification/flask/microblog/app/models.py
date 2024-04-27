
import sqlalchemy as sa
import sqlalchemy.orm as so

from datetime import datetime, timezone
from hashlib import md5
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = sa.Column(sa.Integer, primary_key=True, nullable=False)
    username: so.Mapped[str] = sa.Column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = sa.Column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = sa.Column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = sa.Column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    posts: so.Mapped['Post'] = so.relationship("Post", back_populates='author')
    following: so.Mapped['User'] = so.relationship(
        "User",
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: so.Mapped['User'] = so.relationship(
        "User",
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        return len(self.followers)
        # query = sa.select(sa.func.count()).select_from(self.followers.select().subquery())
        # return db.session.scalar(query)

    def following_count(self):
        return len(self.following)
        # query = sa.select(sa.func.count()).select_from(self.following.select().subquery())
        # return db.session.scalar(query)

    def following_posts(self):
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            sa.select(Post)
            .join(Author, Post.user_id == Author.id)
            .join(Follower, Author.followers)
            .where(sa.or_(
                Follower.id == self.id,
                Author.id == self.id,
            ))
            .group_by(Post)
            .order_by(sa.desc(Post.timestamp))
        )
        # return (
        #     sa.select(Post)
        #     .join(Post.author.of_type(Author))
        #     .join(Author.followers.of_type(Follower), isouter=True)
        #     .where(sa.or_(
        #         Follower.id == self.id,
        #         Author.id == self.id,
        #     ))
        #     .group_by(Post)
        #     .order_by(Post.timestamp.desc())
        # )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Post(db.Model):
    id: so.Mapped[int] = sa.Column(sa.Integer, primary_key=True, nullable=False)
    body: so.Mapped[str] = sa.Column(sa.String(140))
    timestamp: so.Mapped[datetime] = sa.Column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = sa.Column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship("User", back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)