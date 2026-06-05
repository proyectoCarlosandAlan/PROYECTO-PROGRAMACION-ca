import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime
import json
import os
class Paciente:
    def __init__(self, nombre, fecha_nacimiento, apellido_p, apellido_m, curp, sexo, cartilla):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.apellido_p = apellido_p
        self.apellido_m = apellido_m
        self.curp = curp
        self.sexo = sexo
        self.cartilla = cartilla
        self.vacunas = {}
        self.vacunas_extra = []
        self.lista_vacunas_widget = None
        self.fechas_vacunas = {}
pacientes = []
ARCHIVO = "pacientes.json"
def guardar_pacientes():
    datos = []
    for paciente in pacientes:
        datos.append({
            "nombre": paciente.nombre,
            "fecha_nacimiento": paciente.fecha_nacimiento,
            "apellido_p": paciente.apellido_p,
            "apellido_m": paciente.apellido_m,
            "curp": paciente.curp,
            "sexo": paciente.sexo,
            "cartilla": paciente.cartilla,
            "vacunas_extra": [
    {
        "nombre": vacuna["nombre"],
        "fecha": vacuna["fecha"],
        "dosis": vacuna["dosis"],
        "lote": vacuna["lote"]
    }
    for vacuna in paciente.vacunas_extra
],
"fechas_vacunas": paciente.fechas_vacunas
        })
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4,
            default=str
        )
def cargar_pacientes():
    print(f"Pacientes cargados: {len(pacientes)}")
    if not os.path.exists(ARCHIVO):
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    for dato in datos:
        paciente = Paciente(
            dato["nombre"],
            dato["fecha_nacimiento"],
            dato["apellido_p"],
            dato["apellido_m"],
            dato["curp"],
            dato["sexo"],
            dato["cartilla"]
        )
        paciente.fechas_vacunas = dato.get(
        "fechas_vacunas",
        {}
)
        paciente.vacunas_extra = []
        for vacuna in dato.get("vacunas_extra", []):
            try:
                fecha_obj = datetime.strptime(
                vacuna["fecha"],
                "%d/%B/%Y"
        )
            except:
                fecha_obj = datetime.now()
            vacuna["fecha_obj"] = fecha_obj
            paciente.vacunas_extra.append(vacuna)
        pacientes.append(paciente)
cartillas = {
    "Niñas y niños (0-9 años)": [
        ("BCG", "Al nacer", "Aplicar al nacimiento"),
        ("Hepatitis B", "Al nacer", "Aplicar al nacimiento"),
        ("Hexavalente", "2 meses", "Primera dosis"),
        ("Hexavalente", "4 meses", "Segunda dosis"),
        ("Hexavalente", "6 meses", "Tercera dosis"),
        ("Rotavirus", "2 meses", "Primera dosis"),
        ("Rotavirus", "4 meses", "Segunda dosis"),
        ("Neumococo", "2 meses", "Primera dosis"),
        ("Neumococo", "4 meses", "Segunda dosis"),
        ("SRP", "12 meses", "Primera dosis contra sarampión"),
        ("DPT", "4 años", "Refuerzo")
    ],
    "Adolescentes (10-19)": [
        ("VPH", "11-16 años", "Protección contra VPH"),
        ("Td", "Refuerzo", "Cada 10 años"),
        ("SR", "Recuperación", "Si faltó aplicación previa")
    ],
    "Mujeres (20-59)": [
        ("Td", "Cada 10 años", "Refuerzo periódico"),
        ("Influenza", "Campañas", "Aplicación anual")
    ],
    "Hombres (20-59)": [
        ("Td", "Cada 10 años", "Refuerzo periódico"),
        ("Influenza", "Campañas", "Aplicación anual")
    ],
    "Adultos mayores (60+)": [
        ("Influenza", "Anual", "Una vez por año"),
        ("Neumococo", "60+", "Al cumplir 60 años"),
        ("COVID-19", "Refuerzos", "Según campaña vigente")
    ]
}
def obtener_cartillas(edad, sexo):
    lista = ["Niñas y niños (0-9 años)"]
    if edad >= 10:
        lista.append("Adolescentes (10-19)")
    if edad >= 20:
        if sexo == "Mujer":
            lista.append("Mujeres (20-59)")
        else:
            lista.append("Hombres (20-59)")
    if edad >= 60:
        lista.append("Adultos mayores (60+)")
    return lista
