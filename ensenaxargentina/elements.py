from app.app.common_elements.user import USER_APP_ELEMENTS
from app.app.common_elements.common_elements import AddressAppElm
from app.app.element import NOTREQ, REQ, AppElm

EXA_APP_ELMS_INFO = USER_APP_ELEMENTS + [
    AddressAppElm("ensenaxargentina"),
    AppElm("school", {
        "private": {
            "model": "ensenaxargentina.School"
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
            "model": "ensenaxargentina.SubjectType"
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
            "model": "ensenaxargentina.Subject"
        },
        "public": {
            "title": {
                "singular": "Materia" ,
                "plural"  : "Materias",
            },
            "list_item_fields": ["title", "school"],
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
            "model": "ensenaxargentina.ExamType"
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
            "model": "ensenaxargentina.SubjectExam"
        },
        "public": {
            "title": {
                "singular": "Examen"  ,
                "plural"  : "Examenes",
            },
            "list_item_fields": ["subject", "type", "date"],
            "fields": {
                "subject": [REQ, "subject"  , "Materia"       ],
                "type"   : [REQ, "exam_type", "Tipo de examen"],
                "date"   : [REQ, "date"     , "Fecha"         ],
            },
        },
    }),
    AppElm("note_x_student", {
        "private": {
            "model": "ensenaxargentina.NoteXStudent"
        },
        "public": {
            "title": {
                "singular": "Nota de alumno"  ,
                "plural"  : "Notas de alumnos",
            },
            "list_item_fields": ["exam", "student", "note"],
            "fields": {
                "exam"   : [REQ, "subject_exam"   , "Examen"    ],
                "student": [REQ, "student", "Estudiante"],
                "note"   : [REQ, "int"    , "Nota"      ],
            },
        },
    }),
    AppElm("subject_x_teacher", {
        "private": {
            "model": "ensenaxargentina.SubjectXTeacher"
        },
        "public": {
            "title": {
                "singular": "Materia por docente"  ,
                "plural"  : "Materias por docentes",
            },
            "list_item_fields": ["subject", "teacher"],
            "fields": {
                "subject": [REQ, "subject", "Materia" ],
                "teacher": [REQ, "user"   , "Profesor"],
            },
        },
    }),
    AppElm("subject_x_student", {
        "private": {
            "model": "ensenaxargentina.SubjectXStudent"
        },
        "public": {
            "title": {
                "singular": "Materia por estudiante"  ,
                "plural"  : "Materias por estudiantes",
            },
            "list_item_fields": ["subject", "student"],
            "fields": {
                "subject": [REQ, "subject", "Materia"   ],
                "student": [REQ, "user"   , "Estudiante"],
            },
        },
    }),
    AppElm("class_attendance", {
        "private": {
            "model": "ensenaxargentina.ClassAttendance"
        },
        "public": {
            "title": {
                "singular": "Asistencia de estudiante"  ,
                "plural"  : "Asistencias de estudiantes",
            },
            "list_item_fields": ["subject_x_student", "date"],
            "fields": {
                "subject_x_student": [REQ, "subject_x_student", "Materia"],
                "date"             : [REQ, "date"             , "Fecha"  ],
            },
        },
    }),
]