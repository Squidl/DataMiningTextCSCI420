import text_format
import text_proccessing
import stat_proccessing

def main():
    for x in text_format.texts:
        text_proccessing(x)
        stat_proccessing(x)
    
