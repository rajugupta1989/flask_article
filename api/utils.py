from flask import jsonify, request

def paginate_query(query, page, per_page):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items

def validate_article_data(data):
    errors = []
    if not data.get('title'):
        errors.append('Title is required.')
    if not data.get('content'):
        errors.append('Content is required.')
    return errors

def validate_comment_data(data):
    errors = []
    if not data.get('author'):
        errors.append('Author is required.')
    if not data.get('content'):
        errors.append('Content is required.')
    return errors

def json_response(status, data, status_code=200):
    response = jsonify({
        'status': status,
        'data': data
    })
    response.status_code = status_code
    return response

def error_response(errors, status_code=400):
    response = jsonify({
        'status': 'error',
        'errors': errors
    })
    response.status_code = status_code
    return response

def require_json(f):
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return error_response(['Invalid JSON request.'])
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
