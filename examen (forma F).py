def validar_texto_no_vacio(valor):
    return valor.strip() != ""

def validar_codigo(codigo, productos, stock):
    if not validar_texto_no_vacio(codigo):
        return False
    if codigo.upper() in [c.upper() for c in productos] or codigo.upper() in [c.upper() for c in stock]:
        return False
    return True

def validar_peso(peso_texto):
    try:
        peso = float(peso_texto)
        return peso > 0
    except ValueError:
        return False

def validar_si_no(valor):
    return valor.strip().lower() in ("s", "n")

def validar_precio(precio_texto):
    try:
        precio = int(precio_texto)
        return precio > 0
    except ValueError:
        return False

def validar_unidades(unidades_texto):
    try:
        unidades = int(unidades_texto)
        return unidades >= 0
    except ValueError:
        return False

def leer_opcion():
    while True:
        entrada = input("Ingrese opción: ")
        try:
            opcion = int(entrada)
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")

def unidades_categoria(categoria, productos, stock):
    total = 0
    for codigo in productos:
        if productos[codigo][1].lower() == categoria.lower():
            if codigo in stock:
                total += stock[codigo][1]
    print(f"El total de unidades disponibles es: {total}")

def busqueda_precio(p_min, p_max, productos, stock):
    resultados = []
    for codigo in stock:
        precio = stock[codigo][0]
        unidades = stock[codigo][1]
        if p_min <= precio <= p_max and unidades != 0:
            nombre = productos[codigo][0]
            resultados.append(f"{nombre}--{codigo}")

    if len(resultados) == 0:
        print("No hay productos en ese rango de precios.")
    else:
        resultados.sort()
        print(f"Los productos encontrados son: {resultados}")

def buscar_codigo(codigo, diccionario):
    for clave in diccionario:
        if clave.lower() == codigo.lower():
            return True
    return False

def _codigo_real(codigo, diccionario):
    for clave in diccionario:
        if clave.lower() == codigo.lower():
            return clave
    return None

def actualizar_precio(codigo, nuevo_precio, stock):
    if buscar_codigo(codigo, stock):
        clave_real = _codigo_real(codigo, stock)
        stock[clave_real][0] = nuevo_precio
        return True
    else:
        return False

def agregar_producto(codigo, nombre, categoria, marca, peso_kg, es_importado,
                      es_para_cachorro, precio, unidades, productos, stock):
    if buscar_codigo(codigo, productos) or buscar_codigo(codigo, stock):
        return False

    productos[codigo] = [nombre, categoria, marca, peso_kg, es_importado, es_para_cachorro]
    stock[codigo] = [precio, unidades]
    return True

def eliminar_producto(codigo, productos, stock):
    if buscar_codigo(codigo, productos):
        clave_real = _codigo_real(codigo, productos)
        del productos[clave_real]
        if codigo in stock or buscar_codigo(codigo, stock):
            clave_stock = _codigo_real(codigo, stock)
            if clave_stock is not None:
                del stock[clave_stock]
        return True
    else:
        return False

