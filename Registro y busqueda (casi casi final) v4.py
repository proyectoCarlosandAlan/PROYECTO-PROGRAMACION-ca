import tkinter as tk
from tkinter import ttk
class Paciente:
    def __init__(self, nombre, fecha_nacimiento, apellido_p, apellido_m, curp, sexo, cartilla):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.apellido_p = apellido_p
        self.apellido_m = apellido_m
        self.curp = curp
        self.sexo = sexo
        self.cartilla = cartilla
        self.vacunas = []
pacientes = []
def cambiar_curp(event=None):
    if  combo_tiene_curp.get() == "Sí":
        label_curp_registro.grid(row=8, column=0)
        entrada_curp.grid(row=8, column=1)
        error_curp.grid(row=8, column=2)
    else:
        label_curp_registro.grid_remove()
        entrada_curp.grid_remove()
        error_curp.grid_remove()
def registrar():
    error_cartilla.config(text="")
    error_nombre.config(text="")
    error_paterno.config(text="")
    error_materno.config(text="")
    error_fecha.config(text="")
    error_curp.config(text="")
    error_sexo.config(text="")
    valido = True
    if entrada_nombre.get() == "":
        error_nombre.config(text="Este campo es obligatorio")
        valido = False
    if entrada_paterno.get() == "":
        error_paterno.config(text="Este campo es obligatorio")
        valido = False
    if entrada_materno.get() == "":
        error_materno.config(text="Este campo es obligatorio")
        valido = False
    if combo_dia.get() == "DÍA" or combo_mes.get() == "MES" or combo_anio.get() == "AÑO":
        error_fecha.config(text="Este campo es obligatorio")
        valido = False
    if combo_cartilla.get() == "Seleccione una cartilla":
        error_cartilla.config(text="Este campo es obligatorio")
        valido = False
    else:
        try:
            anio = int(combo_anio.get())
            if anio < 1900 or anio > 2100:
                error_fecha.config(text="Año no válido")
                valido = False
        except ValueError:
            error_fecha.config(text="Año no válido")
            valido = False
    if combo_sexo.get() == "Elija una opción":
        error_sexo.config(text="Este campo es obligatorio")
        valido = False
    if combo_cartilla.get() == "Elija una opcion":
     error_cartilla.config(text="Este campo es obligatorio")
     valido = False
    if combo_tiene_curp.get() == "Sí" and entrada_curp.get() == "":
        error_curp.config(text="Este campo es obligatorio")
        valido = False
    if not valido:
     return
    nombre = entrada_nombre.get().strip().title()
    apellido_p = entrada_paterno.get().strip().title()
    apellido_m = entrada_materno.get().strip().title()
    fecha = f"{combo_dia.get()}/{combo_mes.get()}/{combo_anio.get()}"
    for paciente in pacientes:
        if (
            paciente.nombre.upper() == nombre.upper()
            and paciente.apellido_p.upper() == apellido_p.upper()
            and paciente.apellido_m.upper() == apellido_m.upper()
            and paciente.fecha_nacimiento == fecha
        ):
            resultado_registro.config(
                text="Paciente ya registrado",
                fg="red"
            )
            return
    nuevo=Paciente(
        nombre,
        fecha,
        apellido_p,
        apellido_m,
        entrada_curp.get(),
        combo_sexo.get(),
        combo_cartilla.get()
    )
    pacientes.append(nuevo)
    contador_pacientes.config(
    text=f"Pacientes registrados: {len(pacientes)}"
)
    resultado_registro.config(
    text=f"Paciente registrado. Total: {len(pacientes)}",
    fg="green"
)
    entrada_nombre.delete(0, tk.END)
    entrada_paterno.delete(0, tk.END)
    entrada_materno.delete(0, tk.END)
    combo_anio.set("AÑO")
    entrada_curp.delete(0, tk.END)
    combo_dia.set("DÍA")
    combo_mes.set("MES")
    combo_sexo.set("Elija una opción")
    combo_cartilla.set("Seleccione una opcion")
    combo_tiene_curp.set("No")
