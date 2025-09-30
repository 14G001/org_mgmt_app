from app.app.common_elements.user import USER_APP_ELEMENTS
from app.app.common_elements.address import AddressAppElm
from app.app.element import NOTREQ, REQ, AppElm

CAMPUS_APP_ELMS_INFO = USER_APP_ELEMENTS + [
    AddressAppElm("campus"),
    AppElm("school", {
        "private": {
            "model": "campus.School"
        },
        "public": {
            "title": {
                "singular": "Escuela" ,
                "plural"  : "Escuelas",
            },
            "list_item_fields": ["name"],
            "fields": {
                "name"        :[REQ, "str"    , "Nombre"   ],
                "address"     :[REQ, "address", "Dirección"],
            },
        },
    }),
    AppElm("subject_type", {
        "private": {
            "model": "campus.SubjectType"
        },
        "public": {
            "title": {
                "singular": "Tipo de Materia"  ,
                "plural"  : "Tipos de Materias",
            },
            "list_item_fields": ["name"],
            "fields": {
                "name":[REQ, "str", "Nombre"],
            },
        },
    }),
    AppElm("subject", {
        "private": {
            "model": "campus.Subject"
        },
        "public": {
            "title": {
                "singular": "Materia" ,
                "plural"  : "Materias",
            },
            "list_item_fields": ["school", "title"],
            "fields": {
                "school"    :[REQ, "school"      , "Escuela"              ],
                "type"      :[REQ, "subject_type", "Tipo de materia"      ],
                "title"     :[REQ, "str"         , "Título"               ],
                "start_date":[REQ, "date"        , "Fecha de inicio"      ],
                "end_date"  :[REQ, "date"        , "Fecha de finalización"],
            },
        },
    }),
    AppElm("exam_type", {
        "private": {
            "model": "campus.ExamType"
        },
        "public": {
            "title": {
                "singular": "Tipo de Examen" ,
                "plural"  : "Tipos de Examen",
            },
            "list_item_fields": ["value"],
            "fields": {
                "value": [REQ, "str", "Tipo"],
            },
        },
    }),
    AppElm("subject_exam", {
        "private": {
            "model": "campus.SubjectExam",
            "list_item_sort_criteria": ["subject__school__name", "subject__title", "-date"],
        },
        "public": {
            "title": {
                "singular": "Examen"  ,
                "plural"  : "Examenes",
            },
            "list_item_fields": ["subject", "date", "type"],
            "fields": {
                "subject": [REQ, "subject"  , "Materia"       ],
                "type"   : [REQ, "exam_type", "Tipo de examen"],
                "date"   : [REQ, "date"     , "Fecha"         ],
            },
        },
    }),
    AppElm("subject_x_teacher", {
        "private": {
            "model": "campus.SubjectXTeacher"
        },
        "public": {
            "title": {
                "singular": "Materia de docente"  ,
                "plural"  : "Materias de docentes",
            },
            "list_item_fields": ["teacher", "subject"],
            "fields": {
                "subject": [REQ, "subject", "Materia" ],
                "teacher": [REQ, "user"   , "Profesor"],
            },
        },
    }),
    AppElm("subject_x_student", {
        "private": {
            "model": "campus.SubjectXStudent",
            "list_item_sort_criteria": ["student__name", "student__surname"],
        },
        "public": {
            "title": {
                "singular": "Materia de estudiante"  ,
                "plural"  : "Materias de estudiantes",
            },
            "list_item_fields": ["student", "subject"],
            "fields": {
                "subject": [REQ, "subject", "Materia"   ],
                "student": [REQ, "user"   , "Estudiante"],
            },
        },
    }),
    AppElm("note_x_student", {
        "private": {
            "model": "campus.NoteXStudent",
            "list_item_sort_criteria": ["student__name", "student__surname", "exam__subject__title", "-exam__date"],
        },
        "public": {
            "title": {
                "singular": "Nota de alumno"  ,
                "plural"  : "Notas de alumnos",
            },
            "list_item_fields": ["student", "exam", "note"],
            "fields": {
                "exam"   : [REQ, "subject_exam", "Examen"    ],
                "student": [REQ, "user"        , "Estudiante"],
                "note"   : [REQ, "int"         , "Nota"      ],
            },
        },
    }),
    AppElm("class_attendance", {
        "private": {
            "model": "campus.ClassAttendance",
            "list_item_sort_criteria": [
                "subject_x_student__student__name", "subject_x_student__student__surname",
                "subject_x_student__subject__title", "-date"],
        },
        "public": {
            "title": {
                "singular": "Asistencia de alumno"  ,
                "plural"  : "Asistencias de alumnos",
            },
            "list_item_fields": ["subject_x_student", "date"],
            "fields": {
                "subject_x_student": [REQ, "subject_x_student", "Materia de alumno"],
                "date"             : [REQ, "date"             , "Fecha"            ],
            },
        },
    }),
]