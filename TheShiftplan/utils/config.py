dummy_username = "NOT ASSIGNED"

code_to_file_dict = {
    "forename": ["forename", "vorname", "first name"],
    "surname": ["surname", "nachname", "last name"],
    "email": ["email", "e-mail", "mail"]
}


def vals_to_keys(d):
    vtk_dict = {}
    for key in d:
        for val in d[key]:
            vtk_dict[val] = key
    return vtk_dict

file_to_code_dict =  vals_to_keys(code_to_file_dict)

