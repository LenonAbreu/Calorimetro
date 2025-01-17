O código a seguir, recebe os dados (tempo, temperatura_1, temperatura_2) os salva em uma lista e exibe dois gráficos em tempo real de temperatura x tempo.
import serial # necessário "instalar py.serial"
import time
import csv
import keyboard  # Biblioteca para capturar teclas, necessário ser instalada "keyboard"
import matplotlib.pyplot as plt # necessário instalar "matplotlib" 

# Configurações da porta serial
PORTA = "COM3"  # Substitua pela sua porta serial
BAUDRATE = 9600
TIMEOUT = 1  # Em segundos
ARQUIVO = "dados_coletados.csv"  # Nome do arquivo para salvar os dados

# Inicialização das variáveis para os dados
tempos = []
temperatura_1 = []
temperatura_2 = []
pausado = False  # Controle de pausa

def atualiza_graficos():
    """Atualiza os dois gráficos na mesma janela."""
    plt.clf()  # Limpa a janela de gráficos

    # Gráfico 1: Temperatura 1 acumulativa
    plt.subplot(1, 2, 1)  # Divisão da janela em 2 linhas, 1 coluna, 1º gráfico
    plt.plot(tempos, temperatura_1, label="Temperatura 1", color="blue")
    plt.title("Calorimetro 1")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Temp 1 (°C)")
    plt.grid(True)
    plt.legend()

    # Gráfico 2: Temperatura 2 acumulativa
    plt.subplot(1, 2, 2)  # 2º gráfico na mesma janela
    plt.plot(tempos, temperatura_2, label="Temperatura 2", color="red")
    plt.title("Calorimetro 2")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Temp 2 (°C)")
    plt.grid(True)
    plt.legend()

    # Ajusta o layout e exibe
    plt.tight_layout()
    plt.pause(0.1)

def coleta_dados_serial():
    """Lê dados da porta serial e atualiza os gráficos."""
    global pausado
    try:
        with serial.Serial(PORTA, BAUDRATE, timeout=TIMEOUT) as ser, open(ARQUIVO, mode='w', newline='') as arquivo_csv:
            print("Conexão serial aberta. Pressione ESPAÇO para pausar/retomar ou ESC para encerrar.")
            
            escritor_csv = csv.writer(arquivo_csv)
            escritor_csv.writerow(["tempo", "temperatura_1", "temperatura_2"])  # Cabeçalho
            
            inicio_tempo = time.time()

            while True:
                # Controle de pausa
                if keyboard.is_pressed("space"):
                    pausado = not pausado  # Alterna entre pausado e retomado
                    if pausado:
                        print("Coleta pausada. Pressione ESPAÇO para retomar.")
                    else:
                        print("Coleta retomada.")
                    time.sleep(0.5)  # Evita múltiplos registros da mesma tecla

                # Verifica se o programa deve ser encerrado
                if keyboard.is_pressed("esc"):
                    print("Coleta encerrada pelo usuário.")
                    break

                # Ignora a coleta de dados se estiver pausado
                if pausado:
                    continue

                linha = ser.readline().decode('utf-8').strip()
                if linha:
                    try:
                        dados = linha.split(",")
                        if len(dados) == 3:
                            # Parse dos dados
                            tempo = float(dados[0])
                            temp1 = float(dados[1])
                            temp2 = float(dados[2])

                            # Adiciona aos dados
                            tempos.append(tempo)
                            temperatura_1.append(temp1)
                            temperatura_2.append(temp2)

                            # Salva no arquivo CSV
                            escritor_csv.writerow([tempo, temp1, temp2])

                            # Atualiza os gráficos
                            atualiza_graficos()

                    except ValueError as e:
                        print(f"Erro ao processar linha: {linha}, erro: {e}")

    except KeyboardInterrupt:
        print("\nInterrupção pelo usuário. Encerrando...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    # Configura o modo interativo do Matplotlib
    plt.ion()
    coleta_dados_serial()

