# Pattern: page_controllers

from framework_wsgi import views
from framework_wsgi.http.response import Response

from framework_wsgi.design_patterns.connector import ConnectorDB
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
from framework_wsgi.design_patterns.domain_courses import Categories


class CategoryListView(views.ListView):
    model = Categories
    template_name = "categories/category_list.html"


class CategoryDetailView(views.DetailView):
    model = Categories
    template_name = "categories/category_detail.html"


class CategoryCreateView(views.CreateView):
    model = Categories
    template_name = "categories/category_form.html"
    success_url = "/categories/"

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            categories = repo(Categories).all()
        context.update({"categories": categories})
        return context


class CategoryUpdateView(views.UpdateView):
    model = Categories
    template_name = "categories/category_form.html"
    success_url = "/categories/"

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            categories = repo(Categories).all()
            categories = [
                c for c in categories if c.id != int(self.request.kwargs["id"])
            ]
        context.update({"categories": categories})
        return context


class CategoryDeleteView(views.DeleteView):
    model = Categories
    template_name = "categories/category_delete.html"
    success_url = "/categories/"
