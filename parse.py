
from flask import Flask, jsonify, request, render_template
import json
import httplib
import urllib

app = Flask(__name__)
parse_app_id = "zmWJCe0SgbXzRnFm9zipa9lFxdW15UdE6FHY7HOs"
parse_app_key = "LwRjbjxVPfyhJgzdxv9YLifWMun5gdA5xIbrcbfQ"

@app.route('/')
def hello_world():
    """
    :serves: index
    :return: index page
    """
    return render_template('index.html')


@app.route('/user/', methods=['PUT', 'POST'])
def user_signup():
    """
    new user object creation
    :return: session id and object id
    """
    signup_data = request.data
    data = json.loads(signup_data)
    username = data['username']
    password = data['password']
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/users', json.dumps({
        "username": username,
        "password": password,
    }), {
        "X-Parse-Application-Id": parse_app_id,
        "X-Parse-REST-API-Key": parse_app_key,
        "Content-Type": "application/json"
    })
    result = json.loads(connection.getresponse().read())
    try:
        sess_dict = {"id": result['sessionToken'], "objectId": result['objectId']}
    except KeyError:
        return jsonify(**result), 400
    return jsonify(**sess_dict), 201


@app.route('/user/', methods=['GET'])
def user_edit():
    """
    dummy fetch for backbone model
    :return:
    """
    result = dict(username="username", password="password", objectId="df43qgfbuvo34ug",
                  id="fe7d34f493yut84hg8v")
    return jsonify(**result)


@app.route('/user/login/', methods=['PUT', 'POST'])
def user_login():
    """
    creates a new session
    :return: session id and object id
    """
    user_login_cred = request.data
    data = json.loads(user_login_cred)
    username = data['username']
    password = data['password']
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"username": username, "password": password})
    connection.connect()
    connection.request('GET', '/1/login?%s' % params, '', {
        "X-Parse-Application-Id": parse_app_id,
        "X-Parse-REST-API-Key": parse_app_key
    })
    result = json.loads(connection.getresponse().read())
    print result
    try:
        sess_dict = {"id": result["sessionToken"], "objectId": result["objectId"]}
    except KeyError:
        return jsonify(**result), 401
    return jsonify(**sess_dict)


@app.route('/user/<path:sess_id>', methods=['DELETE'])
def user_logout(sess_id):
    """
    deletes session id
    :return: deleted session id
    """
    print sess_id
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/logout', '', {
        "X-Parse-Application-Id": parse_app_id,
        "X-Parse-REST-API-Key": parse_app_key,
        "X-Parse-Session-Token": sess_id
    })
    result = json.loads(connection.getresponse().read())
    print result

    return jsonify(**result)


if __name__ == '__main__':
    app.run(debug=True)
