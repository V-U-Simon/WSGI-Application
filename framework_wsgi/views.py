import os
import sqlite3

from typing import TypeVar, Optional, List
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
        context.update(**kwargs)
        TemplateEngine: TemplateEngine = self.get_template_engine()

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

    def get_context_data(self) -> dict:
        return {}


T = TypeVar("T")


class ModelAndQuerySet:
    model: T | None = None

    def get_queryset(self):
        if self.model:
            with uow as repo:
                qs = repo(self.model).all()
                return qs
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name


class ListView(ModelAndQuerySet, TemplateView):
    model: T | None = None
    template_name = "template_list.html"
    queryset = []
    context_object_name = "object_list"

    def get_context_data(self) -> dict:
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class DetailView(ModelAndQuerySet, TemplateView):
    model: T | None = None
    template_name = "template_detail.html"
    object_id: Optional[int] = "id"
    queryset: List[T] = []
    context_object_name = "object"

    def get_object_id(self):
        object_id = self.request.kwargs.get(self.object_id, None)
        return int(object_id)

    def get_object(self):
        queryset = self.get_queryset()
        object_id = self.get_object_id()

        if queryset and object_id:
            return next((item for item in queryset if item.id == object_id), None)
        raise Exception("QuerySet or object_id not found")

    def get_context_data(self) -> dict:
        obj = self.get_object()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: obj}
        return context


from typing import Any, Dict


class CreateView(TemplateView):
    model: T | None = None
    template_name = "template_form.html"
    context_object_name = "form"
    success_url = "/courses/"

    def post(self, request: Request, *args, **kwargs) -> Response:
        # Замените на ваш метод для получения данных формы
        form_data: dict = self.prepare_form_data(request)
        response = self.process_form_data(request, form_data)
        return response

    def prepare_form_data(self, request: Request) -> dict:
        return request.POST

    def process_form_data(self, request, form_data) -> Response:
        # valid form
        try:
            with uow as repo:
                obj = self.model(**form_data)
                repo.save(obj)
            return Response(request).redirect(self.success_url)
        # invalid form
        except Exception:
            template_name = self.get_template()
            context = self.get_context_data()
            context.update({"form": form_data})
            context.update({"excpt": "Someting going wrong. Try again."})

            TemplateEngine: TemplateEngine = self.get_template_engine()

            template_engine = TemplateEngine(
                request=request,
                template_name=template_name,
                context=context,
            )
            str_body = template_engine.render()
            return Response(request=request, body=str_body)


def page_not_found(request) -> Response:
    response = render(request, "page_not_found.html")
    response.status = "404 Not Found"
    return response
