import json
import controller_db

this_need_be_commited = []
trans_stand_by = []
linhas_divididas = []

controller_db.start_db()


with open('Caminho do arquivo de execução/transacoes.txt', 'r') as arquivo:
    linhas = arquivo.readlines()


for linha in linhas:
    partes = linha.split(',')

    linhas_divididas.extend(partes)



ct = 0

print("1 - Executar transação\n")
print("2 - Verificar valores salvos\n")


n = int(input("Selecione um valor: \n"))

while (n!= 0):

    if (n == 1):
        for parte in linhas_divididas:
            if "<start T" in parte:
                trans_stand_by.append(linhas_divididas[ct][7:][:-2])
            if "<T" in parte:
                this_need_be_commited.append(linhas_divididas[ct])
                this_need_be_commited.append(linhas_divididas[ct + 1])
                this_need_be_commited.append(linhas_divididas[ct + 2])
                this_need_be_commited.append(linhas_divididas[ct + 3][:+2])
            if "<START CKPT" in parte:
                ctc = 0
                for vlr in this_need_be_commited:
                    if "<T" in vlr:
                        controller_db.commit(this_need_be_commited[ctc+1], this_need_be_commited[ctc+2], this_need_be_commited[ctc+3])
                    ctc+=1
                this_need_be_commited = [] 
                trans_stand_by = []
            if "END" in parte: 
                ctc = 0
                for vlr in this_need_be_commited:
                    if "<T" in vlr:
                            controller_db.commit(this_need_be_commited[ctc+1], this_need_be_commited[ctc+2], this_need_be_commited[ctc+3])
                    ctc+=1
                this_need_be_commited = []
                trans_stand_by = []
            ct+=1

        for t in trans_stand_by:
            print("Transação {} realizou UNDO".format(t))
    if (n == 2):
        controller_db.select_db()
    n = int(input("Selecione um valor: \n"))

controller_db.NOW_GO_AND_JUST_DROP_IT()