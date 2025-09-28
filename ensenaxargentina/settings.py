from user.permissons import get_admin_permissons
from ensenaxargentina.elements import EXA_APP_ELMS_INFO
from django.db.models import Q

def get_ensenaxargentina_app_info():
    return {
        "title":"Enseñá X Argentina Campus",
        "user_types": {
            "admin": {
                "title": "Admin",
                "permissons": get_admin_permissons(EXA_APP_ELMS_INFO)
            },
            "accounts_and_info_manager" : {
                "title": "Gestión de cuentas y información",
                "permissons": {
                    "user"   : {"actions":"cru", "user_filter":"id", "filter":Q(type__value__in=["teacher","student"])},
                    "address": {"actions": "cru"},
                    "school" : {"actions": "cru"},
                }
            },
            "teacher" : {
                "title": "Profesor",
                "permissons": {
                    "user"             : {"actions":"r", "user_filter":"id", "filter":Q(type__value="student")},
                    "address"          : {"actions":"r"  },
                    "school"           : {"actions":"r"  },
                    "subject_type"     : {"actions":"cru"},
                    "subject"          : {"actions":"cru"},
                    "exam_type"        : {"actions":"cru"},
                    "subject_exam"     : {"actions":"cru" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_teacher": {"actions":"cru" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_student": {"actions":"cru" , "user_filter":"subject__teachers__teacher"      },
                    "class_attendance" : {"actions":"crud", "user_filter":"subject_x_student__subject__teachers__teacher"},
                    "note_x_student"   : {"actions":"cru" , "user_filter":"exam__subject__teachers__teacher"},
                }
            },
            "student" : {
                "title": "Alumno",
                "permissons": {
                    "user"             : {"actions":"r", "user_filter":"id"                },
                    "address"          : {"actions":"r", "user_filter":"schools__subjects__students"},
                    "school"           : {"actions":"r", "user_filter":"subjects__students"},
                    "subject_type"     : {"actions":"r", "user_filter":"subjects__students"},
                    "subject"          : {"actions":"r", "user_filter":"students"          },
                    "exam_type"        : {"actions":"r", "user_filter":"exams__subject__students"   },
                    "subject_exam"     : {"actions":"r", "user_filter":"subject__students" },
                    "subject_x_teacher": {"actions":"r", "user_filter":"subject__students" },
                    "subject_x_student": {"actions":"r", "user_filter":"student"           },
                    "class_attendance" : {"actions":"r", "user_filter":"subject_x_student__student" },
                    "note_x_student"   : {"actions":"r", "user_filter":"student"           },
                }
            },
        }
    }