def buscar():
    curp_buscada = entrada_buscar_curp.get()
    for paciente in pacientes:
        if paciente.curp == curp_buscada:
            texto = (
                f"Nombre: {paciente.nombre}\n"
                f"Apellido paterno: {paciente.apellido_p}\n"
                f"Apellido materno: {paciente.apellido_m}\n"
                f"Fecha nacimiento: {paciente.fecha_nacimiento}\n"
                f"Sexo: {paciente.sexo}"
            )
            resultado_busqueda.config(text=texto)
            resultado_busqueda.grid(row=8, column=0, columnspan=2)
            return
    resultado_busqueda.config(text="Paciente no encontrado")
def cambiar_busqueda(event=None):
    if combo_tipo_busqueda.get() == "CURP":
        label_curp.grid()
        entrada_buscar_curp.grid()
        label_nombre.grid_remove()
        entrada_nombre_buscar.grid_remove()
        label_paterno.grid_remove()
        entrada_paterno_buscar.grid_remove()
        label_materno.grid_remove()
        entrada_materno_buscar.grid_remove()
        label_fecha.grid_remove()
        combo_dia_buscar.grid_remove()
        combo_mes_buscar.grid_remove()
        combo_anio_buscar.grid_remove()
        combo_sexo_buscar.grid()
        combo_sexo_buscar.grid_remove()
        label_sexo.grid_remove()
        label_cartilla.grid_remove()
        combo_cartilla_buscar.grid_remove()
    else:
     label_curp.grid_remove()
     entrada_buscar_curp.grid_remove()
     label_nombre.grid(row=1, column=0)
     entrada_nombre_buscar.grid(row=1, column=1)
     label_paterno.grid(row=2, column=0)
     entrada_paterno_buscar.grid(row=2, column=1)
     label_materno.grid(row=3, column=0)
     entrada_materno_buscar.grid(row=3, column=1)
     label_fecha.grid(row=4, column=0)
     combo_dia_buscar.grid(row=4, column=1, sticky="w")
     combo_mes_buscar.grid(row=4, column=1)
     combo_anio_buscar.grid(row=4, column=1, sticky="e")
     label_sexo.grid(row=5, column=0)
     combo_sexo_buscar.grid(row=5, column=1)
     label_cartilla.grid(row=6, column=0)
     combo_cartilla_buscar.grid(row=6, column=1)
