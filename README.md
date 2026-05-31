def registrar_donante():
    tipos_sangre = [
        "A+", "A-",
        "B+", "B-",
        "AB+", "AB-",
        "O+", "O-"
    ]

    nombre = input("Nombre completo: ")
    edad = int(input("Edad: "))
    peso = float(input("Peso (kg): "))

    print("\nTipos de sangre disponibles:")
    for tipo in tipos_sangre:
        print("-", tipo)

    tipo_sangre = input("Tipo de sangre: ").upper()

    while tipo_sangre not in tipos_sangre:
        print("Tipo de sangre inválido.")
        tipo_sangre = input("Tipo de sangre: ").upper()

    telefono = input("Teléfono: ")
    correo = input("Correo electrónico: ")
    ciudad = input("Ciudad: ")

    disponible = input("¿Está disponible para donar? (si/no): ").lower()

    donante = {
        "nombre": nombre,
        "edad": edad,
        "peso": peso,
        "tipo_sangre": tipo_sangre,
        "telefono": telefono,
        "correo": correo,
        "ciudad": ciudad,
        "disponible": disponible
    }

    return donante
