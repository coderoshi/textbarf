#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



import os
import wsgiref.handlers


from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db

class Barf(db.Model):
  text = db.StringProperty(required=True)
  phone = db.PhoneNumberProperty()
  date = db.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp.RequestHandler):
  def get(self):
    barfs = Barf.all().order('-date').fetch(250)
    
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, {'barfs': barfs}))


class TxtBackHandler(webapp.RequestHandler):
  def get(self):
    text = self.request.get('message')
    if text: text = text.strip().lower()
    phone = self.request.get('min')
    if phone: phone = phone[-10:]
    
    b = Barf(text=text, phone=phone)
    b.put()
    
    self.response.out.write('http://textbarf.com')


def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/txtback', TxtBackHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
