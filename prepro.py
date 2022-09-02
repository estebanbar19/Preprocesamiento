from sys import flags
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import pandas

def preprocesamiento():
    #dataframe
    dataframe = pandas.read_csv("datos.csv", delimiter=",", header=None)
    abreviaciones = pandas.read_csv("abreviaciones.csv", delimiter=";")
    contracciones = pandas.read_csv("contracciones.csv", delimiter=";")
    etiquetas = pandas.read_csv("etiquetas.csv", delimiter=";")
    tweets = pandas.DataFrame(data=dataframe)

    #Reemplazando contracciones
    for i in range(len(contracciones['contraccion'])):
        tweets.iloc[:,10].replace(to_replace=r'\s'+contracciones['contraccion'][i]+'\s', value =" "+contracciones['palabra'][i]+" ", inplace=True, regex=True)
        
    #Reemplazando abreviaciones
    for i in range(len(abreviaciones['abreviacion'])):
        tweets.iloc[:,10].replace(to_replace=abreviaciones['abreviacion'][i]+'\s', value=f" {abreviaciones['palabra'][i]} ", regex=True, inplace=True)

    #Reemplazando nombres de usuario    
    tweets.iloc[:,10].replace(to_replace=r'@[\w]{1,15}', value="username", regex=True, inplace=True)

    #Añadir etiquetas(Reemplazar simbolos por etiquetas)
    for i in range(len(etiquetas['simbolos'])):
        tweets.iloc[:,10].replace(to_replace=etiquetas['simbolos'][i], value= etiquetas['etiquetas'][i], regex=True, inplace=True)
    
    #Reemplazo de Urls
    tweets.iloc[:,10].replace("http\S+", "", regex=True, inplace=True)

    #Reemplazo de numeros
    tweets.iloc[:,10].replace("[0-9]+", "", regex=True, inplace=True)

    #Remover stopwords
    aux = tweets.iloc[:,10].lower()
    out = ''.join([i for i in aux if i not in string.punctuation])
    stop_words = set(stopwords.words('spanish'))
    word_tokens = word_tokenize(out)
    out1 = ""
    for w in word_tokens:
        if w not in stop_words:
            out1 += w +" "
    out1 = out1.strip()
    tweets.iloc[:,10] = out1

    #Guardando los cambios los cambios
    tweets.to_csv("preprocesamiento.csv")
    

