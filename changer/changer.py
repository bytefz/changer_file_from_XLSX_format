from os.path import join
from operator import xor
import pandas as pd
import sys
import os


"""
It is a simple script that changes the name of files from a directory
taking from a xlsx file's columns.

Conditions:
    - The path have to be indicated in the first argument on the command line.
    - Each file must have the same name as each column name called 'CÓDIGO CATALOGO'
    - The file's sheet must have the name 'DATA'
    - The '.xlsx' extension must just have 3 columns ["CODIGO INTERNO","CÓDIGO CATALOGO","MARCA"]

"""


def list_path() -> list:
    """
    Setting the location file and the directory where the files will be changed
    """
    return sys.argv


def procesing_data(_path) -> tuple:
    """
    Function that takes the data from the xlsx file and returns a cleaned dataframe.
    """
    # Getting the file
    excel = pd.read_excel(_path, sheet_name="DATA")

    # Changing the name columns
    excel.columns = excel.iloc[0]

    # Updating and deleting the row
    excel = excel.drop(excel.index[0])
    excel = excel.reset_index()

    # Selecting usefull columns
    data = excel[["CODIGO INTERNO", "CÓDIGO CATALOGO", "MARCA"]]

    # Converting in a better format for using easily
    data["CÓDIGO CATALOGO"] = data["CÓDIGO CATALOGO"].apply(lambda _: str(_))
    data["CODIGO INTERNO"] = data["CODIGO INTERNO"].apply(lambda _: str(_))

    # Selecting unique brands
    brand_list = data["MARCA"].unique()

    return data, brand_list


def without_back(variable) -> str:
    """
    Function that takes a string and returns the string without the ('/', ':', '|'),
    beacuse it is not allowed in the name of the file.
    In the case the name file does not have any caracter from the tuple created, the function
    just returns the string inself.

    """
    for caracter in ("/", ":", "|"):
        if caracter in variable:
            return variable.replace(caracter, " ")
        else:
            return variable
        
        
def rename_function(product, producto_excel, _direc, data, jpg=True, pdf=False) -> None:
    
    """
    Change the name of the file.
    
    Parameters:
    ----------
        * product: The name file to change.
        * producto_excel: New name of the file.
        * data: Dataframe with the cleaned data.
        * jpg: If the file is a jpg, so True. If not, so False. (Default: True)
        * pdf: If the file is a pdf, so True. If not, so False. (Default: False)
    
    Returns:
    -------
    None
    """
    
    producto_excel_out = without_back(producto_excel)
    
    if xor(jpg,pdf):
        if jpg==True and pdf==False:
            formato = ".jpg"
            
            if product.replace(formato, "") == producto_excel_out:
                nuevo_producto = data.loc[data["CÓDIGO CATALOGO"]== producto_excel]["CODIGO INTERNO"].values[0]

                print(f"{product} --> {nuevo_producto}{formato}")
                os.rename(join(os.getcwd(), product), join(os.getcwd(), nuevo_producto+formato))
                
        if jpg==False and pdf==True:
            formato = ".pdf"
            
            if product.replace(formato, "") == producto_excel_out:
                nuevo_producto = data.loc[data["CÓDIGO CATALOGO"]== producto_excel]["CODIGO INTERNO"].values[0]

                print(f"{product} --> {nuevo_producto}{formato}")
                os.rename(join(os.getcwd(), product), join(os.getcwd(), nuevo_producto+formato))

    else:
        return f"La extensión del archivo solo puede ser una de las siguientes: jpg o pdf"
    


