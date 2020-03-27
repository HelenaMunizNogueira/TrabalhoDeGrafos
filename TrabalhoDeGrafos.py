'''
Projeto final de Algoritmos em Grafos - 2019/1
Roteirização de caminhoões para abastecimento de cidades e regiões
Integrantes: Altieres Pereira, Angelo Savioti, Helena Nogueira, Rafaela Custódio
'''
import warnings
import networkx as nx
import matplotlib.pyplot as plt
import copy
from collections import defaultdict 
import argparse
import time

class Grafo:
	def __init__(self, _clusters, _todosVertices):
		self.vertices = defaultdict(list) #Vertices que pertencem à lista de clusters percorridos do veículo
		self.matrizDistancias = None
		self.clustersAExplorar = [] #Clusters que estão na lista de "clusters percorridos" do veículo
		self.arestas = []
		self.arestasDicionario = defaultdict(list)
		self.caminhoEuler = []
		self.caminhoHamiltoniano = []
		self.montaVertices(_todosVertices)

	def adicionarVertice(self, _vertice):
		self.vertices[_vertice.indice].append(_vertice)

	def adicionarAresta(self, _vertice1, _vertice2, _distancia):
		self.arestas.append([_vertice1, _vertice2, _distancia])

	def montaVertices(self, _listaVertices):
		self.adicionarVertice(_listaVertices[0]) #Adiciona o primeiro vértice, aquele que não pertence a nenhum cluster
		for i in range(len(_listaVertices)):
			self.adicionarVertice(_listaVertices[i])

	def criarMatrizAdj(self):
		self.matrizDistancias = MatrizAdj(len(self.vertices)+1)
		for i, keyI in enumerate(self.vertices):
			for j, keyJ in enumerate(self.vertices):
				if((self.vertices[keyI][0].cluster == None and self.vertices[keyJ][0].cluster in self.clustersAExplorar) or (self.vertices[keyJ][0].cluster == None and self.vertices[keyI][0].cluster in self.clustersAExplorar) or (self.vertices[keyI][0].cluster != self.vertices[keyJ][0].cluster
						and self.vertices[keyI][0].cluster in self.clustersAExplorar and self.vertices[keyJ][0].cluster in self.clustersAExplorar and keyI != keyJ)):
					'''
					Verifica se o cluster está na lista de clusters que serão explorados pelo veículo e o vertice u e v não estão no mesmo cluster
					'''
					distancia = self.vertices[keyI][0].calcularDistancia(self.vertices[keyJ][0])
					self.matrizDistancias.adicionarValor(keyI, keyJ, distancia)
					self.adicionarAresta(keyI, keyJ, distancia)

	def duplicarArestas(self):
		arestasAux = []
		for aresta in self.arestas:
			arestasAux.append([aresta[1], aresta[0], aresta[2]])
		for aresta in arestasAux:
			self.arestas.append([aresta[0], aresta[1], aresta[2]])

	def adicionarArestasDicionario(self, _u, _v): 
		self.arestasDicionario[_u].append(_v)
		self.arestasDicionario[_v].append(_u)

	def removerArestaDicionario(self, _u, _v): 
		for index, key in enumerate(self.arestasDicionario[_u]): 
			if key == _v: 
				self.arestasDicionario[_u].pop(index)
				break
		for index, key in enumerate(self.arestasDicionario[_v]): 
			if key == _u: 
				self.arestasDicionario[_v].pop(index)
				break

	def plotarGrafo(self, _arestas, _listaVerticesBase = None, _arquivoImg = None, exibirImagem = None):
		G=nx.Graph(strict=False)
		if(_listaVerticesBase == None):
			_listaVerticesBase = self.vertices

		if(len(_arestas[0]) == 4):
			for u, v, weight, cor  in _arestas:
				#Imprime o grafo com as informações v/c na imagem, onde o 'v' é o indice do vertice e 'c' o indice do cluster
				if(_listaVerticesBase[u][0].cluster == None):
					G.add_edge(str(_listaVerticesBase[u][0].indice)+"/X", str(_listaVerticesBase[v][0].indice)+"/"+str(_listaVerticesBase[v][0].cluster.indice), color=cor, subtitle=round(weight,2))
				elif(_listaVerticesBase[v][0].cluster == None):
					G.add_edge(str(_listaVerticesBase[u][0].indice)+"/"+str(_listaVerticesBase[u][0].cluster.indice), str(_listaVerticesBase[v][0].indice)+"/X", color=cor, subtitle=round(weight,2))
				else:#Caso onde o cluster é nulo
					G.add_edge(str(_listaVerticesBase[u][0].indice)+"/"+str(_listaVerticesBase[u][0].cluster.indice), str(_listaVerticesBase[v][0].indice)+"/"+str(_listaVerticesBase[v][0].cluster.indice), color=cor, subtitle=round(weight,2))
		else:
			for u, v, weight, cor  in _arestas:
				#Imprime o grafo com as informações v/c na imagem, onde o 'v' é o indice do vertice e 'c' o indice do cluster
				if(_listaVerticesBase[u][0].cluster == None):
					G.add_edge(str(_listaVerticesBase[u][0].indice)+"/X", str(_listaVerticesBase[v][0].indice)+"/"+str(_listaVerticesBase[v][0].cluster.indice))
				elif(_listaVerticesBase[v][0].cluster == None):
					G.add_edge(str(_listaVerticesBase[u][0].indice)+"/"+str(_listaVerticesBase[u][0].cluster.indice), str(_listaVerticesBase[v][0].indice)+"/X")
				else:#Caso onde o cluster é nulo
					G.add_edge(str(_listaVerticesBase[u][0].indice)+"/"+str(_listaVerticesBase[u][0].cluster.indice), str(_listaVerticesBase[v][0].indice)+"/"+str(_listaVerticesBase[v][0].cluster.indice))

		edges = G.edges()
		colors = [G[u][v]['color'] for u,v in edges]
		pos=nx.circular_layout(G)
		edge_labels = nx.get_edge_attributes(G, 'subtitle')
		nx.draw(G, pos, with_labels=True, edge_color=colors)
		nx.draw_networkx_edge_labels(G,pos, with_labels=True, edge_labels=edge_labels, font_size=8)
		if(_arquivoImg != None):
			plt.savefig(_arquivoImg, dpi=199)

		if(exibirImagem):
			plt.show()

