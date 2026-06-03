def registrar_donante():
    tipos_sangre = [
        "A+", "A-",
        "B+", "B-",
        "AB+", "AB-",
        "O+", "O-"
    ]
    nombre = input("nombre completo: ")
    edad = int(input("edad: "))
    peso = float(input("Peso (kg): "))
    print("\nTipos de sangre disponibles:")
    for tipo in tipos_sangre:
        print("-", tipo)
    tipo_sangre = input("tipo de sangre: ").upper()
    while tipo_sangre not in tipos_sangre:
        print("tipo de sangre inválido.")
        tipo_sangre = input("tipo de sangre: ").upper()
    telefono = input("Teléfono: ")
    correo = input("correo electrónico: ")
    ciudad = input("ciudad: ")
    disponible = input("¿está disponible para donar? (si/no): ").lower()
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

donante = registrar_donante()

print("\nDonante registrado:")
for clave, valor in donante.items():
    print(f"{clave}: {valor}")
