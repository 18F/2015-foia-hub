from django_jinja import library


@library.global_function
def generate_get_req(parameters):
    list_of_params = []
    for param in parameters:
        if param[1]:
            list_of_params.append('{0}={1}'.format(param[0], param[1]))
    return '?%s' % '&'.join(list_of_params)