class MatrizAdj:
	def __init__(self, _n):
		self.n = _n
		self.matriz = []
		for i in range(_n):
			self.matriz.append([])
			for j in range(_n):
				self.matriz[i].append(0)

	def adicionarValor(self, _x, _y, _valor):
		self.matriz[_x][_y] = _valor

	def getValor(self, _x, _y):
		return self.matriz[_x][_y]

class TSPMetrico:
	def __init__(self, _grafo, _veiculo):
		self.grafo = _grafo
		self.distanciaTotal = 0

		for i in range(len(_veiculo.clustersASeremPercorridos)):
			self.grafo.clustersAExplorar.append(_veiculo.clustersASeremPercorridos[i]) # Uma lista de clusters a explorar é preenchido no grafo, as arestas serão formadas apenas por vértices que pertencem aos clusters dessa lista

		self.grafo.criarMatrizAdj()
		self.AGMKruskal()
		self.grafo.duplicarArestas()

		for aresta in self.grafo.arestas:
			self.grafo.adicionarArestasDicionario(aresta[0], aresta[1]) # Após a agm passamos a representar as arestas em uma dictionary list
		
		self.imprimirCaminhoEuler()
		self.criarCaminhoHamiltoniano()

		self.atualizarVerticesQueOVeiculoPercorreu(_veiculo, self.grafo.caminhoHamiltoniano) # Busca quais vertices tal veículo passou, é utilizado para a impressão da solução (argumento -sol)

	def encontrar(self, _pai, _i): #Função pra agm
		if _pai[_i] == _i: 
			return _i
		return self.encontrar(_pai, _pai[_i])

	def uniao(self, _pai, _rank, _x, _y): #Une as florestas do kruskal a partir da ordenação
		raizX = self.encontrar(_pai, _x)
		raizY = self.encontrar(_pai, _y) 
		'''
		A immplementação utilizando o conceito de rank visa diminuir a complexidade do algoritmo,
		Faz a raiz da arvore de menor rank se tornar o filho da raiz do de maior rank, caso o rank seja igual define o primeiro como raiz e incrementa o rank dele.
		'''
		if _rank[raizX] < _rank[raizY]: 
			_pai[raizX] = raizY 
		elif _rank[raizX] > _rank[raizY]: 
			_pai[raizY] = raizX 
  
		else: 
			_pai[raizY] = raizX 
			_rank[raizX] += 1

	def AGMKruskal(self):
		arestasAux =[]
		i = 0 
		grafoOrdenado =  sorted(self.grafo.arestas,key=lambda item: item[2]) #Ordena pelas distancias (de u até v)

		pai = defaultdict(list)
		rank = defaultdict(list)
  
		for index, node in enumerate(self.grafo.vertices):
			pai[node] = node 
			rank[node] = 0
		ultimoVisitado = None

		while i < len(grafoOrdenado): 
			u, v, w =  grafoOrdenado[i]
			i = i + 1
			x = self.encontrar(pai, u) 
			y = self.encontrar(pai ,v) 
			if x != y:
				'''
				Verifica se os vertices são aptos a serem adicionados na agm, visando ter apenas um vértice por cluster, as regras definem que o vértice não deve possuir cluster (caso do vértice 1, que nunca pertence a um cluster) ou ser um vértice com cluster não visitado ou então ser um vértice com cluster visitado e o vertice visitado do cluster ser o próprio
				'''
				if((self.grafo.vertices[u][0].cluster == None or self.grafo.vertices[u][0].cluster.verticeVisitado == self.grafo.vertices[u][0] or self.grafo.vertices[u][0].cluster.visitado == False)
					and (self.grafo.vertices[v][0].cluster == None or self.grafo.vertices[v][0].cluster.verticeVisitado == self.grafo.vertices[v][0] or self.grafo.vertices[v][0].cluster.visitado == False)):

					if(self.grafo.vertices[u][0].cluster != None and (self.grafo.vertices[u][0].cluster.verticeVisitado == self.grafo.vertices[u][0] or self.grafo.vertices[u][0].cluster.visitado == False)):
						self.grafo.vertices[u][0].cluster.visitado = True
						self.grafo.vertices[u][0].cluster.verticeVisitado = self.grafo.vertices[u][0]
					if(self.grafo.vertices[v][0].cluster != None and (self.grafo.vertices[v][0].cluster.verticeVisitado == self.grafo.vertices[v][0] or self.grafo.vertices[v][0].cluster.visitado == False)):
						self.grafo.vertices[v][0].cluster.visitado = True
						self.grafo.vertices[v][0].cluster.verticeVisitado = self.grafo.vertices[v][0]

					arestasAux.append([u,v,w]) 
					self.uniao(pai, rank, x, y)
		self.grafo.arestas = arestasAux

	def clonarGrafo(self):
		return copy.copy(self)
		

	def buscaEmProfundidade(self, _v, _visitado): 
		contador = 1
		_visitado[_v] = True
		for i in self.grafo.arestasDicionario[_v]: 
			if _visitado[i] == False: 
				contador = contador + self.buscaEmProfundidade(i, _visitado)          
		return contador


	def proximaArestaEhValida(self, _u, _v):
		if len(self.grafo.arestasDicionario[_u]) == 1: #v é o unico adjacente de u
			return True
		else:
			visitados = [False]*(len(self.grafo.vertices)+1) 
			contador1 = self.buscaEmProfundidade(_u, visitados) 
			self.grafo.removerArestaDicionario(_u, _v) 
			visitados = [False]*(len(self.grafo.vertices)+1) 
			contador2 = self.buscaEmProfundidade(_u, visitados) 
			self.grafo.adicionarArestasDicionario(_u,_v) 

			if(contador1 < contador2):
				return False
			else: #É ponte
				return True
  
  
	def imprimirCaminhoEulerUtil(self, _u): 
		for v in self.grafo.arestasDicionario[_u]: 
			if self.proximaArestaEhValida(_u, v):
				self.grafo.caminhoEuler.append([_u,v, self.grafo.matrizDistancias.getValor(_u, v)])
				self.grafo.removerArestaDicionario(_u, v) 
				self.imprimirCaminhoEulerUtil(v) 
  
	def imprimirCaminhoEuler(self): 
		u = 1
		for i in range(len(self.grafo.vertices)):
			if len(self.grafo.arestasDicionario[i]) %2 != 0:
				u = i
				break
		self.imprimirCaminhoEulerUtil(u)

	def criarCaminhoHamiltoniano(self):
		verticesCaminhoHamiltoniano = []
		primeiroInvalidoExplorado = -1
		ultimoExplorado = -1
		distanciaCaminhoCompleto = 0
		arestasCaminho = []
		for i in range(len(self.grafo.caminhoEuler)):
			'''
			Pra cada aresta(u, v) do caminho euleriano, se nenhum dos dois vertices estiver na lista vertices do caminho hamiltoniano, adiciona na lista de vertices e na de arestas,
			caso apenas o vertice v estiver na lista de vertices no caminho nós adicionamos a aresta com o último vertice válido anterior ao v (não explorado pelo caminho) e o u,
			caso apenas o vertice u estiver na lista de vertices no caminho nós adicionamos a aresta com o último vértice válido anterior a u (não explorado pelo caminho) e u,
			em todos os casos a soma das distancias é atualizada.
			'''
			if(self.grafo.caminhoEuler[i][0] not in verticesCaminhoHamiltoniano and self.grafo.caminhoEuler[i][1] not in verticesCaminhoHamiltoniano):
				arestasCaminho.append([self.grafo.caminhoEuler[i][0], self.grafo.caminhoEuler[i][1], self.grafo.caminhoEuler[i][2]])
				verticesCaminhoHamiltoniano.append(self.grafo.caminhoEuler[i][0])
				verticesCaminhoHamiltoniano.append(self.grafo.caminhoEuler[i][1])
				distanciaCaminhoCompleto = 0
				ultimoExplorado = self.grafo.caminhoEuler[i][1]
				ultimoValidoExplorado = self.grafo.caminhoEuler[i][1]
			elif(self.grafo.caminhoEuler[i][0] not in verticesCaminhoHamiltoniano): # U nao está na lista de vertices já percorridos pelo caminho
				arestasCaminho.append([ultimoValidoExplorado, self.grafo.caminhoEuler[i][0], self.grafo.matrizDistancias.getValor(ultimoValidoExplorado, self.grafo.caminhoEuler[i][0])])

				if(primeiroInvalidoExplorado != -1):
					distanciaCaminhoCompleto += self.grafo.matrizDistancias.getValor(primeiroInvalidoExplorado, ultimoExplorado)
					#Distancia do último valido explorado até o atual tem que ser menor ou igual que o caminho completo (diferença triangular)
					if(self.grafo.matrizDistancias.matriz[ultimoValidoExplorado][self.grafo.caminhoEuler[i][0]] > distanciaCaminhoCompleto):
						print("O grafo não respeita a diferença triangular")

				if(primeiroInvalidoExplorado == -1):
					primeiroInvalidoExplorado = self.grafo.caminhoEuler[i][1]

				ultimoExplorado = self.grafo.caminhoEuler[i][0]
				verticesCaminhoHamiltoniano.append(self.grafo.caminhoEuler[i][0])

				ultimoValidoExplorado = self.grafo.caminhoEuler[i][0]
			elif(self.grafo.caminhoEuler[i][1] not in verticesCaminhoHamiltoniano): # V nao está na lista de vertices já percorridos pelo caminho
				arestasCaminho.append([ultimoValidoExplorado, self.grafo.caminhoEuler[i][1], self.grafo.matrizDistancias.getValor(ultimoValidoExplorado, self.grafo.caminhoEuler[i][1])])

				if(primeiroInvalidoExplorado != -1):
					distanciaCaminhoCompleto += self.grafo.matrizDistancias.getValor(ultimoExplorado, self.grafo.caminhoEuler[i][0])
					#Distancia do último valido explorado até o atual tem que ser menor ou igual que o caminho completo (diferença triangular)
					if(self.grafo.matrizDistancias.getValor(ultimoValidoExplorado, self.grafo.caminhoEuler[i][1]) > distanciaCaminhoCompleto):
						print("O grafo não respeita a diferença triangular")

				ultimoExplorado = self.grafo.caminhoEuler[i][1]
				verticesCaminhoHamiltoniano.append(self.grafo.caminhoEuler[i][1])

				ultimoValidoExplorado = self.grafo.caminhoEuler[i][1]
			else:
				distanciaCaminhoCompleto += self.grafo.caminhoEuler[i][2]

		arestasCaminho.append([verticesCaminhoHamiltoniano[len(verticesCaminhoHamiltoniano)-1], verticesCaminhoHamiltoniano[0], self.grafo.matrizDistancias.getValor(verticesCaminhoHamiltoniano[len(verticesCaminhoHamiltoniano)-1], verticesCaminhoHamiltoniano[0])]) # Adiciona uma aresta do último vertice do caminho pro primeiro (a volta pro centro de distribuição)
		distanciaTotal = 0

		for i in range(len(arestasCaminho)):
			distanciaTotal += arestasCaminho[i][2]

		self.distanciaTotal = distanciaTotal
		self.grafo.caminhoHamiltoniano = arestasCaminho

	def atualizarVerticesQueOVeiculoPercorreu(self, _veiculo, _arestas): #Adiciona vertices à lista de vertices percorridos pelo veículo
		for i in range(len(_arestas)):
			if(_arestas[i][0] not in _veiculo.verticesPercorridos):
				_veiculo.verticesPercorridos.append(_arestas[i][0])
			if(_arestas[i][1] not in _veiculo.verticesPercorridos):
				_veiculo.verticesPercorridos.append(_arestas[i][1])


