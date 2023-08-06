

## Web

JSON Scheme 校验及将结果绑定到类-对象：

```python
from flask import g
from flask_expects_json import expects_json
from pushy_utils import web

class User(object):
    name = str
    age = int
    hobby = list

    required_include = ['all']
    required_exclude = ['name']

@app.route('/users', methods=['POST'])
@expects_json(schema=web.generate_schema(User), force=True)
def save():
    user = web.bind_body(g.data, User)
    return web.succeed(user.__dict__)
```