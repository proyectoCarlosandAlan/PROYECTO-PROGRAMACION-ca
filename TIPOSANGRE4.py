import tkinter as tk
#NO EDITAR NADA DE ESTEEEEEEEEEEEEEEEE

from tkinter import messagebox, ttk

TIPOS_SANGRE = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
SI_NO = ["si", "no"]
FACTORES_RH = ["+", "-"]
COMPATIBILIDAD = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "AB-": ["A-", "B-", "AB-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"]
}
donantes = []


def limpiar_formulario():
    nombre_var.set("")
    edad_var.set("")
    sexo_var.set("H")
    curp_var.set("")
    telefono_var.set("")
    correo_var.set("")
    direccion_var.set("")
    tipo_sangre_var.set(TIPOS_SANGRE[0])
    factor_rh_var.set("+")
    peso_var.set("")
    ultima_donacion_var.set("")
    embarazada_var.set("no aplica")
    enfermedades_var.set("no")
    cirugias_var.set("no")
    tatuajes_var.set("no")
    medicamentos_var.set("no")
    alcohol_var.set("no")
    disponible_var.set("si")
    fecha_registro_var.set("")
    actualizar_embarazo()


def actualizar_embarazo():
    if sexo_var.get() == "M":
        label_embarazo.grid(row=embarazo_row, column=0, sticky="w", padx=10, pady=4)
        menu_embarazo.grid(row=embarazo_row, column=1, sticky="ew", padx=10, pady=4)
        embarazada_var.set("si")
    else:
        label_embarazo.grid_remove()
        menu_embarazo.grid_remove()
        embarazada_var.set("no aplica")


def registrar_donante_gui():
    try:
        edad = int(edad_var.get())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor valido para la edad.")
        return

    try:
        peso = float(peso_var.get())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor valido para el peso.")
        return

    if sexo_var.get() not in ["H", "M"]:
        messagebox.showerror("Error", "Seleccione H para hombre o M para mujer.")
        return

    donante = {
        "nombre": nombre_var.get().strip(),
        "edad": edad,
        "sexo": sexo_var.get(),
        "curp": curp_var.get().strip(),
        "telefono": telefono_var.get().strip(),
        "correo": correo_var.get().strip(),
        "direccion": direccion_var.get().strip(),
        "tipo_sangre": tipo_sangre_var.get(),
        "factor_rh": factor_rh_var.get(),
        "peso": peso,
        "ultima_donacion": ultima_donacion_var.get().strip(),
        "embarazada_lactando": embarazada_var.get(),
        "enfermedades": enfermedades_var.get(),
        "cirugias": cirugias_var.get(),
        "tatuajes": tatuajes_var.get(),
        "medicamentos": medicamentos_var.get(),
        "alcohol": alcohol_var.get(),
        "disponible": disponible_var.get(),
        "fecha_registro": fecha_registro_var.get().strip(),
    }

    razones_no = []
    if edad < 18:
        razones_no.append("Edad menor a 18 años")
    if donante["enfermedades"] == "si":
        razones_no.append("Tiene una enfermedad que impide donar")
    if donante["tatuajes"] == "si":
        razones_no.append("Se tatuó hace menos de un año")
    if donante["medicamentos"] == "si":
        razones_no.append("Tomó medicamento en las últimas 48 horas")
    if donante["alcohol"] == "si":
        razones_no.append("Tomó alcohol en las últimas 48 horas")
    if donante["disponible"] == "no":
        razones_no.append("No está disponible para donar")

    if razones_no:
        donante["disponible"] = "no"
        estado = "No disponible para donar: " + "; ".join(razones_no)
    else:
        estado = "Disponible para donar."

    resumen = "Donante registrado:\n"
    for clave, valor in donante.items():
        resumen += f"{clave}: {valor}\n"
    resumen += f"\nEstado: {estado}"

    donantes.append(donante)
    messagebox.showinfo("Registro completado", resumen)
    limpiar_formulario()


def buscar_donante_receptor():
    tipo_necesitado = receptor_tipo_var.get()
    compatibles = COMPATIBILIDAD.get(tipo_necesitado, [])
    disponibles = [d for d in donantes if d["tipo_sangre"] in compatibles and d["disponible"] != "no"]

    if not disponibles:
        resultado_receptor.config(text="No hay donantes disponibles para este tipo de sangre.")
        return

    texto = f"Donantes compatibles para {tipo_necesitado}:\n\n"
    for d in disponibles:
        texto += "-------------------------\n"
        for clave, valor in d.items():
            texto += f"{clave}: {valor}\n"
        texto += "\n"

    resultado_receptor.config(text=texto)


