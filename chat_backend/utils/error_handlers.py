

def handle_error_response(serializer):
    errors = {}
    for key, value in serializer.errors.items():
        errors['error'] = True
        errors[key] = str(value[0])
    return errors