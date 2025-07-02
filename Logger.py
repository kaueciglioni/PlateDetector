import os
from datetime import datetime
import os.path


# nome do arquivo: data, Transcription, .log
# 20220920_Transcription.log
# virar o dia cria um novo arquivo
strPath = os.path.realpath(__file__)
nmFolders = strPath.split(os.path.sep)
nmFolders = nmFolders[4]


pasta = "Logs/"
create_logtime = datetime.now().strftime("%Y%m%d")
#current_time = datetime.now().strftime("%Y%m%d_%H%M%S.%f")

filename = pasta+ nmFolders + '_' + str(create_logtime) + '.log'
#metodo central, tipo escrever tudo, o resto só informa o nivel


# info
# padrão C# Log.Logger.Debug("ServerCommunication", "ProcessMessage", l_msg);


def writeLog(p_className,  p_method,  p_message):
        
    try:
        global create_logtime
        global filename
        check_logtime = datetime.now().strftime("%Y%m%d")
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        
        if(create_logtime != check_logtime):
            create_logtime = check_logtime
            filename = pasta+ nmFolders + '_' + str(create_logtime) + '.log'

        if(os.path.isdir(pasta)!= True):
            os.mkdir(pasta)
            
        if(os.path.exists(filename)):
            count = 1
            tamanho = (os.stat(filename).st_size) / (1024 * 1024)
            while((os.path.exists(filename) and tamanho >= 300)):
                filename = pasta+nmFolders + '_' + str(create_logtime) + '_' + str(datetime.now().strftime("%H%M%S")) + '.log'
                count+=1
        
        msg = "["+ current_time + "] " + p_className + "." + p_method + ": " + p_message +"\n"
        
        with open(filename, "a+") as f:
            f.write(msg)
        list_of_files = os.listdir('./Logs')
        files = []
        for item in list_of_files :
            files.append("Logs/" + item)
        if len(files) > 20:
            oldest_file = min(files, key=os.path.getctime)
            os.remove((oldest_file))

    except Exception as e:
        print("Error writeLog: "+str(e))
        print()

def info(p_message):

    try:
        global create_logtime
        global filename
        check_logtime = datetime.now().strftime("%Y%m%d")
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S.%f")

        if(create_logtime != check_logtime):
            create_logtime = check_logtime
            filename = pasta+ nmFolders + '_' + str(create_logtime) + '.log'
       
        if(os.path.isdir(pasta)!= True):
            os.mkdir(pasta)
        if(os.path.exists(filename)):
            count = 1
            tamanho = (os.stat(filename).st_size) / (1024 * 1024)
            while((os.path.exists(filename) and tamanho >= 300)):
                filename=pasta+nmFolders + '_' + str(create_logtime) +'_' + str(datetime.now().strftime("%H%M%S")) + '.log'
                count+=1

        msg = "["+ current_time + "] Info: " +  p_message+"\n"
        
        with open(filename, "a+") as f:
            f.write(msg)

        list_of_files = os.listdir('./Logs')
        files = []
        for item in list_of_files :
            files.append("Logs/" + item)
        if len(files) > 20:
            oldest_file = min(files, key=os.path.getctime)
            os.remove((oldest_file))    
            
    except Exception as e:
        print("Error info: "+str(e))
        print()


# error
def error(p_className,  p_method,  p_exception):

    try:
        #print(p_className, "****", p_method, "****", p_exception)
        writeLog(("Error: " + p_className), p_method, p_exception)

    except Exception as e:
        print("Error error: "+str(e))
        print()

# debug
def debug(p_className,  p_method,  p_message):

    try:
        #print(p_className, "****", p_method, "****", p_message)
        writeLog(("Debug: " +p_className), p_method, p_message)
        

    except Exception as e:
        print("Error debug: "+str(e))
        print()


if __name__ == "__main__":
    '''#info("teste testes")
    try:
        #info("Main: before creating thread")
        x = 0
        while(True):
            info("Iniciando teste *******")
            debug("Logger","Thread","Decorrer do teste")
            x1 = threading.Thread(target=info, args=(str('testando info'),))
            x1.start()
            x2 = threading.Thread(target=debug, args=("Logger", "Thread", "testando debug"))
            x2.start()
            x3 = threading.Thread(target=error, args=("Logger", "Thread", "testando error"))
            x3.start()
            error("Logger","Thread","Fim do teste *******")
            x+=1
    except Exception as e:
        print(e)'''