def main():

    """
    Main Program that gets a list name files from a directory and change the name of the files.
    
    """

    _, _path, general_path = list_path()

    data, brand_list = procesing_data(_path)

    with os.scandir(general_path) as ficheros:
        subdirectorios = [fichero.name for fichero in ficheros if fichero.is_dir()]

    for brand in brand_list:
        if brand in subdirectorios:
            brand_path = join(general_path, brand)
            os.chdir(brand_path)

            with os.scandir(os.getcwd()) as dir:
                # Para los directorios
                sub = [a.name for a in dir if a.is_dir()]
                print(sub)

            if len(sub) == 0:
                content = os.listdir(os.getcwd())
                files = []

                for i in content:
                    if os.path.isfile(join(os.getcwd(), i)) and i.endswith(".jpg"):
                        files.append(i)

                for product in files:
                    product = str(product)
                    try:
                        if os.path.exists(join(os.getcwd(), product)):
                            for producto_excel in data["CÓDIGO CATALOGO"].values:

                                producto_excel = str(producto_excel)
                                
                                if ("/" in producto_excel) or (":" in producto_excel) or ("|" in producto_excel):
                                    producto_excel_out = without_back(producto_excel)
                                    
                                    rename_function(product, producto_excel, data, jpg=True, pdf=False)
                                    
                                else:
                                    rename_function(product, producto_excel, data, jpg=True, pdf=False)

                    except BaseException as e:
                        print(f"No existe el producto: {product}")
                        print(e)
                        continue

            else:
                for direc in sub:
                    if direc == "images":
                        actual_images_path = join(os.getcwd(), direc)
                        
                        content = os.listdir(actual_images_path)
                        files = []

                        for i in content:
                            image_file = join(actual_images_path, i)
                            if os.path.isfile(image_file) and i.endswith(".jpg"):
                                files.append(i)

                        for product in files:
                            product = str(product)
                            try:

                                if os.path.exists(join(actual_images_path, product)):

                                    for producto_excel in data["CÓDIGO CATALOGO"].values:

                                        producto_excel = str(producto_excel)

                                        if ("/" in producto_excel) or (":" in producto_excel) or ("|" in producto_excel):

                                            producto_excel_out = without_back(producto_excel)

                                            if product.replace(".jpg", "") == producto_excel_out:

                                                nuevo_producto = data.loc[data["CÓDIGO CATALOGO"]== producto_excel]["CODIGO INTERNO"].values[0]

                                                print(f"{product} --> {nuevo_producto}.jpg")

                                                os.rename(join(actual_images_path, product), join(actual_images_path, nuevo_producto+".jpg"))

                                        else:
                                            if product.replace(".jpg", "") == producto_excel:

                                                nuevo_producto = data.loc[data["CÓDIGO CATALOGO"] == product.replace(".jpg", "")]["CODIGO INTERNO"].values[0]

                                                print(f"{product} --> {nuevo_producto}.jpg")

                                                os.rename(join(actual_images_path, product), join(actual_images_path, nuevo_producto+".jpg"))

                            except BaseException as e:
                                print(f"No existe el producto: {product}")
                                print(e)
                                continue

                    if direc == "files":

                        actual_images_path = join(os.getcwd(), direc)
                        content = os.listdir(actual_images_path)
                        files = []
                        # print(content)

                        for i in content:
                            image_file = join(actual_images_path, i)
                            if os.path.isfile(image_file) and i.endswith(".pdf"):
                                files.append(i)

                        for product in files:
                            product = str(product)

                            try:
                                # print(join(actual_images_path,product))

                                if os.path.exists(join(actual_images_path, product)):

                                    for producto_excel in data["CÓDIGO CATALOGO"].values:

                                        producto_excel = str(producto_excel)

                                        if ("/" in producto_excel) or (":" in producto_excel) or ("|" in producto_excel):

                                            producto_excel_out = without_back(
                                                producto_excel)

                                            if product.replace(".pdf", "") == producto_excel_out:

                                                nuevo_producto = data.loc[data["CÓDIGO CATALOGO"]== producto_excel]["CODIGO INTERNO"].values[0]

                                                print(
                                                    f"{product} --> {nuevo_producto}.pdf")

                                                os.rename(join(actual_images_path, product), join(actual_images_path, nuevo_producto+".pdf"))

                                        else:
                                            if product.replace(".pdf", "") == producto_excel:

                                                nuevo_producto = data.loc[data["CÓDIGO CATALOGO"] == product.replace(".pdf", "")]["CODIGO INTERNO"].values[0]

                                                print(
                                                    f"{product} --> {nuevo_producto}.pdf")

                                                os.rename(join(actual_images_path, product), join(actual_images_path, nuevo_producto+".pdf"))

                            except BaseException as e:
                                print()
                                print(f"{producto_excel}")
                                print(f"No existe el producto: {product}")
                                print(e)
                                continue


if __name__ == "__main__":
    main()