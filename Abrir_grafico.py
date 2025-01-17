import matplotlib.pyplot as plt
import csv

ARQUIVO = "dados_coletados.csv"

def gerar_graficos():
    tempos = []
    dados_1 = []
    dados_2 = []

    # Ler dados do arquivo CSV
    try:
        with open(ARQUIVO, mode='r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            next(leitor_csv)  # Ignorar o cabeçalho
            
            for linha in leitor_csv:
                tempos.append(float(linha[0]))
                dados_1.append(float(linha[1]))
                dados_2.append(float(linha[2]))

    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # Criar gráficos
    plt.figure(figsize=(12, 6))

    # Gráfico 1: dado_1 x tempo
    plt.subplot(1, 2, 1)
    plt.plot(tempos, dados_1, label="Dado 1", color="blue")
    plt.title("Calorimetro 1")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatura 1")
    plt.grid(True)
    plt.legend()

    # Gráfico 2: dado_2 x tempo
    plt.subplot(1, 2, 2)
    plt.plot(tempos, dados_2, label="Dado 2", color="red")
    plt.title("Calorimetro 2")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatur 2")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    gerar_graficos()