ventana = tk.Tk()
ventana.title("Cartilla de Vacunación")
ventana.geometry("600x400")
notebook = ttk.Notebook(ventana)
pestana_registro = ttk.Frame(notebook)
pestana_busqueda = ttk.Frame(notebook)
notebook.add(pestana_registro, text="Registro")
notebook.add(pestana_busqueda, text="Buscar")
notebook.pack(expand=True, fill="both")
tk.Label(pestana_busqueda, text="Buscar por").grid(row=0, column=0)
combo_tipo_busqueda = ttk.Combobox(
    pestana_busqueda,
    values=["CURP", "Datos personales"],
    state="readonly"
)
combo_tipo_busqueda.bind(
    "<<ComboboxSelected>>",
    cambiar_busqueda
)
tk.Label(pestana_registro, text="¿Tiene CURP?").grid(row=6, column=0)
combo_tiene_curp = ttk.Combobox(
    pestana_registro,
    values=["Sí", "No"],
    state="readonly"
)
contador_pacientes = tk.Label(
    pestana_registro,
    text="Pacientes registrados: 0"
)
contador_pacientes.grid(row=0, column=3, padx=20, sticky="e")
combo_tiene_curp.grid(row=6, column=1)
combo_tiene_curp.set("Sí")
label_curp = tk.Label(pestana_busqueda, text="CURP")
label_curp.grid(row=1, column=0)
label_nombre = tk.Label(pestana_busqueda, text="Nombre/s")
entrada_nombre_buscar = tk.Entry(pestana_busqueda)
label_paterno = tk.Label(pestana_busqueda, text="Apellido paterno")
entrada_paterno_buscar = tk.Entry(pestana_busqueda)
label_materno = tk.Label(pestana_busqueda, text="Apellido materno")
entrada_materno_buscar = tk.Entry(pestana_busqueda)
label_fecha = tk.Label(
    pestana_busqueda,
    text="Fecha nacimiento"
)
combo_dia_buscar = ttk.Combobox(
    pestana_busqueda,
    values=list(range(1, 32)),
    state="readonly",
    width=5
)
combo_mes_buscar = ttk.Combobox(
    pestana_busqueda,
    values=[
        "Enero", "Febrero", "Marzo", "Abril",
        "Mayo", "Junio", "Julio", "Agosto",
        "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ],
    state="readonly",
    width=10
)
combo_anio_buscar = ttk.Combobox(
    pestana_busqueda,
    values=list(range(2026, 1899, -1)),
    state="readonly",
    width=8
)
combo_dia_buscar.set("DÍA")
combo_mes_buscar.set("MES")
combo_anio_buscar.set("AÑO")
label_sexo = tk.Label(
    pestana_busqueda,
    text="Sexo"
)
combo_sexo_buscar = ttk.Combobox(
    pestana_busqueda,
    values=["Hombre", "Mujer"],
    state="readonly"
)
combo_sexo_buscar.set("Elija una opción")
tk.Label(
    pestana_registro,
    text="Cartilla"
).grid(row=5, column=0)
combo_cartilla = ttk.Combobox(
    pestana_registro,
    values=[
        "Niñas y niños",
        "Adolescentes",
        "Mujeres",
        "Hombres",
        "Adultos mayores"
    ],
    state="readonly"
)
combo_cartilla.grid(row=5, column=1)
combo_cartilla.set("Seleccione una cartilla")
error_cartilla = tk.Label(
    pestana_registro,
    text="",
    fg="red"
)
error_cartilla.grid(row=5, column=2)
label_fecha = tk.Label(
    pestana_busqueda,
    text="Fecha nacimiento"
)
combo_dia_buscar = ttk.Combobox(
    pestana_busqueda,
    values=list(range(1, 32)),
    state="readonly",
    width=5
)
combo_mes_buscar = ttk.Combobox(
    pestana_busqueda,
    values=[
        "Enero", "Febrero", "Marzo", "Abril",
        "Mayo", "Junio", "Julio", "Agosto",
        "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ],
    state="readonly",
    width=10
)
combo_anio_buscar = ttk.Combobox(
    pestana_busqueda,
    values=list(range(2026, 1899, -1)),
    state="readonly",
    width=8
)
combo_anio_buscar.set("AÑO")
combo_dia_buscar.set("DÍA")
combo_mes_buscar.set("MES")
label_sexo = tk.Label(pestana_busqueda, text="Sexo")
combo_sexo_buscar = ttk.Combobox(
    pestana_busqueda,
    values=["Hombre", "Mujer"],
    state="readonly"
)
combo_sexo_buscar.set("Elija una opción")
label_cartilla = tk.Label(pestana_busqueda, text="Seleccione la cartilla")
combo_cartilla_buscar = ttk.Combobox(
    pestana_busqueda,
    values=["Niñas y niños (0-9 años)", "Adolescentes (10-19 años)", "Mujeres (20-59 años)", "Hombres (20-59 años)", "Adultos mayores (60 años o más)"
],
    state="readonly"
)
combo_cartilla_buscar.set("Elija una opcion")
entrada_buscar_curp = tk.Entry(pestana_busqueda)
entrada_buscar_curp.grid(row=1, column=1)
combo_tipo_busqueda.grid(row=0, column=1)
combo_tipo_busqueda.set("CURP")
label_cartilla.grid_remove()
combo_cartilla_buscar.grid_remove()
label_nombre.grid_remove()
entrada_nombre_buscar.grid_remove()
label_paterno.grid_remove()
entrada_paterno_buscar.grid_remove()
label_materno.grid_remove()
entrada_materno_buscar.grid_remove()
label_fecha.grid_remove()
combo_dia_buscar.grid_remove()
combo_mes_buscar.grid_remove()
combo_anio_buscar.grid_remove()
label_sexo.grid_remove()
combo_sexo_buscar.grid_remove()
label_cartilla.grid_remove()
combo_cartilla_buscar.grid_remove()
tk.Label(pestana_registro, text="Nombre/s").grid(row=0, column=0)
entrada_nombre = tk.Entry(pestana_registro)
entrada_nombre.grid(row=0, column=1)
error_nombre = tk.Label(pestana_registro, text="", fg="red")
error_nombre.grid(row=0, column=2)
tk.Label(pestana_registro, text="Apellido paterno").grid(row=1, column=0)
entrada_paterno = tk.Entry(pestana_registro)
entrada_paterno.grid(row=1, column=1)
error_paterno = tk.Label(pestana_registro, text="", fg="red")
error_paterno.grid(row=1, column=2)
tk.Label(pestana_registro, text="Apellido materno").grid(row=2, column=0)
entrada_materno = tk.Entry(pestana_registro)
entrada_materno.grid(row=2, column=1)
error_materno = tk.Label(pestana_registro, text="", fg="red")
error_materno.grid(row=2, column=2)
tk.Label(pestana_registro, text="Fecha nacimiento").grid(row=3, column=0)
combo_dia = ttk.Combobox(
    pestana_registro,
    values=list(range(1, 32)),
    state="readonly",
    width=5
)
combo_dia.grid(row=3, column=1, sticky="w")
combo_mes = ttk.Combobox(
    pestana_registro,
    values=[
        "Enero", "Febrero", "Marzo", "Abril",
        "Mayo", "Junio", "Julio", "Agosto",
        "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ],
    state="readonly",
    width=10
)
combo_mes.grid(row=3, column=1)
entrada_anio = tk.Entry(
    pestana_registro,
    width=8
)
combo_anio = ttk.Combobox(
    pestana_registro,
    values=list(range(2026, 1899, -1)),
    state="readonly",
    width=8
)
combo_anio.grid(row=3, column=1, sticky="e")
combo_anio.set("AÑO")
error_fecha = tk.Label(
    pestana_registro,
    text="",
    fg="red"
)
combo_dia.set("DÍA")
combo_mes.set("MES")
error_fecha.grid(row=3, column=2)
error_fecha = tk.Label(pestana_registro, text="", fg="red")
error_fecha.grid(row=3, column=2)
label_curp_registro = tk.Label(pestana_registro, text="CURP")
entrada_curp = tk.Entry(pestana_registro)
error_curp = tk.Label(
    pestana_registro,
    text="",
    fg="red"
)
combo_tiene_curp.bind(
    "<<ComboboxSelected>>",
    cambiar_curp
)
combo_tiene_curp.set("No")
cambiar_curp()
error_curp = tk.Label(pestana_registro, text="", fg="red")
error_curp.grid(row=7, column=2)
tk.Label(pestana_registro, text="Sexo").grid(row=4, column=0)
combo_sexo = ttk.Combobox(
    pestana_registro,
    values=["Hombre", "Mujer"],
    state="readonly"
)
combo_sexo.grid(row=4, column=1)
combo_sexo.set("Elija una opción")
error_sexo = tk.Label(pestana_registro, text="", fg="red")
error_sexo.grid(row=4, column=2)
tk.Label(pestana_registro, text="Seleccione la cartilla").grid(row=5, column=0)
combo_cartilla = ttk.Combobox(
    pestana_registro,
    values=[
    "Niñas y niños (0-9 años)",
    "Adolescentes (10-19 años)",
    "Mujeres (20-59 años)",
    "Hombres (20-59 años)",
    "Adultos mayores (60 años o más)"
],
    state="readonly"
)
combo_cartilla.grid(row=5, column=0)
combo_cartilla.grid(row=5, column=1)
combo_cartilla.set("Elija una opcion")
tk.Button(
    pestana_registro,
    text="Registrar",
    command=registrar
).grid(row=9, column=1, pady=10)
tk.Button(
    pestana_busqueda,
    text="Buscar",
    command=buscar
).grid(row=9, column=1, pady=10)
resultado_busqueda = tk.Label(
    pestana_busqueda,
    text="",
    justify="left"
)
resultado_registro = tk.Label(
    pestana_registro,
    text=""
)
resultado_registro.grid(row=10, column=0, columnspan=3)
resultado_busqueda.grid(row=10, column=0, columnspan=2)
ventana.mainloop()