class Vertice: #Classe para armazenar cada Vértice
	def __init__(self, _indice, _lat, _longi):
		self.indice = _indice
		self.lat = _lat
		self.longi = _longi
		self.cluster = None

	def calcularDistancia(self, _vertice2): #Calcula a distância do vértice do objeto atual em comparação a um passado por paramêtro
		auxLat = self.lat - _vertice2.lat
		auxLong = self.longi - _vertice2.longi
		distancia = (auxLat*auxLat)+(auxLong*auxLong)
		distancia = distancia ** (1/2)
		return distancia

class Cluster: #Classe cluster com a lista de vértices que o compõe e um atributo que indica se já foi visitado
	def __init__(self, _indice, _indicesVertices, _demanda, _listaVertices):
		self.indice = _indice
		self.vertices = []
		for indice in _indicesVertices:
			indice = indice
			self.vertices.append(_listaVertices[indice-1])
			_listaVertices[indice-1].cluster = self
		self.demanda = _demanda
		self.visitado = False
		self.verticeVisitado = None #Caso o cluster tenha sido visitado, indica qual foi o vértice em questão (pois só ele será tratado)

class Veiculo: #Veículo com a capacidade atual e restante
	def __init__(self, _indice, _capacidade):
		self.indice = _indice
		self.capacidade = _capacidade
		self.capacidadeRestante = _capacidade
		self.clustersASeremPercorridos = []
		self.verticesPercorridos = []

	def adicionarClusterARota(self, _cluster): #Função que calcula a capacidade restante após passar por um cluster (também altera dados do cluster)
		self.clustersASeremPercorridos.append(_cluster)
		self.capacidadeRestante -= _cluster.demanda #
		_cluster.visitado = True

	def adicionarVerticePercorrido(self, _vertice):
		self.verticesPercorridos.append(_vertice)

