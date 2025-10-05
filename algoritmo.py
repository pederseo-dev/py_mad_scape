import heapq

class Algoritmo:
    def __init__(self, mapa, inicio, objetivo):
        '''declaracion de las variables'''
        self.mapa = mapa
        self.filas = len(mapa)
        self.columnas = len(mapa[0])
        self.inicio = inicio
        self.objetivo = objetivo

    def heuristic(self, nodo_actual, nodo_final):
        '''Calcula la distancia Manhattan entre dos puntos a y b.'''
        x_ab = abs(nodo_actual[0] - nodo_final[0])
        y_ab = abs(nodo_actual[1] - nodo_final[1])
        return x_ab + y_ab
    
    def es_transitable(self, valor_celda):
        '''Verifica si una celda es transitable (no es pared)'''
        # ✅ CORREGIDO para tu mapa específico
        # 0 = camino, 1 = muro, 2 = spawn players
        # "px" = enemigo, "p1","p2","p3"... = jugadores
        
        if isinstance(valor_celda, int):
            return valor_celda != 1  # Todo menos muros (0, 2, etc.)
        elif isinstance(valor_celda, str):
            # Puede pasar por jugadores (p1, p2...) y posición enemigo (px)
            return True  # Todos los strings son transitables
        return False

    def a_star(self):
        '''algoritmo de busqueda en grafos'''
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        open_set = []
        close_set = {}
        heapq.heappush(open_set, (0, self.inicio))

        g_score = [[float('inf')] * self.columnas for _ in range(self.filas)]
        g_score[self.inicio[1]][self.inicio[0]] = 0

        f_score = [[float('inf')] * self.columnas for _ in range(self.filas)]
        f_score[self.inicio[1]][self.inicio[0]] = self.heuristic(self.inicio, self.objetivo)

        while open_set:
            _, pos_actual = heapq.heappop(open_set)

            if pos_actual == self.objetivo:
                camino = []
                while pos_actual in close_set:
                    camino.append(pos_actual)
                    pos_actual = close_set[pos_actual]
                camino.append(self.inicio)
                camino.reverse()
                return camino

            for direction in movimientos:
                mov_eval = (pos_actual[0] + direction[0], pos_actual[1] + direction[1])
                
                # Validar límites
                if 0 <= mov_eval[0] < self.columnas and 0 <= mov_eval[1] < self.filas:
                    # ✅ CORREGIDO: Usar función es_transitable
                    valor_celda = self.mapa[mov_eval[1]][mov_eval[0]]
                    
                    if self.es_transitable(valor_celda):
                        tentative_g_score = g_score[pos_actual[1]][pos_actual[0]] + 1

                        if tentative_g_score < g_score[mov_eval[1]][mov_eval[0]]:
                            close_set[mov_eval] = pos_actual
                            g_score[mov_eval[1]][mov_eval[0]] = tentative_g_score
                            h_score = self.heuristic(mov_eval, self.objetivo)
                            f_score[mov_eval[1]][mov_eval[0]] = tentative_g_score + h_score
                            heapq.heappush(open_set, (f_score[mov_eval[1]][mov_eval[0]], mov_eval))

        return None