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


    def a_star(self):
        # print(self.mapa,self.inicio,self.objetivo)
        '''agloritmo de busqueda en grafos'''
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        open_set = []
        close_set = {}
        heapq.heappush(open_set, (0, self.inicio))

        g_score = [[float('inf')] * self.columnas for _ in range(self.filas)]
        g_score[self.inicio[1]][self.inicio[0]] = 0 #agrega un 0 a la primera posicion

        f_score = [[float('inf')] * self.columnas for _ in range(self.filas)]
        f_score[self.inicio[1]][self.inicio[0]] = self.heuristic(self.inicio, self.objetivo)


        #1)_______________________buscamos el coste total mas pequeno_________________________#
        while open_set:
            _, pos_actual = heapq.heappop(open_set) #extrae la posicion con menor coste


        #2)_______________________comprobamos si encontro el objetivo_________________________#
            if pos_actual == self.objetivo:
                camino = []
                while pos_actual in close_set:
                    camino.append(pos_actual)
                    pos_actual = close_set[pos_actual]
                camino.append(self.inicio)
                camino.reverse()
                return camino


        #3)_______________________evaluacion de movimientos posibles____________________________#
            for direction in movimientos:
                mov_eval = (pos_actual[0] + direction[0], pos_actual[1] + direction[1])
                #evaluacion si esta dentro de los limites y es un camino

                if 0 <= mov_eval[0] < self.filas and 0 <= mov_eval[1] < self.columnas:

                    if self.mapa[mov_eval[0]][mov_eval[1]] == 0 or self.mapa[mov_eval[0]][mov_eval[1]] == 2:

                        tentative_g_score = g_score[pos_actual[1]][pos_actual[0]] + 1
                        

            #4)________________________actualizacion de la cola de prioridades_______________________#
                        if tentative_g_score < g_score[mov_eval[1]][mov_eval[0]]:
                            close_set[mov_eval] = pos_actual #nos indica de donde viene el movimiento evaluado

                            g_score[mov_eval[1]][mov_eval[0]] = tentative_g_score #+1
                            h_score = self.heuristic(mov_eval, self.objetivo)
                            f_score[mov_eval[1]][mov_eval[0]] = tentative_g_score + h_score #costo total

                            heapq.heappush(open_set, (f_score[mov_eval[1]][mov_eval[0]], mov_eval)) #carga los movimientos despues de la evaluacion
            # print(close_set)                

        return None  # No se encontró una ruta