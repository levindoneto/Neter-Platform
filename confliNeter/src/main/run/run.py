#!/usr/bin/python
# coding: UTF-8

# Bibliotecas utilizadas
import os
import sys
import json
from os import system
import time

cont_time = 0

arquivoFormatadoJson = "../data/dataflow_formato.json"

# Inicializando variaveis - Adicionar regras no Firewall (opt 2)
#-> Informações - Match - Flowtable
eth_src = ""
eth_dst = ""
eth_type = ""
in_port = ""
eth_vlan_vid = ""
eth_vlan_pcp = ""
ip_proto = ""
ipv4_src = ""
ipv4_dst = ""
ipv6_src = ""
ipv6_dst = ""
ipv6_label = ""
ip_tos = ""
ip_ecn = ""
ip_dscp = ""
tp_src = ""
tp_dst = ""
udp_src = ""
udp_dst = ""
tcp_src = ""
tcp_dst = ""
sctp_src = ""
sctp_dst = ""
icmpv4_type = ""
icmpv4_code = ""
icmpv6_type = ""
icmpv6_code = ""
ipv6_nd_ssl = ""
ipv6_nd_ttl = ""
ipv6_nd_target = ""
arp_opcode = ""
arp_tha = ""
arp_spa = ""
arp_tpa = ""
mpls_label = ""
mpls_tc = ""
mpls_bos = ""
tunnel_id = ""
metadata = ""
#-> Informações - Match - Firewall
dl_type = ""
nw_src_prefix = ""
any_nw_dst = ""
any_nw_proto = ""
any_in_port = ""
any_nw_srcany_tp_ds = ""
ruleid = ""
any_dl_type = ""
priority = ""
in_port = ""
any_dpid = ""
dl_src = ""
nw_src_maskbits = ""
nw_dst_maskbits = ""
dpid = ""
tp_src = ""
any_dl_dst = ""
nw_dst_prefix = ""
nw_proto = ""
tp_dst = ""
dl_dst = ""
any_tp_src = ""
action = ""

''' Funcoes principais '''
# Para formatacao de arquivos json gerados pela rede
def formatarJson(nome_do_arquivo, var_buffer):
	arquivo_json = nome_do_arquivo
	var_buffer = open(arquivo_json, "r")
	dicionario = ""

	for i in var_buffer:
		dicionario += i

	strings = ""
	cont = 0

	for j in dicionario:
	    if j == "u":
		    if dicionario[cont+1] == "'":
		        strings +=""
		    else:
		        strings += j
	    else:
		    strings += j
	    cont += 1

	dicionario = ""

	for k in strings:
	    if k!= "'":
		    dicionario += k
	    else:
		    dicionario += '"'

	strings = ""
	for l in dicionario:
	    if l=="]" or l=="}":
		    strings += "\n" + l
	    elif l==",":
		    strings += l + "\n"
	    elif l=="{" or l=="[":
		    strings += "\n" + l + "\n"
	    else:
		    strings += l

	var_buffer = open(arquivo_json, "w")
	var_buffer.write(strings)
	var_buffer.close()
###########################################################

# Para deteccao de conflito entre dois fluxos
def conflito(fluxoCI, fluxoCJ, SwitchC):
	print "Detectado conflito entre o fluxo " + str(fluxoCI) + " e entre o fluxo " + str(fluxoCJ) + " no switch " + str(SwitchC)
###########################################################

# Para deteccao de redundancia entre dois fluxos
def redundancia(fluxoRI, fluxoRJ, SwitchR):
	print "Detectado redundancia entre o fluxo " + str(fluxoRI) + " e entre o fluxo " + str(fluxoRJ) + " no switch " + str(SwitchR)
###########################################################


opt = 10 # Inicializando variavel do menu
def menu():
    print("|---------------------------------------------|")
    print("|--------- SCRIPT FLOWTABLE FIREWALL ---------|")
    print("|---------------------------------------------|")
    print("| 1 - Gerar/atualizar tabela/csv              |")
    print("|     e verificar conflitos e                 |")
    print("|     redundancias da topologia criada        |")
    print("| 2 - Adicionar regra no Firewall (1 a 1)     |")
    print("| 3 - Adicionar regras no Firewall {string}   |")
    print("| 4 - Deletar regra no Fiewall                |")
    print("| 5 - Ver todas regras do Firewall            |")
    print("| 6 - Gerar/atualizar tabela/csv do Firewall  |")
    print("|     e verificar conflitos e redundancias    |")
    print("| 0 - Sair                                    |")
    print("|---------------------------------------------|")

    opt = raw_input("\nEscolha: ")

    return opt