def guardar_fecha(
    clave,
    paciente,
    combo_dia,
    combo_mes,
    combo_anio,
    btn_guardar,
    fila,
    pestaña
):
    if (
        combo_dia.get() == "Día" or
        combo_mes.get() == "Mes" or
        combo_anio.get() == "Año"
):
        tk.Label(
        pestaña,
        text="Fecha no válida",
        fg="red"
        ).grid(row=fila+1, column=4, columnspan=3)
        return
    meses = {
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12
}
    try:
        datetime(
        int(combo_anio.get()),
        meses[combo_mes.get()],
        int(combo_dia.get())
    )
    except ValueError:
        tk.Label(
            pestaña,
            text="Fecha no válida",
            fg="red"
            ).grid(row=fila+1, column=4, columnspan=3)
        return
    fecha = (
        f"{combo_dia.get()}/"
        f"{combo_mes.get()}/"
        f"{combo_anio.get()}"
    )
    paciente.fechas_vacunas[clave] = fecha
    combo_dia.destroy()
    combo_mes.destroy()
    combo_anio.destroy()
    btn_guardar.destroy()
    tk.Label(
        pestaña,
        text=fecha
    ).grid(row=fila, column=5, columnspan=2)
    tk.Button(
        pestaña,
        text="Editar fecha",
        command=lambda: editar_fecha(
            clave,
            fila,
            pestaña,
            paciente
        )
    ).grid(row=fila, column=6)
def editar_fecha(clave, fila, pestaña, paciente):
    for widget in pestaña.grid_slaves(row=fila):
        if int(widget.grid_info()["column"]) >= 5:
            widget.destroy()
    mostrar_fecha(
        clave,
        fila,
        pestaña,
        paciente
    )
def mostrar_fecha(clave, fila, pestaña, paciente):
    widgets = pestaña.grid_slaves(row=fila, column=7)
    if widgets:
        widgets[0].destroy()
    combo_dia = ttk.Combobox(
        pestaña,
        values=list(range(1, 32)),
        width=4,
        state="readonly"
    )
    combo_mes = ttk.Combobox(
        pestaña,
        values=[
            "Enero","Febrero","Marzo","Abril",
            "Mayo","Junio","Julio","Agosto",
            "Septiembre","Octubre","Noviembre","Diciembre"
        ],
        width=10,
        state="readonly"
    )
    combo_anio = ttk.Combobox(
        pestaña,
        values=list(range(datetime.now().year, 1900, -1)),
        width=6,
        state="readonly"
    )
    combo_dia.set("Día")
    combo_mes.set("Mes")
    combo_anio.set("Año")
    combo_dia.grid(row=fila, column=5, sticky="w")
    combo_mes.grid(row=fila, column=6)
    combo_anio.grid(row=fila, column=7, sticky="e")
    btn_guardar = tk.Button(
        pestaña,
        text="Guardar",
        command=lambda: guardar_fecha(
            clave,
            paciente,
            combo_dia,
            combo_mes,
            combo_anio,
            btn_guardar,
            fila,
            pestaña
        )
    )
    btn_guardar.grid(row=fila, column=8, pady=5)
