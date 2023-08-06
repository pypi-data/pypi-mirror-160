import os
from os.path import dirname, join
from django.conf import settings

from crud_framework.errors import Error, HttpStatus
from crud_framework.schemas.base import BaseSchema


class CrudSchema(BaseSchema):
    GET, POST, PUT, DELETE = True, True, True, True
    MODEL_CLASS = None
    FIELDS = []
    MAPPED_FILTERS = {}
    ANNOTATIONS = {}
    SUB_CLASSES = {}  # {relation_key, CrudSchema}
    MANY_MODELS = {}  # {field_name, CrudSchema}
    ANCHOR = 'id'
    ALWAYS_LIST = True  # todo add as filter
    ORDER_BY = []
    EXPAND = True
    TRIM_NULL_VALUES = False  # TODO
    PAGE_SIZE = 0

    def __init__(self, filters, initkwargs=None):
        # self.url_path = self.URL_PATH
        self.path = self.PATH
        self.model_class = self.MODEL_CLASS
        self.model_name = self.model_class.__name__
        self.initkwargs = initkwargs if initkwargs else {}

        for k, v in self.MAPPED_FILTERS.items():
            filters[k] = filters.pop(v)

            # Pop page number or 1
        self.page_number = int(filters.pop('page_number', 1))
        # Pop page size ELSE use default
        self.page_size = int(filters.pop('page_size', self.PAGE_SIZE))

        if 'order_by' in filters:
            srt = filters.pop('order_by', [])
            if isinstance(srt, list):
                self.ORDER_BY += srt
            else:
                self.ORDER_BY.append(srt)
        elif not self.ORDER_BY:
            # Order by Anchor if no ordering sent
            self.ORDER_BY = [self.ANCHOR]

        self.filters = filters if filters else {}

        if self.FIELDS:
            if self.ANCHOR not in self.FIELDS:
                self.FIELDS.append(self.ANCHOR)
            self.FIELDS += list(self.SUB_CLASSES.keys())
            self.fields_data = [f for f in self.model_class._meta.fields if f.name in self.FIELDS]
        else:
                self.fields_data = self.model_class._meta.fields
        self.annotations = self.ANNOTATIONS
        self.required_fields = [f.name for f in self.fields_data if not f.blank]

    def get_queryset(self):
        return self.model_class.objects.filter(**self.filters).order_by(*self.ORDER_BY)

    def get(self):
        if not (self.GET or self.POST or self.PUT):
            raise Error(field_name=None, message='GET not allowed', status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)
        res = list(self.get_queryset().values(*self.FIELDS).annotate(**self.ANNOTATIONS).distinct())
        total_count = len(res)
        if self.page_size > 0:
            i = (self.page_number - 1) * self.page_size
            res = res[i:i + self.page_size]
        for item in res:
            for relation_key, crud_schema in self.SUB_CLASSES.items():  # TODO dont call items everytime
                model_class = crud_schema.model_class
                model_name = model_class.__name__.lower()
                relation_id = item.get(relation_key)
                if not relation_id:
                    item[model_name] = None
                else:
                    i = crud_schema(filters={'id': relation_id}).get()
                    item[model_name] = i[0] if isinstance(i, list) else i
            for field_name, crud_schema in self.MANY_MODELS.items():
                join_key = f'{self.model_name.lower()}__{self.ANCHOR}'
                if '__' in field_name:
                    join_key = '__'.join(field_name.split('__')[:-1]) + f'__{join_key}'
                item[field_name] = crud_schema(initkwargs=self.initkwargs, filters={join_key: item[self.ANCHOR]}).get()
            # if self.TRIM_NULL_VALUES: #TODO
            #     item = {k: v for k, v in item.values() if v}

        if not self.ALWAYS_LIST and len(res) == 1:
            return res[0]
        return {
            'data': res,
            'total_count': total_count,
        }

    def post(self, **data):
        if not self.POST:
            raise Error(field_name=None, message='POST not allowed', status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)
        many_models_data = []
        for field in self.MANY_MODELS.keys():
            if field in data:
                many_models_data.append((field, data.pop(field)))

        self.item = self.model_class(**data)
        self.item.full_clean()
        self.item.save()

        for field, ids in many_models_data:
            ids = ','.join(str(i) for i in ids)
            exec(f'self.item.{field}.add({ids})')

        self.filters = {'id': self.item.id}
        return self.get()

    def bulk_post(self, data, force=False, **kwargs):
        if not self.POST:
            raise Error(field_name=None, message='POST not allowed', status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)
        if not force:
            res = []
            item_ids = []
            for item in data:
                item = self.model_class(**item, **kwargs)
                item.full_clean()
                res.append(item)
            for item in res:
                item.save()
                item_ids.append(item.id)
        else:
            self.model_class.objects.bulk_create([self.model_class(**item, **kwargs) for item in data])
            ln = len(data)
            item_ids = list(self.model_class.objects.order_by('-id')[:ln].values_list('id', flat=True))
        self.filters = {'id__in': item_ids}
        return self.get()

    def put(self, **data):
        if not self.PUT:
            raise Error(field_name=None, message='PUT not allowed', status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)
        res = []
        item_ids = []
        many_models_data = {}
        for item in self.get_queryset():
            many_models_data[item.id] = []
            for field in self.MANY_MODELS.keys():
                if field in data:
                    many_models_data[item.id].append((field, data.pop(field)))
                else:
                    many_models_data.pop(item.id)

            for key, value in data.items():
                setattr(item, key, value)
            item.full_clean()
            res.append(item)

        for item in res:
            item.save()
            item_ids.append(item.id)
            if item.id in many_models_data:
                for field, ids in many_models_data[item.id]:
                    ids = ','.join(str(i) for i in ids)
                    exec(f'item.{field}.clear()')
                    exec(f'item.{field}.add({ids})')

        self.filters = {'id__in': item_ids}
        return self.get()

    def delete(self, **data):
        if not self.DELETE:
            raise Error(field_name=None, message='DELETE not allowed', status=HttpStatus.HTTP_405_METHOD_NOT_ALLOWED)
        if data:  # Update date like editor before delete
            for item in self.get_queryset():
                for k, v in data.items():
                    setattr(item, k, v)
                item.save()
                item.delete()
        return True

    def _get_swaggar_query_parameters(self):
        return '\n'.join([
            '        - in: query\n'
            f'          name: {field.name}\n'
            f'          description: {field.help_text} '
            f'==> Available lookups {[str(a) for a in field.class_lookups]}\n'
            f'          required: false\n'
            '          schema: \n'
            f'            type: {field.description}'
            for field in self.fields_data])

    def swaggar_definition(self):
        rqs = '\n'.join(f'    - {field}' for field in self.required_fields)
        flds = '\n'.join([
            f'      {field.name}:\n'
            f'         type: {field.description}'
            # f'         format:{field}\n' \
            # f'         example:{field}\n' \
            for field in self.fields_data])
        return f'  {self.model_name}Item:\n' \
               '    type: object\n' \
               '    required:\n' \
               f'{rqs}\n' \
               '    properties:\n' \
               f'{flds}'

    def swagger_get(self):
        summary = f'Get a list of filtered {self.model_name}s'
        operation_id = f'search{self.model_name}'
        return '''
    get:
      tags:
        - developers
      summary: {summary}
      operationId: {operation_id}
      description: |
        By passing in the appropriate options, you can search for
        available {model_name} in the system
      parameters:\n{query_parameters}
      responses:
        '200':
          description: search results matching criteria
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/StoryItem'
      '400':
        description: bad input parameter
        '''.format(summary=summary, operation_id=operation_id, model_name=self.model_name,
                   query_parameters=self._get_swaggar_query_parameters())  # TODO

    def swagger_post(self):
        summary = f'Adds item to {self.model_name}s'
        operation_id = f'add{self.model_name}'
        return '''
    post:
      tags:
        - developers
      summary: {summary}
      operationId: {operation_id}
      description: Adds an item to system
      consumes:
      - application/json
      produces:
      - application/json
      parameters:\n{query_parameters}
        - in: body
          name: {model_name}Item
          description: {model_name} item to add
          schema:
            $ref: \'#/definitions/{model_name}Item\'
      responses:
        201:
          description: item created
        400:
          description: invalid input, object invalid
        409:
          description: an existing item already exists
        '''.format(summary=summary, operation_id=operation_id, model_name=self.model_name,
                   query_parameters=self._get_swaggar_query_parameters())

    def swagger_put(self):
        summary = f'Edits item in {self.model_name}s'
        operation_id = f'edit{self.model_name}'
        return '''
    put:
      tags:
        - developers
      summary: {summary}
      operationId: {operation_id}
      description: Edits item in system
      consumes:
      - application/json
      produces:
      - application/json
      parameters:
      - in: body
        name: {model_name}Item
        description: {model_name} item to add
        schema:
          $ref: \'#/definitions/{model_name}Item\'
      responses:
        201:
          description: item created
        400:
          description: invalid input, object invalid
        409:
          description: an existing item already exists
            '''.format(summary=summary, operation_id=operation_id, model_name=self.model_name)

    def swagger_delete(self):
        summary = f'Delete using filters {self.model_name}s'
        operation_id = f'delete{self.model_name}'
        return '''
    delete:
      tags:
        - developers
      summary: {summary}
      operationId: {operation_id}
      description: |
        By passing in the appropriate options, you can search for
        available {model_name} in the system
      parameters:
{parameters}
      responses:
        '204':
          description: search results matching criteria 
        '400':
          description: bad input parameter
        '''.format(summary=summary, operation_id=operation_id, model_name=self.model_name,
                   parameters=self._get_swaggar_query_parameters())  # TODO

    def swagger_doc(self):
        header = '''
openapi: 3.0.0
info:
  description: This is a simple CRUD API for {model_name}
  version: 1.0.0-oas3
  title: {model_name}
  license:
    name: AmeRepos
    url: https://github.com/amerepos

paths:
  /{url_path}:
'''.format(model_name=self.model_name, url_path=self.url_path)
        return f'{header} \n' \
               f'{self.swagger_get()}\n' \
               f'{self.swagger_post()}\n' \
               f'{self.swagger_put()}\n' \
               f'{self.swagger_delete()}\n' \
               f'definitions:\n' \
               f'{self.swaggar_definition()}'

    def _get_html_template(self):
        return '<html><head>' \
               '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.17.0/swagger-ui.css">' \
               '<script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>' \
               '<script>function render() ' \
               '{{var ui = SwaggerUIBundle({{url:\'{model_name}.yaml\',dom_id: \'#swagger-ui\',' \
               'presets: [SwaggerUIBundle.presets.apis,SwaggerUIBundle.SwaggerUIStandalonePreset]}});}}' \
               '</script></head><body onload="render()"><div id="swagger-ui"></div></body></html>'.format(
            model_name=self.model_name)

    @property
    def url_path(self):
        return '{base_app}/{path}'.format(base_app=self.__module__.split('.')[0], path=self.path)

    @property
    def docs_path(self):
        return join(self.__module__.split('.')[0], 'templates/swaggar', self.path, 'doc.html')
        return f'./templates/swaggar/{self.url_path}'

    @property
    def docs_path_to_yaml(self):
        return join(settings.STATIC_ROOT, 'swaggar', self.url_path, 'definition.yaml')
        return f'{self.docs_path}{self.model_name}.html'

    @property
    def docs_path_to_html(self):
        return join(self.__module__.split('.')[0], 'templates/swaggar', self.path, 'doc.html')
        return f'{self.docs_path}doc.html'

    @property
    def template_path(self):
        return f'swaggar/{self.url_path}doc.html'

    def generate_swagger_files(self):
        dr = dirname(self.docs_path_to_yaml)
        if not os.path.exists(dr):
            os.makedirs(dr)
        dr = dirname(self.docs_path_to_html)
        if not os.path.exists(dr):
            os.makedirs(dr)

        with open(self.docs_path_to_yaml, 'w') as f:
            f.write(self.swagger_doc())

        with open(self.docs_path_to_html, 'w') as f:
            f.write(self._get_html_template())