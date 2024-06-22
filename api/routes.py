from flask import Blueprint, request
from .models import Article, Comment
from .utils import paginate_query, validate_article_data, validate_comment_data, json_response, error_response, require_json
import datetime
from flask_restx import Api, Resource, fields
from extensions import db

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, doc='/docs')

ns = api.namespace('', description='Operations related to articles')

article_model = ns.model('Article', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an article'),
    'title': fields.String(required=True, description='Title of the article'),
    'content': fields.String(required=True, description='Content of the article'),
    'author': fields.String(description='Author of the article'),
    'pub_date': fields.DateTime(description='Publication date of the article')
})

comment_model = ns.model('Comment', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a comment'),
    'article_id': fields.Integer(required=True, description='ID of the related article'),
    'content': fields.String(required=True, description='Content of the comment'),
    'author': fields.String(description='Author of the comment'),
    'pub_date': fields.DateTime(description='Publication date of the comment')
})

@ns.route('/articles')
class ArticleListResource(Resource):
    @ns.doc(description='List all articles with pagination, filtering, and sorting options')
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        author = request.args.get('author', type=str)
        keyword = request.args.get('keyword', type=str)
        sort_by = request.args.get('sort_by', 'title', type=str)
        sort_order = request.args.get('sort_order', 'desc', type=str)

        query = Article.query
        if author:
            query = query.filter(Article.author.like(f'%{author}%'))
        if keyword:
            query = query.filter(Article.content.like(f'%{keyword}%') | Article.title.like(f'%{keyword}%'))
        # Apply sorting
        if sort_order == 'desc':
            query = query.order_by(db.desc(getattr(Article, sort_by)))
        else:
            query = query.order_by(getattr(Article, sort_by))

        articles = paginate_query(query, page, per_page)
        return json_response('success', [article.to_dict() for article in articles])

    @ns.expect(article_model)
    @require_json
    def post(self):
        data = request.get_json()
        errors = validate_article_data(data)
        if errors:
            return error_response(errors)

        article = Article(
            title=data['title'],
            content=data['content'],
            author=data.get('author', 'Anonymous'),
            publication_date=datetime.datetime.utcnow()
        )
        db.session.add(article)
        db.session.commit()
        return json_response('success', article.to_dict(), 201)

@ns.route('/articles/<int:article_id>')
class ArticleResource(Resource):
    @ns.marshal_with(article_model)
    def get(self, article_id):
        article = Article.query.get_or_404(article_id)
        article_data = article.to_dict()
        article_data['comments'] = [comment.to_dict() for comment in article.comments]
        return article_data

    @ns.expect(article_model)
    @require_json
    def put(self, article_id):
        article = Article.query.get_or_404(article_id)
        data = request.get_json()
        errors = validate_article_data(data)
        if errors:
            return error_response(errors)

        article.title = data['title']
        article.content = data['content']
        article.author = data.get('author', article.author)
        article.publication_date = datetime.datetime.utcnow()
        db.session.commit()
        return json_response('success', article.to_dict())

    def delete(self, article_id):
        article = Article.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()
        return json_response('success', {'message': 'Article deleted'})

@ns.route('/articles/<int:article_id>/comments')
class CommentListResource(Resource):
    @ns.expect(comment_model)
    @require_json
    def post(self, article_id):
        data = request.get_json()
        errors = validate_comment_data(data)
        if errors:
            return error_response(errors)

        comment = Comment(
            article_id=article_id,
            author=data['author'],
            content=data['content'],
            publication_date=datetime.datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        return json_response('success', comment.to_dict(), 201)

api.add_namespace(ns)