def ventana_agregar_vacuna(paciente):
    ventana = tk.Toplevel()
    ventana.title("Agregar vacuna")
    ventana.geometry("800x500")
    tk.Label(
        ventana,
        text="Nombre de la vacuna"
    ).grid(row=0, column=0, padx=5, pady=5)
    entrada_vacuna = tk.Entry(ventana, width=25)
    entrada_vacuna.grid(row=0, column=1)
    tk.Label(
        ventana,
        text="Fecha de aplicación"
    ).grid(row=1, column=0)
    combo_dia = ttk.Combobox(
        ventana,
        values=list(range(1, 32)),
        width=5,
        state="readonly"
    )
    combo_dia.grid(row=1, column=1, sticky="w")
    combo_mes = ttk.Combobox(
        ventana,
        values=[
            "Enero","Febrero","Marzo","Abril",
            "Mayo","Junio","Julio","Agosto",
            "Septiembre","Octubre","Noviembre","Diciembre"
        ],
        width=10,
        state="readonly"
    )
    combo_mes.grid(row=1, column=1)
    combo_anio = ttk.Combobox(
        ventana,
        values=list(range(datetime.now().year, 1900, -1)),
        width=8,
        state="readonly"
    )
    combo_anio.grid(row=1, column=1, sticky="e")
    combo_dia.set("Día")
    combo_mes.set("Mes")
    combo_anio.set("Año")
    tk.Label(
        ventana,
        text="Dosis"
    ).grid(row=2, column=0)
    combo_dosis = ttk.Combobox(
        ventana,
        values=[
            "Primera",
            "Segunda",
            "Tercera",
            "Cuarta",
            "Refuerzo"
        ],
        state="readonly"
    )
    combo_dosis.grid(row=2, column=1)
    tk.Label(
        ventana,
        text="Número de lote"
    ).grid(row=3, column=0)
    entrada_lote = tk.Entry(ventana)
    entrada_lote.grid(row=3, column=1)
    error = tk.Label(
        ventana,
        text="",
        fg="red"
    )
    error.grid(row=4, column=0, columnspan=2)
    tk.Label(
        ventana,
        text="Vacunas agregadas",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=3, padx=20)
    lista_vacunas = tk.Listbox(
        ventana,
        width=50,
        height=15
    )
    lista_vacunas.grid(
        row=1,
        column=3,
        rowspan=6,
        padx=20
    )
    def eliminar_vacuna():
        seleccion = lista_vacunas.curselection()
        if not seleccion:
            return
        indice = seleccion[0]
        paciente.vacunas_extra.pop(indice)
        lista_vacunas.delete(indice)
        guardar_pacientes()
    tk.Button(
        ventana,
        text="Eliminar seleccionada",
        command=eliminar_vacuna
).grid(row=8, column=3, pady=10)
    for vacuna in paciente.vacunas_extra:
        texto = (
            f"{vacuna['fecha']} - "
            f"{vacuna['nombre']} - "
            f"{vacuna['dosis']} - "
            f"Lote: {vacuna['lote']}"
        )
        lista_vacunas.insert(tk.END, texto)
    def guardar():
        if entrada_vacuna.get() == "":
            error.config(text="Ingrese una vacuna")
            return
        if combo_dosis.get() == "":
            error.config(text="Seleccione una dosis")
            return
        if entrada_lote.get() == "":
            error.config(text="Ingrese un lote")
            return
        meses = {
            "Enero":1,
            "Febrero":2,
            "Marzo":3,
            "Abril":4,
            "Mayo":5,
            "Junio":6,
            "Julio":7,
            "Agosto":8,
            "Septiembre":9,
            "Octubre":10,
            "Noviembre":11,
            "Diciembre":12
        }
        try:
            fecha_obj = datetime(
                int(combo_anio.get()),
                meses[combo_mes.get()],
                int(combo_dia.get())
            )
        except:
            error.config(text="Fecha inválida")
            return
        vacuna = {
            "nombre": entrada_vacuna.get(),
            "fecha":
                f"{combo_dia.get()}/"
                f"{combo_mes.get()}/"
                f"{combo_anio.get()}",
            "fecha_obj": fecha_obj,
            "dosis": combo_dosis.get(),
            "lote": entrada_lote.get()
        }
        paciente.vacunas_extra.append(vacuna)
        guardar_pacientes()
        paciente.vacunas_extra.sort(
            key=lambda x: x["fecha_obj"],
            reverse=True
        )
        lista_vacunas.delete(0, tk.END)
        for vacuna in paciente.vacunas_extra:
            texto = (
                f"{vacuna['fecha']} - "
                f"{vacuna['nombre']} - "
                f"{vacuna['dosis']} - "
                f"Lote: {vacuna['lote']}"
            )
            lista_vacunas.insert(
                tk.END,
                texto
            )
            if paciente.lista_vacunas_widget:
                paciente.lista_vacunas_widget.delete(0, tk.END)
                for v in paciente.vacunas_extra:
                    texto = (
                    f"{v['fecha']} - "
                    f"{v['nombre']} - "
                    f"{v['dosis']} - "
                    f"Lote: {v['lote']}"
        )
        paciente.lista_vacunas_widget.insert(
            tk.END,
            texto
        )
        entrada_vacuna.delete(0, tk.END)
        entrada_lote.delete(0, tk.END)
        combo_dia.set("Día")
        combo_mes.set("Mes")
        combo_anio.set("Año")
        combo_dosis.set("")
        error.config(text="")
    tk.Button(
        ventana,
        text="Agregar",
        command=guardar
    ).grid(
        row=7,
        column=0,
        columnspan=2,
        pady=15
    )
