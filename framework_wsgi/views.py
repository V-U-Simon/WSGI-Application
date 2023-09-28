import os
import sqlite3
from typing import TypeVar
from framework_wsgi.design_patterns.connector import ConnectorDB
from framework_wsgi.design_patterns.repository import SQLiteRepository
from framework_wsgi.http import Response, Request
from framework_wsgi.templator import render, TemplateEngineHTML, TemplateEngine
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork


# connection = ConnectorDB.connect()
uow = SQLiteUnitOfWork(ConnectorDB)


# pattern: template method, CBV
class View:
    def get(self, request, *args, **kwargs) -> Response:
        self.request = request

    def post(self, request, *args, **kwargs) -> Response:
        self.request = request


class TemplateView(View):
    template_name = "template.html"
    template_engine: TemplateEngine = TemplateEngineHTML

    def get(self, request: Request, *args, **kwargs) -> Response:
        super().get(request, *args, **kwargs)
        return self.render_to_response(request, *args, **kwargs)

    def render_to_response(self, request, *args, **kwargs):
        template_name = self.get_template()
        context = self.get_context_data()
        TemplateEngine = self.get_template_engine()

        template_engine = TemplateEngine(
            request=request,
            template_name=template_name,
            context=context,
        )
        str_body = template_engine.render()
        return Response(request=request, body=str_body)

    def get_template(self):
        return self.template_name

    def get_template_engine(self) -> TemplateEngine:
        return self.template_engine

    def get_context_data(self):
        return {}


T = TypeVar("T")


class ListView(TemplateView):
    model: T | None = None
    template_name = "list_template.html"
    queryset = []
    context_object_name = "object_list"

    def get_queryset(self):
        if self.model:
            with uow as repo:
                qs = repo(self.model).all()
                return qs

        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self) -> dict:
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


# class ListView(TemplateView):
#     queryset = []
#     template_name = "list.html"
#     context_object_name = "objects_list"

#     def get_queryset(self):
#         return self.queryset

#     def get_context_object_name(self):
#         return self.context_object_name

#     def get_context_data(self):
#         queryset = self.get_queryset()
#         context_object_name = self.get_context_object_name()
#         context = {context_object_name: queryset}
#         return context


def page_not_found(request) -> Response:
    response = render(request, "page_not_found.html")
    response.status = "404 Not Found"
    return response
