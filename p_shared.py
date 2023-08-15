class PSharePredictor:
    def __init__(self, bits_to_index, local_history_size):
        self.bits_to_index = bits_to_index  # num. bits a indexar
        self.size_of_history_table = 2**bits_to_index  # tamaño de buffer (lista simple)
        self.history_table = [0 for i in range(self.size_of_history_table)]  # inicialización de buffer en 00's
        
        self.local_history_size = local_history_size  # tamaño reg historia local
        self.pattern_table = [0 for i in range(2**self.local_history_size)]  # inicialización tabla patrones 
        
        self.total_predictions = 0  # predicciones totales
        self.total_taken_pred_taken = 0  # tomados bien predecidos
        self.total_taken_pred_not_taken = 0  # tomados mal predecidos
        self.total_not_taken_pred_taken = 0  # no tomados mal predecidos
        self.total_not_taken_pred_not_taken = 0  # no tomados bien predecidos

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tP-Shared")
        print("\tEntradas en el History Table:\t\t\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia local:\t\t\t\t\t"+str(self.local_history_size))
        print("\tEntradas en el Pattern Table \t\t\t\t\t"+str(2**self.local_history_size))

    # Muestra resultados
    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    # Calcula si predicción fue correcta o no (usado para actualizar stats)
    def predict(self, PC):
        # indexación en history table
        index = int(PC) % self.size_of_history_table  # calcula 'n' bits LSB de PC
        pseudo_shift_reg = self.history_table[index] % 2**self.local_history_size  # shift reg de history table de 'local_hist_size' bits
        
        # indexación en pattern table
        pattern_table_entry = self.pattern_table[pseudo_shift_reg]  # Predicción: cont. 2 bits de pattern table
        if pattern_table_entry in [0,1]: # if predicción == 00 or 01: no tomado
            return "N"
        else:                           # if predicción == 10 or 11: tomado
            return "T"

    # algoritmo de predicción: Actualiza predicción de pattern table y registro actual de historia local 
    def update(self, PC, result, prediction):
        index = int(PC) % self.size_of_history_table  
        pseudo_shift_reg = self.history_table[index] % 2**self.local_history_size 
        pattern_table_entry = self.pattern_table[pseudo_shift_reg]

        # Actualiza predicción de pattern table (contador) y registro de history table
        if pattern_table_entry == 0 and result == "N":
            updated_pattern_table_entry = pattern_table_entry
            updated_pseudo_shift_reg = pseudo_shift_reg << 1       # shift reg left with 0

        elif pattern_table_entry != 0 and result == "N":
            updated_pattern_table_entry = pattern_table_entry - 1
            updated_pseudo_shift_reg = pseudo_shift_reg << 1       # shift reg left with 0

        elif pattern_table_entry == 3 and result == "T":
            updated_pattern_table_entry = pattern_table_entry
            updated_pseudo_shift_reg = (pseudo_shift_reg << 1) + 1     # shift reg left with 1

        else:  # se toma y contador = 10
            updated_pattern_table_entry = pattern_table_entry + 1
            updated_pseudo_shift_reg = (pseudo_shift_reg << 1) + 1       # shift reg left with 1
            
        # Guarda predicción actualizada de índice actual y historia global
        self.pattern_table[pseudo_shift_reg] = updated_pattern_table_entry
        self.history_table[index] = updated_pseudo_shift_reg
    

        # Update stats según valor de retorno de predict()
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
