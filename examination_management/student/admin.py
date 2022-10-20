from django.contrib import admin
from django.contrib.admin import display
from django.urls import path
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from examination_management.batch.models import Batch
from examination_management.branch.models import Branch
from examination_management.student.api.v1.views import StudentTemplateDownloadView
from examination_management.student.models import Student


class StudentResource(resources.ModelResource):
    batch = fields.Field(column_name='batch', attribute='batch', widget=ForeignKeyWidget(Batch, 'start'))
    branch = fields.Field(column_name='branch', attribute='branch', widget=ForeignKeyWidget(Branch, 'code'))

    class Meta:
        model = Student
        exclude = ('id',)
        import_id_fields = ('roll_no',)


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    # model = Student
    list_display = ('name', 'roll_no',)
    list_filter = ('branch__code', 'batch__start',)

    change_list_template = 'student/student_change_list.html'

    def branch__code(self, obj):
        return obj.branch.code

    def batch__start(self, obj):
        return obj.batch.start

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('download/', StudentTemplateDownloadView.as_view(), name='student_template_download'),
        ]
        return admin_urls + urls
