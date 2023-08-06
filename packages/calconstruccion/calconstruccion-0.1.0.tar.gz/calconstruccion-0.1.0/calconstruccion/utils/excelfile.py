#funciones
import pandas as pd
import openpyxl

#Leer archivo
def read_funciones(excel_file):
  df = pd.read_excel(excel_file,sheet_name=5)
  return df

#Editar contenido archivo basado en código
def edit_value (id,param,new_value,df):
  df.loc[(df.Codigo == id),param]= new_value
  return update_values(df)

def update_values(df):
  df['precio_total'] = df['cantidad'] * df['precio_unitario']
  df.loc[(df.precio_unitario == 'SUBTOTAL'),'precio_total']= df['precio_total'].sum()
  return df

def save_changes(df,input_file):
  ##modify sheet PYTHON as needed.. then to save it back:
  with pd.ExcelWriter(input_file) as writer:
      df.to_excel(writer, sheet_name="PYTHON", index=False)
  return('file saved successfully')