def main():
    productos = {
        'M001': ['Alimento Premium', 'comida', 'DogPlus', 10, True, False],
        'M002': ['Arena Aglomerante', 'higiene', 'CatClean', 8, False, False],
        'M003': ['Snack Dental', 'snack', 'BiteJoy', 1, True, True],
        'M004': ['Shampoo Suave', 'higiene', 'PetCare', 0.5, False, True],
        'M005': ['Correa Nylon', 'accesorio', 'WalkPro', 0.3, True, False],
        'M006': ['Cama Mediana', 'accesorio', 'CozyPet', 2, False, False],
    }

    stock = {
        'M001': [32990, 12],
        'M002': [9990, 0],
        'M003': [5490, 25],
        'M004': [7990, 5],
        'M005': [11990, 7],
        'M006': [24990, 3],
    }

    continuar = True
    while continuar:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Unidades por categoría")
        print("2. Búsqueda de productos por rango de precio")
        print("3. Actualizar precio de producto")
        print("4. Agregar producto")
        print("5. Eliminar producto")
        print("6. Salir")
        print("=====================================")

        opcion = leer_opcion()

        if opcion == 1:
            categoria = input("Ingrese categoría a consultar: ")
            unidades_categoria(categoria, productos, stock)

        elif opcion == 2:
            valores_validos = False
            while not valores_validos:
                try:
                    p_min = int(input("Ingrese precio mínimo: "))
                    p_max = int(input("Ingrese precio máximo: "))
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        valores_validos = True
                    else:
                        print("Debe ingresar valores enteros")
                except ValueError:
                    print("Debe ingresar valores enteros")
            busqueda_precio(p_min, p_max, productos, stock)

        elif opcion == 3:
            repetir = True
            while repetir:
                codigo = input("Ingrese código del producto: ")

                nuevo_precio = None
                while nuevo_precio is None:
                    try:
                        valor = int(input("Ingrese nuevo precio: "))
                        if valor > 0:
                            nuevo_precio = valor
                        else:
                            print("El precio debe ser un entero positivo")
                    except ValueError:
                        print("El precio debe ser un entero positivo")

                resultado = actualizar_precio(codigo, nuevo_precio, stock)
                if resultado:
                    print("Precio actualizado")
                else:
                    print("El código no existe")

                respuesta = input("¿Desea actualizar otro precio (s/n)?: ")
                while respuesta.strip().lower() not in ("s", "n"):
                    respuesta = input("¿Desea actualizar otro precio (s/n)?: ")
                repetir = respuesta.strip().lower() == "s"

        elif opcion == 4:
            codigo = input("Ingrese código del producto: ")
            nombre = input("Ingrese nombre: ")
            categoria = input("Ingrese categoría: ")
            marca = input("Ingrese marca: ")
            peso_texto = input("Ingrese peso (kg): ")
            es_importado_texto = input("¿Es importado? (s/n): ")
            es_para_cachorro_texto = input("¿Es para cachorro? (s/n): ")
            precio_texto = input("Ingrese precio: ")
            unidades_texto = input("Ingrese unidades: ")

            valido = True

            if not validar_codigo(codigo, productos, stock):
                print("El código no es válido o ya existe")
                valido = False

            if valido and not validar_texto_no_vacio(nombre):
                print("El nombre no es válido")
                valido = False

            if valido and not validar_texto_no_vacio(categoria):
                print("La categoría no es válida")
                valido = False

            if valido and not validar_texto_no_vacio(marca):
                print("La marca no es válida")
                valido = False

            if valido and not validar_peso(peso_texto):
                print("El peso no es válido")
                valido = False

            if valido and not validar_si_no(es_importado_texto):
                print("El valor de importado no es válido")
                valido = False

            if valido and not validar_si_no(es_para_cachorro_texto):
                print("El valor de cachorro no es válido")
                valido = False

            if valido and not validar_precio(precio_texto):
                print("El precio no es válido")
                valido = False

            if valido and not validar_unidades(unidades_texto):
                print("Las unidades no son válidas")
                valido = False

            if valido:
                peso_kg = float(peso_texto)
                es_importado = es_importado_texto.strip().lower() == "s"
                es_para_cachorro = es_para_cachorro_texto.strip().lower() == "s"
                precio = int(precio_texto)
                unidades = int(unidades_texto)

                resultado = agregar_producto(codigo, nombre, categoria, marca, peso_kg,
                                              es_importado, es_para_cachorro, precio,
                                              unidades, productos, stock)
                if resultado:
                    print("Producto agregado")
                else:
                    print("El código ya existe")

        elif opcion == 5:
            codigo = input("Ingrese código del producto: ")
            resultado = eliminar_producto(codigo, productos, stock)
            if resultado:
                print("Producto eliminado")
            else:
                print("El código no existe")

        elif opcion == 6:
            print("Programa finalizado.")
            continuar = False