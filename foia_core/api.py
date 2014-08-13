from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from foia_core.models import *


class AgencyResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'abbreviation': 'abbreviation',
        'description': 'description',
        'slug': 'slug',
    })

    # GET /
    def list(self):
        return Agency.objects.all()


class OfficeResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'slug': 'slug',

        'service_center': 'service_center',
        'fax': 'fax',

        'request_form': 'request_form',
        'website': 'website',
        'emails': 'emails',

        'contact': 'contact',
        'contact_phone': 'contact_phone',
        'public_liaison': 'public_liaison',

        'notes': 'notes',
    })

    # GET /
    def list(self, slug):
        return Office.objects.filter(agency__slug=slug)


class FOIARequestResource(DjangoResource):

    preparer = FieldsPreparer(fields={
        'status': 'status',
        'requester': 'requester',
        'date_start': 'date_start',
        'date_end': 'date_end',
        'fee_limit': 'fee_limit',
        'request_body': 'request_body',
        'custom_fields': 'custom_fields',
        'agency': 'agency',
    })

    # POST /
    def create(self):

        office = Office.objects.get(
            agency__slug=self.data['agency'],
            slug=self.data['office'],
        )

        requester = Requester.objects.create(
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
            email=self.data['email']
        )

        return FOIARequest.objects.create(
            status='O',
            requester = requester,
            office = office,
            date_start=self.data['date_start'],
            date_end=self.data['data_end'],
            request_body=self.data['request_body'],
            custom_fields=self.data['custom_fields'],
        )

    # GET /
    def list(self):
        return FOIARequest.objects.all()

    # Open everything wide!
    # DANGEROUS, DO NOT DO IN PRODUCTION.
    # more info here: https://github.com/toastdriven/restless/blob/master/docs/tutorial.rst
    def is_authenticated(self):
        return True


# class PostResource(DjangoResource):
#     # Controls what data is included in the serialized output.
#     preparer = Preparer(fields={
#         'id': 'id',
#         'title': 'title',
#         'author': 'user.username',
#         'body': 'content',
#         'posted_on': 'posted_on',
#     })

#     # GET /
#     def list(self):
#         return Post.objects.all()

#     # GET /pk/
#     def detail(self, pk):
#         return Post.objects.get(id=pk)

#     # POST /
#     def create(self):
#         return Post.objects.create(
#             title=self.data['title'],
#             user=User.objects.get(username=self.data['author']),
#             content=self.data['body']
#         )

#     # # PUT /pk/
#     # def update(self, pk):
#     #     try:
#     #         post = Post.objects.get(id=pk)
#     #     except Post.DoesNotExist:
#     #         post = Post()

#     #     post.title = self.data['title']
#     #     post.user = User.objects.get(username=self.data['author'])
#     #     post.content = self.data['body']
#     #     post.save()
#     #     return post

#     # # DELETE /pk/
#     # def delete(self, pk):
#     #     Post.objects.get(id=pk).delete()