root = tk.Tk()
root.title("Registro de Donantes y Receptores")
root.configure(bg="#e6f7ff")
root.geometry("700x900")
root.minsize(700, 760)
root.resizable(True, True)

notebook = ttk.Notebook(root)
frame_donante = ttk.Frame(notebook)
frame_receptor = ttk.Frame(notebook)
notebook.add(frame_donante, text="Donante")
notebook.add(frame_receptor, text="Receptor")
notebook.pack(expand=True, fill="both")

canvas = tk.Canvas(frame_donante, bg="#e6f7ff", highlightthickness=0)
scrollbar = tk.Scrollbar(frame_donante, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas, bg="#e6f7ff")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollable_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

nombre_var = tk.StringVar()
edad_var = tk.StringVar()
sexo_var = tk.StringVar(value="H")
curp_var = tk.StringVar()
telefono_var = tk.StringVar()
correo_var = tk.StringVar()
direccion_var = tk.StringVar()
tipo_sangre_var = tk.StringVar(value=TIPOS_SANGRE[0])
factor_rh_var = tk.StringVar(value="+")
peso_var = tk.StringVar()
ultima_donacion_var = tk.StringVar()
embarazada_var = tk.StringVar(value="no aplica")
enfermedades_var = tk.StringVar(value="no")
cirugias_var = tk.StringVar(value="no")
tatuajes_var = tk.StringVar(value="no")
medicamentos_var = tk.StringVar(value="no")
alcohol_var = tk.StringVar(value="no")
disponible_var = tk.StringVar(value="si")
fecha_registro_var = tk.StringVar()
receptor_tipo_var = tk.StringVar(value=TIPOS_SANGRE[0])
receptor_nombre_var = tk.StringVar()
receptor_telefono_var = tk.StringVar()
receptor_correo_var = tk.StringVar()
receptor_ciudad_var = tk.StringVar()

row = 0
fields = [
    ("Nombre completo:", nombre_var),
    ("Edad:", edad_var),
    ("CURP (opcional):", curp_var),
    ("Telefono:", telefono_var),
    ("Correo electronico:", correo_var),
    ("Direccion:", direccion_var),
]

for texto, variable in fields:
    tk.Label(scrollable_frame, text=texto, bg="#e6f7ff", fg="#003366", font=("Arial", 11)).grid(row=row, column=0, sticky="w", padx=10, pady=4)
    tk.Entry(scrollable_frame, textvariable=variable, width=40).grid(row=row, column=1, padx=10, pady=4)
    row += 1