def existeClusterNaoExplorado(_clusters):# Percorre todos os clusters, retorna True se existe algum nao visitado
	for x in range(len(_clusters)):
		if not _clusters[x].visitado:
			return True

def gerarCombinacaoViavelClusters(_veiculos, _clusters): #Gera ao menos uma sequência viável de clusters a se passar (heurística)
	_clusters.sort(key=lambda x: x.demanda, reverse = True)
	i = 0
	j = 0
	soma = [0, 0]
	while(existeClusterNaoExplorado(_clusters) and i < len(_clusters)):
		if(_veiculos[j].capacidadeRestante >= _clusters[i].demanda):
			_veiculos[j].adicionarClusterARota(_clusters[i])
			i += 1
			j = 0
		else:
			j += 1
		if(j >= len(_veiculos)):
			j = 0
	for veiculo in _veiculos:
		veiculo.capacidadeRestante = veiculo.capacidade
	for cluster in _clusters:
		cluster.visitado = False

def pegarInformacoesArquivo(_vertices, _clusters, _veiculos, _nomeArquivoEntrada):
	f = open(_nomeArquivoEntrada + ".txt")
	clustersAux = defaultdict(list)
	quantidadeVeiculos = 0
	linha = f.readline().strip()
	lendoAgora = ""
	i = 0
	while(linha != "EOF"):
		if(i == 1):# Linha da quantidade de veículo
			auxVeiculo = linha.split(" : ")
			quantidadeVeiculos = int(auxVeiculo[1])
		if(i == 3):# Linha da capacidade do veículo
			auxCapacidade = linha.split(" : ")
			capacidade = int(auxCapacidade[1])
			for indiceVeiculo in range(1, quantidadeVeiculos+1):
				_veiculos.append(Veiculo(indiceVeiculo, capacidade))
		if(i > 4):
			#Define o que será executado de acordo com o 'titulo' da última seção
			if(linha == "NODE_COORD_SECTION"):
				lendoAgora = "vertices"
			elif(linha == "SET_SECTION"):
				lendoAgora = "clusters"
			elif(linha == "DEMAND_SECTION"):
				lendoAgora = "demandas"
			else:
				aux = ""
				if(lendoAgora == "vertices"):
					verticeDados = linha.split(" ")
					_vertices.append(Vertice(int(verticeDados[0]), int(verticeDados[1]), int(verticeDados[2])))
				elif(lendoAgora == "clusters"):
					clusterDados = linha.split(" ")
					indiceCluster = -1
					listaVertices = []
					for j in range(len(clusterDados)):
						if(j == 0):
							indiceCluster = clusterDados[j]
						elif(clusterDados[j] != "-1"):
							listaVertices.append(int(clusterDados[j]))
					clustersAux[indiceCluster].append(listaVertices) #Armazenamos os dados em uma lista auxiliar pois é mais vantajoso inserir o objeto todo apenas quando tivermos também as demandas de cada cluster
				elif(lendoAgora == "demandas"):
					demandaDados = linha.split(" ")
					indiceCluster = demandaDados[0]
					demandaCluster = int(demandaDados[1])
					clustersAux[indiceCluster].append(demandaCluster)
		i += 1	
		linha = f.readline().strip()
	f.close()
	i = 0
	for index, key in enumerate(clustersAux):
		_clusters.append(Cluster(key, clustersAux[key][0], clustersAux[key][1], _vertices))