while opt != "0":
    opt = menu()
    if opt=="1":
        start = time.time()
        print "\n"
        '''
        ip = raw_input("|----- Insira o IP da maquina: ")
        porta = raw_input("|----- Insira a porta: ")
        command = "curl -s http://" + ip + ":" + porta + "/wm/core/switch/all/flow/json"
        '''

        '''
        command = "curl -s http://143.54.12.11:8080/wm/core/switch/all/flow/json"

        command_output = os.popen(command).read()
        topology = json.loads(command_output)

        # Criando o arquivo com os dados de fluxos
        fluxos_dados = open("dataflow.json", "w")
        fluxos_dados.write(str(topology))
        fluxos_dados.close()

        '''
        ################################################################ >>>>>> DESCOMENTAR PORQUE TA FORMATANDO O ARQUIVO A CADA EXECUCAO
        #formatarJson("dataflow.json", "arquivoJson")

        flag_confRed = 0



        strings = ""
        arquivo_dados = open(arquivoFormatadoJson, "r")
        for i in arquivo_dados:
            strings += i
        arquivo_dados.close()

        with open(arquivoFormatadoJson) as f:
            data = f.read()
            json_data = json.loads(data)

        lista_switches = json_data.keys()

        # Arquivos de regras
        arquivo_regras = open("../data/regras.txt", "w")
        arquivo_regras_conflitantes = open("../data/regras_conflitantes.txt", "w")
        arquivo_regras_redundantes = open("../data/regras_redundantes.txt", "w")

        lista_csv = []                                    # Lista para armazenar os dicionarios que serao impressos no arquivo .csv
        contSwitch = 0
        for s in lista_switches:
            dicFlows = {}                             #Inicia/limpa dicFlows a cada execucao
                                  # Tabela com os fluxos sendo as linhas e as informacoes sendo as colunas
            with open(arquivoFormatadoJson) as f:
                data = f.read()
                json_data = json.loads(data)

            json_data = json_data[str(s)] # Tem que salvar isso no nome do switch
            json_data = json_data["flows"]

            # Listas organizadas por indice
            lista_prioridade =      []
            lista_duracao =         []
            lista_byteCount =       []
            lista_packetCount =     []
            lista_cookie =          []
            # Listas - Match
            lista_ethSrc =          []
            lista_ethDst =          []
            lista_ethType =         []
            lista_inPort =          []
            lista_eth_vlan_vid =    []
            lista_eth_vlan_pcp =    []
            lista_ip_proto =        []
            lista_ipv4_src =        []
            lista_ipv4_dst =        []
            lista_ipv6_src =        []
            lista_ipv6_dst =        []
            lista_ipv6_label =      []
            lista_ip_tos =          []
            lista_ip_ecn =          []
            lista_ip_dscp =         []
            lista_tp_src =          []
            lista_tp_dst =          []
            lista_udp_src =         []
            lista_udp_dst =         []
            lista_tcp_src =         []
            lista_tcp_dst =         []
            lista_sctp_src =        []
            lista_sctp_dst =        []
            lista_icmpv4_type =     []
            lista_icmpv4_code =     []
            lista_icmpv6_type =     []
            lista_icmpv6_code =     []
            lista_ipv6_nd_ssl =     []
            lista_ipv6_nd_ttl =     []
            lista_ipv6_nd_target =  []
            lista_arp_opcode =      []
            lista_arp_opcode =      []
            lista_arp_tha =         []
            lista_arp_spa =         []
            lista_arp_tpa =         []
            lista_mpls_label =      []
            lista_mpls_tc =         []
            lista_mpls_bos =        []
            lista_tunnel_id =       []
            lista_metadata =        []

            lista_actions =         []

            dicAux = {}   # Fica com o primeiro item da lista {0:lista0}

            #  Para verificar se a informacao(value) esta no arquivo json
            #  lista de dicionarios que contem listas, pega-se a primeira lista, porque se a informacao
            # esta' na primeira lista da key 0, entao a informacao esta' em todas keys do dicionario que
            # esta' dentro da lista principal do arquivo json
            cont = 0      # Indice do fluxo
            for dur in  json_data[0:-1]:
                dicAux = json_data[contSwitch]
                if dicAux.has_key('priority') == True:
                    lista_prioridade.append(str(json_data[cont]['priority']))
                else:
                    lista_prioridade.append("x")

                if dicAux.has_key('actions') == True:
                    lista_actions.append(str(json_data[cont]['actions']['actions']))
                else:
                    lista_actions.append("x")

                if dicAux.has_key('durationSeconds') == True:
                    lista_duracao.append(str(json_data[cont]['durationSeconds']))
                else:
                    lista_duracao.append("x")

                if dicAux.has_key('byteCount') == True:
                    lista_byteCount.append(str(json_data[cont]['byteCount']))
                else:
                    lista_byteCount.append("x")

                if dicAux.has_key('packetCount') == True:
                    lista_packetCount.append(str(json_data[cont]['packetCount']))
                else:
                    lista_packetCount.append("x")

                if dicAux.has_key('cookie') == True:
                    lista_cookie.append(str(json_data[cont]['cookie']))
                else:
                    lista_cookie.append("x")

                # O dicionario so' contem as keys "match" e nao o que tem de valor dentro delas, as
                # keys abaixo para o programa sao values e nao keys

                if dicAux.has_key('match') == True:
                    dicAux = dicAux["match"]

                    if dicAux.has_key('eth_src') == True:
                        lista_ethSrc.append(str(json_data[cont]['match']['eth_src']))
                    else:
                        lista_ethSrc.append("x")

                    if dicAux.has_key('eth_dst') == True:
                        lista_ethDst.append(str(json_data[cont]['match']['eth_dst']))
                    else:
                        lista_ethDst.append("x")

                    if dicAux.has_key('eth_type') == True:
                        lista_ethType.append(str(json_data[cont]['match']['eth_type']))
                    else:
                        lista_ethType.append("x")

                    if dicAux.has_key('in_port') == True:
                            lista_inPort.append(str(json_data[cont]['match']['in_port']))
                    else:
                        lista_inPort.append("x")

                    if dicAux.has_key('eth_vlan_vid') == True:
                        lista_eth_vlan_vid.append(str(json_data[cont]['match']['eth_vlan_vid']))
                    else:
                        lista_eth_vlan_vid.append("x")

                    if dicAux.has_key('eth_vlan_pcp') == True:
                            lista_eth_vlan_pcp.append(str(json_data[cont]['match']['eth_vlan_pcp']))
                    else:
                        lista_eth_vlan_pcp.append("x")

                    if dicAux.has_key('ip_proto') == True:
                            lista_ip_proto.append(str(json_data[cont]['match']['ip_proto']))
                    else:
                        lista_ip_proto.append("x")

                    if dicAux.has_key('lista_ipv4_src') == True:
                        lista_ipv4_src.append(str(json_data[cont]['match']['lista_ipv4_src']))
                    else:
                        lista_ipv4_src.append("x")

                    if dicAux.has_key('lista_ipv4_dst') == True:
                        lista_ipv4_dst.append(str(json_data[cont]['match']['lista_ipv4_dst']))
                    else:
                        lista_ipv4_dst.append("x")

                    if dicAux.has_key('lista_ipv6_src') == True:
                        lista_ipv6_src.append(str(json_data[cont]['match']['lista_ipv6_src']))
                    else:
                        lista_ipv6_src.append("x")

                    if dicAux.has_key('lista_ipv6_dst') == True:
                        lista_ipv6_dst.append(str(json_data[cont]['match']['lista_ipv6_dst']))
                    else:
                        lista_ipv6_dst.append("x")

                    if dicAux.has_key('ipv6_label') == True:
                            lista_ipv6_label.append(str(json_data[cont]['match']['ipv6_label']))
                    else:
                        lista_ipv6_label.append("x")

                    if dicAux.has_key('ip_tos') == True:
                            lista_ip_tos.append(str(json_data[cont]['match']['ip_tos']))
                    else:
                        lista_ip_tos.append("x")

                    if dicAux.has_key('ip_ecn') == True:
                            lista_ip_ecn.append(str(json_data[cont]['match']['ip_ecn']))
                    else:
                        lista_ip_ecn.append("x")

                    if dicAux.has_key('ip_dscp') == True:
                            lista_ip_dscp.append(str(json_data[cont]['match']['ip_dscp']))
                    else:
                        lista_ip_dscp.append("x")

                    if dicAux.has_key('tp_src') == True:
                            lista_tp_src.append(str(json_data[cont]['match']['tp_src']))
                    else:
                        lista_tp_src.append("x")

                    if dicAux.has_key('tp_dst') == True:
                            lista_tp_dst.append(str(json_data[cont]['match']['tp_dst']))
                    else:
                        lista_tp_dst.append("x")

                    if dicAux.has_key('udp_src') == True:
                            lista_udp_src.append(str(json_data[cont]['match']['udp_src']))
                    else:
                        lista_udp_src.append("x")

                    if dicAux.has_key('udp_dst') == True:
                        lista_udp_dst.append(str(json_data[cont]['match']['udp_dst']))
                    else:
                        lista_udp_dst.append("x")

                    if dicAux.has_key('tcp_src') == True:
                        lista_tcp_src.append(str(json_data[cont]['match']['tcp_src']))
                    else:
                        lista_tcp_src.append("x")

                    if dicAux.has_key('tcp_dst') == True:
                        lista_tcp_dst.append(str(json_data[cont]['match']['tcp_dst']))
                    else:
                        lista_tcp_dst.append("x")

                    if dicAux.has_key('sctp_src') == True:
                        lista_sctp_src.append(str(json_data[cont]['match']['sctp_src']))
                    else:
                        lista_sctp_src.append("x")

                    if dicAux.has_key('sctp_dst') == True:
                        lista_sctp_dst.append(str(json_data[cont]['match']['sctp_dst']))
                    else:
                        lista_sctp_dst.append("x")

                    if dicAux.has_key('icmpv4_type') == True:
                        lista_icmpv4_type.append(str(json_data[cont]['match']['icmpv4_type']))
                    else:
                        lista_icmpv4_type.append("x")
                    if dicAux.has_key('icmpv4_code') == True:
                        lista_icmpv4_code.append(str(json_data[cont]['match']['icmpv4_code']))
                    else:
                        lista_icmpv4_code.append("x")
                    if dicAux.has_key('icmpv6_type') == True:
                        lista_icmpv6_type.append(str(json_data[cont]['match']['icmpv6_type']))
                    else:
                        lista_icmpv6_type.append("x")

                    if dicAux.has_key('icmpv6_code') == True:
                        lista_icmpv6_code.append(str(json_data[cont]['match']['icmpv6_code']))
                    else:
                        lista_icmpv6_code.append("x")

                    if dicAux.has_key('ipv6_nd_ssl') == True:
                        lista_ipv6_nd_ssl .append(str(json_data[cont]['match']['ipv6_nd_ssl']))
                    else:
                        lista_ipv6_nd_ssl .append("x")

                    if dicAux.has_key('ipv6_nd_ttl') == True:
                        lista_ipv6_nd_ttl.append(str(json_data[cont]['match']['ipv6_nd_ttl']))
                    else:
                        lista_ipv6_nd_ttl.append("x")

                    if dicAux.has_key('ipv6_nd_target') == True:
                        lista_ipv6_nd_target.append(str(json_data[cont]['match']['ipv6_nd_target']))
                    else:
                        lista_ipv6_nd_target.append("x")

                    if dicAux.has_key('arp_opcode') == True:
                        lista_arp_opcode.append(str(json_data[cont]['match']['arp_opcode']))
                    else:
                        lista_arp_opcode.append("x")

                    if dicAux.has_key('arp_tha') == True:
                        lista_arp_tha.append(str(json_data[cont]['match']['arp_tha']))
                    else:
                        lista_arp_tha.append("x")

                    if dicAux.has_key('arp_spa') == True:
                        lista_arp_spa.append(str(json_data[cont]['match']['arp_spa']))
                    else:
                        lista_arp_spa.append("x")

                    if dicAux.has_key('arp_tpa') == True:
                        lista_arp_tpa.append(str(json_data[cont]['match']['arp_tpa']))
                    else:
                        lista_arp_tpa.append("x")

                    if dicAux.has_key('mpls_label') == True:
                        lista_mpls_label.append(str(json_data[cont]['match']['mpls_label']))
                    else:
                        lista_mpls_label.append("x")

                    if dicAux.has_key('mpls_tc') == True:
                        lista_mpls_tc.append(str(json_data[cont]['match']['mpls_tc']))
                    else:
                        lista_mpls_tc.append("x")

                    if dicAux.has_key('mpls_bos') == True:
                        lista_mpls_bos.append(str(json_data[cont]['match']['mpls_bos']))
                    else:
                        lista_mpls_bos.append("x")

                    if dicAux.has_key('tunnel_id') == True:
                        lista_tunnel_id.append(str(json_data[cont]['match']['tunnel_id']))
                    else:
                        lista_tunnel_id.append("x")

                    if dicAux.has_key('metadata') == True:
                        lista_metadata.append(str(json_data[cont]['match']['metadata']))
                    else:
                        lista_metadata.append("x")

                cont += 1

            # chave:valores, nao pode ter mais que uma chave igual, dai se usa os valores como chave ele pega so' os valores unicos
            flowCont = 0                                # Indice do dicionario de dados
            arquivo_regras.write("[Switch: " + str(contSwitch+1) + "]\n")
            for m in range(cont):
                arquivo_regras.write("("+str(lista_ethSrc[flowCont]) + " ^ " + str(lista_ethDst[flowCont]) + " ^ " + str(lista_ethType[flowCont]) + " ^ " + str(lista_inPort[flowCont]) + " ^ " + str(lista_eth_vlan_vid[flowCont]) + " ^ " + str(lista_eth_vlan_pcp[flowCont]) + " ^ " + str(lista_ip_proto[flowCont]) + " ^ " + str(lista_ipv4_src[flowCont]) + " ^ " + str(lista_ipv4_dst[flowCont]) + " ^ " + str(lista_ipv6_src[flowCont]) + " ^ " + str(lista_ipv6_dst[flowCont]) + " ^ " + str(lista_ipv6_label[flowCont]) + " ^ " + str(lista_ip_tos[flowCont]) + " ^ " + str(lista_ip_ecn[flowCont]) + " ^ " + str(lista_ip_dscp[flowCont]) + " ^ " + str(lista_tp_src[flowCont]) + " ^ " + str(lista_tp_dst[flowCont]) + " ^ " + str(lista_udp_src[flowCont]) + " ^ " + str(lista_udp_dst[flowCont]) + " ^ " + str(lista_tcp_src[flowCont]) + " ^ " + str(lista_tcp_dst[flowCont]) + " ^ " + str(lista_sctp_src[flowCont]) + " ^ " + str(lista_sctp_dst[flowCont]) + " ^ " + str(lista_icmpv4_type[flowCont]) + " ^ " + str(lista_icmpv4_code[flowCont]) + " ^ " + str(lista_icmpv6_type[flowCont]) + " ^ " + str(lista_icmpv6_code[flowCont]) + " ^ " + str(lista_ipv6_nd_ssl[flowCont]) + " ^ " + str(lista_ipv6_nd_ttl[flowCont]) + " ^ " + str(lista_ipv6_nd_target[flowCont]) + " ^ " + str(lista_arp_opcode[flowCont]) + " ^ " + str(lista_arp_opcode[flowCont]) + " ^ " + str(lista_arp_tha[flowCont]) + " ^ " + str(lista_arp_spa[flowCont]) + " ^ " + str(lista_arp_tpa[flowCont]) + " ^ " + str(lista_mpls_label[flowCont]) + " ^ " + str(lista_mpls_tc[flowCont]) + " ^ " + str(lista_mpls_bos[flowCont]) + " ^ " + str(lista_tunnel_id[flowCont]) + " ^ " + str(lista_metadata[flowCont]) + ") -> " + str(lista_actions[flowCont]) + "\n")

                dicFlows.update({str(m):[lista_prioridade[flowCont],lista_duracao[flowCont],lista_byteCount[flowCont],lista_packetCount[flowCont],lista_cookie[flowCont],lista_ethSrc[flowCont],lista_ethDst[flowCont],lista_ethType[flowCont],lista_inPort[flowCont],lista_eth_vlan_vid[flowCont],lista_eth_vlan_pcp[flowCont],lista_ip_proto[flowCont],lista_ipv4_src[flowCont],lista_ipv4_dst[flowCont],lista_ipv6_src[flowCont],lista_ipv6_dst[flowCont],lista_ipv6_label[flowCont],lista_ip_tos[flowCont],lista_ip_ecn[flowCont],lista_ip_dscp[flowCont],lista_tp_src[flowCont],lista_tp_dst[flowCont],lista_udp_src[flowCont],lista_udp_dst[flowCont],lista_tcp_src[flowCont],lista_tcp_dst[flowCont],lista_sctp_src[flowCont],lista_sctp_dst[flowCont],lista_icmpv4_type[flowCont],lista_icmpv4_code[flowCont],lista_icmpv6_type[flowCont],lista_icmpv6_code[flowCont],lista_ipv6_nd_ssl[flowCont],lista_ipv6_nd_ttl[flowCont],lista_ipv6_nd_target[flowCont],lista_arp_opcode[flowCont],lista_arp_opcode[flowCont],lista_arp_tha[flowCont],lista_arp_spa[flowCont],lista_arp_tpa[flowCont],lista_mpls_label[flowCont],lista_mpls_tc[flowCont],lista_mpls_bos[flowCont],lista_tunnel_id[flowCont],lista_metadata[flowCont],lista_actions[flowCont]]})
                flowCont += 1
            arquivo_regras.write("\n\n")
            contSwitch += 1

            # Aqui fica o algoritmo de deteccao de conflito e redundancia
            i = 0
            j = 0

            for l  in range(len(lista_actions)-1):
                j = i + 1
                for k in range(len(lista_actions)-(i+1)):
                    if (lista_ethSrc[i]=='x'):
                        lista_ethSrc[i] = lista_ethSrc[j]
                    if (lista_ethDst[i]=='x'):
                        lista_Dst[i] = lista_Dst[j]
                    if (lista_ethType[i]=='x'):
                        lista_ethType[i] = lista_ethType[j]
                    if (lista_inPort[i]=='x'):
                        lista_inPort[i] = lista_inPort[j]
                    if (lista_eth_vlan_vid[i]=='x'):
                        lista_eth_vlan_vid[i] = lista_eth_vlan_vid[j]
                    if (lista_eth_vlan_pcp[i]=='x'):
                        lista_eth_vlan_pcp[i] = lista_eth_vlan_pcp[j]
                    if (lista_ip_proto[i]=='x'):
                        lista_ip_proto[i] = lista_ip_proto[j]
                    if (lista_ipv4_src[i]=='x'):
                        lista_ipv4_src[i] = lista_ipv4_src[j]
                    if (lista_ipv4_dst[i]=='x'):
                        lista_ipv4_dst[i] = lista_ipv4_dst[j]
                    if (lista_ipv6_src[i]=='x'):
                        lista_ipv6_src[i] = lista_ipv6_src[j]
                    if (lista_ipv6_dst[i]=='x'):
                        lista_ipv6_dst[i] = lista_ipv6_dst[j]
                    if (lista_ipv6_label[i]=='x'):
                        lista_ipv6_label[i] = lista_ipv6_label[j]
                    if (lista_ip_tos[i]=='x'):
                        lista_ip_tos[i] = lista_ip_tos[j]
                    if (lista_ip_ecn[i]=='x'):
                        lista_ip_ecn[i] = lista_ip_ecn[j]
                    if (lista_ip_dscp[i]=='x'):
                        lista_ip_dscp[i] = lista_ip_dscp[j]
                    if (lista_tp_src[i]=='x'):
                        lista_tp_src[i] = lista_tp_src[j]
                    if (lista_tp_dst[i]=='x'):
                        lista_tp_dst[i] = lista_tp_dst[j]
                    if (lista_udp_src[i]=='x'):
                        lista_udp_src[i] = lista_udp_src[j]
                    if (lista_udp_dst[i]=='x'):
                        lista_udp_dst[i] = lista_udp_dst[j]
                    if (lista_tcp_src[i]=='x'):
                        lista_tcp_src[i] = lista_tcp_src[j]
                    if (lista_tcp_dst[i]=='x'):
                        lista_tcp_dst[i] = lista_tcp_dst[j]
                    if (lista_sctp_src[i]=='x'):
                        lista_sctp_src[i] = lista_sctp_src[j]
                    if (lista_sctp_dst[i]=='x'):
                        lista_sctp_dst[i] = lista_sctp_dst[j]
                    if (lista_icmpv4_type[i]=='x'):
                        lista_icmpv4_type[i] = lista_icmpv4_type[j]
                    if (lista_icmpv4_code[i]=='x'):
                        lista_icmpv4_code[i] = lista_icmpv4_code[j]
                    if (lista_icmpv6_type[i]=='x'):
                        lista_icmpv6_type[i] = lista_icmpv6_type[j]
                    if (lista_icmpv6_code[i]=='x'):
                        lista_icmpv6_code[i] = lista_icmpv6_code[j]
                    if (lista_ipv6_nd_ssl[i]=='x'):
                        lista_ipv6_nd_ssl[i] = lista_ipv6_nd_ssl[j]
                    if (lista_ipv6_nd_ttl[i]=='x'):
                        lista_ipv6_nd_ttl[i] = lista_ipv6_nd_ttl[j]
                    if (lista_ipv6_nd_target[i]=='x'):
                        lista_ipv6_nd_target[i] = lista_ipv6_nd_target[j]
                    if (lista_arp_opcode[i]=='x'):
                        lista_arp_opcode[i] = lista_arp_opcode[j]
                    if (lista_arp_opcode[i]=='x'):
                        lista_arp_opcode[i] = lista_arp_opcode[j]
                    if (lista_arp_tha[i]=='x'):
                        lista_arp_tha[i] = lista_arp_tha[j]
                    if (lista_arp_spa[i]=='x'):
                        lista_arp_spa[i] = lista_arp_spa[j]
                    if (lista_arp_tpa[i]=='x'):
                        lista_arp_tpa[i] = lista_arp_tpa[j]
                    if (lista_mpls_label[i]=='x'):
                        lista_mpls_label[i] = lista_mpls_label[j]
                    if (lista_mpls_tc[i]=='x'):
                        lista_mpls_tc[i] = lista_mpls_tc[j]
                    if (lista_mpls_bos[i]=='x'):
                        lista_mpls_bos[i] = lista_mpls_bos[j]
                    if (lista_tunnel_id[i]=='x'):
                        lista_tunnel_id[i] = lista_tunnel_id[j]
                    if (lista_metadata[i]=='x'):
                        lista_metadata[i] = lista_metadata[j]
                    if (lista_actions[i]=='x'):
                        lista_actions[i] = lista_actions[j]

                    if (lista_ethSrc[j]=='x'):
                        lista_ethSrc[j] = lista_ethSrc[i]
                    if (lista_ethDst[j]=='x'):
                        lista_Dst[j] = lista_Dst[i]
                    if (lista_ethType[j]=='x'):
                        lista_ethType[j] = lista_ethType[i]
                    if (lista_inPort[j]=='x'):
                        lista_inPort[j] = lista_inPort[i]
                    if (lista_eth_vlan_vid[j]=='x'):
                        lista_eth_vlan_vid[j] = lista_eth_vlan_vid[i]
                    if (lista_eth_vlan_pcp[j]=='x'):
                        lista_eth_vlan_pcp[j] = lista_eth_vlan_pcp[i]
                    if (lista_ip_proto[j]=='x'):
                        lista_ip_proto[j] = lista_ip_proto[i]
                    if (lista_ipv4_src[j]=='x'):
                        lista_ipv4_src[j] = lista_ipv4_src[i]
                    if (lista_ipv4_dst[j]=='x'):
                        lista_ipv4_dst[j] = lista_ipv4_dst[i]
                    if (lista_ipv6_src[j]=='x'):
                        lista_ipv6_src[j] = lista_ipv6_src[i]
                    if (lista_ipv6_dst[j]=='x'):
                        lista_ipv6_dst[j] = lista_ipv6_dst[i]
                    if (lista_ipv6_label[j]=='x'):
                        lista_ipv6_label[j] = lista_ipv6_label[i]
                    if (lista_ip_tos[j]=='x'):
                        lista_ip_tos[j] = lista_ip_tos[i]
                    if (lista_ip_ecn[j]=='x'):
                        lista_ip_ecn[j] = lista_ip_ecn[i]
                    if (lista_ip_dscp[j]=='x'):
                        lista_ip_dscp[j] = lista_ip_dscp[i]
                    if (lista_tp_src[j]=='x'):
                        lista_tp_src[j] = lista_tp_src[i]
                    if (lista_tp_dst[j]=='x'):
                        lista_tp_dst[j] = lista_tp_dst[i]
                    if (lista_udp_src[j]=='x'):
                        lista_udp_src[j] = lista_udp_src[i]
                    if (lista_udp_dst[j]=='x'):
                        lista_udp_dst[j] = lista_udp_dst[i]
                    if (lista_tcp_src[j]=='x'):
                        lista_tcp_src[j] = lista_tcp_src[i]
                    if (lista_tcp_dst[j]=='x'):
                        lista_tcp_dst[j] = lista_tcp_dst[i]
                    if (lista_sctp_src[j]=='x'):
                        lista_sctp_src[j] = lista_sctp_src[i]
                    if (lista_sctp_dst[j]=='x'):
                        lista_sctp_dst[j] = lista_sctp_dst[i]
                    if (lista_icmpv4_type[j]=='x'):
                        lista_icmpv4_type[j] = lista_icmpv4_type[i]
                    if (lista_icmpv4_code[j]=='x'):
                        lista_icmpv4_code[j] = lista_icmpv4_code[i]
                    if (lista_icmpv6_type[j]=='x'):
                        lista_icmpv6_type[j] = lista_icmpv6_type[i]
                    if (lista_icmpv6_code[j]=='x'):
                        lista_icmpv6_code[j] = lista_icmpv6_code[i]
                    if (lista_ipv6_nd_ssl[j]=='x'):
                        lista_ipv6_nd_ssl[j] = lista_ipv6_nd_ssl[i]
                    if (lista_ipv6_nd_ttl[j]=='x'):
                        lista_ipv6_nd_ttl[j] = lista_ipv6_nd_ttl[i]
                    if (lista_ipv6_nd_target[j]=='x'):
                        lista_ipv6_nd_target[j] = lista_ipv6_nd_target[i]
                    if (lista_arp_opcode[j]=='x'):
                        lista_arp_opcode[j] = lista_arp_opcode[i]
                    if (lista_arp_opcode[j]=='x'):
                        lista_arp_opcode[j] = lista_arp_opcode[i]
                    if (lista_arp_tha[j]=='x'):
                        lista_arp_tha[j] = lista_arp_tha[i]
                    if (lista_arp_spa[j]=='x'):
                        lista_arp_spa[j] = lista_arp_spa[i]
                    if (lista_arp_tpa[j]=='x'):
                        lista_arp_tpa[j] = lista_arp_tpa[i]
                    if (lista_mpls_label[j]=='x'):
                        lista_mpls_label[j] = lista_mpls_label[i]
                    if (lista_mpls_tc[j]=='x'):
                        lista_mpls_tc[j] = lista_mpls_tc[i]
                    if (lista_mpls_bos[j]=='x'):
                        lista_mpls_bos[j] = lista_mpls_bos[i]
                    if (lista_tunnel_id[j]=='x'):
                        lista_tunnel_id[j] = lista_tunnel_id[i]
                    if (lista_metadata[j]=='x'):
                        lista_metadata[j] = lista_metadata[i]
                    if (lista_actions[j]=='x'):
                        lista_actions[j] = lista_actions[i]

                    if(lista_ethSrc[i]==lista_ethSrc[j] and lista_ethDst[i]==lista_ethDst[j] and lista_ethType[i]==lista_ethType[j] and lista_inPort[i]==lista_inPort[j] and lista_eth_vlan_vid[i]==lista_eth_vlan_vid[j] and lista_eth_vlan_pcp[i]==lista_eth_vlan_pcp[j] and lista_ip_proto[i]==lista_ip_proto[j] and lista_ipv4_src[i]==lista_ipv4_src[j] and lista_ipv4_dst[i]==lista_ipv4_dst[j] and lista_ipv6_src[i]==lista_ipv6_src[j] and lista_ipv6_dst[i]==lista_ipv6_dst[j] and lista_ipv6_label[i]==lista_ipv6_label[j] and lista_ip_tos[i]==lista_ip_tos[j] and lista_ip_ecn[i]==lista_ip_ecn[j] and lista_ip_dscp[i]==lista_ip_dscp[j] and lista_tp_src[i]==lista_tp_src[j] and lista_tp_dst[i]==lista_tp_dst[j] and lista_udp_src[i]==lista_udp_src[j] and lista_udp_dst[i]==lista_udp_dst[j] and lista_tcp_src[i]==lista_tcp_src[j] and lista_tcp_dst[i]==lista_tcp_dst[j] and lista_sctp_src[i]==lista_sctp_src[j] and lista_sctp_dst[i]==lista_sctp_dst[j] and lista_icmpv4_type[i]==lista_icmpv4_type[j] and lista_icmpv4_code[i]==lista_icmpv4_code[j] and lista_icmpv6_type[i]==lista_icmpv6_type[j] and lista_icmpv6_code[i]==lista_icmpv6_code[j] and lista_ipv6_nd_ssl[i]==lista_ipv6_nd_ssl[j] and  lista_ipv6_nd_ttl[i]==lista_ipv6_nd_ttl[j] and lista_ipv6_nd_target[i]==lista_ipv6_nd_target[j] and  lista_arp_opcode[i]==lista_arp_opcode[j] and lista_arp_tha[i]==lista_arp_tha[j] and  lista_arp_spa[i]==lista_arp_spa[j] and lista_arp_tpa[i]==lista_arp_tpa[j] and lista_mpls_label[i]==lista_mpls_label[j] and lista_mpls_tc[i]==lista_mpls_tc[j] and lista_mpls_bos[i]==lista_mpls_bos[j] and lista_tunnel_id[i]==lista_tunnel_id[j] and lista_metadata[i]==lista_metadata[j]):

                        if (lista_actions[i] != lista_actions[j]):
                            arquivo_regras_conflitantes.write("(" + str(lista_ethSrc[i]) + " ^ " + str(lista_ethDst[i]) + " ^ " + str(lista_eth_vlan_vid[i]) + " ^ " + str(lista_eth_vlan_pcp[i]) + " ^ " + str(lista_ip_proto[i]) + " ^ " + str(lista_ipv4_src[i]) + " ^ " + str(lista_ipv4_dst[i]) + " ^ " + str(lista_ipv6_src[i]) + " ^ " + str(lista_ipv6_dst[i]) + " ^ " + str(lista_ipv6_label[i]) + " ^ " + str(lista_ip_tos[i]) + " ^ " + str(lista_ip_ecn[i]) + " ^ " + str(lista_ip_dscp[i]) + " ^ " + str(lista_tp_src[i]) + " ^ " + str(lista_tp_dst[i]) + " ^ " + str(lista_udp_src[i]) + " ^ " + str(lista_udp_dst[i]) + " ^ " + str(lista_tcp_src[i]) + " ^ " + str(lista_tcp_dst[i]) + " ^ " + str(lista_sctp_src[i]) + " ^ " + str(lista_sctp_dst[i]) + " ^ " + str(lista_icmpv4_type[i]) + " ^ " + str(lista_icmpv4_code[i]) + " ^ " + str(lista_icmpv6_type[i]) + " ^ " + str(lista_icmpv6_code[i]) + " ^ " + str(lista_ipv6_nd_ssl[i]) + " ^ " + str(lista_ipv6_nd_ttl[i]) + " ^ " + str(lista_ipv6_nd_target[i]) + " ^ " + str(lista_arp_opcode[i]) + " ^ " + str(lista_arp_tha[i]) + " ^ " + str(lista_arp_spa[i]) + " ^ " + str(lista_arp_tpa[i]) + " ^ " + str(lista_mpls_label[i]) + " ^ " + str(lista_mpls_tc[i]) + " ^ " + str(lista_mpls_bos[i]) + " ^ " + str(lista_tunnel_id[i]) + " ^ " + str(lista_metadata[i]) + ") -> " + str(lista_actions[i]) + "\n")
                            arquivo_regras_conflitantes.write("Detectado conflito entre o fluxo " + str(i) + " e entre o fluxo " + str(j) + " no switch " + str(contSwitch) + "\n\n")
                            conflito(i,j,contSwitch)
                            flag_confRed = 1
                        else:
                            arquivo_regras_redundantes.write("(" + str(lista_ethSrc[i]) + " ^ " + str(lista_ethDst[i]) + " ^ " + str(lista_eth_vlan_vid[i]) + " ^ " + str(lista_eth_vlan_pcp[i]) + " ^ " + str(lista_ip_proto[i]) + " ^ " + str(lista_ipv4_src[i]) + " ^ " + str(lista_ipv4_dst[i]) + " ^ " + str(lista_ipv6_src[i]) + " ^ " + str(lista_ipv6_dst[i]) + " ^ " + str(lista_ipv6_label[i]) + " ^ " + str(lista_ip_tos[i]) + " ^ " + str(lista_ip_ecn[i]) + " ^ " + str(lista_ip_dscp[i]) + " ^ " + str(lista_tp_src[i]) + " ^ " + str(lista_tp_dst[i]) + " ^ " + str(lista_udp_src[i]) + " ^ " + str(lista_udp_dst[i]) + " ^ " + str(lista_tcp_src[i]) + " ^ " + str(lista_tcp_dst[i]) + " ^ " + str(lista_sctp_src[i]) + " ^ " + str(lista_sctp_dst[i]) + " ^ " + str(lista_icmpv4_type[i]) + " ^ " + str(lista_icmpv4_code[i]) + " ^ " + str(lista_icmpv6_type[i]) + " ^ " + str(lista_icmpv6_code[i]) + " ^ " + str(lista_ipv6_nd_ssl[i]) + " ^ " + str(lista_ipv6_nd_ttl[i]) + " ^ " + str(lista_ipv6_nd_target[i]) + " ^ " + str(lista_arp_opcode[i]) + " ^ " + str(lista_arp_tha[i]) + " ^ " + str(lista_arp_spa[i]) + " ^ " + str(lista_arp_tpa[i]) + " ^ " + str(lista_mpls_label[i]) + " ^ " + str(lista_mpls_tc[i]) + " ^ " + str(lista_mpls_bos[i]) + " ^ " + str(lista_tunnel_id[i]) + " ^ " + str(lista_metadata[i]) + ") -> " + str(lista_actions[i]) + "\n")
                            arquivo_regras_redundantes.write("Detectada a redundancia acima entre o fluxo " + str(i) + " e entre o fluxo " + str(j) + " no switch " + str(contSwitch) + "\n\n")
                            redundancia(i,j,contSwitch)
                            flag_confRed = 1
                    j = j + 1
                i = i + 1

            lista_csv.append(dicFlows)                  # E' adicionado na lista_csv cada switch com seus respectivos fluxos


        arquivo_regras.close()
        arquivo_regras_conflitantes.close()
        arquivo_regras_redundantes.close()


        arquivoDadosCSV = open("../data/arquivoDados.csv", "w")

        if flag_confRed != 1:
            print "\nNenhum conflito e nenhuma redundancia foram encontrados!\n"

        # len(lista_csv[r]) e' igual ao numero de fluxos contidos na lista_csv[r]
        for r in range(len(lista_csv)):
            dicAux_CSV = lista_csv[r]
            #print dicAux_CSV
            for n in range(len(lista_csv[r])):
                arquivoDadosCSV.write(str(dicAux_CSV[str(n)])+"\n")
            arquivoDadosCSV.write("\n")

        arquivoDadosCSV.close()
        end = time.time()

        print (end-start), "seconds"
        raw_input("\nPressione [Enter] para voltar ao menu principal\n")
        #system("clear")
