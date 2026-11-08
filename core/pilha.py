class No:
    """Nó para a lista encadeada."""
    def __init__(self, item=None):
        self.item = item
        self.proximo = None


class PilhaSentinela:
    def __init__(self):
        # O nó sentinela fica no início. 
        # O topo da pilha é sempre o 'proximo' do sentinela.
        self.sentinela = No()
        self.tam = 0

    def esta_vazia(self):
        # A pilha só está vazia se o sentinela não aponta para ninguém
        return self.sentinela.proximo is None

    def empilhar(self, item):
        """Insere no topo (início da lista) em O(1)."""
        novo_no = No(item)
        
        # O novo nó aponta para o que era o topo anterior
        novo_no.proximo = self.sentinela.proximo
        
        # O sentinela aponta para o novo nó (novo topo)
        self.sentinela.proximo = novo_no
        
        self.tam += 1

    def desempilhar(self):
        """Remove do topo em O(1)."""
        if self.esta_vazia():
            return None
        
        # O nó a ser removido é o topo atual
        no_remover = self.sentinela.proximo
        item = no_remover.item
        
        # O sentinela pula o nó removido e aponta para o próximo
        self.sentinela.proximo = no_remover.proximo
        
        self.tam -= 1
        del no_remover  # Libera a memória
        
        return item

    def topo(self):
        """Retorna o item do topo sem remover."""
        if self.esta_vazia():
            return None
        return self.sentinela.proximo.item

    def __len__(self):
        return self.tam

    def __str__(self):
        if self.esta_vazia():
            return "[ Vazia ]"
        
        elementos = []
        atual = self.sentinela.proximo
        while atual is not None:
            elementos.append(str(atual.item))
            atual = atual.proximo
            
        return "Topo -> [" + ", ".join(elementos) + "]"


# ==========================================
# TESTES
# ==========================================
if __name__ == "__main__":
    print("Testando Pilha com Sentinela")
    p = PilhaSentinela()
    
    print(p) # [ Vazia ]
    
    p.empilhar(10)
    p.empilhar(20)
    p.empilhar(30)
    
    print(p) # Topo -> [30, 20, 10]
    print(f"Tamanho: {len(p)}")
    print(f"Topo atual: {p.topo()}")
    
    print(f"Desempilhado: {p.desempilhar()}") # 30
    print(p) # Topo -> [20, 10]
    
    p.desempilhar()
    p.desempilhar()
    
    print(f"Desempilhado de pilha vazia: {p.desempilhar()}") # None
    print(p) # [ Vazia ]