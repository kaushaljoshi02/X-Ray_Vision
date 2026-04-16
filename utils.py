def get_doctor(disease):
    return {
        "Pneumonia": "Pulmonologist",
        "COVID": "General Physician",
        "Tuberculosis": "Pulmonologist",
        "Normal": "No Doctor Required"
    }.get(disease, "General Physician")


def get_diet(disease):
    return {
        "Pneumonia": "High protein diet + fluids like orange juice,coconut water,herbal teas,lentils",
        "COVID": "Vitamin C, warm fluids, immunity boosters like soy,nuts,beans,orange",
        "Tuberculosis": "High calorie and protein rich diet like nuts,beans,lentils,avocado",
        "Normal": "Balanced healthy diet"
    }.get(disease, "Healthy diet")


def get_hospitals(location):
    return [
        f"{location} SMS Hospital",
        f"{location} CK Birla Hospital",
        f"{location} Apex Hospital",
        f"{location} Soni Hospital",
        f"{location} Manipal Hospital"
    ]