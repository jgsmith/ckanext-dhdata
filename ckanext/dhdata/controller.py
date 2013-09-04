import ckan.lib.helpers as h

from ckan.lib.base import BaseController, response

class DHDataAPIController(BaseController):
  def popular_tags(self):
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    response_data = h.get_facet_items_dict('tags', limit=3)
    response_msg = h.json.dumps({ 'success': True, 'result': response_data })
    return response_msg
