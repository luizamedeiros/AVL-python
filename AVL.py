from no import No
from random import randint


class AVL:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor):
        if self.raiz is None:
            self.raiz = No(valor)
        else:
            # criando outra função para lidar com recursividade e deixar o código mais legível
            self._inserir(valor, self.raiz)

    def __repr__(self):
        if self.raiz is None:
            return ''
        content = '\n'  # to hold final string
        cur_nodes = [self.raiz]  # all nodes at current level
        cur_height = self.raiz.altura  # height of nodes at current level
        sep = ' ' * (2 ** (cur_height - 1))  # variable sized separator between elements
        while True:
            cur_height += -1  # decrement current height
            if len(cur_nodes) == 0:
                break
            cur_row = ' '
            next_row = ''
            next_nodes = []

            if all(n is None for n in cur_nodes):
                break

            for n in cur_nodes:

                if n is None:
                    cur_row += '   ' + sep
                    next_row += '   ' + sep
                    next_nodes.extend([None, None])
                    continue

                if n.valor is not None:
                    buf = ' ' * int((5 - len(str(n.valor))) / 2)
                    cur_row += '%s%s%s' % (buf, str(n.valor), buf) + sep
                else:
                    cur_row += ' ' * 5 + sep

                if n.esquerda is not None:
                    next_nodes.append(n.esquerda)
                    next_row += ' /' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

                if n.direita != None:
                    next_nodes.append(n.direita)
                    next_row += '\ ' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

            content += (cur_height * '   ' + cur_row + '\n' + cur_height * '   ' + next_row + '\n')
            cur_nodes = next_nodes
            sep = ' ' * int(len(sep) / 2)  # cut separator size in half
        return content

    def _inserir(self, valor, no_atual):
        if valor < no_atual.valor:
            if no_atual.esquerda is None:
                # ligando o novo nó ao nó de origem
                no_atual.esquerda = No(valor)
                # ligando o elemento filho ao pai
                no_atual.esquerda.pai = no_atual
                # avaliando balanceamento
                self._avalia_insercao(no_atual.esquerda)
            else:
                # caso o nó já tenha elemento esquerdo, vá até ele e tente a inserção lá
                self._inserir(valor, no_atual.esquerda)
        elif valor > no_atual.valor:
            if no_atual.direita is None:
                # ligando o novo nó ao nó original
                no_atual.direita = No(valor)
                # ligando o elemento filho ao pai
                no_atual.direita.pai = no_atual
                # print(f'{no_atual.direita.valor}')
                # avaliando balanceamento
                self._avalia_insercao(no_atual.direita)
            else:
                self._inserir(valor, no_atual.direita)
        else:
            print("Valor já está na árvore!")

    def printa_arvore(self):
        if self.raiz is not None:
            self._printa_arvore(self.raiz)

    def _printa_arvore(self, no_atual):
        if no_atual is not None:
            self._printa_arvore(no_atual.esquerda)
            print(f"{no_atual.valor}, h ={no_atual.altura}")
            self._printa_arvore(no_atual.direita)

    def altura_arvore(self):
        if self.raiz is not None:
            return self._altura_arvore(self.raiz, 0)
        else:
            return 0

    def _altura_arvore(self, no_atual, altura_atual):
        if no_atual is None:
            return altura_atual
        # percorre os nós através do nó esquerdo e direito do nó atual, somando altura conforme "desce"
        altura_esquerda = self._altura_arvore(no_atual.esquerda, altura_atual + 1)
        altura_direita = self._altura_arvore(no_atual.direita, altura_atual + 1)
        # retorna o máximo das alturas
        return max(altura_esquerda, altura_direita)

    def acha_elemento(self, elemento):
        if self.raiz is not None:
            return self._acha_elemento(self.raiz, elemento)
        else:
            return None

    def _acha_elemento(self, no_atual, elemento):
        if no_atual.valor == elemento:
            return no_atual
        elif no_atual.esquerda is not None and no_atual.valor > elemento:
            return self._acha_elemento(no_atual.esquerda, elemento)
        elif no_atual.direita is not None and no_atual.valor < elemento:
            return self._acha_elemento(no_atual.direita, elemento)

    def procura_no(self, elemento):
        if self.raiz is not None:
            return self._procura_no(self.raiz, elemento)
        else:
            return None

    def _procura_no(self, no_atual, elemento):
        if no_atual.valor == elemento:
            return True
        elif no_atual.esquerda is not None and elemento < no_atual.valor:
            self._procura_no(no_atual.esquerda, elemento)
        elif no_atual.direita is not None and elemento > no_atual.valor:
            self._procura_no(no_atual.direita, elemento)

    def exclui_elemento(self, valor):
        return self.exclui_no(self.acha_elemento(valor))

    def exclui_no(self, no):

        if no is None or self.acha_elemento(no.valor) is None:
            print("Elemento não encontrado!")
            return None

        def menor_no(elemento):
            no_atual = elemento
            while no_atual.esquerda is not None:
                no_atual = no_atual.esquerda
            return no_atual

        def numero_de_filhos(n):
            numero_filhos = 0
            if n.esquerda is not None:
                numero_filhos += 1
            if n.direita is not None:
                numero_filhos += 1
            return numero_filhos

        num_filhos = numero_de_filhos(no)
        no_pai = no.pai

        if num_filhos == 0:
            # se o número de filhos do nó for 0, precisamos apenas
            # desfazer a ligação do pai a ele. Assim, ele será "pego pelo
            # coletor de lixo"!.
            if no_pai is not None:
                if no_pai.esquerda == no:
                    no_pai.esquerda = None
                    # se não for o filho esquerdo o nó desejado, por eliminação,
                    # será o direito
                else:
                    no_pai.direita = None
            else:
                self.raiz = None

        elif num_filhos == 1:
            # se o num_filhos for só um, precisamos apenas substituir
            # o nó pai pelo filho.

            # salvando o nó filho correto
            if no.esquerda is not None:
                no_filho = no.esquerda
            else:
                no_filho = no.direita

            # fazendo a substituição para que o pai do nó atual aponte
            # para o filho do nó atual
            if no_pai is not None:
                if no_pai.esquerda == no:
                    no_pai.esquerda = no_filho
                else:
                    no_pai.direita = no_filho
            else:
                self.raiz = no_filho

            # atualizando o pai do "no_filho" para o seu "avô"
            no_filho.pai = no_pai

        elif num_filhos == 2:
            # se o número de filhos for igual a dois,
            # passaremos pelos filhos a procura do menor nó
            # para achar o nó que será utilizado para fazer a substituição

            prox_na_ordem = menor_no(no)

            no.valor = prox_na_ordem.valor

            # apagando o nó que "puxamos para cima"
            self.exclui_no(prox_na_ordem)
            # return para não rodar _avalia_exclusao mais de uma vez
            return

        if no_pai is not None:
            no_pai.altura = 1 + max(self.pega_altura(no_pai.esquerda), self.pega_altura(no_pai.direita))
            self._avalia_exclusao(no_pai)

    def _avalia_insercao(self, no_atual, caminho=[]):
        if no_atual.pai is None:
            return
        caminho = [no_atual] + caminho
        # pegando altura dos filhos
        altura_esquerda = self.pega_altura(no_atual.esquerda)
        altura_direita = self.pega_altura(no_atual.direita)
        # validando se árvore está balançeada
        if altura_esquerda is not None and altura_direita is not None:
            if abs(altura_esquerda - altura_direita) > 1:
                caminho = [no_atual.pai] + caminho
                # z = no_atual, y e x são seus filhos
                self._reequilibra_no(caminho[0], caminho[1], caminho[2])
                return

        nova_altura = 1 + no_atual.altura
        if nova_altura > no_atual.pai.altura:
            no_atual.pai.altura = nova_altura
        self._avalia_insercao(no_atual.pai, caminho)

    def _avalia_exclusao(self, no_atual):
        if no_atual is None:
            return
        altura_esquerda = self.pega_altura(no_atual.esquerda)
        altura_direita = self.pega_altura(no_atual.direita)
        # validando se árvore está balançeada
        if abs(altura_esquerda - altura_direita) > 1:
            # z = no_atual
            y = self.no_filho_maior(no_atual)
            x = self.no_filho_maior(y)
            self._reequilibra_no(no_atual, y, x)

        self._avalia_exclusao(no_atual.pai)

    # para lidar com o caso de "linha reta"
    def _reequilibra_no(self, z, y, x):
        if y == z.esquerda and x == y.esquerda:
            self._rotacao_direita(z)
        elif y == z.esquerda and x == y.direita:
            self._rotaciona_esquerda(y)
            self._rotacao_direita(z)
        elif y == z.direita and x == y.direita:
            self._rotaciona_esquerda(z)
        elif y == z.direita and x == y.esquerda:
            self._rotacao_direita(y)
            self._rotaciona_esquerda(z)
        else:
            print("Erro! Estrutura não reconhecida.")

    def _rotacao_direita(self, z):
        avo = z.pai
        y = z.esquerda
        t3 = y.direita
        y.direita = z
        z.pai = y
        z.esquerda = t3
        # se existir elemento direito a y, reposiciona ele para ser o esquerdo de z.
        if t3 is not None:
            t3.pai = z
        # fazendo ligacao entre antigo pai de z e y.
        y.pai = avo
        # se não houver antigo pai de z, é porque z era a raiz
        # agora, se esse for o caso, Y é raiz.
        if y.pai is None:
            self.raiz = y
        else:
            # ligando y ao antigo pai de z caso esse exista
            if y.pai.esquerda == z:
                y.pai.esquerda = y
            # se z não estava à esquerda, por eliminação, estava à direita.
            else:
                y.pai.direita = y
        z.altura = 1 + max(self.pega_altura(z.esquerda), self.pega_altura(z.direita))
        y.altura = 1 + max(self.pega_altura(y.esquerda), self.pega_altura(y.direita))

    def _rotaciona_esquerda(self, z):
        # sendo o elemento z menor que y, mas pai de y, e t2 o elemento filho esquerdo de y, reposicionaremos.
        # não mexemos em x pois ele não se moverá, apenas trocaremos z, y, e t2 de lugar.
        avo = z.pai
        y = z.direita
        t2 = y.esquerda
        y.esquerda = z
        z.pai = y
        z.direita = t2
        if t2 is not None:
            t2.pai = z
        y.pai = avo
        if y.pai is None:
            self.raiz = y
        else:
            if y.pai.esquerda == z:
                y.pai.esquerda = y
            else:
                y.pai.direita = y
        z.altura = 1 + max(self.pega_altura(z.esquerda), self.pega_altura(z.direita))
        y.altura = 1 + max(self.pega_altura(y.esquerda), self.pega_altura(y.direita))

    def pega_altura(self, no_atual):
        if no_atual is None:
            return
        return no_atual.altura

    def no_filho_maior(self, no_atual):
        esquerda = self.pega_altura(no_atual.esquerda)
        direita = self.pega_altura(no_atual.direita)
        if esquerda > direita:
            return no_atual.esquerda
        else:
            return no_atual.direita

arvore= AVL()
for i in range(10):
    print(f"Inserindo {i}...")
    arvore.inserir(i)
    print(arvore)