def ventana_vacunas(paciente):
    ventana_vac = tk.Toplevel()
    ventana_vac.title("Cartilla de Vacunación")
    ventana_vac.geometry("800x500")
    edad = datetime.now().year - int(
        paciente.fecha_nacimiento[-4:]
    )
    notebook_vacunas = ttk.Notebook(ventana_vac)
    notebook_vacunas.pack(
        expand=True,
        fill="both",
        padx=10,
        pady=10
    )
    tk.Button(
        ventana_vac,
        text="Agregar vacuna",
        command=lambda:
        ventana_agregar_vacuna(paciente)
        ).pack(side="right", padx=10, pady=10)
    cartillas_mostrar = obtener_cartillas(
        edad,
        paciente.sexo
    )
    frame_vacunas_extra = tk.Frame(ventana_vac)
    frame_vacunas_extra.pack(
        side="right",
        fill="y",
        padx=10
)
    tk.Label(
        frame_vacunas_extra,
        text="Vacunas agregadas",
        font=("Arial", 10, "bold")
).pack()
    lista_vacunas = tk.Listbox(
        frame_vacunas_extra,
        width=45,
        height=15
)
    lista_vacunas.pack()
    paciente.lista_vacunas_widget = lista_vacunas
    for vacuna in paciente.vacunas_extra:
        texto = (
            f"{vacuna['fecha']} - "
            f"{vacuna['nombre']} - "
            f"{vacuna['dosis']} - "
            f"Lote: {vacuna['lote']}"
        )
        lista_vacunas.insert(tk.END, texto)
    indice_cartilla_actual = 0
    for indice, nombre_cartilla in enumerate(cartillas_mostrar):
        pestaña = ttk.Frame(notebook_vacunas)
        notebook_vacunas.add(
            pestaña,
            text=nombre_cartilla
        )
        if nombre_cartilla == paciente.cartilla:
            indice_cartilla_actual = indice
        tk.Label(
            pestaña,
            text=nombre_cartilla,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=4)
        tk.Label(
            pestaña,
            text="Vacuna"
        ).grid(row=1, column=0)
        tk.Label(
            pestaña,
            text="Edad"
        ).grid(row=1, column=1)
        tk.Label(
            pestaña,
            text="Indicaciones"
        ).grid(row=1, column=2)
        tk.Label(
            pestaña,
            text="Aplicada"
        ).grid(row=1, column=3)
        tk.Label(
            pestaña,
            text="Fecha aplicación"
            ).grid(row=1, column=5, columnspan=3)
        tk.Label(
            pestaña,
            text="Acción"
            ).grid(row=1, column=8)
        fila = 2
        for vacuna, edad_vacuna, descripcion in cartillas[nombre_cartilla]:
            tk.Label(
                pestaña,
                text=vacuna
            ).grid(row=fila, column=0, sticky="w")
            tk.Label(
                pestaña,
                text=edad_vacuna
            ).grid(row=fila, column=1)
            tk.Label(
                pestaña,
                text=descripcion,
                wraplength=200,
                justify="left"
                ).grid(row=fila, column=2, sticky="w")
            clave = f"{nombre_cartilla}_{vacuna}_{edad_vacuna}"
            if clave not in paciente.vacunas:
                paciente.vacunas[clave] = tk.StringVar(value="NINGUNO")
            estado = paciente.vacunas[clave]
            tk.Radiobutton(
                pestaña,
                text="Sí",
                variable=estado,
                value="Sí"
            ).grid(row=fila, column=3)
            tk.Radiobutton(
                pestaña,
                text="No",
                variable=estado,
                value="No"
            ).grid(row=fila, column=4)
            if clave in paciente.fechas_vacunas:
                tk.Label(
                    pestaña,
                    text=paciente.fechas_vacunas[clave]
                    ).grid(row=fila, column=5, columnspan=2)
                tk.Button(
                    pestaña,
                    text="Editar fecha",
                    command=lambda c=clave, f=fila:
                    editar_fecha(c, f, pestaña, paciente)
                    ).grid(row=fila, column=6)
            else:
                tk.Button(
                pestaña,
                text="Agregar fecha",
                width=15,
                command=lambda c=clave, f=fila:
                mostrar_fecha(c, f, pestaña, paciente)
                ).grid(row=fila, column=7, padx=5)
            fila += 1
    notebook_vacunas.select(indice_cartilla_actual)
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
    hoy = datetime.now()
    edad = hoy.year - int(combo_anio.get())
    if (
        hoy.month < list(meses.keys()).index(combo_mes.get()) + 1 or
    (
            hoy.month == list(meses.keys()).index(combo_mes.get()) + 1 and
            hoy.day < int(combo_dia.get())
    )
):
        edad -= 1
    if edad <= 9:
        cartilla = "Niñas y niños (0-9 años)"
    elif edad <= 19:
        cartilla = "Adolescentes (10-19)"
    elif edad >= 60:
        cartilla = "Adultos mayores (60+)"
    elif combo_sexo.get() == "Mujer":
        cartilla = "Mujeres (20-59)"
    else:
        cartilla = "Hombres (20-59)"
    nuevo = Paciente(
        nombre,
        fecha,
        apellido_p,
        apellido_m,
        curp,
        combo_sexo.get(),
        cartilla
)
    pacientes.append(nuevo)
    guardar_pacientes()
    ventana_vacunas(nuevo)
    contador_pacientes.config(
    text=f"Pacientes registrados: {len(pacientes)}"
)
    resultado_registro.config(
    text=f"Paciente registrado correctamente\nCartilla: {cartilla}",
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
    resultado_busqueda.config(text="")
    if combo_tipo_busqueda.get() == "CURP":
        curp = entrada_buscar_curp.get().strip().upper()
        if curp == "":
            resultado_busqueda.config(
                text="Ingrese una CURP"
            )
            return
        patron_curp = r"^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$"
        if not re.match(patron_curp, curp):
            resultado_busqueda.config(
                text="Formato de CURP inválido"
            )
            return
        for paciente in pacientes:
            if paciente.curp == curp:
                texto = (
                f"Nombre: {paciente.nombre}\n"
                f"Apellido paterno: {paciente.apellido_p}\n"
                f"Apellido materno: {paciente.apellido_m}\n"
                f"Fecha nacimiento: {paciente.fecha_nacimiento}\n"
                f"Sexo: {paciente.sexo}\n"
                f"Cartilla: {paciente.cartilla}"
    )
            resultado_busqueda.config(text=texto)
            tk.Button(
                pestana_busqueda,
                text="Abrir cartilla",
                command=lambda p=paciente: ventana_vacunas(p)
                ).grid(row=11, column=1)
            return
        resultado_busqueda.config(
            text="Paciente no encontrado"
        )
    else:
        nombre = entrada_nombre_buscar.get().strip().upper()
        paterno = entrada_paterno_buscar.get().strip().upper()
        materno = entrada_materno_buscar.get().strip().upper()
        if (
            combo_dia_buscar.get() == "DÍA" or
            combo_mes_buscar.get() == "MES" or
            combo_anio_buscar.get() == "AÑO"
        ):
            resultado_busqueda.config(
                text="Seleccione una fecha válida"
            )
            return
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
        fecha = (
            f"{combo_dia_buscar.get().zfill(2)}/"
            f"{meses[combo_mes_buscar.get()]}/"
            f"{combo_anio_buscar.get()}"
        )
        sexo = combo_sexo_buscar.get()
        for paciente in pacientes:
            if (
                paciente.nombre.upper() == nombre and
                paciente.apellido_p.upper() == paterno and
                paciente.apellido_m.upper() == materno and
                paciente.fecha_nacimiento == fecha and
                paciente.sexo == sexo
            ):
                texto = (
                    f"Nombre: {paciente.nombre}\n"
                    f"Apellido paterno: {paciente.apellido_p}\n"
                    f"Apellido materno: {paciente.apellido_m}\n"
                    f"Fecha nacimiento: {paciente.fecha_nacimiento}\n"
                    f"Sexo: {paciente.sexo}\n"
                    f"CURP: {paciente.curp}\n"
                )
                resultado_busqueda.config(text=texto)
                tk.Button(
                    pestana_busqueda,
                    text="Abrir cartilla",
                    command=lambda p=paciente: ventana_vacunas(p)
                    ).grid(row=11, column=1)
                return
        resultado_busqueda.config(
            text="Paciente no encontrado"
        )
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
ventana = tk.Tk()
cargar_pacientes()
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
    text=f"Pacientes registrados: {len(pacientes)}"
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
ventana.protocol(
    "WM_DELETE_WINDOW",
    lambda: (
        guardar_pacientes(),
        ventana.destroy()
    )
)
ventana.mainloop()