from campus.models import (Address, School, SubjectType,
    Subject, ExamType, SubjectExam, NoteXStudent, SubjectXTeacher,
    SubjectXStudent, ClassAttendance, Form, FormFieldType, FormField,)
from app.apps.info import EXAMPLE_APP_INDICATOR
from app.test_values.utils import create_models
from app.test_values.user import create_test_user

def create_test_subjects_x_item(item_type, subjects, item):
    test_subjects_x_item = []
    for subject in subjects:
        test_subjects_x_item.append(
            {"subject":subject, item_type:item})
    return test_subjects_x_item
def create_test_subject_x_student(app, subjects, students):
    subject_x_student = create_models(app, SubjectXStudent, 
          create_test_subjects_x_item("student", subjects[ :3], students[0])
        + create_test_subjects_x_item("student", subjects[ :6], students[1])
        + create_test_subjects_x_item("student", subjects[3:9], students[2])
        + create_test_subjects_x_item("student", subjects[9: ], students[3]))
    test_stdt_clss_atdc = []
    test_student_notes = []
    for subj_x_stdt in subject_x_student:
        for month in range(6, 8):
            for week in range(0, 3):
                for day in range(1, 6):
                    test_stdt_clss_atdc.append({
                        "subject_x_student":subj_x_stdt,
                        "date":("2025"
                            + f"-{str(month).rjust(2,"0")}"
                            + f"-{str((week*7)+day).rjust(2,"0")}")})
        for exam in subj_x_stdt.subject.exams.all():
            test_student_notes.append(
                {"exam":exam, "student":subj_x_stdt.student, "note":7})
    class_attendances = create_models(app, ClassAttendance, test_stdt_clss_atdc)
    note_x_student = create_models(app, NoteXStudent, test_student_notes)
    return subject_x_student

def init_campus_db_test_values(app):
    is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
    if (not is_example_app
        or Address.objects.using(app).exists()):
        return
    
    usr_root      = create_test_user(app, "root"                     , "test_root"     , "CRoot"  )
    usr_admin     = create_test_user(app, "admin"                    , "test_admin"    , "CAdmin" )
    usr_accinfmgr = create_test_user(app, "accounts_and_info_manager", "test_accinfmgr", "CGestor")
    teacher_users = [
        create_test_user(app, "teacher", "test_teacher1", "PJuan" ),
        create_test_user(app, "teacher", "test_teacher2", "PLucía"),
    ]
    student_users = [
        create_test_user(app, "student", "test_student1", "AJose"  ),
        create_test_user(app, "student", "test_student2", "AAlma"  ),
        create_test_user(app, "student", "test_student3", "AJulian"),
        create_test_user(app, "student", "test_student4", "ASofia" ),
    ]

    addresses = create_models(app, Address, [
        {"street_address1":"San Martin 2382"     , "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
        {"street_address1":"Yrigoyen 1395"       , "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
        {"street_address1":"Belgrano 1630"       , "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
        {"street_address1":"Bartolomé Mitre 3164", "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
        {"street_address1":"Juana Azurduy 1877"  , "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
    ])
    schools = create_models(app, School, [{"address":addresses[school_num], "name":f"Escuela N{school_num}"} for school_num in range(0, len(addresses))])
    subject_type = create_models(app, SubjectType, [
        {"name":"Matemática"        },
        {"name":"Lengua"            },
        {"name":"Biología"          },
        {"name":"Química"           },
        {"name":"Historia"          },
        {"name":"Ciencias Sociales" },
        {"name":"Ciencias Naturales"},
        {"name":"Arte"              },
    ])
    test_subjects = []
    for school in schools[:2]:
        test_subjects += [
            {"title":"Matematica 4to grado 2025", "type":subject_type[0], "school":school, "start_date":"2025-03-11", "end_date":"2025-12-15"},
            {"title":"Matematica 5to grado 2025", "type":subject_type[0], "school":school, "start_date":"2025-03-11", "end_date":"2025-12-15"},
            {"title":"Lengua 4to grado 2025"    , "type":subject_type[1], "school":school, "start_date":"2025-03-11", "end_date":"2025-12-15"},
            {"title":"Lengua 5to grado 2025"    , "type":subject_type[1], "school":school, "start_date":"2025-03-11", "end_date":"2025-12-15"},
            {"title":"Biología 4to grado 2025"  , "type":subject_type[2], "school":school, "start_date":"2025-03-11", "end_date":"2025-12-15"},
            {"title":"Biología 5to grado 2025"  , "type":subject_type[2], "school":school, "start_date":"2025-03-11", "end_date":"2025-12-15"},
        ]
    subjects = create_models(app, Subject, test_subjects)
    exam_types = create_models(app, ExamType, [
        {"value":"Examen"          },
        {"value":"Trabajo Práctico"},
        {"value":"Recuperatorio"   },
    ])
    test_subject_exams = []
    for subject in subjects:
        test_subject_exams += [
            {"subject":subject, "type":exam_types[0], "date":"2025-05-10"},
            {"subject":subject, "type":exam_types[1], "date":"2025-08-10"},
            {"subject":subject, "type":exam_types[0], "date":"2025-09-10"},
            {"subject":subject, "type":exam_types[2], "date":"2025-09-20"},
        ]
    subject_exams = create_models(app, SubjectExam, test_subject_exams)
    subject_x_teacher = create_models(app, SubjectXTeacher,
          create_test_subjects_x_item("teacher", subjects[:5], teacher_users[0])
        + create_test_subjects_x_item("teacher", subjects[4:], teacher_users[1]))
    subject_x_student = create_test_subject_x_student(app, subjects, student_users)
    