def escreverArquivoSaida(_nomeArquivoSaida, _nomeArquivoEntrada, _distanciaTotal, _tempoExecucao): # Função auxiliar para escrever o arquivo de saída
	if(_nomeArquivoSaida != None):
		f = open(_nomeArquivoSaida + ".txt", "a")
		f.write(_nomeArquivoEntrada + " " + str(_distanciaTotal) + " " + str(_tempoExecucao) + "\n")
		f.close()

def limparArquivoSolucao(_nomeArquivoSolucao): # Função auxiliar para limpar o arquivo de solução
	if(_nomeArquivoSolucao != None):
		f = open(_nomeArquivoSolucao + ".txt", "w")
		f.close()

def escreverArquivoSolucao(_nomeArquivoSolucao, _veiculo): # Função auxiliar para escrever o arquivo de solução
	if(_nomeArquivoSolucao != None):
		f = open(_nomeArquivoSolucao + ".txt", "a")
		for i in range(len(_veiculo.verticesPercorridos)):
			f.write(str(_veiculo.verticesPercorridos[i]) + " ")
		f.write("\n")
		f.close()


def tratarArgumentos(): # Interpreta os argumentos e retorna um array com os mesmos
	parser = argparse.ArgumentParser()
	parser.add_argument('-in', action='store', dest='entrada', help="Caminho do arquivo para leitura", required=True)
	parser.add_argument('-out', action='store', dest='saida', help="Caminho do arquivo para escrita")
	parser.add_argument('-sol', action='store', dest='solucao', help="Caminho do arquivo que contem a solução (sequencia de vertices explorados por cada veículo)")
	parser.add_argument('-img', action='store', dest='imagem', help="Caminho para a criação da imagem")
	parser.add_argument('-showImg', dest='showImg', action='store_true', help="Define se também será exibida uma janela plotando o grafo (que dá novas possibilidades ao usuário, como dar zoom na imagem)")
	parser.set_defaults(showImg=False)
	args = parser.parse_args()
	return args

