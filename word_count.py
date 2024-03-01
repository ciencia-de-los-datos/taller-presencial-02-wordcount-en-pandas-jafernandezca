"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    files = glob.glob(f"{input_directory}/*.txt")
    dataframes = []

    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            df = pd.DataFrame(lines, columns=['Contenido'])
            dataframes.append(df)

    # Concatena todos los DataFrames en uno solo
    result_df = pd.concat(dataframes, ignore_index=True)

    return result_df



def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    if 'Contenido' in dataframe.columns:
        dataframe['Cleaned_Contenido'] = dataframe['Contenido'].str.replace('[^\w\s]', '', regex=True).str.lower()
    else:
        print("La columna 'Contenido' no existe en el DataFrame.")

    return dataframe



def count_words(dataframe):
    """Word count"""
    if 'Cleaned_Contenido' in dataframe.columns:
        # Divide cada línea en palabras y cuenta la frecuencia de cada palabra en cada fila
        words_per_row = dataframe['Cleaned_Contenido'].str.split().apply(lambda x: pd.Series(x).value_counts())

        # Suma la frecuencia de cada palabra en todo el DataFrame
        total_word_count = words_per_row.sum(axis=0, skipna=True).reset_index()
        total_word_count.columns = ['word', 'count']
        
        # Ordena el DataFrame por palabra en orden ascendente
        total_word_count = total_word_count.sort_values(by='word')


        return total_word_count
    else:
        print("La columna 'Cleaned_Contenido' no existe en el DataFrame.")
        return None




def save_output(dataframe, output_filename):
    """Save output to a file."""
    # Guarda el DataFrame en un archivo de texto con formato txt y tabulador como delimitador
    dataframe.to_csv(output_filename, sep='\t', header=None)


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    # Cargar datos
    loaded_data = load_input(input_directory)

    # Limpiar texto
    cleaned_data = clean_text(loaded_data)

    # Contar palabras
    word_count_result = count_words(cleaned_data)

    # Guardar resultado
    save_output(word_count_result, output_filename)


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
