# Copyright (c) 2017 Maina Nick

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import os

from sqlalchemy import create_engine


class DatabaseConnection(object):
    _config = None
    engine = None

    @classmethod
    def config(self):
        if self._config is not None:
            return self._config

        if not os.environ['DSCONFIG']:
            raise ValueError("Database Config Missing")

        self._config = os.environ['DSCONFIG']
        return self._config

    @classmethod
    def connect(self):
        self.engine = create_engine(self.config())

    @classmethod
    def execute(self, query):
        if self.engine is None:
            self.connect()
        connection = self.engine.connect()
        results = connection.execute(query).fetchall()
        connection.close()
        return results
