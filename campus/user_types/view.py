APP_USER_TYPE_VIEWS = {
    "root" : {},
    "admin": {},
    "accounts_and_info_manager" : {
        "user_type":{"display_at_home":False,},
    },
    "teacher" : {
        "address"     :{"display_at_home":False,},
        "subject_type":{"display_at_home":False,},
    },
    "student" : {
    "address"       :{"display_at_home":False,},
        "school"        :{"display_at_home":False,},
        "subject_type"  :{"display_at_home":False,},
        "exam_type"     :{"display_at_home":False,},
        "subject_x_student": {
            "public": {
                "title": ["Materia", "Materias"],
                "list_item_fields": ["subject"],
            }
        },
        "note_x_student":{
            "public": {
                "title": ["Nota de examen", "Notas de examenes"],
                "list_item_fields": ["exam", "note"],
            }
        }
    },
}