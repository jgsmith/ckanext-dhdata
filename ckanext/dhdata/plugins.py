import ckan.plugins as p

class DHDataPlugin(p.SingletonPlugin):

  p.implements(p.IConfigurer)
  p.implements(p.IRoutes, inherit=True)
  p.implements(p.ITemplateHelpers)

  FORMAT_NAMES = {
    'atom': 'Atom Feed',
    'rss': 'RSS Feed',
    'ore': 'ORE Collection',
    'csv': 'Comma Separated Value (CSV)',
    'json': 'JSON',
    'json-ld':'JSON-LD',
    'owl+xml':'OWL/XML',
    'rdf+json':'RDF/JSON',
    'n3':'RDF/N3',
    'n-triples':'RDF/N-Triples',
    'turtle':'RDF/Turtle',
    'rdf+xml':'RDF/XML',
    'kml':'KML',
    'KML':'KML',
    'tsv':'Tab Separated Value (TSV)',
    'htm':'Interactive Resource',
    'mei':'MEI',
    'api':'Generic Service',
    'api/rest':'REST Service',
    'api/sparql':'SPARQL Service',
    'html':'HTML',
    'txt':'Text',
    'pdf':'PDF',
    'tei':'TEI',
    'rtf':'RTF',
    'tei+zip':'TEI Archive',
    'svg': 'SVG',
    'snapshot': 'Snapshot',
    'iso': 'ISO',
    'gedcom': 'GEDCOM',
  }

  def update_config(self, config):
    p.toolkit.add_template_directory(config, 'templates')
    p.toolkit.add_public_directory(config, 'public')

  def before_map(self, map):
    dhdata_controller = 'ckanext.dhdata.controller:DHDataAPIController'

    map.connect('/api/3/dhdata/popular-tags', controller=dhdata_controller, action='popular_tags')

    return map

  def get_format_namer(cls, item):
    dn = item.get('display_name', 'unknown type')
    return cls.FORMAT_NAMES.get(dn, "(%s)" % (dn))

  def get_format_name(cls, f):
    return cls.FORMAT_NAMES.get(f, "(%s)" % (f))

  def get_helpers(self):
    return {
      'dhdata_format_facet_namer': self.get_format_namer,
      'dhdata_format_facet_name': self.get_format_name
    }
