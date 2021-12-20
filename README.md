# Flask-SemanticUI (Building)

[![Build status](https://github.com/juniors90/Flask-SemanticUI/actions/workflows/testing-package.yml/badge.svg)](https://github.com/juniors90/Flask-SemanticUI/actions)
[![codecov](https://codecov.io/gh/juniors90/Flask-SemanticUI/branch/main/graph/badge.svg?token=V03GVOHP77)](https://codecov.io/gh/juniors90/Flask-SemanticUI)
![docstr-cov](https://img.shields.io/endpoint?url=https://jsonbin.org/juniors90/Flask-SemanticUI/badges/docstr-cov)
[![Forks](https://img.shields.io/github/forks/juniors90/Flask-SemanticUI)](https://github.com/juniors90/Flask-SemanticUI/stargazers)
[![star](https://img.shields.io/github/stars/juniors90/Flask-SemanticUI?color=yellow)](https://github.com/juniors90/Flask-SemanticUI/network/members)
[![issues](https://img.shields.io/github/issues/juniors90/Flask-SemanticUI?color=teal)](https://github.com/juniors90/Flask-SemanticUI/issues)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Requirements

Python 3.8+

## Dependecies for this project.

- [Flask(>=2.0.2)](https://flask.palletsprojects.com/en/2.0.x/) for build the backend.

## intallation

You can install via pip:

```cmd
    $> pip install Flask-SemanticUI
```
   
For development, clone the [official github repository](https://github.com/juniors90/Flask-SemanticUI) instead and use:

```cmd
    $ git clone git@github.com:juniors90/Flask-SemanticUI.git
    $ cd Flask-SemanticUI
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements/dev.txt
```

## Quick start

```python
    from flask import Flask, render_template_string
    from flask_semantic import SemanticUI
    
    app = Flask(__name__)
    semantic = SemanticUI(app)

    # routes
    @app.route("/")
    def index():
        # Make data:
        return render_template()

    if __name__ == "__main__":
        app.run(port=5000, debug=True)
```

## Links

- [Documentation](https://flask-semanticui.readthedocs.io)
- [Example Application](https://github.com/juniors90/Flask-SemanticUI/tree/main/sample_app)
- [PyPI Releases](https://pypi.org/project/Flask-SemanticUI/)
- [Changelog](https://github.com/juniors90/Flask-SemanticUI/blob/main/CHANGELOG.rst)


## Authors

- Ferreira, Juan David

Please submit bug reports, suggestions for improvements and patches via
the (E-mail: juandavid9a0@gmail.com).

## Official repository and Issues

- https://github.com/juniors90/Flask-SemanticUI


## License

`Flask-SemanticUI` is free software you can redistribute it and/or modify it
under the terms of the MIT License. For more information, you can see the
[LICENSE](https://github.com/juniors90/Flask-SemanticUI/blob/main/LICENSE) file
for details.

