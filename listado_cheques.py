import csv
import time
import os

# Solicitar al usuario el nombre del archivo CSV
nombre_archivo = input("Ingrese el nombre del archivo CSV: ")

# Validar si el archivo existe
if not os.path.exists(nombre_archivo):
    print("El archivo especificado no existe.")
    exit()

DNI_cliente = input("Ingrese el DNI del cliente: ")

# Validar si el DNI es numérico y tiene longitud correcta
if not DNI_cliente.isdigit() or len(DNI_cliente) < 7 or len(DNI_cliente) > 8:
    print("DNI inválido. Debe contener solo números y tener entre 7 y 8 dígitos.")
    exit()

tipo_cheque = input("Ingrese el tipo de cheque (EMITIDO o DEPOSITADO): ").upper()

# Validar tipo de cheque
if tipo_cheque not in ['EMITIDO', 'DEPOSITADO']:
    print("Tipo de cheque inválido. Debe ser 'EMITIDO' o 'DEPOSITADO'.")
    exit()

salida_cheque = input("Ingrese la salida del cheque (PANTALLA o CSV): ").upper()

# Validar salida
if salida_cheque not in ['PANTALLA', 'CSV']:
    print("Salida inválida. Debe ser 'PANTALLA' o 'CSV'.")
    exit()

# Abrir y leer el archivo CSV
try:
    with open(nombre_archivo, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        filtered_rows = [row for row in reader if row['DNI'] == DNI_cliente and row['Tipo'].upper() == tipo_cheque]
        
        if salida_cheque == 'PANTALLA':
            if filtered_rows:
                for row in filtered_rows:
                    print(row)
            else:
                print("No se encontraron cheques con el DNI y tipo especificados.")
        elif salida_cheque == 'CSV':
            if filtered_rows:
                timestamp = time.strftime("%Y%m%d%H%M%S")
                output_filename = f"{DNI_cliente}_{timestamp}.csv"
                # Solo se crea el archivo si hay filas para escribir
                with open(output_filename, mode='w', newline='') as output_csv:
                    fieldnames = ['NroCheque', 'CodigoBanco', 'CodigoSucursal', 'NumeroCuentaOrigen', 'NumeroCuentaDestino', 'Valor', 'FechaOrigen', 'FechaPago', 'DNI', 'Estado', 'Tipo']
                    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(filtered_rows)
                print(f"Archivo CSV generado: {output_filename}")
            else:
                print("No se encontraron cheques con el DNI y tipo especificados, no se generó ningún archivo.")
except Exception as e:
    print(f"Error al procesar el archivo: {e}")