label_sexo = tk.Label(scrollable_frame, text="Sexo:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_sexo.grid(row=row, column=0, sticky="w", padx=10, pady=4)
frame_sexo = tk.Frame(scrollable_frame, bg="#e6f7ff")
frame_sexo.grid(row=row, column=1, sticky="w", padx=10, pady=4)
for valor, texto in [("H", "Hombre"), ("M", "Mujer")]:
    tk.Radiobutton(frame_sexo, text=texto, variable=sexo_var, value=valor, bg="#e6f7ff", fg="#003366", selectcolor="#e6f7ff", command=actualizar_embarazo).pack(side="left", padx=8)
row += 1

label_tipo_sangre = tk.Label(scrollable_frame, text="Tipo de sangre:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_tipo_sangre.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, tipo_sangre_var, *TIPOS_SANGRE).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_factor_rh = tk.Label(scrollable_frame, text="Factor Rh:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_factor_rh.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, factor_rh_var, *FACTORES_RH).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_peso = tk.Label(scrollable_frame, text="Peso (kg):", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_peso.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.Entry(scrollable_frame, textvariable=peso_var, width=40).grid(row=row, column=1, padx=10, pady=4)
row += 1

label_ultima_donacion = tk.Label(scrollable_frame, text="Fecha de ultima donacion:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_ultima_donacion.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.Entry(scrollable_frame, textvariable=ultima_donacion_var, width=40).grid(row=row, column=1, padx=10, pady=4)
row += 1

embarazo_row = row
label_embarazo = tk.Label(scrollable_frame, text="¿Esta embarazada o lactando?:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
menu_embarazo = tk.OptionMenu(scrollable_frame, embarazada_var, *SI_NO)
row += 1

label_enfermedades = tk.Label(scrollable_frame, text="¿Tiene enfermedades que impidan donar?:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_enfermedades.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, enfermedades_var, *SI_NO).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_cirugias = tk.Label(scrollable_frame, text="¿Ha tenido cirugias en los ultimos 6 meses?:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_cirugias.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, cirugias_var, *SI_NO).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_tatuajes = tk.Label(scrollable_frame, text="¿Se tatuó hace menos de un año?:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_tatuajes.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, tatuajes_var, *SI_NO).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_medicamentos = tk.Label(scrollable_frame, text="¿Tomó medicamento en las últimas 48 horas?:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_medicamentos.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, medicamentos_var, *SI_NO).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_alcohol = tk.Label(scrollable_frame, text="¿Tomó alcohol en las últimas 48 horas?:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_alcohol.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, alcohol_var, *SI_NO).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_disponible = tk.Label(scrollable_frame, text="¿Disponible para donar?:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_disponible.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(scrollable_frame, disponible_var, *SI_NO).grid(row=row, column=1, sticky="ew", padx=10, pady=4)
row += 1

label_fecha = tk.Label(scrollable_frame, text="Fecha de registro:", bg="#e6f7ff", fg="#003366", font=("Arial", 11))
label_fecha.grid(row=row, column=0, sticky="w", padx=10, pady=4)
tk.Entry(scrollable_frame, textvariable=fecha_registro_var, width=40).grid(row=row, column=1, padx=10, pady=4)
row += 1

boton_guardar = tk.Button(scrollable_frame, text="Registrar donante", command=registrar_donante_gui, bg="#99ccff", fg="#003366", font=("Arial", 11, "bold"))
boton_guardar.grid(row=row, column=0, columnspan=2, pady=18, ipadx=10)

actualizar_embarazo()

# Receptor - sólo datos principales
row_r = 0
tk.Label(frame_receptor, text="Nombre completo:", bg="#e6f7ff", fg="#003366", font=("Arial", 11)).grid(row=row_r, column=0, sticky="w", padx=10, pady=4)
tk.Entry(frame_receptor, textvariable=receptor_nombre_var, width=40).grid(row=row_r, column=1, padx=10, pady=4)
row_r += 1
tk.Label(frame_receptor, text="Telefono:", bg="#e6f7ff", fg="#003366", font=("Arial", 11)).grid(row=row_r, column=0, sticky="w", padx=10, pady=4)
tk.Entry(frame_receptor, textvariable=receptor_telefono_var, width=40).grid(row=row_r, column=1, padx=10, pady=4)
row_r += 1
tk.Label(frame_receptor, text="Correo electronico:", bg="#e6f7ff", fg="#003366", font=("Arial", 11)).grid(row=row_r, column=0, sticky="w", padx=10, pady=4)
tk.Entry(frame_receptor, textvariable=receptor_correo_var, width=40).grid(row=row_r, column=1, padx=10, pady=4)
row_r += 1
tk.Label(frame_receptor, text="Ciudad o municipio:", bg="#e6f7ff", fg="#003366", font=("Arial", 11)).grid(row=row_r, column=0, sticky="w", padx=10, pady=4)
tk.Entry(frame_receptor, textvariable=receptor_ciudad_var, width=40).grid(row=row_r, column=1, padx=10, pady=4)
row_r += 1
tk.Label(frame_receptor, text="Tipo de sangre que necesita:", bg="#e6f7ff", fg="#003366", font=("Arial", 11)).grid(row=row_r, column=0, sticky="w", padx=10, pady=4)
tk.OptionMenu(frame_receptor, receptor_tipo_var, *TIPOS_SANGRE).grid(row=row_r, column=1, sticky="ew", padx=10, pady=4)
row_r += 1
boton_buscar_receptor = tk.Button(frame_receptor, text="Buscar donantes disponibles", command=buscar_donante_receptor, bg="#99ccff", fg="#003366", font=("Arial", 11, "bold"))
boton_buscar_receptor.grid(row=row_r, column=0, columnspan=2, pady=18)
row_r += 1
resultado_receptor = tk.Label(frame_receptor, text="", bg="#e6f7ff", fg="#003366", justify="left", font=("Arial", 10), wraplength=650)
resultado_receptor.grid(row=row_r, column=0, columnspan=2, sticky="w", padx=10)

root.mainloop()
