def cimprime(**kwargs) -> None:
    if "titulo" in kwargs.keys():
        print(kwargs["titulo"])
    else:
        print("VARIABLES MONITOREADAS")
    print("--------------------------")
    for llave in kwargs.keys():
        if llave != "titulo":
            print(f"{llave}: {kwargs[llave]}")
    print("--------------------------\n")