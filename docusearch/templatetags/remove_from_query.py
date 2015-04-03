from django.http import QueryDict
from django_jinja import library


@library.global_function
def remove_from_query(query_string, remove_list):

    query = QueryDict(query_string, mutable=True)

    for item in remove_list:
        if query.get(item):
            del query[item]

    return query.urlencode()
