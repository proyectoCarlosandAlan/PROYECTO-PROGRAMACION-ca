import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime
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
def registrar():
    error_cartilla.config(text="")
    error_nombre.config(text="")
    error_paterno.config(text="")
    error_materno.config(text="")
    error_fecha.config(text="")
    error_curp.config(text="")
    error_sexo.config(text="")
    valido = True
    meses = {
        "Enero":"01",
        "Febrero":"02",
        "Marzo":"03",
        "Abril":"04",
        "Mayo":"05",
        "Junio":"06",
        "Julio":"07",
        "Agosto":"08",
        "Septiembre":"09",
        "Octubre":"10",
        "Noviembre":"11",
        "Diciembre":"12"
    }
    if entrada_nombre.get() == "":
        error_nombre.config(text="Este campo es obligatorio")
        valido = False
    elif not entrada_nombre.get().replace(" ", "").isalpha():
     error_nombre.config(text="Solo letras")
     valido = False
    if entrada_paterno.get() == "":
        error_paterno.config(text="Este campo es obligatorio")
        valido = False
    elif not entrada_paterno.get().replace(" ", "").isalpha():
     error_paterno.config(text="Solo letras")
     valido = False
    if entrada_materno.get() == "":
        error_materno.config(text="Este campo es obligatorio")
        valido = False
    elif not entrada_materno.get().replace(" ", "").isalpha():
     error_materno.config(text="Solo letras")
     valido = False
    if combo_dia.get() != "DÍA" and combo_mes.get() != "MES" and combo_anio.get() != "AÑO":
     try:
        datetime(
            int(combo_anio.get()),
            list(meses.keys()).index(combo_mes.get()) + 1,
            int(combo_dia.get())
        )
     except ValueError:
        error_fecha.config(text="Fecha no válida")
        valido = False
    if combo_dia.get() == "DÍA" or combo_mes.get() == "MES" or combo_anio.get() == "AÑO":
        error_fecha.config(text="Este campo es obligatorio")
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
    if combo_cartilla.get() == "Cartilla":
     error_cartilla.config(text="Este campo es obligatorio")
     valido = False
    if entrada_curp.get() == "":
     error_curp.config(text="Este campo es obligatorio")
     valido = False
    curp = entrada_curp.get().strip().upper()
    if curp != "" and len(curp) != 18:
     error_curp.config(text="Debe tener 18 caracteres")
     valido = False
    for paciente in pacientes:
     if paciente.curp == curp:
         resultado_registro.config(
            text="CURP ya registrada",
            fg="red"
        )
         return
    patron_curp = r"^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$"
    if entrada_curp.get() != "" and not re.match(patron_curp, curp):
     error_curp.config(text="CURP no válida")
     valido = False
    if re.match(patron_curp, curp):
     nombre = entrada_nombre.get().strip().upper()
     apellido_p = entrada_paterno.get().strip().upper()
     apellido_m = entrada_materno.get().strip().upper()
     primera_letra_p = apellido_p[0]
     vocal_interna = ""
     for letra in apellido_p[1:]:
        if letra in "AEIOU":
            vocal_interna = letra
            break
     iniciales_esperadas = (
        primera_letra_p +
        vocal_interna +
        apellido_m[0] +
        nombre[0]
    )
     if curp[:4] != iniciales_esperadas:
        error_curp.config(
            text="Iniciales no coinciden con el CURP"
        )
        valido = False
    fecha_curp = (
        combo_anio.get()[2:] +
        meses[combo_mes.get()] +
        combo_dia.get().zfill(2)
    )
    if curp[4:10] != fecha_curp:
        error_curp.config(
            text="Fecha no coincide con el CURP"
        )
        valido = False
    sexo_curp = curp[10]
    if combo_sexo.get() == "Hombre" and sexo_curp != "H":
        error_curp.config(
            text="Sexo no coincide con el CURP"
        )
        valido = False
    if combo_sexo.get() == "Mujer" and sexo_curp != "M":
        error_curp.config(
            text="Sexo no coincide con el CURP"
        )
        valido = False
    if not valido:
     return
    nombre = entrada_nombre.get().strip().title()
    apellido_p = entrada_paterno.get().strip().title()
    apellido_m = entrada_materno.get().strip().title()
    fecha = (
    f"{combo_dia.get().zfill(2)}/"
    f"{meses[combo_mes.get()]}/"
    f"{combo_anio.get()}"
)
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
        curp,
        combo_sexo.get(),
        combo_cartilla.get()
    )
    pacientes.append(nuevo)
    contador_pacientes.config(
    text=f"Pacientes registrados: {len(pacientes)}"
)
    resultado_registro.config(
    text=f"Paciente registrado correctamente\nCartilla: {combo_cartilla.get()}",
    fg="green"
)
    error_nombre.config(text="")
    error_paterno.config(text="")
    error_materno.config(text="")
    error_fecha.config(text="")
    error_curp.config(text="")
    error_sexo.config(text="")
    error_cartilla.config(text="")
    entrada_nombre.delete(0, tk.END)
    entrada_paterno.delete(0, tk.END)
    entrada_materno.delete(0, tk.END)
    combo_anio.set("AÑO")
    entrada_curp.delete(0, tk.END)
    combo_dia.set("DÍA")
    combo_mes.set("MES")
    combo_sexo.set("Elija una opción")
    combo_cartilla.config(state="normal")
    combo_cartilla.set("")
    combo_cartilla.config(state="disabled")
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
def autocompletar_curp(event=None):
    curp = entrada_curp.get().strip().upper()
    patron_curp = r"^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$"
    if re.match(patron_curp, curp):
        anio = int(curp[4:6])
        mes = int(curp[6:8])
        dia = int(curp[8:10])
        if anio <= 26:
            anio += 2000
        else:
            anio += 1900
        meses = {
            1:"Enero",
            2:"Febrero",
            3:"Marzo",
            4:"Abril",
            5:"Mayo",
            6:"Junio",
            7:"Julio",
            8:"Agosto",
            9:"Septiembre",
            10:"Octubre",
            11:"Noviembre",
            12:"Diciembre"
        }
        combo_dia.set(str(dia))
        combo_mes.set(meses[mes])
        combo_anio.set(str(anio))
        if curp[10] == "H":
            combo_sexo.set("Hombre")
        else:
            combo_sexo.set("Mujer")
        edad = datetime.now().year - anio
        if edad <= 9:
            combo_cartilla.set("Niñas y niños (0-9 años)")
            combo_cartilla.config(state="disabled")
        elif edad <= 19:
            combo_cartilla.set("Adolescentes (10-19)")
            combo_cartilla.config(state="disabled")
        elif edad >= 60:
            combo_cartilla.set("Adultos mayores (60+)")
            combo_cartilla.config(state="disabled")
        else:
            if curp[10] == "M":
                combo_cartilla.set("Mujeres (20-59)")
                combo_cartilla.config(state="disabled")
            else:
                combo_cartilla.set("Hombres (20-59)")
                combo_cartilla.config(state="disabled")
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
contador_pacientes = tk.Label(
    pestana_registro,
    text="Pacientes registrados: 0"
)
contador_pacientes.grid(row=0, column=3, padx=20, sticky="e")
label_curp = tk.Label(pestana_busqueda, text="CURP (18 caracteres)")
label_curp.grid(row=0, column=0)
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
combo_cartilla = ttk.Combobox(
    pestana_registro,
    values=[
        "Niñas y niños (0-9 años)",
        "Adolescentes (10-19)",
        "Mujeres (20-59)",
        "Hombres (20-59)",
        "Adultos mayores (60+)"
    ],
    state="disabled"
)
tk.Label(
    pestana_registro,
    text="Cartilla:"
).grid(row=6, column=0)
combo_cartilla.grid(row=6, column=1)
combo_cartilla.set("--------")
error_cartilla = tk.Label(
    pestana_registro,
    text="",
    fg="red"
)
error_cartilla.grid(row=6, column=2)
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
tk.Label(pestana_registro, text="Nombre/s").grid(row=1, column=0)
entrada_nombre = tk.Entry(pestana_registro)
entrada_nombre.grid(row=1, column=1)
error_nombre = tk.Label(pestana_registro, text="", fg="red")
error_nombre.grid(row=1, column=2)
tk.Label(pestana_registro, text="Apellido paterno").grid(row=2, column=0)
entrada_paterno = tk.Entry(pestana_registro)
entrada_paterno.grid(row=2, column=1)
error_paterno = tk.Label(pestana_registro, text="", fg="red")
error_paterno.grid(row=2, column=2)
tk.Label(pestana_registro, text="Apellido materno").grid(row=3, column=0)
entrada_materno = tk.Entry(pestana_registro)
entrada_materno.grid(row=3, column=1)
error_materno = tk.Label(pestana_registro, text="", fg="red")
error_materno.grid(row=3, column=2)
tk.Label(pestana_registro, text="Fecha nacimiento").grid(row=5, column=0)
combo_dia = ttk.Combobox(
    pestana_registro,
    values=list(range(1, 32)),
    state="readonly",
    width=5
)
combo_dia.grid(row=5, column=1, sticky="w")
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
combo_mes.grid(row=5, column=1)
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
combo_anio.grid(row=5, column=1, sticky="e")
combo_anio.set("AÑO")
error_fecha = tk.Label(
    pestana_registro,
    text="",
    fg="red"
)
combo_dia.set("DÍA")
combo_mes.set("MES")
error_fecha.grid(row=5, column=2)
error_fecha = tk.Label(pestana_registro, text="", fg="red")
error_fecha.grid(row=5, column=2)
label_curp_registro = tk.Label(pestana_registro, text="CURP (18 caracteres)")
label_curp_registro.grid(row=0, column=0)
entrada_curp = tk.Entry(pestana_registro)
entrada_curp.grid(row=0, column=1)
entrada_curp.bind("<KeyRelease>", autocompletar_curp)
error_curp = tk.Label(
    pestana_registro,
    text="",
    fg="red"
)
error_curp.grid(row=0, column=2)
error_curp = tk.Label(pestana_registro, text="", fg="red")
error_curp.grid(row=0, column=2)
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