####################################################################################################
    elif opt == "2":                                                   # Adicionar regra no firewall da rede
        print "- Para seguir adicionando regras: [Enter]"
        print "- Para pular para adicionar regras especificas: [@]"
        print "- Para parar de adicionar regras [@@]\n"             #VER SE USO FUNCAO E TAL E ADD NOS ELIFS ABAIXO
        verificaMenu   = ""                                         # Regra para verificacao
        firewallSwitch = ""		             		    # Switch no qual a regra vai ser adicionada
        while (verificaMenu != "@@"):                               # Para para de adicionar uma regra no switch em questao
            firewallSwitch = raw_input("Insira o [Switch] ao qualquer quer adicionar uma ou mais regras: ")
            if firewallSwitch=="":
                system("clear")
                print "\nNenhuma regra podera' ser adicionada sem a informacao do Switch"
                print "Abaixo, escolha uma nova opcao\n"
                break

            comando = "curl -s -d '{" + "\"switch\":\"" + firewallSwitch + "\""

            print "Inserir regras - Match - Flowtable"
            eth_src = raw_input("eth_src: ")
            if eth_src!="": comando += ",eth_src\":" + "\"" + eth_src + "\""
            elif eth_src=="@": break

            eth_dst = raw_input("eth_dst: ")
            if eth_dst!="": comando += "," + "\"eth_dst\":" + "\"" + eth_dst + "\""
            elif eth_dst=="@": break

            eth_type = raw_input("eth_type: ")
            if eth_type!="": comando += "," + "\"eth_type\":" + "\"" + eth_type + "\""
            elif eth_type=="@": break

            in_port = raw_input("in_port: ")
            if in_port!="": comando += "," + "\"in_port\":" + "\"" + in_port + "\""
            elif in_port=="@": break

            eth_vlan_vid = raw_input("eth_vlan_vid: ")
            if eth_vlan_vid!="": comando += "," + "\"eth_vlan_vid\":" + "\"" + eth_vlan_vid + "\""
            elif eth_vlan_vid=="@": break

            eth_vlan_pcp = raw_input("eth_vlan_pcp: ")
            if eth_vlan_pcp!="": comando += "," +  "\"eth_vlan_pcp\":" + "\"" + eth_vlan_pcp + "\""
            elif eth_vlan_pcp=="@": break

            ip_proto = raw_input("ip_proto: ")
            if ip_proto!="": comando += "," +  "\"ip_proto\":" + "\"" + ip_proto + "\""
            elif ip_proto=="@": break

            ipv4_src = raw_input("ipv4_src: ")
            if ipv4_src!="": comando += "," +  "\"ipv4_src\":" + "\"" + ipv4_src + "\","
            elif ipv4_src=="@": break

            ipv4_dst = raw_input("ipv4_dst: ")
            if ipv4_dst!="": comando += "," +  "\"ipv4_dst\":" + "\"" + ipv4_dst + "\""
            elif ipv4_dst=="@": break

            ipv6_src = raw_input("ipv6_src: ")
            if ipv6_src!="": comando += "," +  "\"ipv6_src\":" + "\"" + ipv6_src + "\""
            elif ipv6_src=="@": break

            ipv6_dst = raw_input("ipv6_dst: ")
            if ipv6_dst!="": comando += "," + "\"ipv6_dst\":" + "\"" + ipv6_dst + "\""
            elif ipv6_dst=="@": break

            ipv6_label = raw_input("ipv6_label: ")
            if ipv6_label!="": comando += "\"ipv6_label\":" + "\"" + ipv6_label + "\""
            elif ipv6_label=="@": break

            ip_tos = raw_input("ip_tos: ")
            if ip_tos!="": comando += "," +  "\"ip_tos\":" + "\"" + ip_tos + "\""
            elif ip_tos=="@": break

            ip_ecn = raw_input("ip_ecn: ")
            if ip_ecn!="": comando += "," +  "\"ip_ecn\":" + "\"" + ip_ecn + "\""
            elif ip_ecn=="@": break

            ip_dscp = raw_input("ip_dscp: ")
            if ip_dscp!="": comando += "," +  "\"ip_dscp\":" + "\"" + ip_dscp + "\""
            elif ip_dscp=="@": break

            tp_src = raw_input("tp_src: ")
            if tp_src!="": comando += "," +  "\"tp_srcn\":" + "\"" + tp_src + "\""
            elif tp_src=="@": break

            tp_dst = raw_input("tp_dst: ")
            if tp_dst!="": comando += "," +  "\"tp_dst\":" + "\"" + tp_dst + "\""
            elif tp_dst=="@": break

            udp_src = raw_input("udp_src: ")
            if udp_src!="": comando += "," +  "\"udp_src\":" + "\"" + udp_src + "\""
            elif udp_src=="@": break

            udp_dst = raw_input("udp_dst: ")
            if udp_dst!="": comando += "," +  "\"udp_dst\":" + "\"" + udp_dst + "\""
            elif udp_dst=="@": break

            tcp_src = raw_input("tcp_src: ")
            if tcp_src!="": comando += "," +  "\"tcp_src\":" + "\"" + tcp_src + "\""
            elif tcp_src=="@": break

            tcp_dst = raw_input("tcp_dst: ")
            if tcp_dst!="": comando += "," +  "\"tcp_dst\":" + "\"" + tcp_dst + "\""
            elif tcp_dst=="@": break

            sctp_src = raw_input("sctp_src: ")
            if sctp_src!="": comando += "," +  "\"sctp_src\":" + "\"" + sctp_src + "\""
            elif sctp_src=="@": break

            sctp_dst = raw_input("sctp_dst: ")
            if sctp_dst!="": comando += "," +  "\"sctp_dst\":" + "\"" + sctp_dst + "\""
            elif sctp_dst=="@": break

            icmpv4_type = raw_input("icmpv4_type: ")
            if icmpv4_type!="": comando += "," +  "\"icmpv4_type\":" + "\"" + icmpv4_type + "\""
            elif icmpv4_type=="@": break

            icmpv4_code = raw_input("icmpv4_code: ")
            if icmpv4_code!="": comando += "," +  "\"icmpv4_code\":" + "\"" + icmpv4_code + "\""
            elif icmpv4_code=="@": break

            icmpv6_type = raw_input("icmpv6_type: ")
            if icmpv6_type!="": comando += "," +  "\"icmpv6_type\":" + "\"" + icmpv6_type + "\""
            elif icmpv6_type=="@": break

            icmpv6_code = raw_input("icmpv6_code: ")
            if icmpv6_code!="": comando += "," +  "\"icmpv6_code\":" + "\"" + icmpv6_code + "\""
            elif icmpv6_code=="@": break

            ipv6_nd_ssl = raw_input("ipv6_nd_ssl: ")
            if ipv6_nd_ssl!="": comando += "," +  "\"ipv6_nd_ssl\":" + "\"" + ipv6_nd_ssl + "\""
            elif ipv6_nd_ssl=="@": break

            ipv6_nd_ttl = raw_input("ipv6_nd_ttl: ")
            if ipv6_nd_ttl!="": comando += "," +  "\"ipv6_nd_ttl\":" + "\"" + ipv6_nd_ttl + "\""
            elif ipv6_nd_ttl=="@": break

            ipv6_nd_target = raw_input("ipv6_nd_target: ")
            if ipv6_nd_target!="": comando += "," +  "\"ipv6_nd_target\":" + "\"" + ipv6_nd_target + "\""
            elif ipv6_nd_target=="@": break

            arp_opcode = raw_input("arp_opcode: ")
            if arp_opcode!="": comando += "," +  "\"arp_opcode\":" + "\"" + arp_opcode + "\""
            elif arp_opcode=="@": break

            arp_tha = raw_input("arp_tha: ")
            if arp_tha!="": comando += "," +  "\"arp_tha\":" + "\"" + arp_tha + "\""
            elif arp_tha=="@": break

            arp_spa = raw_input("arp_spa: ")
            if arp_spa!="": comando += "," +  "\"arp_spa\":" + "\"" + arp_spa + "\""
            elif arp_spa=="@": break

            arp_tpa = raw_input("arp_tpa: ")
            if arp_tpa!="": comando += "," +  "\"arp_tpa\":" + "\"" + arp_tpa + "\""
            elif arp_tpa=="@": break

            mpls_label = raw_input("mpls_label: ")
            if mpls_label!="": comando += "," +  "\"mpls_label\":" + "\"" + mpls_label + "\""
            elif mpls_label=="@": break

            mpls_tc = raw_input("mpls_tc: ")
            if mpls_tc!="": comando += "," +  "\"mpls_tc\":" + "\"" + mpls_tc + "\""
            elif mpls_tc=="@": break

            mpls_bos = raw_input("mpls_bos: ")
            if mpls_bos!="": comando += "," +  "\"mpls_bos\":" + "\"" + mpls_bos + "\""
            elif mpls_bos=="@": break

            tunnel_id = raw_input("tunnel_id: ")
            if tunnel_id!="": comando += "," +  "\"tunnel_id\":" + "\"" + tunnel_id + "\""
            elif tunnel_id=="@": break

            metadata = raw_input("metadata: ")
            if metadata!="": comando += "," +  "\"metadata\":" + "\"" + metadata + "\""
            elif metadata=="@": break

            print "\nAqui comeca as regras especificas para o Firewall\n"

            version = raw_input("version: ")
            if version!="": comando += "," +  "\"version\":" + "\"" + version + "\""
            elif version=="@": break

            command = raw_input("command: ")
            if command!="": comando += "," +  "\"command\":" + "\"" + command + "\""
            elif command=="@": break

            cookie = raw_input("cookie: ")
            if cookie!="": comando += "," +  "\"cookie\":" + "\"" + cookie + "\""
            elif cookie=="@": break

            src_ip = raw_input("src_ip: ")
            if src_ip!="": comando += "," +  "\"src_ip\":" + "\"" + src_ip + "\""
            elif src_ip=="@": break

            dst_ip = raw_input("dst_ip: ")
            if dst_ip!="": comando += "," +  "\"dst_ip\":" + "\"" + dst_ip + "\""
            elif dst_ip=="@": break

            dl_type = raw_input("dl_type: ")
            if dl_type!="": comando += "," +  "\"dl_type\":" + "\"" + dl_type + "\""
            elif dl_type=="@": break

            nw_dst_prefix = raw_input("nw_dst_prefix: ")
            if nw_dst_prefix!="": comando += "," +  "\"nw_dst_prefix\":" + "\"" + nw_dst_prefix + "\""
            elif nw_dst_prefix=="@": break

            nw_src_prefix = raw_input("nw_src_prefix: ")
            if nw_src_prefix!="": comando += "," +  "\"nw_src_prefix\":" + "\"" + nw_src_prefix + "\""
            elif nw_src_prefix=="@": break

            nw_src_maskbits = raw_input("nw_src_maskbits: ")
            if nw_src_maskbits != "":comando += "," + "\"nw_src_maskbits\":" + "\"" + nw_src_maskbits + "\""
            elif nw_src_maskbits == "@":break

            nw_dst_maskbits = raw_input("nw_dst_maskbits: ")
            if nw_dst_maskbits!="": comando += "," +  "\"nw_dst_maskbits\":" + "\"" + nw_dst_maskbits + "\""
            elif nw_dst_maskbits=="@": break

            any_nw_dst = raw_input("any_nw_dst: ")
            if any_nw_dst!="": comando += "," +  "\"any_nw_dst\":" + "\"" + any_nw_dst + "\""
            elif any_nw_dst=="@": break

            any_nw_proto = raw_input("any_nw_proto: ")
            if any_nw_proto!="": comando += "," +  "\"any_nw_proto\":" + "\"" + any_nw_proto + "\""
            elif any_nw_proto=="@": break

            any_in_port = raw_input("any_in_port: ")
            if any_in_port!="": comando += "," +  "\"any_in_port\":" + "\"" + any_in_port + "\""
            elif any_in_port=="@": break

            any_nw_srcany_tp_ds = raw_input("any_nw_srcany_tp_ds: ")
            if any_nw_srcany_tp_ds!="": comando += "," +  "\"any_nw_srcany_tp_ds\":" + "\"" + any_nw_srcany_tp_ds + "\""
            elif any_nw_srcany_tp_ds=="@": break

            ruleid = raw_input("ruleid: ")
            if ruleid!="": comando += "," +  "\"ruleid\":" + "\"" + ruleid + "\""
            elif ruleid=="@": break

            idleTimeoutSec = raw_input("idleTimeoutSec: ")
            if idleTimeoutSec!="": comando += "," +  "\"idleTimeoutSec\":" + "\"" + idleTimeoutSec + "\""
            elif idleTimeoutSec=="@": break

            hardTimeoutSec = raw_input("hardTimeoutSec: ")
            if hardTimeoutSec!="": comando += "," +  "\"hardTimeoutSec\":" + "\"" + hardTimeoutSec + "\""
            elif hardTimeoutSec=="@": break

            any_dl_type = raw_input("any_dl_type: ")
            if any_dl_type!="": comando += "," +  "\"any_dl_type\":" + "\"" + any_dl_type + "\""
            elif any_dl_type=="@": break

            priority = raw_input("priority: ")
            if priority!="": comando += "," +  "\"priority\":" + "\"" + priority + "\""
            elif priority=="@": break

            in_port = raw_input("in_port: ")
            if in_port!="": comando += "," +  "\"in_port\":" + "\"" + in_port + "\""
            elif in_port=="@": break

            any_dpid = raw_input("any_dpid: ")
            if any_dpid!="": comando += "," +  "\"any_dpid\":" + "\"" + any_dpid + "\""
            elif any_dpid=="@": break

            dl_src = raw_input("dl_src: ")
            if dl_src!="": comando += "," +  "\"dl_src\":" + "\"" + dl_src + "\""
            elif dl_src=="@": break

            dpid = raw_input("dpid: ")
            if dpid!="": comando += "," +  "\"dpid\":" + "\"" + dpid + "\""
            elif dpid=="@": break

            tp_src = raw_input("tp_src: ")
            if tp_src!="": comando += "," +  "\"tp_src\":" + "\"" + tp_src + "\""
            elif tp_src=="@": break

            any_dl_dst = raw_input("any_dl_dst: ")
            if any_dl_dst!="": comando += "," +  "\"any_dl_dst\":" + "\"" + any_dl_dst + "\""
            elif any_dl_dst=="@": break

            nw_proto = raw_input("nw_proto: ")
            if nw_proto!="": comando += "," +  "\"nw_proto\":" + "\"" + nw_proto + "\""
            elif nw_proto=="@": break

            tp_dst = raw_input("tp_dst: ")
            if tp_dst!="": comando += "," +  "\"tp_dst\":" + "\"" + tp_dst + "\""
            elif tp_dst=="@": break

            dl_dst = raw_input("dl_dst: ")
            if dl_dst!="": comando += "," +  "\"dl_dst\":" + "\"" + dl_dst + "\""
            elif dl_dst=="@": break

            any_tp_src = raw_input("any_tp_src: ")
            if any_tp_src!="": comando += "," +  "\"any_tp_src\":" + "\"" + any_tp_src + "\""
            elif any_tp_src=="@": break

            outPort = raw_input("outPort: ")
            if outPort!="": comando += "," +  "\"outPort\":" + "\"" + outPort + "\""
            elif outPort=="@": break

            src_mac = raw_input("src_mac: ")
            if src_mac!="": comando += "," +  "\"src_mac\":" + "\"" + src_mac + "\""
            elif src_mac=="@": break

            dst_mac = raw_input("dst_mac: ")
            if dst_mac!="": comando += "," +  "\"dst_mac\":" + "\"" + dst_mac + "\""
            elif dst_mac=="@": break

            action = raw_input("action: ")
            if action!="": comando += "," +  "\"action\":" + "\"" + action + "\""
            elif action=="@": break

            #ARRUMAR PRO USUARIO COLOCAR O IP:PORTA
            comando += "}' http://143.54.12.10:8080/wm/staticflowpusher/json"

            print comando

            command_output = os.popen(comando).read()  # Executando comando dado no terminal
            status_regraAdicionada = json.loads(command_output)
            print "\nStatus da regra adicionada: ", status_regraAdicionada, "\n"



            ''' curl -s -d '{"switch":"00:00:00:00:00:00:00:02","ether-type":"0x0800","name":"flow-mod-5","nw_proto":"50","priority":"1","eth_src":"00:00:00:00:00:04","eth_dst":"00:00:00:00:00:02", "action": "<DENY>" '''
            ''' curl -s -d '{"switch":"00:00:00:00:00:00:00:02",eth_src":"00:00:00:00:00:04","eth_dst":"00:00:00:00:00:02","priority":"1","action":"DENY"}' http://143.54.12.10:8080/wm/staticflowpusher/json '''
            ''' "switchid":"<xx:xx:xx:xx:xx:xx:xx:xx>", "src-inport":"<short>",
                "src-mac": "<xx:xx:xx:xx:xx:xx>", "dst-mac": "<xx:xx:xx:xx:xx:xx>",
                "dl-type": "<ARP or IPv4>", "src-ip": "<A.B.C.D/M>", "dst-ip": "<A.B.C.D/M>",
                "nw-proto": "<TCP or UDP or ICMP>", "tp-src": "<short>", "tp-dst": "<short>",
                "priority": "<int>", "action": "<ALLOW or DENY>"  '''
            verificaMenu = raw_input("\n\n[1] - Ver regra adicionada (Durante 5 segundos)\n[2] - Menu\n[3] - Adicionar mais regras ao Firewall\n[4] - Sair\n-> ")

            if verificaMenu=='1':
                print "\nMENU\n"
                print "Regra adicionada:", comando
                while cont_time<5:
                    time.sleep(1)
                    cont_time+=1
                    #print ""
                #Final do while
                system("clear")
            elif verificaMenu=='2':
                system("clear")
                menu()
            elif verificaMenu=='3':
                system("clear")
                continue
            elif verificaMenu=='4':
                system("clear")
                sys.exit()
            else:
                system("clear")
                print "\nOpcao nao existente\n"