def gerarRotasDemanda(_vertices, _clusters, _veiculos, _cores, _listaArestasGrafoFinal, _nomeArquivoSolucao):
	distanciaTotal = 0
	limparArquivoSolucao(_nomeArquivoSolucao) # Limpa o arquivo de solução, pois não é pra manter os dados da última execução do programa
	for i in range(len(_veiculos)): # Executa o tsp métrico para cada veículo e escreve no arquivo de solução, além disso também soma a distancia total
		grafo = Grafo(_clusters, _vertices)
		tsp = TSPMetrico(grafo, _veiculos[i])
		escreverArquivoSolucao(_nomeArquivoSolucao, _veiculos[i])
		distanciaTotal += tsp.distanciaTotal
		for j in range(len(grafo.caminhoHamiltoniano)): #Adiciona cada aresta do caminho hamiltoniano a lista de arestas do grafo final, que gerará a impressão do arquivo
			grafo.caminhoHamiltoniano[j].append(_cores[i])
			_listaArestasGrafoFinal.append(grafo.caminhoHamiltoniano[j])
	return distanciaTotal

def main():
	warnings.filterwarnings("ignore")
	inicio = time.time()

	args = tratarArgumentos()
	nomeArquivoEntrada = args.entrada
	nomeArquivoSaida = args.saida
	nomeArquivoImagem = args.imagem
	nomeArquivoSolucao = args.solucao
	exibirImagem = args.showImg
	cores = ["#000000", "#00FFFF", "#FF4500", "#000080", "#F5F5DC", "#B22222", "#00FF7F", "#C71585", "#87CEEB", "#00FF00", "#48D1CC", "#696969", "#4682B4", "#808000",
		 "#8B4513", "#D2691E", "#FF00FF", "#E6E6FA", "#F5DEB3", "#D8BFD8", "#7B68EE", "#B0E0E6", "#4B0082", "#8B008B", "#FFD700"]
	vertices = []
	clusters = []
	veiculos = []
	listaArestasGrafoFinal = []
	pegarInformacoesArquivo(vertices, clusters, veiculos, nomeArquivoEntrada)

	gerarCombinacaoViavelClusters(veiculos, copy.copy(clusters))

	distanciaTotal = gerarRotasDemanda(vertices, clusters, veiculos, cores, listaArestasGrafoFinal, nomeArquivoSolucao) #Algoritmo principal

	fim = time.time()

	escreverArquivoSaida(nomeArquivoSaida, nomeArquivoEntrada, distanciaTotal, (fim - inicio))

	printG = Grafo(clusters, vertices)

	printG.plotarGrafo(listaArestasGrafoFinal, printG.vertices, nomeArquivoImagem, exibirImagem)
	return

if __name__ == '__main__':
	main()