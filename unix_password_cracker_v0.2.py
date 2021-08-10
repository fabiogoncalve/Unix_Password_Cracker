import crypt
from time import process_time

#indica a primeira contagem de tempo do script
t_start_script = process_time() 

#Abre o ficheiro 'top_worst_passwords.txt' e armazena todas password
#numa lista já sem "Enter´s"
list_pass_worst = []                                                                            
with open ('top_worst_passwords.txt') as file_pass_worst:                  
    for line_pass_worst in file_pass_worst:               
        list_pass_worst.append(line_pass_worst.rstrip())  
                                 
        
#Abre o ficheiro 'linux_passwd_sample.txt' e primeiro descarta todas as linhas
#que nao contenham $ e depois separa as Strings pelo operador ':' 
#Em seguida guarda em duas listas diferentes tudo que está posição 0 e 1        
list_user= []
list_hash=[]
with open('linux_passwd_sample.txt') as file_pass_server:
    for line_server_pass in file_pass_server: 
        if '$' in line_server_pass:
            file_server_pass = line_server_pass.split(':')
            list_user.append(file_server_pass[0])
            list_hash.append(file_server_pass[1])
            
            
#incicio da função principal, recebe os imputs do utilizador
def unix_password_cracker(first_reading,last_reading,first_read_pass,last_read_pass):
    
    #indica a primeira contagem de tempo da funçao
    t_start_func = process_time()
    
    #listas que vai guarda o nome dos clientes com password fraca
    #e respectiva password
    list_user_found=[]
    list_pass_found=[]

    #incio do ciclo para percorrer o numero de linhas do ficheiro 'linux_passwd_sample.txt' 
    for i in range(first_reading, last_reading+1):
        
       #incio do ciclo para percorrer o numero de linhas do ficheiro 'top_worst_passwords.txt' 
        for x in range(first_read_pass,last_read_pass+1):
            
            #formula para increpetar as password do ficheiro 'top_worst_passwords.txt' 
            # ou seja colocar como Hash para poder comparar
            hash_bad_pass = crypt.crypt(list_pass_worst[x], list_hash[i])
            
            #comparar o Hash dos 2 ficheiros
            #se encontrar deve indicar o user associado e o hash encontrado.
            if hash_bad_pass==list_hash[i]:
                print(f"\nFOUND!! Username {list_user[i]} uses password {list_pass_worst[x]}!")
                
                # guarda o nome dos clientes com password fraca   
                list_user_found=[list_user[i]]
                list_pass_found=[list_pass_worst[x]]
                
            #senão continua a pesquisa mas imprime 1 '*' sempre que acaba comparar
            # com uma das piores passwords
            else:
                print(end='*')

        #compara quando enconta a primeira linha do ficheiro 'linux_passwd_sample.txt'
        if i == first_reading:
            #indica a ultima contagem de tempo da função quando acaba de ler a primeira linha 
            t_inic_1line = process_time()
            
            #calcula de tempo o tempo de incio da função e ultimo tempo quando acaba de ler a primeira linha 
            t_estim_1line = t_inic_1line - t_start_func
            
            #Calculo de estimativa de tempo que o progama vai demorar
            #numero de linhas vezes o tempo estimado da primeira + o tempo desde começa a função e acaba o script do programa
            t_total_estim= round(t_estim_1line * (last_reading - first_reading) +  t_start_func - t_start_script, 1)
            print (f'\nEstimated time what program will take is: {t_total_estim}s!')
            
            #Input do utilizador se pretende continuar com a pesquisa
            q1 = str(input('Do you want to continue?(Y/N)'))
            if q1 == 'N' or q1 == 'n':
                break  
                
      # faz o calculo da estimativa de tempo que falta cada 10 linhas 
        for y in range(0,last_reading,10):
            if i==y:
                t_inicial_10lines=process_time()
                t_total_10lines=round(t_inicial_10lines-t_start_func,2)
                t_estim_10lines=round((t_total_estim-t_total_10lines)-t_estim_1line,2)
                if(t_estim_10lines>=0.00):
                    print(f'\n The expected time the program will take is: {t_estim_10lines}s!')
                else:
                    print(f'\n The program is taking longer than what was expected. It will end soon')
                
            
            
           
    #imprime o nome dos clientes com password fraca
    for z in range(len(list_user_found)):
        print(f'\nCustomers who have a weak password are: {list_user_found[z]} = {list_pass_found[z]};')
    
    #indica a ultima contagem de tempo do script
    t_stop_script = process_time()
    #Tempo real da duração do programa no completo
    t_total = round((t_stop_script - t_start_script),2)
    print(f'\nThe program took {t_total}s!')
    print('Finished!')

    
###########################################################################    

#função que facilita colocar (-1) nos ciclos,
#a todos valores que peço para utilizador colocar esta função desconta 1 
def conv_num (numero):  
    return numero - 1   

###########################################################################

#imputs pedidos ao utilizador
first_read_server =conv_num(int(input('Enter the number of the 1st line to check the "linux password file" (greater than 1): ')))
last_read_server = conv_num(int(input(f'Enter the number of the last line to check the "linux password file" (less than {len(list_hash)}): ')))
first_read_pass = conv_num (int(input('Enter the number of the 1st line to check the "worst password file" (greater than 1): ')))
last_read_pass = conv_num (int(input(f'Enter the number of the last line to check the "worst password file" (less than {len(list_pass_worst)}): ')))

#função principal do programa com os imputs do utilizador 
unix_password_cracker(first_read_server,last_read_server,first_read_pass,last_read_pass)