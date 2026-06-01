import tkinter as tk
from tkinter import ttk
class Paciente:
    def __init__(self, nombre, fecha_nacimiento, apellido_p, apellido_m, curp, sexo, recien_nacido):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.apellido_p = apellido_p
        self.apellido_m = apellido_m
        self.curp = curp
        self.sexo = sexo
        self.recien_nacido = recien_nacido
        self.vacunas = []
pacientes = []
def registrar():
    nuevo = Paciente(
        entrada_nombre.get(),
        entrada_fecha.get(),
        entrada_paterno.get(),
        entrada_materno.get(),
        entrada_curp.get(),
        entrada_sexo.get(),
        recien_nacido = combo_recien.get()
    )
    pacientes.append(nuevo)
    resultado_registro.config(
        text=f"Paciente registrado. Total: {len(pacientes)}"
    )
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
        entrada_fecha_buscar.grid_remove()
        label_sexo.grid_remove()
        entrada_sexo_buscar.grid_remove()
        label_recien.grid_remove()
        combo_recien_buscar.grid_remove()
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
        entrada_fecha_buscar.grid(row=4, column=1)
        label_sexo.grid(row=5, column=0)
        entrada_sexo_buscar.grid(row=5, column=1)
        label_recien.grid(row=6, column=0)
        combo_recien_buscar.grid(row=6, column=1)
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
label_curp = tk.Label(pestana_busqueda, text="CURP")
label_curp.grid(row=1, column=0)
label_nombre = tk.Label(pestana_busqueda, text="Nombre")
entrada_nombre_buscar = tk.Entry(pestana_busqueda)
label_paterno = tk.Label(pestana_busqueda, text="Apellido paterno")
entrada_paterno_buscar = tk.Entry(pestana_busqueda)
label_materno = tk.Label(pestana_busqueda, text="Apellido materno")
entrada_materno_buscar = tk.Entry(pestana_busqueda)
label_fecha = tk.Label(pestana_busqueda, text="Fecha de nacimiento")
entrada_fecha_buscar = tk.Entry(pestana_busqueda)
label_sexo = tk.Label(pestana_busqueda, text="Sexo")
entrada_sexo_buscar = tk.Entry(pestana_busqueda)
label_recien = tk.Label(pestana_busqueda, text="¿Recién nacido?")
combo_recien_buscar = ttk.Combobox(
    pestana_busqueda,
    values=["Sí", "No"],
    state="readonly"
)
combo_recien_buscar.set("No")
entrada_buscar_curp = tk.Entry(pestana_busqueda)
entrada_buscar_curp.grid(row=1, column=1)
combo_tipo_busqueda.grid(row=0, column=1)
combo_tipo_busqueda.set("CURP")
label_recien.grid_remove()
combo_recien_buscar.grid_remove()
tk.Label(pestana_registro, text="Nombre").grid(row=0, column=0)
entrada_nombre = tk.Entry(pestana_registro)
entrada_nombre.grid(row=0, column=1)
tk.Label(pestana_registro, text="Apellido paterno").grid(row=1, column=0)
entrada_paterno = tk.Entry(pestana_registro)
entrada_paterno.grid(row=1, column=1)
tk.Label(pestana_registro, text="Apellido materno").grid(row=2, column=0)
entrada_materno = tk.Entry(pestana_registro)
entrada_materno.grid(row=2, column=1)
tk.Label(pestana_registro, text="Fecha nacimiento").grid(row=3, column=0)
entrada_fecha = tk.Entry(pestana_registro)
entrada_fecha.grid(row=3, column=1)
tk.Label(pestana_registro, text="CURP").grid(row=4, column=0)
entrada_curp = tk.Entry(pestana_registro)
entrada_curp.grid(row=4, column=1)
tk.Label(pestana_registro, text="Sexo").grid(row=5, column=0)
entrada_sexo = tk.Entry(pestana_registro)
entrada_sexo.grid(row=5, column=1)
tk.Label(pestana_registro, text="¿Recién nacido?").grid(row=6, column=0)
combo_recien = ttk.Combobox(
    pestana_registro,
    values=["Sí", "No"],
    state="readonly"
)
combo_recien.grid(row=5, column=0)
combo_recien.grid(row=6, column=1)
combo_recien.set("No")
tk.Button(
    pestana_registro,
    text="Registrar",
    command=registrar
).grid(row=7, column=1, pady=10)
tk.Button(
    pestana_busqueda,
    text="Buscar",
    command=buscar
).grid(row=7, column=1, pady=10)
resultado_busqueda = tk.Label(
    pestana_busqueda,
    text="",
    justify="left"
)
resultado_busqueda.grid(row=10, column=0, columnspan=2)
ventana.mainloop()