# ⏳ HORAS_EXTRAS: Calculadora de Turnos y Recargos

Este es un sistema simple de consola escrito en Python para calcular las horas trabajadas en diferentes tipos de turnos (Diurno, Nocturno, Festivo) y desglosar los recargos correspondientes.

## 🚀 Despliegue y Uso (Versión Ejecutable)

La forma más sencilla de utilizar la aplicación en Windows es descargando la versión compilada:

1.  **Descargue el Ejecutable:** Diríjase a la sección [**Releases**](https://github.com/juanangel89/horas_extras/releases/tag/horas_extras) del repositorio.
2.  Busque el último lanzamiento y descargue el archivo `main.exe`.
3.  Ejecute el archivo `main.exe` haciendo doble clic. La aplicación se abrirá en la terminal de Windows.

*(Nota: El archivo `main.exe` se encuentra en la carpeta `dist/` en el código fuente, pero se recomienda descargar desde la sección Releases.)*

## 🐍 Estructura del Proyecto

* `main.py`: Script principal que maneja la entrada de usuario y la lógica del bucle.
* `clases/turnos.py`: Contiene la lógica de las clases y métodos para el cálculo de turnos (`calcular_turnos`, `partir_horas_nocturnas`, etc.).
* `dist/`: Carpeta que contiene el binario compilado (`main.exe`) generado por PyInstaller.

## 💻 Requerimientos para Ejecutar el Código Fuente

Si desea modificar el código o ejecutarlo sin el `.exe`, necesitará:
1. Python 3.x
2. Las dependencias listadas en `requirements.txt` (si aplica).
