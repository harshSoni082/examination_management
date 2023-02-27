import tempfile
from collections import OrderedDict

from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.semester.models import SemesterInstance, Semester
from examination_management.grade.models import Grade
from examination_management.batch.models import Batch
from examination_management.branch.models import Branch
from examination_management.subject.models import Subject
from examination_management.student.api.v1.serializers import StudentSerializer, StudentDetailSerializer
from examination_management.student.models import Student
from examination_management.utils.utils import create_empty_excel, create_result_excel, get_roman


def _get_semester_data(semester, branch, batch):
    subjects = {}
    subject_instances = Subject.objects.filter(subject_semester__code=semester)
    semester_number = Semester.objects.get(code=semester).semester
    core_credit = 0
    for subject in subject_instances.all():
        subjects[subject.code] = {
            'name': subject.name,
            'code': subject.code,
            'credit': subject.credit / 1
        }
        if not subject.is_elective:
            core_credit += subject.credit

    students = OrderedDict()
    students_instances = Student.objects.filter(student_semester_instance__semester__code=semester,
                                                branch__code=branch, batch__start=batch).order_by('roll_no')
    for student in students_instances.all():
        # For current semester

        semester_instance = SemesterInstance.objects.get(student__roll_no=student.roll_no,
                                                         semester__code=semester)

        credit = 0
        for subject in semester_instance.semester.subject.all():
            if not subject.is_elective:
                credit += subject.credit
        for elective in semester_instance.elective.all():
            credit += elective.credit

        cg_sum = 0
        grades = OrderedDict()
        reappear = []
        grade_instances = Grade.objects.filter(semester_instance=semester_instance.id)
        for grade in grade_instances.all():
            grades[grade.subject.code] = {
                'grade': grade.grade,
                'score': grade.score / 1
            }
            cg_sum += grade.score

            if grade.grade and grade.grade >= 'F':
                reappear.append(grade.subject.code)
        reappear = ','.join(reappear)
        sgpa = round(cg_sum / credit, 4)

        for subject in subject_instances.all():
            if not grades.get(subject.code, None):
                grades[subject.code] = {
                    'grade': '',
                    'score': 0
                }

        # print(f'############### {semester_instance.sr_no}')
        students[student.roll_no] = {
            'name': student.name,
            'fathers_name': student.fathers_name,
            'roll_no': student.roll_no,
            'grades': grades,
            'total_credit': credit / 1,
            'cg_sum': cg_sum / 1,
            'sgpa': sgpa,
            'reappear': reappear,
            'backlogs': student.backlogs,
            'sr_no': ''
        }

        if semester_number > 4:
            # For previous semesters
            semester_instances = SemesterInstance.objects.filter(student__roll_no=student.roll_no)
            prev_semesters = {}
            total_credits = 0
            cgpa = 0
            for semester_instance in semester_instances.all():
                curr_credit = 0
                sem_no = semester_instance.semester.semester
                curr_sem = Semester.objects.get(code=semester)
                if sem_no > curr_sem.semester:
                    continue
                for subject in semester_instance.semester.subject.all():
                    if not subject.is_elective:
                        curr_credit += subject.credit
                for elective in semester_instance.elective.all():
                    curr_credit += elective.credit

                cg_sum = 0
                grade_instances = Grade.objects.filter(semester_instance=semester_instance.id)
                for grade in grade_instances:
                    cg_sum += grade.score

                total_credits += curr_credit

                sgpa = round(cg_sum / curr_credit, 4)
                cgpa += cg_sum
                year = batch + sem_no // 2
                prev_semesters[sem_no] = {
                    'session': f'Nov./Dec., {year}' if sem_no % 2 else f'May./June., {year}',
                    'roman_sem': get_roman(sem_no),
                    'credit': curr_credit / 1,
                    'sgpa': sgpa,
                }

            students[student.roll_no]['total_credits'] = total_credits / 1
            students[student.roll_no]['cgpa'] = round(cgpa / total_credits, 4)
    students = OrderedDict(sorted(students.items()))
    return subjects, students


