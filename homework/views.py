# -*- coding: utf-8 -*- !!!Задание выполнил Шевченко Глеб!!!
from copy import copy
from statistics import mean
from typing import List

from django.views.generic.base import TemplateView

data = [
        {
            'id': 1,
            'fio': 'Albert Sonw',
            'Drawing': 2,
            'Geometry': 3,
            'Philosophy': 4,
            'English': 5,
            'Technology': 3
        },
        {
            'id': 2,
            'fio': 'Gusw Linht',
            'Drawing': 5,
            'Geometry': 3,
            'Philosophy': 5,
            'English': 4,
            'Technology': 5
        },
        {
            'id': 3,
            'fio': 'Oparet Tonivich',
            'Drawing': 3,
            'Geometry': 2,
            'Philosophy': 3,
            'English': 3,
            'Technology': 4
        },
        {
            'id': 4,
            'fio': 'Loti RewAci',
            'Drawing': 5,
            'Geometry': 5,
            'Philosophy': 5,
            'English': 5,
            'Technology': 5
        }
    ]

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        generator = EntityGenerator(data)
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            {
                'students_statistics': generator.get_statistics(),
                'excellent_students': generator.get_excellent_students(),
                'bad_students': generator.get_bad_students()
            }
        )
        return context

class EntityGenerator:


    def __init__(self, data):
        self.data = data
        self.statistics = Statistics()
        for s_data in self.data:
            scores = [Score(key, value) for key, value in s_data.items() if key not in ('id', 'fio')]
            self.statistics.set_student_scores(Student(s_data['id'], s_data['fio']), scores)

    def get_students(self):
        return '; '.join(self.statistics.get_students())

    def get_statistics(self):
        for s_data in self.data:
            s_data['average'] = self.statistics.get_average_score(Student(s_data['id'], s_data['fio']))
        return self.data

    def get_excellent_students(self):
        return '; '.join(self.statistics.get_excellent())

    def get_bad_students(self):
        return '; '.join(self.statistics.get_bad())



class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'student'({self.name})

class Statistics:
    # student_id, [Scores]
    def __init__(self):
        self.stat = dict()

    def set_student_scores(self, student, scores):
        self.stat[student] = scores

    def get_student_scores(self, student):
        return self.stat.get(student, [])

    def get_students(self):
        return self.stat.keys()

    def get_average_score(self, student):
        student_scores = self.get_student_scores(student)
        return mean((score.value for score in student_scores))

    def get_excellent(self):
        result = [student.name for student in self.get_students() if self.get_average_score(student) >= 4.5]
        return result

    def get_bad(self):
        return [student.name for student in self.get_students() if self.get_average_score(student) <= 3]

class Score:
    # Subject, value
    def __init__(self, subject, value):
        self.subject = subject
        self.value = value