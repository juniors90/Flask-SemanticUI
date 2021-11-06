#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Flask-SemanticUI Project (https://github.com/juniors90/Flask-SemanticUI/).
# Copyright (c) 2022, Ferreira Juan David
# License: MIT
# Full Text: https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =============================================================================
# TEST SAMPLE
# =============================================================================


def test_sample_request(app, client):
    @app.get("/sample")
    def sample():
        return "OK"

    r = client.get("/sample")
    assert r.status_code == 200
    assert r.data == b"OK"