class StudentCreateView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Student.objects.get_or_create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class StudentDetailView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        student = Student.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Student with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': StudentDetailSerializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class StudentListView(GenericAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        roll_no = request.GET.get('roll_no', None)
        batch = request.GET.get('batch', None)
        branch = request.GET.get('branch', None)

        queryset = self.get_queryset()
        students = queryset
        if roll_no:
            students = queryset.filter(roll_no=roll_no)
        if batch:
            students = queryset.filter(batch__start=batch)
        if branch:
            students = queryset.filter(branch__code=branch)

        response = {
            'error': False,
            'data': StudentDetailSerializer(students, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class StudentUpdateView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Student.objects.get(id=id)
        if not student:
            response = {
                'error': True,
                'message': f'Student with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student = student.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class StudentDeleteView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        student = Student.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Student with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student.is_deleted = True
        student.save()

        response = {
            'error': False,
            'message': f'Student with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)


class StudentTemplateDownloadView(GenericAPIView):

    def get(self, request):
        with tempfile.NamedTemporaryFile(prefix=f'Student Admission', suffix='.xlsx') as fp:
            create_empty_excel(path=fp.name,
                               columns=['jee_application_no', 'roll_no', 'name', 'fathers_name', 'mothers_name', 'category',
                                        'pwd', 'gender', 'dob', 'state_of_eligibility', 'address', 'is_prep', 'nationality', 'branch',
                                        'allocated', 'mobile', 'email', 'batch', 'remarks'])
            fp.seek(0)
            response = HttpResponse(fp,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Student Admission.xlsx'
            return response


class StudentResultTemplateDownloadView(GenericAPIView):

    def get(self, request):
        semester = request.GET.get('student_semester_instance__semester__code', None)
        branch = request.GET.get('branch__code', None)
        batch = int(request.GET.get('batch__start', None))

        if not (semester and branch and batch):
            return HttpResponseRedirect('../')

        branch_name = Branch.objects.get(code=branch)
        batch_instance = Batch.objects.get(start=batch)
        semester_number = Semester.objects.get(code=semester).semester

        subjects, students = _get_semester_data(semester, branch, batch)

        xlsx_name = f'Result Sheet {semester_number} Semester Batch {batch_instance.start}-{batch_instance.end}'
        with tempfile.NamedTemporaryFile(prefix=xlsx_name, suffix='.xlsx') as fp:
            create_result_excel(fp.name, subjects, students, semester_number, branch_name, batch_instance.start,
                                batch_instance.end)
            fp.seek(0)
            response = HttpResponse(fp,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={xlsx_name}.xlsx'
            return response


class StudentSemesterResultDownloadView(GenericAPIView):

    def get(self, request):
        semester = request.GET.get('student_semester_instance__semester__code', None)
        branch = request.GET.get('branch__code', None)
        batch = int(request.GET.get('batch__start', None))

        if not (semester and branch and batch):
            return HttpResponseRedirect('../')

        branch_name = Branch.objects.get(code=branch)
        batch_instance = Batch.objects.get(start=batch)

        subjects, students = _get_semester_data(semester, branch, batch)
        semester_number = Semester.objects.get(code=semester).semester

        xlsx_name = f'Result Sheet {semester_number} Semester Batch {batch_instance.start}-{batch_instance.end}'
        with tempfile.NamedTemporaryFile(prefix=xlsx_name, suffix='.xlsx') as fp:
            create_result_excel(fp.name, subjects, students, semester_number, branch_name,
                                batch_instance.start, batch_instance.end)
            fp.seek(0)
            response = HttpResponse(fp,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={xlsx_name}.xlsx'
            return response


class SemesterResultTemplateDownloadView(GenericAPIView):

    def get(self, request):
        semester = request.GET.get('student_semester_instance__semester__code', None)
        branch = request.GET.get('branch__code', None)
        batch = int(request.GET.get('batch__start', None))

        if not (semester and branch and batch):
            return HttpResponseRedirect('../')

        semester_number = Semester.objects.get(code=semester).semester
        branch_name = Branch.objects.get(code=branch).branch
        batch_instance = Batch.objects.get(start=batch)
        year = batch + semester_number // 2

        subjects, students = _get_semester_data(semester, branch, batch)
        semester_number = Semester.objects.get(code=semester).semester

        title = f'Final Result Sheet {semester_number} Semester Batch {batch_instance.start}-{batch_instance.end}'
        template_path = 'student/student_semester_result.html'
        context = {
            'subjects': sorted(subjects.items()),
            'students': students,
            'title': title,
            'branch': branch_name,
            'semester': get_roman(semester_number),
            'session': f'Nov./Dec., {year}' if semester_number % 2 else f'May./June., {year}',
            'batch_start': batch_instance.start,
            'batch_end': batch_instance.end
        }
        template = get_template(template_path)

        return HttpResponse(template.render(context))


class StudentDMCDownloadView(GenericAPIView):
    def get(self, request):
        semester = request.GET.get('student_semester_instance__semester__code', None)
        branch = request.GET.get('branch__code', None)
        batch = int(request.GET.get('batch__start', 0)) if request.GET.get('batch__start', None) else None

        if not (semester and branch and batch):
            return HttpResponseRedirect('../')

        subjects, students = _get_semester_data(semester, branch, batch)
        semester_number = Semester.objects.get(code=semester).semester

        title = f'DMC Semester {semester_number} Branch {branch} Batch {batch}.pdf'
        full_branch = Branch.objects.get(code=branch).branch
        year = batch + semester_number // 2

        if semester_number <= 4:
            template_path = 'student/dmc/student_dmc_till_4_sem_template.html'
        else:
            template_path = 'student/dmc/student_dmc_after_4_sem_template.html'
        context = {
            'subjects': sorted(subjects.items()),
            'students': students,
            'title': title,
            'branch': full_branch,
            'semester': get_roman(semester_number),
            'session': f'Nov./Dec., {year}' if semester_number % 2 else f'May./June., {year}',
        }
        template = get_template(template_path)

        return HttpResponse(template.render(context))
