import igraph
import random
import numpy as np
import math
from graphcoltests.gulosos import Gulosos

class Metaheuristicas:
    """
    Classe com funções que executam algoritmos de coloração que usam metaheurísticas.
    """

    def tabucol(grafo, solucao_inicial=None, tabu=5, iteracoes_min=20, iteracoes_max=50, cores_max = None, iteracoes_s_mudanca = 10):
        """
        Função usada para devolver uma coloração do grafo passado como parâmetro
        usando o algoritmo Coloração Tabu. A função realiza uma exploração do espaço de soluções
        impróprio e devolve a primeira melhor solução viável encontrada. Caso não seja encontrada solução
        viável com os parâmetros passados será retornada uma mensagem indicando isso e o grafo com 
        uma coloração imprópria. 

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        solucao_inicial (list): Lista de inteiros que deve possuir uma coloração inicial do grafo passado.
                                Caso não seja passado uma solução aleatória será construída.
        tabu (int): Valor tabu, quantidade de iterações que um movimento permanecerá na lista tabu. O valor
                    padrão é 5.
        iteracoes_min (int): Número mínimo de iterações que o algoritmo deve realizar antes da solução ser devolvida.
        iteracoes_max (int): Número mínimo de iterações que o algoritmo pode realizar antes da solução ser devolvida.
        cores_max (int): Número de cores máximo que deve ser considerado durante a construção da solução. Caso não seja
                         passado um valor, será usada a quantidade de vértices do grafo.
        limite_melhora (int): Caso o algoritmo faça essa quantidade de iterações em sequência e não haja uma mudança
                              na quantidade de cores da solução calculada o algoritmo para a execução.
    
        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
        para acessá-la use grafo.vs["cor"]
        """

        if isinstance(grafo, igraph.Graph) is False:
            raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph.")

        if cores_max is None:
            cores_max = grafo.vcount()
        else:
            if isinstance(cores_max, int) is False:
                raise("O parâmetro cores_max deve ser um int.") 

        def criar_solucao_inicial(grafo):
            """
            Função usada para criar uma solução inicial caso essa não seja passada na chamada da função TabuCol.
            Por ser um algoritmo que trabalha no espaço de soluções impróprias, a solução gerada aqui é totalmente
            feita de forma aleatória.
            """
            for vertice in range(grafo.vcount()):
                cor_aleatoria = random.choice(list(range(cores_max)))
                grafo.vs[vertice]["cor"] = cor_aleatoria
            return grafo
        
        if solucao_inicial is None:
            grafo = criar_solucao_inicial(grafo)
        else:
            if isinstance(solucao_inicial, list) is False:
                raise Exception("A solução inicial passada deve estar no formato de uma lista de inteiros com tamanho igual à quantidade de vértices do grafo.")
            if len(solucao_inicial) != grafo.vcount():
                raise Exception("O tamanho da lista de solução inicial deve ser igual à quantidade de vértices do grafo.")
            if all([isinstance(cor, int) for cor in solucao_inicial]) is False:
                raise Exception("Todos os elementos da solução inicial passada devem ser inteiros.")
            if max(solucao_inicial) > grafo.vcount():
                raise Exception("Na solução inicial passada não deve ter um inteiro maior que a quantidade de vértices do grafo.")
            cores_max = len(set(solucao_inicial))
            grafo.vs["cor"] = solucao_inicial

        lista_cores = list(range(cores_max))

        lista_tabu = np.zeros((grafo.vcount(), len(lista_cores)))

        def cria_lista_auxiliar(grafo):
            """
            Função que cria e atualiza a lista auxiliar usada no algoritmo de Coloração Tabu.
            Essa lista mantém a referência de quantos vértices de uma cor X são vizinhos de um vértice Y.
            """
            lista_auxiliar = np.zeros((grafo.vcount(), len(lista_cores)))
            lista_arestas = grafo.get_edgelist()
            for v_1, v_2 in lista_arestas:
                lista_auxiliar[v_1][grafo.vs[v_2]["cor"]] += 1
                lista_auxiliar[v_2][grafo.vs[v_1]["cor"]] += 1
            return lista_auxiliar
        lista_auxiliar = cria_lista_auxiliar(grafo)

        def cria_lista_colisoes(grafo):
            """
            Função que devolve uma lista com as colisões no grafo. Cada elemento da lista é uma 
            tupla com a aresta causadora da colisão.
            """
            lista_arestas = grafo.get_edgelist()
            colisoes = []
            for v_1, v_2 in lista_arestas:
                if grafo.vs[v_1]["cor"]==grafo.vs[v_2]["cor"]:
                    colisoes.append((v_1,v_2))
            return colisoes        
        lista_colisoes = cria_lista_colisoes(grafo)

        def movimento(grafo, lista_cores, lista_tabu, lista_auxiliar, lista_colisoes, tabu, iteracao):
            """
            Função que realiza um movimento de exploração dentro do algoritmo de Coloração Tabu.
            A função envolve selecionar um vértice para explorar soluções vizinhas relacionadas à troca de cor desse vértice,
            calcular o custo de cada movimento e verificar qual o próximo movimento.
            """
            if not lista_colisoes:
                vertice_selecionado = random.choice(list(range(grafo.vcount())))
            else:
                vertice_selecionado = random.choice(list(random.choice(lista_colisoes)))
            cor_inicial = grafo.vs[vertice_selecionado]["cor"]

            melhor_colisoes = len(lista_colisoes)
            cor_movimento = cor_inicial
            for cor in lista_cores:
                if cor != cor_inicial and lista_tabu[vertice_selecionado][cor] <= iteracao:
                    grafo.vs[vertice_selecionado]["cor"] = cor
                    colisoes = len(lista_colisoes) + lista_auxiliar[vertice_selecionado][cor] - lista_auxiliar[vertice_selecionado][cor_inicial]
                    if colisoes <= melhor_colisoes:
                        melhor_colisoes = colisoes
                        cor_movimento = cor
            if cor_movimento == cor_inicial:
                cor_movimento = random.choice(lista_cores)
            lista_tabu[vertice_selecionado][cor_inicial] = tabu + iteracao
            grafo.vs[vertice_selecionado]["cor"] = cor_movimento
            return grafo, lista_tabu

        iteracoes = 1
        melhor_coloracao = grafo.vcount()
        cores_atual = melhor_coloracao
        melhor_grafo = grafo
        cores_anterior = -1
        contador_iteracoes_iguais = 0
        if isinstance(iteracoes_min, int) is False:
            raise("O número de iterações mínimo deve ser um inteiro.")
        while(len(lista_colisoes) > 0) or (iteracoes < iteracoes_min):
            if iteracoes > iteracoes_max:
                break
            if cores_anterior == cores_atual:
                contador_iteracoes_iguais = contador_iteracoes_iguais + 1
                if contador_iteracoes_iguais == iteracoes_s_mudanca:
                    break
            else: 
                contador_iteracoes_iguais = 0
            grafo, lista_tabu = movimento(grafo, lista_cores, lista_tabu, lista_auxiliar, lista_colisoes, tabu, iteracoes)
            iteracoes += 1
            lista_colisoes = cria_lista_colisoes(grafo)
            lista_auxiliar = cria_lista_auxiliar(grafo)
            cores_anterior = cores_atual
            cores_atual = len(set(grafo.vs["cor"]))
            if cores_atual < melhor_coloracao and len(lista_colisoes) == 0:
                melhor_coloracao = cores_atual
                melhor_grafo = grafo

        if len(cria_lista_colisoes(melhor_grafo)) > 0:
            print("Não foi possível encontrar solução viável com os parâmetros passados.")      

        return melhor_grafo

    def hill_climbing(grafo, divisao = 0.75, iteracoes_max=50, iteracoes_s_melhora = 10):
        """
        Função usada para devolver uma coloração do grafo passado como parâmetro usando o algoritmo 
        Hill Climbing, algoritmos que trabalha sobre o espaço de soluções viáveis.
        Esse algoritmo divide as cores de uma solução inicial em dois grupos e tenta encontrar 
        vértices de um desses dois grupos que possa ser colorido com alguma das cores
        do primeiro grupo sem perder a viabilidade da solução. O algoritmo também tira proveito do algoritmo
        guloso para aumentar a região de exploração sem aumentar a quantidade de cores usadas a cada iteração.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        divisao_inicial (float): Número entre 0 e 1 que indica qual a divisão de cores inicial que 
        será realizada. Exemplo, 0.75 indica que o algoritmo tentará tranferir os vértices de 1/4 das cores
        existentes.
        max_iteracoes (int): Critério de parada que define número máximo de iterações que o algoritmo realiza

        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
        para acessá-la use grafo.vs["cor"]
        """

        def cria_tabela_viabilidade(grafo, qtd_cores, qtd_vertices):
            """
            Função que cria a tabela de viabilidade que indica se um determinado vértice tem ou 
            não vizinhos em uma cor. Devolve a tabela de viabilidade calculada onde as linhas representam
            os vértices e as colunas representam as cores. Se um vértice possui vizinhos em uma cor então 
            o valor na posição referente a essa combinação é 1, caso não é 0.
            """
            tabela_viabilidade = np.zeros((grafo.vcount(), qtd_cores))
            lista_arestas = grafo.get_edgelist()
            for vertice_1 in range(qtd_vertices):
                for vertice_2 in range(qtd_vertices):
                    if tabela_viabilidade[vertice_1][grafo.vs[vertice_2]["cor"]] == 0:
                        if (vertice_1,vertice_2) in lista_arestas or (vertice_2,vertice_1) in lista_arestas:
                            tabela_viabilidade[vertice_1][grafo.vs[vertice_2]["cor"]] = 1
            return tabela_viabilidade

        def divide_cores(qtd_cores, divisao):
            """
            Função que divide aleatoriamente as cores usadas durante a iteração do grafo em dois
            grupos visando identificar possíveis cores sendo usadas sem utilidade. Retorna os 
            dois grupos de cores em duas listas.
            """
            cores_rand = random.sample(list(range(qtd_cores)), qtd_cores)
            grupo_cores_original = cores_rand[:math.floor(qtd_cores*divisao)]
            grupo_cores_transferir = cores_rand[math.floor(qtd_cores*divisao):]
            return grupo_cores_original, grupo_cores_transferir

        def transferencias(grafo, tabela_viabilidade):
            """
            Função que avalia se existem transferências de vértices coloridos com cores do grupo 2
            que possam ser coloridos com cores do grupo 1 sem fazer a solução se tornar inviável.
            Além de avaliar essa função também realiza essas transferências.
            """
            for vertice in range(qtd_vertices):
                if grafo.vs[vertice]["cor"] in grupo_cores_2:
                    for cor in grupo_cores_1:
                        if tabela_viabilidade[vertice][cor] == 0:
                            grafo.vs[vertice]["cor"] = cor
                            vizinhanca = grafo.neighbors(vertice)
                            for vizinho in vizinhanca:
                                tabela_viabilidade[vizinho][cor] = 1
            return grafo, tabela_viabilidade
        
        def ordem_prox_iteracao(grafo, qtd_vertices):
            """
            Função que recebe o grafo da iteração atual e devolve uma lista com uma ordem dos vértices para
            ser usada na construção da solução inicial da próxima iteração. Essa construção é necessária
            pois o algoritmo aqui implementado usa o algoritmo guloso como heurística auxiliar de exploração.
            A construção dessa ordem é feita com base num teorema que garante que se a ordem passada considera
            cada cor um turno, não há como a solução devolvida ter mais cores do que a inicialmente considerada
            na hora da construção da ordem. 
            """
            cores = grafo.vs["cor"]
            vertices = list(range(qtd_vertices))
            vertices_coloridos = zip(cores, vertices)
            vertices_coloridos_ordenados = sorted(vertices_coloridos)
            ordem = [vertice for _, vertice in vertices_coloridos_ordenados]
            return ordem

        iteracao = 0
        ordem_guloso = None
        qtd_vertices = grafo.vcount()
        qtd_cores = 0
        contador_iteracoes_iguais = 0
        while iteracao <= iteracoes_max:
            cores_anterior = qtd_cores
            grafo_sol_inicial = Gulosos.guloso(grafo, ordem_guloso)
            qtd_cores = len(set(grafo_sol_inicial.vs["cor"]))
            if cores_anterior == qtd_cores:
                contador_iteracoes_iguais = contador_iteracoes_iguais + 1
                if contador_iteracoes_iguais == iteracoes_s_melhora:
                    print(f"Algoritmo não apresenta melhora de resultado há {iteracoes_s_melhora} iterações")
                    break
            else: 
                contador_iteracoes_iguais = 0
            iteracao = iteracao + 1
            tabela_viabilidade = cria_tabela_viabilidade(grafo, qtd_cores, qtd_vertices)
            grupo_cores_1, grupo_cores_2 = divide_cores(qtd_cores, divisao)
            grafo, tabela_viabilidade = transferencias(grafo, tabela_viabilidade)
            ordem_guloso = ordem_prox_iteracao(grafo, qtd_vertices)

        return grafo

    def evolucionario(grafo, pop_n = 20, iteracoes_tuning = 20):
        """
        Função usada para devolver uma coloração do grafo passado como parâmetro usando o algoritmo 
        Híbrido Evolucionário (HE), algoritmos que trabalha sobre o espaço de soluções inviáveis.
        O algoritmo recebe em sua entrada um grafo e devolve a melhor solução viável encontrada durante a exploração.
        Caso nenhuma solução viável seja encontrada é retornada uma mensagem de erro informando isso.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph

        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
        para acessá-la use grafo.vs["cor"]
        """

        pass
 
    def colonia_formigas():
        pass
        


        