####################################################################################################
    elif opt == "3":
        string_regraFirewall = raw_input("Insira a string com a regra: ")

        # Colocar IP:PORTA
        comando = "curl -s -d '{" + string_regraFirewall + "}' http://143.54.12.10:8080/wm/staticflowpusher/json"

        verificaMenu = raw_input("\n\n[1] - Ver opcao desejada (Durante 5 segundos)\n[2] - Menu\n[3] - Adicionar mais regras ao Firewall\n[4] - Sair\n-> ")

        command_output = os.popen(comando).read()
        status_regraAdicionada = json.loads(command_output)
        print "\nStatus da regra adicionada: ", status_regraAdicionada, "\n"

        verificaMenu = raw_input("\n\n[1] - Ver opcao desejada (Durante 5 segundos)\n[2] - Menu\n[3] - Adicionar mais regras ao Firewall\n[4] - Sair\n-> ")

        if verificaMenu=='1':
            print "\nMENU\n"
            print "Regre adicionada:", comando
            while cont_time<5:
                time.sleep(1)
                cont_time+=1
                #print ""
            #Final do while
            system("clear")
        elif verificaMenu=='2':
            system("clear")
            menu()
        elif verificaMenu=='3':
            system("clear")
            continue
        elif verificaMenu=='4':
            system("clear")
            sys.exit()
        else:
            system("clear")
            print "\nOpcao nao existente\n"

####################################################################################################
    elif opt == "4":
        print "\n"
        ruleId = raw_input("Informe o Rule ID da regra a ser excluida: ")
        command = "curl -X DELETE -d "   + "'{" + '"ruleid"' +  ":" + ruleId + "}' http://143.54.12.10:8080/wm/firewall/rules/json"
        print command
        command_output = os.popen(command).read()
        status_regraDeletada = json.loads(command_output)
        print "\n", status_regraDeletada
        raw_input("\nPressione [Enter] para voltar ao menu principal\n")
        #system("clear")
###################################################################################################
    elif opt == "5":
        command = "curl http://143.54.12.10:8080/wm/staticflowpusher/list/all/json"
        command_output = os.popen(command).read()
        status_todasRegras = json.loads(command_output)
        print "\n", status_todasRegras
        raw_input("\nPressione [Enter] para voltar ao menu principal\n")
        #system("clear")
