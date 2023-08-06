# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typeddict']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0', 'typing-extensions>=4.3.0']

setup_kwargs = {
    'name': 'typeddict',
    'version': '0.1.0',
    'description': 'Use `TypedDict` replace pydantic definitions.',
    'long_description': '# TypedDict\n\nUse `TypedDict` replace pydantic definitions.\n\n## Why?\n\n```python\nfrom pydantic import BaseModel\n\n\nclass User(BaseModel):\n    name: str\n    age: int = Field(default=0, ge=0)\n    email: Optional[str]\n\n\nuser: User = {"name": "John", "age": 30}  # Type check, error!\nprint(repr(user))\n```\n\nIn index.py or other framework, maybe you write the following code. And then got an type check error in `Annotated[Message, ...]`, because the type of `{"message": "..."}` is not `Message`.\n\n```python\nclass Message(BaseModel):\n    message: str\n\n\n@routes.http.get("/user")\nasync def create_user(\n    ...\n) -> Annotated[Message, JSONResponse[200, {}, Message]]:\n    ...\n    return {"message": "Created successfully!"}\n```\n\n## Usage\n\nUse `Annotated` to provide extra information to `pydantic.Field`. Other than that, everything conforms to the general usage of `TypedDict`. Using `to_pydantic` will create a semantically equivalent pydantic model. You can use it in frameworks like [index.py](https://github.com/index-py/index.py) / [fastapi](https://fastapi.tiangolo.com/) / [xpresso](https://github.com/adriangb/xpresso).\n\n```python\nfrom typing_extensions import TypedDict, NotRequired, Annotated\n\nimport typeddict\nfrom typeddict import Metadata, Extra\n\n\nclass User(TypedDict):\n    name: str\n    age: Annotated[int, Metadata(default=0), Extra(ge=0)]\n    email: NotRequired[str]\n\n\nuser: User = {"name": "John", "age": 30}  # Type check, pass!\nprint(repr(user))\n\n# Then use it in index.py / fastapi or other frameworks\nUserModel = typeddict.to_pydantic(User)\nprint(repr(UserModel.parse_obj(user)))\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/typeddict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
