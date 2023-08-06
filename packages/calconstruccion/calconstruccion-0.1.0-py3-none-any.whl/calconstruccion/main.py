from calconstruccion.utils.excelfile import *

#main
input_file = '.\calconstruccion\database.xlsx'

df = read_funciones(input_file)
#Modificar la cantidad de tipos hormigones basado en su código
df = edit_value(22,'cantidad',200,df)
#Modificar el precio de tipos hormigones basado en su código
df = edit_value(24,'precio_unitario',106.12,df)
#Modificar el nombre de tipos hormigones basado en su código
df = edit_value(25,'HORMIGONES_ESTRUCTURA','Hormigón en cadena de prueba',df)

#Guardar cambios de archivo
save_changes(df,input_file)

print(df)