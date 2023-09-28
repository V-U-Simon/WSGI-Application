import os
import sqlite3
from typing import TypeVar
from framework_wsgi.design_patterns import connector
from framework_wsgi.design_patterns.repository import SQLiteRepository
from framework_wsgi.http import Response, Request
from framework_wsgi.templator import render, TemplateEngineHTML, TemplateEngine
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork


connection = connector.ConnectorDB.connect()
uow = SQLiteUnitOfWork(connection)


# pattern: template method, CBV
class View:
    def get(self, request, *args, **kwargs) -> Response:
        pass

    def post(self, request, *args, **kwargs) -> Response:
        pass


class TemplateView(View):
    template_name = "template.html"
    template_engine: TemplateEngine = TemplateEngineHTML

    def get(self, request: Request, *args, **kwargs) -> Response:
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


# class ListView(TemplateView):
#     model: T | None = None
#     queryset = []
#     context_object_name = "object_list"
#     template_name = (
#         "list_" + model.__name__.lower() or type(queryset[0]).__name__.lower()
#     )

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context[self.context_object_name] = self.repository.all()
#         return context


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


# # Корректная транзакция
# with uow as repo:
#     users = repo(Users).all()
#     print(users)

#     user = Users(name="Mike")
#     repo.save(user)
#     print(f"{user}")

#     user.name = "Mikki"
#     repo.save(user)
#     print(f"{user}")

#     users = repo(Users).all()
#     print(users)

#     repo.delete(user)
#     print(f"{user}")
