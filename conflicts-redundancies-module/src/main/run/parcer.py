arquivoregras = open("../data/informations.txt", "r")

arquivo_resultado = open("../data/resultado.txt", "w")
string_acc = ""

for info in arquivoregras.readlines():
    string_acc = string_acc + ("str(lista_" + info + "[ifw]) + \" ^ \" + ")

arquivo_resultado.write(string_acc)
arquivoregras.close()
arquivo_resultado.close()