####################################################################################################
    elif opt == "6":
        start_fw = time.time()
        print "\n"

        '''
        ip = raw_input("|----- Insira o IP da maquina: ")
        porta = raw_input("|----- Insira a porta: ")
        command = "curl http://" + str(ip) + ":" + str(porta) + "/wm/staticflowpusher/list/all/json"

        command_output = os.popen(command).read()
        topology = json.loads(command_output)


        # Criando o arquivo com os dados de fluxos do firewall
        fluxos_dados = open("../data/regrasFirewall.json", "w")
        fluxos_dados.write(str(topology))
        fluxos_dados.close()
        '''

        #>>>>>> DESCOMENTAR PORQUE TA FORMATANDO O ARQUIVO A CADA EXECUCAO
        #formatarJson("../data/regrasFirewall.json", "arquivoJsonFW")

        flag_confRedFW = 0


        string_firewall = ""
        fluxos_firewall = open("../data/regrasFirewall.json", "r")
        for f in fluxos_firewall:
            string_firewall += f
        fluxos_firewall.close()

        with open("../data/regrasFirewall.json") as fw:
            dataFW = fw.read()
            json_dataFW = json.loads(dataFW)

        lista_switchesFW = json_dataFW.keys()

        # Arquivos de regras do Firewall
        arquivo_regrasFW = open("../data/regrasFW.txt", "w")
        arquivo_regras_conflitantesFW = open("../data/regras_conflitantesFW.txt", "w")
        arquivo_regras_redundantesFW = open("../data/regras_redundantesFW.txt", "w")


        lista_csvFW = []  # Lista para armazenar os dicionarios que serao impressos no arquivo .csv
        contSwitchFW = 0

        for sfw in lista_switchesFW:
            dicFlowsFW = {}    # Inicicializa o dicionario de fluxos para o firewall a cada execucao

            with open("../data/regrasFirewall.json") as fw:
                dataFW = fw.read()
                json_dataFW = json.loads(dataFW)
            json_dataFW = json_dataFW[str(sfw)]  # Tem que salvar isso no nome do switch
            json_dataFW = json_dataFW["flows"]

            # Inicializacao das listas de dados do Firewall
            lista_eth_src = []
            lista_eth_dst = []
            lista_eth_type = []
            lista_in_port = []
            lista_eth_vlan_vid = []
            lista_eth_vlan_pcp = []
            lista_ip_proto = []
            lista_ipv4_src = []
            lista_ipv4_dst = []
            lista_ipv6_src = []
            lista_ipv6_dst = []
            lista_ipv6_label = []
            lista_ip_tos = []
            lista_ip_ecn = []
            lista_ip_dscp = []
            lista_tp_src = []
            lista_tp_dst = []
            lista_udp_src = []
            lista_udp_dst = []
            lista_tcp_src = []
            lista_tcp_dst = []
            lista_sctp_src = []
            lista_sctp_dst = []
            lista_icmpv4_type = []
            lista_icmpv4_code = []
            lista_icmpv6_type = []
            lista_icmpv6_code = []
            lista_ipv6_nd_ssl = []
            lista_ipv6_nd_ttl = []
            lista_ipv6_nd_target = []
            lista_arp_opcode = []
            lista_arp_tha = []
            lista_arp_spa = []
            lista_arp_tpa = []
            lista_mpls_label = []
            lista_mpls_tc = []
            lista_mpls_bos = []
            lista_tunnel_id = []
            lista_metadata = []
            # Listas especificas para o Firewall
            lista_version = []
            lista_command = []
            lista_cookie = []
            lista_src_ip = []
            lista_dst_ip = []
            lista_dl_type = []
            lista_nw_dst_prefix = []
            lista_nw_src_prefix = []
            lista_nw_src_maskbits = []
            lista_nw_dst_maskbits = []
            lista_any_nw_dst = []
            lista_any_nw_proto = []
            lista_any_in_port = []
            lista_any_nw_srcany_tp_ds = []
            lista_ruleid = []
            lista_idleTimeoutSec = []
            lista_hardTimeoutSec = []
            lista_any_dl_type = []
            lista_priority = []
            lista_in_port = []
            lista_any_dpid = []
            lista_dl_src = []
            lista_dpid = []
            lista_tp_src = []
            lista_any_dl_dst = []
            lista_nw_proto = []
            lista_tp_dst = []
            lista_dl_dst = []
            lista_any_tp_src = []
            lista_outPort = []
            lista_src_mac = []
            lista_dst_mac = []
            lista_action = []

            dicAuxFW = {}

            # Esta' dentro da lista principal do Firewall do arquivo Json
            contFW = 0 # Indice do fluxo

            for durFW in json_dataFW[0:-1]:
                dicAuxFW = json_dataFW[contSwitchFW]

                # Informacoes apenas do Firewall
                if dicAuxFW.has_key('version') == True:
                    lista_version.append(str(json_dataFW[contFW]['version']))
                else:
                    lista_version.append("x")

                if dicAuxFW.has_key('command') == True:
                    lista_command.append(str(json_dataFW[contFW]['command']))
                else:
                    lista_command.append("x")

                if dicAuxFW.has_key('cookie') == True:
                    lista_cookie.append(str(json_dataFW[contFW]['cookie']))
                else:
                    lista_cookie.append("x")

                if dicAuxFW.has_key('src_ip') == True:
                    lista_src_ip.append(str(json_dataFW[contFW]['src_ip']))
                else:
                    lista_src_ip.append("x")

                if dicAuxFW.has_key('dst_ip') == True:
                    lista_dst_ip.append(str(json_dataFW[contFW]['dst_ip']))
                else:
                    lista_dst_ip.append("x")

                if dicAuxFW.has_key('dl_type') == True:
                    lista_dl_type.append(str(json_dataFW[contFW]['dl_type']))
                else:
                    lista_dl_type.append("x")

                if dicAuxFW.has_key('nw_dst_prefix') == True:
                    lista_nw_dst_prefix.append(str(json_dataFW[contFW]['nw_dst_prefix']))
                else:
                    lista_nw_dst_prefix.append("x")

                if dicAuxFW.has_key('nw_src_prefix') == True:
                    lista_nw_src_prefix.append(str(json_dataFW[contFW]['nw_src_prefix']))
                else:
                    lista_nw_src_prefix.append("x")

                if dicAuxFW.has_key('nw_src_maskbits') == True:
                    lista_nw_src_maskbits.append(str(json_dataFW[contFW]['nw_src_maskbits']))
                else:
                    lista_nw_src_maskbits.append("x")

                if dicAuxFW.has_key('nw_dst_maskbits') == True:
                    lista_nw_dst_maskbits.append(str(json_dataFW[contFW]['nw_dst_maskbits']))
                else:
                    lista_nw_dst_maskbits.append("x")

                if dicAuxFW.has_key('any_nw_dst') == True:
                    lista_any_nw_dst.append(str(json_dataFW[contFW]['any_nw_dst']))
                else:
                    lista_any_nw_dst.append("x")

                if dicAuxFW.has_key('any_nw_proto') == True:
                    lista_any_nw_proto.append(str(json_dataFW[contFW]['any_nw_proto']))
                else:
                    lista_any_nw_proto.append("x")

                if dicAuxFW.has_key('any_in_port') == True:
                    lista_any_in_port.append(str(json_dataFW[contFW]['any_in_port']))
                else:
                    lista_any_in_port.append("x")

                if dicAuxFW.has_key('any_nw_srcany_tp_ds') == True:
                    lista_any_nw_srcany_tp_ds.append(str(json_dataFW[contFW]['any_nw_srcany_tp_ds']))
                else:
                    lista_any_nw_srcany_tp_ds.append("x")

                if dicAuxFW.has_key('ruleid') == True:
                    lista_ruleid.append(str(json_dataFW[contFW]['ruleid']))
                else:
                    lista_ruleid.append("x")

                if dicAuxFW.has_key('idleTimeoutSec') == True:
                    lista_idleTimeoutSec.append(str(json_dataFW[contFW]['idleTimeoutSec']))
                else:
                    lista_idleTimeoutSec.append("x")

                if dicAuxFW.has_key('hardTimeoutSec') == True:
                    lista_hardTimeoutSec.append(str(json_dataFW[contFW]['hardTimeoutSec']))
                else:
                    lista_hardTimeoutSec.append("x")

                if dicAuxFW.has_key('any_dl_type') == True:
                    lista_any_dl_type.append(str(json_dataFW[contFW]['any_dl_type']))
                else:
                    lista_any_dl_type.append("x")

                if dicAuxFW.has_key('priority') == True:
                    lista_priority.append(str(json_dataFW[contFW]['priority']))
                else:
                    lista_priority.append("x")

                if dicAuxFW.has_key('in_port') == True:
                    lista_in_port.append(str(json_dataFW[contFW]['in_port']))
                else:
                    lista_in_port.append("x")

                if dicAuxFW.has_key('any_dpid') == True:
                    lista_any_dpid.append(str(json_dataFW[contFW]['any_dpid']))
                else:
                    lista_any_dpid.append("x")

                if dicAuxFW.has_key('dl_src') == True:
                    lista_dl_src.append(str(json_dataFW[contFW]['dl_src']))
                else:
                    lista_dl_src.append("x")

                if dicAuxFW.has_key('dpid') == True:
                    lista_dpid.append(str(json_dataFW[contFW]['dpid']))
                else:
                    lista_dpid.append("x")

                if dicAuxFW.has_key('tp_src') == True:
                    lista_tp_src.append(str(json_dataFW[contFW]['tp_src']))
                else:
                    lista_tp_src.append("x")

                if dicAuxFW.has_key('any_dl_dst') == True:
                    lista_any_dl_dst.append(str(json_dataFW[contFW]['any_dl_dst']))
                else:
                    lista_any_dl_dst.append("x")

                if dicAuxFW.has_key('nw_proto') == True:
                    lista_nw_proto.append(str(json_dataFW[contFW]['nw_proto']))
                else:
                    lista_nw_proto.append("x")

                if dicAuxFW.has_key('tp_dst') == True:
                    lista_tp_dst.append(str(json_dataFW[contFW]['tp_dst']))
                else:
                    lista_tp_dst.append("x")

                if dicAuxFW.has_key('dl_dst') == True:
                    lista_dl_dst.append(str(json_dataFW[contFW]['dl_dst']))
                else:
                    lista_dl_dst.append("x")

                if dicAuxFW.has_key('any_tp_src') == True:
                    lista_any_tp_src.append(str(json_dataFW[contFW]['any_tp_src']))
                else:
                    lista_any_tp_src.append("x")

                if dicAuxFW.has_key('outPort') == True:
                    lista_outPort.append(str(json_dataFW[contFW]['outPort']))
                else:
                    lista_outPort.append("x")

                if dicAuxFW.has_key('src_mac') == True:
                    lista_src_mac.append(str(json_dataFW[contFW]['src_mac']))
                else:
                    lista_src_mac.append("x")

                if dicAuxFW.has_key('dst_mac') == True:
                    lista_dst_mac.append(str(json_dataFW[contFW]['dst_mac']))
                else:
                    lista_dst_mac.append("x")

                if dicAuxFW.has_key('action') == True:
                    lista_action.append(str(json_dataFW[contFW]['action']))
                else:
                    lista_action.append("x")

                if dicAuxFW.has_key('match') == True:
                    dicAuxFW = dicAuxFW["match"]

                    if dicAuxFW.has_key('eth_src') == True:
                        lista_eth_src.append(str(json_dataFW[contFW]['eth_src']))
                    else:
                        lista_eth_src.append("x")

                    if dicAuxFW.has_key('eth_dst') == True:
                        lista_eth_dst.append(str(json_dataFW[contFW]['eth_dst']))
                    else:
                        lista_eth_dst.append("x")

                    if dicAuxFW.has_key('eth_type') == True:
                        lista_eth_type.append(str(json_dataFW[contFW]['eth_type']))
                    else:
                        lista_eth_type.append("x")

                    if dicAuxFW.has_key('in_port') == True:
                        lista_in_port.append(str(json_dataFW[contFW]['in_port']))
                    else:
                        lista_in_port.append("x")

                    if dicAuxFW.has_key('eth_vlan_vid') == True:
                        lista_eth_vlan_vid.append(str(json_dataFW[contFW]['eth_vlan_vid']))
                    else:
                        lista_eth_vlan_vid.append("x")

                    if dicAuxFW.has_key('eth_vlan_pcp') == True:
                        lista_eth_vlan_pcp.append(str(json_dataFW[contFW]['eth_vlan_pcp']))
                    else:
                        lista_eth_vlan_pcp.append("x")

                    if dicAuxFW.has_key('ip_proto') == True:
                        lista_ip_proto.append(str(json_dataFW[contFW]['ip_proto']))
                    else:
                        lista_ip_proto.append("x")

                    if dicAuxFW.has_key('ipv4_src') == True:
                        lista_ipv4_src.append(str(json_dataFW[contFW]['ipv4_src']))
                    else:
                        lista_ipv4_src.append("x")

                    if dicAuxFW.has_key('ipv4_dst') == True:
                        lista_ipv4_dst.append(str(json_dataFW[contFW]['ipv4_dst']))
                    else:
                        lista_ipv4_dst.append("x")

                    if dicAuxFW.has_key('ipv6_src') == True:
                        lista_ipv6_src.append(str(json_dataFW[contFW]['ipv6_src']))
                    else:
                        lista_ipv6_src.append("x")

                    if dicAuxFW.has_key('ipv6_dst') == True:
                        lista_ipv6_dst.append(str(json_dataFW[contFW]['ipv6_dst']))
                    else:
                        lista_ipv6_dst.append("x")

                    if dicAuxFW.has_key('ipv6_label') == True:
                        lista_ipv6_label.append(str(json_dataFW[contFW]['ipv6_label']))
                    else:
                        lista_ipv6_label.append("x")

                    if dicAuxFW.has_key('ip_tos') == True:
                        lista_ip_tos.append(str(json_dataFW[contFW]['ip_tos']))
                    else:
                        lista_ip_tos.append("x")

                    if dicAuxFW.has_key('ip_ecn') == True:
                     lista_ip_ecn.append(str(json_dataFW[contFW]['ip_ecn']))
                    else:
                        lista_ip_ecn.append("x")

                    if dicAuxFW.has_key('ip_dscp') == True:
                        lista_ip_dscp.append(str(json_dataFW[contFW]['ip_dscp']))
                    else:
                        lista_ip_dscp.append("x")

                    if dicAuxFW.has_key('tp_src') == True:
                        lista_tp_src.append(str(json_dataFW[contFW]['tp_src']))
                    else:
                        lista_tp_src.append("x")

                    if dicAuxFW.has_key('tp_dst') == True:
                        lista_tp_dst.append(str(json_dataFW[contFW]['tp_dst']))
                    else:
                        lista_tp_dst.append("x")

                    if dicAuxFW.has_key('udp_src') == True:
                        lista_udp_src.append(str(json_dataFW[contFW]['udp_src']))
                    else:
                        lista_udp_src.append("x")

                    if dicAuxFW.has_key('udp_dst') == True:
                        lista_udp_dst.append(str(json_dataFW[contFW]['udp_dst']))
                    else:
                        lista_udp_dst.append("x")

                    if dicAuxFW.has_key('tcp_src') == True:
                        lista_tcp_src.append(str(json_dataFW[contFW]['tcp_src']))
                    else:
                        lista_tcp_src.append("x")

                    if dicAuxFW.has_key('tcp_dst') == True:
                        lista_tcp_dst.append(str(json_dataFW[contFW]['tcp_dst']))
                    else:
                        lista_tcp_dst.append("x")

                    if dicAuxFW.has_key('sctp_src') == True:
                        lista_sctp_src.append(str(json_dataFW[contFW]['sctp_src']))
                    else:
                        lista_sctp_src.append("x")

                    if dicAuxFW.has_key('sctp_dst') == True:
                        lista_sctp_dst.append(str(json_dataFW[contFW]['sctp_dst']))
                    else:
                        lista_sctp_dst.append("x")

                    if dicAuxFW.has_key('icmpv4_type') == True:
                        lista_icmpv4_type.append(str(json_dataFW[contFW]['icmpv4_type']))
                    else:
                        lista_icmpv4_type.append("x")

                    if dicAuxFW.has_key('icmpv4_code') == True:
                        lista_icmpv4_code.append(str(json_dataFW[contFW]['icmpv4_code']))
                    else:
                        lista_icmpv4_code.append("x")

                    if dicAuxFW.has_key('icmpv6_type') == True:
                        lista_icmpv6_type.append(str(json_dataFW[contFW]['icmpv6_type']))
                    else:
                        lista_icmpv6_type.append("x")

                    if dicAuxFW.has_key('icmpv6_code') == True:
                        lista_icmpv6_code.append(str(json_dataFW[contFW]['icmpv6_code']))
                    else:
                        lista_icmpv6_code.append("x")

                    if dicAuxFW.has_key('ipv6_nd_ssl') == True:
                        lista_ipv6_nd_ssl.append(str(json_dataFW[contFW]['ipv6_nd_ssl']))
                    else:
                        lista_ipv6_nd_ssl.append("x")

                    if dicAuxFW.has_key('arp_spa') == True:
                        lista_arp_spa.append(str(json_dataFW[contFW]['arp_spa']))
                    else:
                        lista_arp_spa.append("x")

                    if dicAuxFW.has_key('arp_tpa') == True:
                        lista_arp_tpa.append(str(json_dataFW[contFW]['arp_tpa']))
                    else:
                        lista_arp_tpa.append("x")

                    if dicAuxFW.has_key('ipv6_nd_target') == True:
                        lista_ipv6_nd_target.append(str(json_dataFW[contFW]['ipv6_nd_target']))
                    else:
                        lista_ipv6_nd_target.append("x")

                    if dicAuxFW.has_key('arp_opcode') == True:
                        lista_arp_opcode.append(str(json_dataFW[contFW]['arp_opcode']))
                    else:
                        lista_arp_opcode.append("x")

                    if dicAuxFW.has_key('arp_tha') == True:
                        lista_arp_tha.append(str(json_dataFW[contFW]['arp_tha']))
                    else:
                        lista_arp_tha.append("x")

                    if dicAuxFW.has_key('arp_spa') == True:
                        lista_arp_spa.append(str(json_dataFW[contFW]['arp_spa']))
                    else:
                        lista_arp_spa.append("x")

                    if dicAuxFW.has_key('arp_tpa') == True:
                        lista_arp_tpa.append(str(json_dataFW[contFW]['arp_tpa']))
                    else:
                        lista_arp_tpa.append("x")

                    if dicAuxFW.has_key('mpls_label') == True:
                        lista_mpls_label.append(str(json_dataFW[contFW]['mpls_label']))
                    else:
                        lista_mpls_label.append("x")

                    if dicAuxFW.has_key('mpls_tc') == True:
                        lista_mpls_tc.append(str(json_dataFW[contFW]['mpls_tc']))
                    else:
                        lista_mpls_tc.append("x")

                    if dicAuxFW.has_key('mpls_bos') == True:
                        lista_mpls_bos.append(str(json_dataFW[contFW]['mpls_bos']))
                    else:
                        lista_mpls_bos.append("x")

                    if dicAuxFW.has_key('tunnel_id') == True:
                        lista_tunnel_id.append(str(json_dataFW[contFW]['tunnel_id']))
                    else:
                        lista_tunnel_id.append("x")

                    if dicAuxFW.has_key('metadata') == True:
                        lista_metadata.append(str(json_dataFW[contFW]['metadata']))
                    else:
                        lista_metadata.append("x")

                contFW += 1
            flowContFW = 0

            arquivo_regrasFW.write("[Switch: " + str(contSwitchFW + 1) + "]\n")

            for mfw in range(contFW):
                arquivo_regrasFW.write("(" + str(lista_eth_src[flowContFW]) + " ^ " + str(lista_eth_dst[flowContFW]) + " ^ " + str(lista_eth_type[flowContFW]) + " ^ " + str(lista_in_porteth_vlan_videth_vlan_pcp[flowContFW]) + " ^ " + str(lista_ip_proto[flowContFW]) + " ^ " + str(lista_ipv4_src[flowContFW]) + " ^ " + str(lista_ipv4_dstipv6_src[flowContFW]) + " ^ " + str(lista_ipv6_dst[flowContFW]) + " ^ " + str(lista_ipv6_label[flowContFW]) + " ^ " + str(lista_ip_tos[flowContFW]) + " ^ " + str(lista_ip_ecn[flowContFW]) + " ^ " + str(lista_ip_dscp[flowContFW]) + " ^ " + str(lista_tp_src[flowContFW]) + " ^ " + str(lista_tp_dst[flowContFW]) + " ^ " + str(lista_udp_src[flowContFW]) + " ^ " + str(lista_udp_dst[flowContFW]) + " ^ " + str(lista_tcp_srctcp_dst[flowContFW]) + " ^ " + str(lista_sctp_src[flowContFW]) + " ^ " + str(lista_sctp_dst[flowContFW]) + " ^ " + str(lista_icmpv4_type[flowContFW]) + " ^ " + str(lista_icmpv4_code[flowContFW]) + " ^ " + str(lista_icmpv6_type[flowContFW]) + " ^ " + str(lista_icmpv6_code[flowContFW]) + " ^ " + str(lista_ipv6_nd_ssl[flowContFW]) + " ^ " + str(lista_ipv6_nd_ttl[flowContFW]) + " ^ " + str(lista_arp_tpa[flowContFW]) + " ^ " + str(lista_ipv6_nd_target[flowContFW]) + " ^ " + str(lista_arp_opcode[flowContFW]) + " ^ " + str(lista_arp_tha[flowContFW]) + " ^ " + str(lista_arp_spa[flowContFW]) + " ^ " + str(lista_arp_tpaipv6_label[flowContFW]) + " ^ " + str(lista_ip_tos[flowContFW]) + " ^ " + str(lista_ip_ecn[flowContFW]) + " ^ " + str(lista_ip_dscp[flowContFW]) + " ^ " + str(lista_tp_src[flowContFW]) + " ^ " + str(lista_tp_dst[flowContFW]) + " ^ " + str(lista_udp_src[flowContFW]) + " ^ " + str(lista_udp_dst[flowContFW]) + " ^ " + str(lista_tcp_src[flowContFW]) + " ^ " + str(lista_tcp_dst[flowContFW]) + " ^ " + str(lista_sctp_src[flowContFW]) + " ^ " + str(lista_sctp_dst[flowContFW]) + " ^ " + str(lista_icmpv4_type[flowContFW]) + " ^ " + str(lista_icmpv4_code[flowContFW]) + " ^ " + str(lista_icmpv6_type[flowContFW]) + " ^ " + str(lista_icmpv6_code[flowContFW]) + " ^ " + str(lista_ipv6_nd_ssl[flowContFW]) + " ^ " + str(lista_ipv6_nd_ttl[flowContFW]) + " ^ " + str(lista_ipv6_nd_target[flowContFW]) + " ^ " + str(lista_arp_opcode[flowContFW]) + " ^ " + str(lista_arp_tha[flowContFW]) + " ^ " + str(lista_arp_spa[flowContFW]) + " ^ " + str(lista_arp_tpa[flowContFW]) + " ^ " + str(lista_mpls_label[flowContFW]) + " ^ " + str(lista_mpls_tc[flowContFW]) + " ^ " + str(lista_mpls_bos[flowContFW]) + " ^ " + str(lista_tunnel_id[flowContFW]) + " ^ " + str(lista_metadata[flowContFW]) + " ^ " + str(lista_version[flowContFW]) + " ^ " + str(lista_command[flowContFW]) + " ^ " + str(lista_cookie[flowContFW]) + " ^ " + str(lista_src_ip[flowContFW]) + " ^ " + str(lista_dst_ip[flowContFW]) + " ^ " + str(lista_dl_type[flowContFW]) + " ^ " + str(lista_nw_dst_prefix[flowContFW]) + " ^ " + str(lista_nw_src_prefix[flowContFW]) + " ^ " + str(lista_nw_src_maskbits[flowContFW]) + " ^ " + str(lista_nw_dst_maskbits[flowContFW]) + " ^ " + str(lista_any_nw_dst[flowContFW]) + " ^ " + str(lista_any_nw_proto[flowContFW]) + " ^ " + str(lista_any_in_port[flowContFW]) + " ^ " + str(lista_any_nw_srcany_tp_ds[flowContFW]) + " ^ " + str(lista_ruleid[flowContFW]) + " ^ " + str(lista_idleTimeoutSec[flowContFW]) + " ^ " + str(lista_hardTimeoutSec[flowContFW]) + " ^ " + str(lista_any_dl_type[flowContFW]) + " ^ " + str(lista_priority[flowContFW]) + " ^ " + str(lista_in_port[flowContFW]) + " ^ " + str(lista_any_dpid[flowContFW]) + " ^ " + str(lista_dl_src[flowContFW]) + " ^ " + str(lista_dpid[flowContFW]) + " ^ " + str(lista_tp_src[flowContFW]) + " ^ " + str(lista_any_dl_dst[flowContFW]) + " ^ " + str(lista_nw_proto[flowContFW]) + " ^ " + str(lista_tp_dst[flowContFW]) + " ^ " + str(lista_dl_dst[flowContFW]) + " ^ " + str(lista_any_tp_src[flowContFW]) + " ^ " + str(lista_outPort[flowContFW]) + " ^ " + str(lista_src_mac[flowContFW]) + " ^ " + str(lista_dst_mac[flowContFW]) + " ^ " + ") -> " + str(lista_action[flowContFW]) + "\n")

                dicFlowsFW.update({str(mfw):[lista_eth_src[flowContFW], lista_eth_dst[flowContFW], lista_eth_type[flowContFW], lista_in_porteth_vlan_videth_vlan_pcp[flowContFW], lista_ip_proto[flowContFW], lista_ipv4_src[flowContFW], lista_ipv4_dstipv6_src[flowContFW], lista_ipv6_dst[flowContFW], lista_ipv6_label[flowContFW], lista_ip_tos[flowContFW], lista_ip_ecn[flowContFW], lista_ip_dscp[flowContFW], lista_tp_src[flowContFW], lista_tp_dst[flowContFW], lista_udp_src[flowContFW], lista_udp_dst[flowContFW], lista_tcp_srctcp_dst[flowContFW], lista_sctp_src[flowContFW], lista_sctp_dst[flowContFW], lista_icmpv4_type[flowContFW], lista_icmpv4_code[flowContFW], lista_icmpv6_type[flowContFW], lista_icmpv6_code[flowContFW], lista_ipv6_nd_ssl[flowContFW], lista_ipv6_nd_ttl[flowContFW], lista_arp_tpa[flowContFW], lista_ipv6_nd_target[flowContFW], lista_arp_opcode[flowContFW], lista_arp_tha[flowContFW], lista_arp_spa[flowContFW], lista_arp_tpaipv6_label[flowContFW], lista_ip_tos[flowContFW], lista_ip_ecn[flowContFW], lista_ip_dscp[flowContFW], lista_tp_src[flowContFW], lista_tp_dst[flowContFW], lista_udp_src[flowContFW], lista_udp_dst[flowContFW], lista_tcp_src[flowContFW], lista_tcp_dst[flowContFW], lista_sctp_src[flowContFW], lista_sctp_dst[flowContFW], lista_icmpv4_type[flowContFW], lista_icmpv4_code[flowContFW], lista_icmpv6_type[flowContFW], lista_icmpv6_code[flowContFW], lista_ipv6_nd_ssl[flowContFW], lista_ipv6_nd_ttl[flowContFW], lista_ipv6_nd_target[flowContFW], lista_arp_opcode[flowContFW], lista_arp_tha[flowContFW], lista_arp_spa[flowContFW], lista_arp_tpa[flowContFW], lista_mpls_label[flowContFW], lista_mpls_tc[flowContFW], lista_mpls_bos[flowContFW], lista_tunnel_id[flowContFW], lista_metadata[flowContFW], lista_[flowContFW], lista_version[flowContFW], lista_command[flowContFW], lista_cookie[flowContFW], lista_src_ip[flowContFW], lista_dst_ip[flowContFW], lista_dl_type[flowContFW], lista_nw_dst_prefix[flowContFW], lista_nw_src_prefix[flowContFW], lista_nw_src_maskbits[flowContFW], lista_nw_dst_maskbits[flowContFW], lista_any_nw_dst[flowContFW], lista_any_nw_proto[flowContFW], lista_any_in_port[flowContFW], lista_any_nw_srcany_tp_ds[flowContFW], lista_ruleid[flowContFW], lista_idleTimeoutSec[flowContFW], lista_hardTimeoutSec[flowContFW], lista_any_dl_type[flowContFW], lista_priority[flowContFW], lista_in_port[flowContFW], lista_any_dpid[flowContFW], lista_dl_src[flowContFW], lista_dpid[flowContFW], lista_tp_src[flowContFW], lista_any_dl_dst[flowContFW], lista_nw_proto[flowContFW], lista_tp_dst[flowContFW], lista_dl_dst[flowContFW], lista_any_tp_src[flowContFW], lista_outPort[flowContFW], lista_src_mac[flowContFW], lista_dst_mac[flowContFW], lista_action[flowContFW]]})
                flowContFW += 1
            arquivo_regrasFW.write("\n\n")
            contSwitchFW += 1

            # Algoritmo de verificacao
            ifw = 0
            jfw = 0

            for lfw in range(len(lista_actions) - 1):
                jfw = ifw + 1
                for kfw in range(len(lista_actions) - (ifw + 1)):
                    if (lista_eth_src[ifw] == 'x'):
                        lista_eth_src[ifw] = lista_eth_src[jfw]
                    if (lista_eth_dst[ifw] == 'x'):
                        lista_eth_dst[ifw] = lista_eth_dst[jfw]
                    if (lista_eth_type[ifw] == 'x'):
                        lista_eth_type[ifw] = lista_eth_type[jfw]
                    if (lista_in_porteth_vlan_videth_vlan_pcp[ifw] == 'x'):
                        lista_in_porteth_vlan_videth_vlan_pcp[ifw] = lista_in_porteth_vlan_videth_vlan_pcp[jfw]
                    if (lista_ip_proto[ifw] == 'x'):
                        lista_ip_proto[ifw] = lista_ip_proto[jfw]
                    if (lista_ipv4_src[ifw] == 'x'):
                        lista_ipv4_src[ifw] = lista_ipv4_src[jfw]
                    if (lista_ipv4_dstipv6_src[ifw] == 'x'):
                        lista_ipv4_dstipv6_src[ifw] = lista_ipv4_dstipv6_src[jfw]
                    if (lista_ipv6_dst[ifw] == 'x'):
                        lista_ipv6_dst[ifw] = lista_ipv6_dst[jfw]
                    if (lista_ipv6_label[ifw] == 'x'):
                        lista_ipv6_label[ifw] = lista_ipv6_label[jfw]
                    if (lista_ip_tos[ifw] == 'x'):
                        lista_ip_tos[ifw] = lista_ip_tos[jfw]
                    if (lista_ip_ecn[ifw] == 'x'):
                        lista_ip_ecn[ifw] = lista_ip_ecn[jfw]
                    if (lista_ip_dscp[ifw] == 'x'):
                        lista_ip_dscp[ifw] = lista_ip_dscp[jfw]
                    if (lista_tp_src[ifw] == 'x'):
                        lista_tp_src[ifw] = lista_tp_src[jfw]
                    if (lista_tp_dst[ifw] == 'x'):
                        lista_tp_dst[ifw] = lista_tp_dst[jfw]
                    if (lista_udp_src[ifw] == 'x'):
                        lista_udp_src[ifw] = lista_udp_src[jfw]
                    if (lista_udp_dst[ifw] == 'x'):
                        lista_udp_dst[ifw] = lista_udp_dst[jfw]
                    if (lista_tcp_srctcp_dst[ifw] == 'x'):
                        lista_tcp_srctcp_dst[ifw] = lista_tcp_srctcp_dst[jfw]
                    if (lista_sctp_src[ifw] == 'x'):
                        lista_sctp_src[ifw] = lista_sctp_src[jfw]
                    if (lista_sctp_dst[ifw] == 'x'):
                        lista_sctp_dst[ifw] = lista_sctp_dst[jfw]
                    if (lista_icmpv4_type[ifw] == 'x'):
                        lista_icmpv4_type[ifw] = lista_icmpv4_type[jfw]
                    if (lista_icmpv4_code[ifw] == 'x'):
                        lista_icmpv4_code[ifw] = lista_icmpv4_code[jfw]
                    if (lista_icmpv6_type[ifw] == 'x'):
                        lista_icmpv6_type[ifw] = lista_icmpv6_type[jfw]
                    if (lista_icmpv6_code[ifw] == 'x'):
                        lista_icmpv6_code[ifw] = lista_icmpv6_code[jfw]
                    if (lista_ipv6_nd_ssl[ifw] == 'x'):
                        lista_ipv6_nd_ssl[ifw] = lista_ipv6_nd_ssl[jfw]
                    if (lista_ipv6_nd_ttl[ifw] == 'x'):
                        lista_ipv6_nd_ttl[ifw] = lista_ipv6_nd_ttl[jfw]
                    if (lista_arp_tpa[ifw] == 'x'):
                        lista_arp_tpa[ifw] = lista_arp_tpa[jfw]
                    if (lista_ipv6_nd_target[ifw] == 'x'):
                        lista_ipv6_nd_target[ifw] = lista_ipv6_nd_target[jfw]
                    if (lista_arp_opcode[ifw] == 'x'):
                        lista_arp_opcode[ifw] = lista_arp_opcode[jfw]
                    if (lista_arp_tha[ifw] == 'x'):
                        lista_arp_tha[ifw] = lista_arp_tha[jfw]
                    if (lista_arp_spa[ifw] == 'x'):
                        lista_arp_spa[ifw] = lista_arp_spa[jfw]
                    if (lista_arp_tpaipv6_label[ifw] == 'x'):
                        lista_arp_tpaipv6_label[ifw] = lista_arp_tpaipv6_label[jfw]
                    if (lista_ip_tos[ifw] == 'x'):
                        lista_ip_tos[ifw] = lista_ip_tos[jfw]
                    if (lista_ip_ecn[ifw] == 'x'):
                        lista_ip_ecn[ifw] = lista_ip_ecn[jfw]
                    if (lista_ip_dscp[ifw] == 'x'):
                        lista_ip_dscp[ifw] = lista_ip_dscp[jfw]
                    if (lista_tp_src[ifw] == 'x'):
                        lista_tp_src[ifw] = lista_tp_src[jfw]
                    if (lista_tp_dst[ifw] == 'x'):
                        lista_tp_dst[ifw] = lista_tp_dst[jfw]
                    if (lista_udp_src[ifw] == 'x'):
                        lista_udp_src[ifw] = lista_udp_src[jfw]
                    if (lista_udp_dst[ifw] == 'x'):
                        lista_udp_dst[ifw] = lista_udp_dst[jfw]
                    if (lista_tcp_src[ifw] == 'x'):
                        lista_tcp_src[ifw] = lista_tcp_src[jfw]
                    if (lista_tcp_dst[ifw] == 'x'):
                        lista_tcp_dst[ifw] = lista_tcp_dst[jfw]
                    if (lista_sctp_src[ifw] == 'x'):
                        lista_sctp_src[ifw] = lista_sctp_src[jfw]
                    if (lista_sctp_dst[ifw] == 'x'):
                        lista_sctp_dst[ifw] = lista_sctp_dst[jfw]
                    if (lista_icmpv4_type[ifw] == 'x'):
                        lista_icmpv4_type[ifw] = lista_icmpv4_type[jfw]
                    if (lista_icmpv4_code[ifw] == 'x'):
                        lista_icmpv4_code[ifw] = lista_icmpv4_code[jfw]
                    if (lista_icmpv6_type[ifw] == 'x'):
                        lista_icmpv6_type[ifw] = lista_icmpv6_type[jfw]
                    if (lista_icmpv6_code[ifw] == 'x'):
                        lista_icmpv6_code[ifw] = lista_icmpv6_code[jfw]
                    if (lista_ipv6_nd_ssl[ifw] == 'x'):
                        lista_ipv6_nd_ssl[ifw] = lista_ipv6_nd_ssl[jfw]
                    if (lista_ipv6_nd_ttl[ifw] == 'x'):
                        lista_ipv6_nd_ttl[ifw] = lista_ipv6_nd_ttl[jfw]
                    if (lista_ipv6_nd_target[ifw] == 'x'):
                        lista_ipv6_nd_target[ifw] = lista_ipv6_nd_target[jfw]
                    if (lista_arp_opcode[ifw] == 'x'):
                        lista_arp_opcode[ifw] = lista_arp_opcode[jfw]
                    if (lista_arp_tha[ifw] == 'x'):
                        lista_arp_tha[ifw] = lista_arp_tha[jfw]
                    if (lista_arp_spa[ifw] == 'x'):
                        lista_arp_spa[ifw] = lista_arp_spa[jfw]
                    if (lista_arp_tpa[ifw] == 'x'):
                        lista_arp_tpa[ifw] = lista_arp_tpa[jfw]
                    if (lista_mpls_label[ifw] == 'x'):
                        lista_mpls_label[ifw] = lista_mpls_label[jfw]
                    if (lista_mpls_tc[ifw] == 'x'):
                        lista_mpls_tc[ifw] = lista_mpls_tc[jfw]
                    if (lista_mpls_bos[ifw] == 'x'):
                        lista_mpls_bos[ifw] = lista_mpls_bos[jfw]
                    if (lista_tunnel_id[ifw] == 'x'):
                        lista_tunnel_id[ifw] = lista_tunnel_id[jfw]
                    if (lista_metadata[ifw] == 'x'):
                        lista_metadata[ifw] = lista_metadata[jfw]
                    if (lista_[ifw] == 'x'):
                        lista_[ifw] = lista_[jfw]
                    if (lista_version[ifw] == 'x'):
                        lista_version[ifw] = lista_version[jfw]
                    if (lista_command[ifw] == 'x'):
                        lista_command[ifw] = lista_command[jfw]
                    if (lista_cookie[ifw] == 'x'):
                        lista_cookie[ifw] = lista_cookie[jfw]
                    if (lista_src_ip[ifw] == 'x'):
                        lista_src_ip[ifw] = lista_src_ip[jfw]
                    if (lista_dst_ip[ifw] == 'x'):
                        lista_dst_ip[ifw] = lista_dst_ip[jfw]
                    if (lista_dl_type[ifw] == 'x'):
                        lista_dl_type[ifw] = lista_dl_type[jfw]
                    if (lista_nw_dst_prefix[ifw] == 'x'):
                        lista_nw_dst_prefix[ifw] = lista_nw_dst_prefix[jfw]
                    if (lista_nw_src_prefix[ifw] == 'x'):
                        lista_nw_src_prefix[ifw] = lista_nw_src_prefix[jfw]
                    if (lista_nw_src_maskbits[ifw] == 'x'):
                        lista_nw_src_maskbits[ifw] = lista_nw_src_maskbits[jfw]
                    if (lista_nw_dst_maskbits[ifw] == 'x'):
                        lista_nw_dst_maskbits[ifw] = lista_nw_dst_maskbits[jfw]
                    if (lista_any_nw_dst[ifw] == 'x'):
                        lista_any_nw_dst[ifw] = lista_any_nw_dst[jfw]
                    if (lista_any_nw_proto[ifw] == 'x'):
                        lista_any_nw_proto[ifw] = lista_any_nw_proto[jfw]
                    if (lista_any_in_port[ifw] == 'x'):
                        lista_any_in_port[ifw] = lista_any_in_port[jfw]
                    if (lista_any_nw_srcany_tp_ds[ifw] == 'x'):
                        lista_any_nw_srcany_tp_ds[ifw] = lista_any_nw_srcany_tp_ds[jfw]
                    if (lista_ruleid[ifw] == 'x'):
                        lista_ruleid[ifw] = lista_ruleid[jfw]
                    if (lista_idleTimeoutSec[ifw] == 'x'):
                        lista_idleTimeoutSec[ifw] = lista_idleTimeoutSec[jfw]
                    if (lista_hardTimeoutSec[ifw] == 'x'):
                        lista_hardTimeoutSec[ifw] = lista_hardTimeoutSec[jfw]
                    if (lista_any_dl_type[ifw] == 'x'):
                        lista_any_dl_type[ifw] = lista_any_dl_type[jfw]
                    if (lista_priority[ifw] == 'x'):
                        lista_priority[ifw] = lista_priority[jfw]
                    if (lista_in_port[ifw] == 'x'):
                        lista_in_port[ifw] = lista_in_port[jfw]
                    if (lista_any_dpid[ifw] == 'x'):
                        lista_any_dpid[ifw] = lista_any_dpid[jfw]
                    if (lista_dl_src[ifw] == 'x'):
                            lista_dl_src[ifw] = lista_dl_src[jfw]
                    if (lista_dpid[ifw] == 'x'):
                        lista_dpid[ifw] = lista_dpid[jfw]
                    if (lista_tp_src[ifw] == 'x'):
                        lista_tp_src[ifw] = lista_tp_src[jfw]
                    if (lista_any_dl_dst[ifw] == 'x'):
                        lista_any_dl_dst[ifw] = lista_any_dl_dst[jfw]
                    if (lista_nw_proto[ifw] == 'x'):
                        lista_nw_proto[ifw] = lista_nw_proto[jfw]
                    if (lista_tp_dst[ifw] == 'x'):
                        lista_tp_dst[ifw] = lista_tp_dst[jfw]
                    if (lista_dl_dst[ifw] == 'x'):
                        lista_dl_dst[ifw] = lista_dl_dst[jfw]
                    if (lista_any_tp_src[ifw] == 'x'):
                        lista_any_tp_src[ifw] = lista_any_tp_src[jfw]
                    if (lista_outPort[ifw] == 'x'):
                        lista_outPort[ifw] = lista_outPort[jfw]
                    if (lista_src_mac[ifw] == 'x'):
                        lista_src_mac[ifw] = lista_src_mac[jfw]
                    if (lista_dst_mac[ifw] == 'x'):
                        lista_dst_mac[ifw] = lista_dst_mac[jfw]
                    if (lista_action[ifw] == 'x'):
                        lista_action[ifw] = lista_action[jfw]

                    if(lista_eth_src[ifw]==lista_eth_src[jfw] and lista_eth_dst[ifw]==lista_eth_dst[jfw] and lista_eth_type[ifw]==lista_eth_type[jfw] and lista_in_porteth_vlan_videth_vlan_pcp[ifw]==lista_in_porteth_vlan_videth_vlan_pcp[jfw] and lista_ip_proto[ifw]==lista_ip_proto[jfw] and lista_ipv4_src[ifw]==lista_ipv4_src[jfw] and lista_ipv4_dstipv6_src[ifw]==lista_ipv4_dstipv6_src[jfw] and lista_ipv6_dst[ifw]==lista_ipv6_dst[jfw] and lista_ipv6_label[ifw]==lista_ipv6_label[jfw] and lista_ip_tos[ifw]==lista_ip_tos[jfw] and lista_ip_ecn[ifw]==lista_ip_ecn[jfw] and lista_ip_dscp[ifw]==lista_ip_dscp[jfw] and lista_tp_src[ifw]==lista_tp_src[jfw] and lista_tp_dst[ifw]==lista_tp_dst[jfw] and lista_udp_src[ifw]==lista_udp_src[jfw] and lista_udp_dst[ifw]==lista_udp_dst[jfw] and lista_tcp_srctcp_dst[ifw]==lista_tcp_srctcp_dst[jfw] and lista_sctp_src[ifw]==lista_sctp_src[jfw] and lista_sctp_dst[ifw]==lista_sctp_dst[jfw] and lista_icmpv4_type[ifw]==lista_icmpv4_type[jfw] and lista_icmpv4_code[ifw]==lista_icmpv4_code[jfw] and lista_icmpv6_type[ifw]==lista_icmpv6_type[jfw] and lista_icmpv6_code[ifw]==lista_icmpv6_code[jfw] and lista_ipv6_nd_ssl[ifw]==lista_ipv6_nd_ssl[jfw] and lista_ipv6_nd_ttl[ifw]==lista_ipv6_nd_ttl[jfw] and lista_arp_tpa[ifw]==lista_arp_tpa[jfw] and lista_ipv6_nd_target[ifw]==lista_ipv6_nd_target[jfw] and lista_arp_opcode[ifw]==lista_arp_opcode[jfw] and lista_arp_tha[ifw]==lista_arp_tha[jfw] and lista_arp_spa[ifw]==lista_arp_spa[jfw] and lista_arp_tpaipv6_label[ifw]==lista_arp_tpaipv6_label[jfw] and lista_ip_tos[ifw]==lista_ip_tos[jfw] and lista_ip_ecn[ifw]==lista_ip_ecn[jfw] and lista_ip_dscp[ifw]==lista_ip_dscp[jfw] and lista_tp_src[ifw]==lista_tp_src[jfw] and lista_tp_dst[ifw]==lista_tp_dst[jfw] and lista_udp_src[ifw]==lista_udp_src[jfw] and lista_udp_dst[ifw]==lista_udp_dst[jfw] and lista_tcp_src[ifw]==lista_tcp_src[jfw] and lista_tcp_dst[ifw]==lista_tcp_dst[jfw] and lista_sctp_src[ifw]==lista_sctp_src[jfw] and lista_sctp_dst[ifw]==lista_sctp_dst[jfw] and lista_icmpv4_type[ifw]==lista_icmpv4_type[jfw] and lista_icmpv4_code[ifw]==lista_icmpv4_code[jfw] and lista_icmpv6_type[ifw]==lista_icmpv6_type[jfw] and lista_icmpv6_code[ifw]==lista_icmpv6_code[jfw] and lista_ipv6_nd_ssl[ifw]==lista_ipv6_nd_ssl[jfw] and lista_ipv6_nd_ttl[ifw]==lista_ipv6_nd_ttl[jfw] and lista_ipv6_nd_target[ifw]==lista_ipv6_nd_target[jfw] and lista_arp_opcode[ifw]==lista_arp_opcode[jfw] and lista_arp_tha[ifw]==lista_arp_tha[jfw] and lista_arp_spa[ifw]==lista_arp_spa[jfw] and lista_arp_tpa[ifw]==lista_arp_tpa[jfw] and lista_mpls_label[ifw]==lista_mpls_label[jfw] and lista_mpls_tc[ifw]==lista_mpls_tc[jfw] and lista_mpls_bos[ifw]==lista_mpls_bos[jfw] and lista_tunnel_id[ifw]==lista_tunnel_id[jfw] and lista_metadata[ifw]==lista_metadata[jfw] and lista_[ifw]==lista_[jfw] and lista_version[ifw]==lista_version[jfw] and lista_command[ifw]==lista_command[jfw] and lista_cookie[ifw]==lista_cookie[jfw] and lista_src_ip[ifw]==lista_src_ip[jfw] and lista_dst_ip[ifw]==lista_dst_ip[jfw] and lista_dl_type[ifw]==lista_dl_type[jfw] and lista_nw_dst_prefix[ifw]==lista_nw_dst_prefix[jfw] and lista_nw_src_prefix[ifw]==lista_nw_src_prefix[jfw] and lista_nw_src_maskbits[ifw]==lista_nw_src_maskbits[jfw] and lista_nw_dst_maskbits[ifw]==lista_nw_dst_maskbits[jfw] and lista_any_nw_dst[ifw]==lista_any_nw_dst[jfw] and lista_any_nw_proto[ifw]==lista_any_nw_proto[jfw] and lista_any_in_port[ifw]==lista_any_in_port[jfw] and lista_any_nw_srcany_tp_ds[ifw]==lista_any_nw_srcany_tp_ds[jfw] and lista_ruleid[ifw]==lista_ruleid[jfw] and lista_idleTimeoutSec[ifw]==lista_idleTimeoutSec[jfw] and lista_hardTimeoutSec[ifw]==lista_hardTimeoutSec[jfw] and lista_any_dl_type[ifw]==lista_any_dl_type[jfw] and lista_priority[ifw]==lista_priority[jfw] and lista_in_port[ifw]==lista_in_port[jfw] and lista_any_dpid[ifw]==lista_any_dpid[jfw] and lista_dl_src[ifw]==lista_dl_src[jfw] and lista_dpid[ifw]==lista_dpid[jfw] and lista_tp_src[ifw]==lista_tp_src[jfw] and lista_any_dl_dst[ifw]==lista_any_dl_dst[jfw] and lista_nw_proto[ifw]==lista_nw_proto[jfw] and lista_tp_dst[ifw]==lista_tp_dst[jfw] and lista_dl_dst[ifw]==lista_dl_dst[jfw] and lista_any_tp_src[ifw]==lista_any_tp_src[jfw] and lista_outPort[ifw]==lista_outPort[jfw] and lista_src_mac[ifw]==lista_src_mac[jfw] and lista_dst_mac[ifw]==lista_dst_mac[jfw] and lista_action[ifw]==lista_action[jfw]):

                        if(lista_action[ifw] == lista_action[jfw]):
                            arquivo_regras_conflitantesFW.write("(" + str(lista_eth_src[ifw]) + " ^ " + str(lista_eth_dst[ifw]) + " ^ " + str(lista_eth_type[ifw]) + " ^ " + str(lista_in_porteth_vlan_videth_vlan_pcp[ifw]) + " ^ " + str(lista_ip_proto[ifw]) + " ^ " + str(lista_ipv4_src[ifw]) + " ^ " + str(lista_ipv4_dstipv6_src[ifw]) + " ^ " + str(lista_ipv6_dst[ifw]) + " ^ " + str(lista_ipv6_label[ifw]) + " ^ " + str(lista_ip_tos[ifw]) + " ^ " + str(lista_ip_ecn[ifw]) + " ^ " + str(lista_ip_dscp[ifw]) + " ^ " + str(lista_tp_src[ifw]) + " ^ " + str(lista_tp_dst[ifw]) + " ^ " + str(lista_udp_src[ifw]) + " ^ " + str(lista_udp_dst[ifw]) + " ^ " + str(lista_tcp_srctcp_dst[ifw]) + " ^ " + str(lista_sctp_src[ifw]) + " ^ " + str(lista_sctp_dst[ifw]) + " ^ " + str(lista_icmpv4_type[ifw]) + " ^ " + str(lista_icmpv4_code[ifw]) + " ^ " + str(lista_icmpv6_type[ifw]) + " ^ " + str(lista_icmpv6_code[ifw]) + " ^ " + str(lista_ipv6_nd_ssl[ifw]) + " ^ " + str(lista_ipv6_nd_ttl[ifw]) + " ^ " + str(lista_arp_tpa[ifw]) + " ^ " + str(lista_ipv6_nd_target[ifw]) + " ^ " + str(lista_arp_opcode[ifw]) + " ^ " + str(lista_arp_tha[ifw]) + " ^ " + str(lista_arp_spa[ifw]) + " ^ " + str(lista_arp_tpaipv6_label[ifw]) + " ^ " + str(lista_ip_tos[ifw]) + " ^ " + str(lista_ip_ecn[ifw]) + " ^ " + str(lista_ip_dscp[ifw]) + " ^ " + str(lista_tp_src[ifw]) + " ^ " + str(lista_tp_dst[ifw]) + " ^ " + str(lista_udp_src[ifw]) + " ^ " + str(lista_udp_dst[ifw]) + " ^ " + str(lista_tcp_src[ifw]) + " ^ " + str(lista_tcp_dst[ifw]) + " ^ " + str(lista_sctp_src[ifw]) + " ^ " + str(lista_sctp_dst[ifw]) + " ^ " + str(lista_icmpv4_type[ifw]) + " ^ " + str(lista_icmpv4_code[ifw]) + " ^ " + str(lista_icmpv6_type[ifw]) + " ^ " + str(lista_icmpv6_code[ifw]) + " ^ " + str(lista_ipv6_nd_ssl[ifw]) + " ^ " + str(lista_ipv6_nd_ttl[ifw]) + " ^ " + str(lista_ipv6_nd_target[ifw]) + " ^ " + str(lista_arp_opcode[ifw]) + " ^ " + str(lista_arp_tha[ifw]) + " ^ " + str(lista_arp_spa[ifw]) + " ^ " + str(lista_arp_tpa[ifw]) + " ^ " + str(lista_mpls_label[ifw]) + " ^ " + str(lista_mpls_tc[ifw]) + " ^ " + str(lista_mpls_bos[ifw]) + " ^ " + str(lista_tunnel_id[ifw]) + " ^ " + str(lista_metadata[ifw]) + " ^ " + str(lista_[ifw]) + " ^ " + str(lista_version[ifw]) + " ^ " + str(lista_command[ifw]) + " ^ " + str(lista_cookie[ifw]) + " ^ " + str(lista_src_ip[ifw]) + " ^ " + str(lista_dst_ip[ifw]) + " ^ " + str(lista_dl_type[ifw]) + " ^ " + str(lista_nw_dst_prefix[ifw]) + " ^ " + str(lista_nw_src_prefix[ifw]) + " ^ " + str(lista_nw_src_maskbits[ifw]) + " ^ " + str(lista_nw_dst_maskbits[ifw]) + " ^ " + str(lista_any_nw_dst[ifw]) + " ^ " + str(lista_any_nw_proto[ifw]) + " ^ " + str(lista_any_in_port[ifw]) + " ^ " + str(lista_any_nw_srcany_tp_ds[ifw]) + " ^ " + str(lista_ruleid[ifw]) + " ^ " + str(lista_idleTimeoutSec[ifw]) + " ^ " + str(lista_hardTimeoutSec[ifw]) + " ^ " + str(lista_any_dl_type[ifw]) + " ^ " + str(lista_priority[ifw]) + " ^ " + str(lista_in_port[ifw]) + " ^ " + str(lista_any_dpid[ifw]) + " ^ " + str(lista_dl_src[ifw]) + " ^ " + str(lista_dpid[ifw]) + " ^ " + str(lista_tp_src[ifw]) + " ^ " + str(lista_any_dl_dst[ifw]) + " ^ " + str(lista_nw_proto[ifw]) + " ^ " + str(lista_tp_dst[ifw]) + " ^ " + str(lista_dl_dst[ifw]) + " ^ " + str(lista_any_tp_src[ifw]) + " ^ " + str(lista_outPort[ifw]) + " ^ " + str(lista_src_mac[ifw]) + " ^ " + str(lista_dst_mac[ifw]) + ") -> " + str(lista_actions[ifw]) + "\n")
                            arquivo_regras_conflitantesFW.write("Detectado conflito entre o fluxo " + str(ifw) + " e entre o fluxo " + str(jfw) + " no switch " + str(contSwitchFW) + "\n\n")
                            conflito(ifw, jfw, contSwitchFW)
                            flag_confRedFW = 1
                        else:
                            arquivo_regras_redundantesFW.write("(" + str(lista_eth_src[ifw]) + " ^ " + str(lista_eth_dst[ifw]) + " ^ " + str(lista_eth_type[ifw]) + " ^ " + str(lista_in_porteth_vlan_videth_vlan_pcp[ifw]) + " ^ " + str(lista_ip_proto[ifw]) + " ^ " + str(lista_ipv4_src[ifw]) + " ^ " + str(lista_ipv4_dstipv6_src[ifw]) + " ^ " + str(lista_ipv6_dst[ifw]) + " ^ " + str(lista_ipv6_label[ifw]) + " ^ " + str(lista_ip_tos[ifw]) + " ^ " + str(lista_ip_ecn[ifw]) + " ^ " + str(lista_ip_dscp[ifw]) + " ^ " + str(lista_tp_src[ifw]) + " ^ " + str(lista_tp_dst[ifw]) + " ^ " + str(lista_udp_src[ifw]) + " ^ " + str(lista_udp_dst[ifw]) + " ^ " + str(lista_tcp_srctcp_dst[ifw]) + " ^ " + str(lista_sctp_src[ifw]) + " ^ " + str(lista_sctp_dst[ifw]) + " ^ " + str(lista_icmpv4_type[ifw]) + " ^ " + str(lista_icmpv4_code[ifw]) + " ^ " + str(lista_icmpv6_type[ifw]) + " ^ " + str(lista_icmpv6_code[ifw]) + " ^ " + str(lista_ipv6_nd_ssl[ifw]) + " ^ " + str(lista_ipv6_nd_ttl[ifw]) + " ^ " + str(lista_arp_tpa[ifw]) + " ^ " + str(lista_ipv6_nd_target[ifw]) + " ^ " + str(lista_arp_opcode[ifw]) + " ^ " + str(lista_arp_tha[ifw]) + " ^ " + str(lista_arp_spa[ifw]) + " ^ " + str(lista_arp_tpaipv6_label[ifw]) + " ^ " + str(lista_ip_tos[ifw]) + " ^ " + str(lista_ip_ecn[ifw]) + " ^ " + str(lista_ip_dscp[ifw]) + " ^ " + str(lista_tp_src[ifw]) + " ^ " + str(lista_tp_dst[ifw]) + " ^ " + str(lista_udp_src[ifw]) + " ^ " + str(lista_udp_dst[ifw]) + " ^ " + str(lista_tcp_src[ifw]) + " ^ " + str(lista_tcp_dst[ifw]) + " ^ " + str(lista_sctp_src[ifw]) + " ^ " + str(lista_sctp_dst[ifw]) + " ^ " + str(lista_icmpv4_type[ifw]) + " ^ " + str(lista_icmpv4_code[ifw]) + " ^ " + str(lista_icmpv6_type[ifw]) + " ^ " + str(lista_icmpv6_code[ifw]) + " ^ " + str(lista_ipv6_nd_ssl[ifw]) + " ^ " + str(lista_ipv6_nd_ttl[ifw]) + " ^ " + str(lista_ipv6_nd_target[ifw]) + " ^ " + str(lista_arp_opcode[ifw]) + " ^ " + str(lista_arp_tha[ifw]) + " ^ " + str(lista_arp_spa[ifw]) + " ^ " + str(lista_arp_tpa[ifw]) + " ^ " + str(lista_mpls_label[ifw]) + " ^ " + str(lista_mpls_tc[ifw]) + " ^ " + str(lista_mpls_bos[ifw]) + " ^ " + str(lista_tunnel_id[ifw]) + " ^ " + str(lista_metadata[ifw]) + " ^ " + str(lista_[ifw]) + " ^ " + str(lista_version[ifw]) + " ^ " + str(lista_command[ifw]) + " ^ " + str(lista_cookie[ifw]) + " ^ " + str(lista_src_ip[ifw]) + " ^ " + str(lista_dst_ip[ifw]) + " ^ " + str(lista_dl_type[ifw]) + " ^ " + str(lista_nw_dst_prefix[ifw]) + " ^ " + str(lista_nw_src_prefix[ifw]) + " ^ " + str(lista_nw_src_maskbits[ifw]) + " ^ " + str(lista_nw_dst_maskbits[ifw]) + " ^ " + str(lista_any_nw_dst[ifw]) + " ^ " + str(lista_any_nw_proto[ifw]) + " ^ " + str(lista_any_in_port[ifw]) + " ^ " + str(lista_any_nw_srcany_tp_ds[ifw]) + " ^ " + str(lista_ruleid[ifw]) + " ^ " + str(lista_idleTimeoutSec[ifw]) + " ^ " + str(lista_hardTimeoutSec[ifw]) + " ^ " + str(lista_any_dl_type[ifw]) + " ^ " + str(lista_priority[ifw]) + " ^ " + str(lista_in_port[ifw]) + " ^ " + str(lista_any_dpid[ifw]) + " ^ " + str(lista_dl_src[ifw]) + " ^ " + str(lista_dpid[ifw]) + " ^ " + str(lista_tp_src[ifw]) + " ^ " + str(lista_any_dl_dst[ifw]) + " ^ " + str(lista_nw_proto[ifw]) + " ^ " + str(lista_tp_dst[ifw]) + " ^ " + str(lista_dl_dst[ifw]) + " ^ " + str(lista_any_tp_src[ifw]) + " ^ " + str(lista_outPort[ifw]) + " ^ " + str(lista_src_mac[ifw]) + " ^ " + str(lista_dst_mac[ifw]) + ") -> " + str(lista_actions[ifw]) + "\n")
                            arquivo_regras_redundantesFW.write("Detectada a redundancia acima entre o fluxo " + str(ifw) + " e entre o fluxo " + str(jfw) + " no switch " + str(contSwitchFW) + "\n\n")
                        redundancia(ifw, jfw, contSwitchFW)
                        flag_confRedFW = 1
                jfw += 1
            ifw += 1
        lista_csvFW.append(dicFlowsFW)
    arquivo_regrasFW.close()
    arquivo_regras_conflitantesFW.close()
    arquivo_regras_redundantesFW.close()
    arquivoDadosCSVFW = open("../data/arquivoDadosFW.csv", "w")

    if flag_confRed != 1:
        print "\nNenhum conflito e nenhuma redundancia foram encontrados no Firewall!\n"

    # len(lista_csvFW[rfw]) e' igual ao numero de fluxos contidos na lista_csv[r]
    for rfw in range(len(lista_csvFW)):
        dicAux_CSV = lista_csvFW[r]
        # print dicAux_CSVFW
        for nfw in range(len(lista_csvFW[r])):
            arquivoDadosCSVFW.write(str(dicAux_CSVFW[str(nfw)]) + "\n")
        arquivoDadosCSVFW.write("\n")

    arquivoDadosCSVFW.close()


    end_fw = time.time()

        ############+++++++++++++++++++++++++++++++++++++++++++++++++++####

    raw_input("\nPressione [Enter] para voltar ao menu principal\n")
    system("clear")
