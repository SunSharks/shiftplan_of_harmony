import json

def json_to_python(json_str):
    """
    Converts json string to corresponding python data structure and returns it.
    @param json_str: [str] json formatted string. 
    """
    return json.load(json_str)

def create_instance_from_dict(model, instance_dict):
    instance = model()
    for k, v in instance_dict.items():
        setattr(instance, k, v)
    instance.save()


def create_instances_from_list_of_dicts(model, instance_dict_list):
    instance = model()
    for inst in instance_dict_list:
        create_instance_from_dict(model, inst)