#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        template = jinja_env.get_template(view_filename)

        return self.response.out.write(template.render(params))

characteristics = {
    'hair': {
        'black': 'CCAGCAATCGC',
        'brown': 'GCCAGTGCCG',
        'blonde': 'TTAGCTATCGC',
        'red': 'TGATCTGGCGC'
    },
    'face': {
        'square': 'GCCACGG',
        'round': 'ACCACAA',
        'oval': 'AGGCCTCA'
    },
    'eyes': {
        'blue': 'TTGTGGTGGC',
        'green': 'GGGAGGTGGC',
        'brown': 'AAGTAGTGAC'
    },
    'gender': {
        'female': 'TGAAGGACCTTC',
        'male': 'TGCAGGAACTTC'
    },
    'race': {
        'white': 'AAAACCTCA',
        'black': 'CGACTACAG',
        'asian': 'CGCGGGCCG'
    }
}
suspects = {
    'Eva': {
        'hair': 'blonde',
        'face': 'oval',
        'eyes': 'blue',
        'gender': 'female',
        'race': 'white'
    },
    'Larisa': {
        'hair': 'brown',
        'face': 'oval',
        'eyes': 'brown',
        'gender': 'female',
        'race': 'white'
    },
    'Matej': {
        'hair': 'black',
        'face': 'oval',
        'eyes': 'blue',
        'gender': 'male',
        'race': 'white'
    },
    'Miha': {
        'hair': 'brown',
        'face': 'square',
        'eyes': 'green',
        'gender': 'male',
        'race': 'white'
    }
}
suspect={}

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("dna.html")


class DNA(BaseHandler):
    def get(self):
     return self.render_template("dna-result.html")

    def post(self):
        yourdna = []
        dna = self.request.get("dna")
        # iteritems() function copy from homework 9.3
        for key, value in characteristics.iteritems():
            for characteristic, sequence in value.iteritems():
                if dna.find(sequence) != -1:
                    suspect[key] = characteristic
                    if suspect[key] == characteristic:
                        data = str(key) + ":" + str(suspect[key])
                        yourdna.append(data)

        params = {"yourdna": yourdna}
        return self.render_template("dna-result.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/dna-result', DNA),
], debug=True)