import requests
import json
import csv

class RiotAPI:
    def __init__(self):
        self.api_key = "RGAPI-75a86f31-c500-49dc-9af4-769a65cabc7d"

    def get_puuid_by_tag_and_game_name(self):
        tag = input("Digite a TAG do invocador: ")
        game_name = input("Digite o nick do invocador: ")
        url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag}?api_key={self.api_key}'
        response = requests.get(url)
        data = response.json()
        return data['puuid']

    def list_maestria(self):
        puuid = input("Digite o PUUID do invocador: ")
        champion_count = input("Digite a quantidade de campeões que deseja listar: ")
        url = f'https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={champion_count}&api_key={self.api_key}'
        response = requests.get(url)
        return response.json()

    def listar_id_partida(self):
        puuid = input("Digite o PUUID do invocador: ")
        count_match = int(input("Digite quantas partidas você deseja: "))
        type_match = ""
        option_type_match = int(input("Deseja filtrar por partidas normais(1) ou partidas ranked(2)?"))

        if option_type_match == 1:
            type_match = "normal"
        elif option_type_match == 2:
            type_match = "ranked"

        url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={type_match}&start=0&count={count_match}&api_key={self.api_key}'
        response = requests.get(url)
        return response.json()

    def obter_detalhes_partida(self, id_partida):
        url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{id_partida}?api_key={self.api_key}'
        response = requests.get(url)
        return response.json()

    def salvar_csv(self, dados, nome_arquivo):
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            escritor = csv.DictWriter(arquivo_csv, fieldnames=dados[0].keys())
            escritor.writeheader()
            escritor.writerows(dados)
        print("Arquivo CSV salvo com sucesso!")
    
    def salvar_json(self, dados, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo_json:
            json.dump(dados, arquivo_json)
        print(f"Arquivo JSON '{nome_arquivo}' salvo com sucesso!")

class analisarPartida:
    def __init__(self):
        print("Está sendo construído!")



def main():
    riot_api = RiotAPI()

    while True:
        print("\nMenu:")
        print("1- Consultar Invocador")
        print("2- Listar Maestria de Campeão")
        print("3- Listar Partidas")
        print("0- Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            puuid = riot_api.get_puuid_by_tag_and_game_name()
            print(f"PUUID: {puuid}")
        elif opcao == "2":
            dados_maestria = riot_api.list_maestria()
            if dados_maestria:
                riot_api.salvar_csv(dados_maestria, 'maestrias.csv')
            else:
                print("Não foi possível obter os dados.")
        elif opcao == "3":
            ids_partidas = riot_api.listar_id_partida()
            salvar = input("Deseja salvar os IDs das partidas em JSON? (S/N): ")
            if salvar.lower() == "s":
                if ids_partidas:
                    riot_api.salvar_csv(ids_partidas, 'partidas.json')
                else:
                    print("Não foi possível obter os IDs das partidas.")

            criar_tabela = input("Deseja criar uma tabela com os dados das partidas? (S/N): ")
            if criar_tabela.lower() == "s":
                if ids_partidas:
                    for id_partida in ids_partidas:
                        dados_partida = riot_api.obter_detalhes_partida(id_partida)
                        if dados_partida:
                            nome_arquivo_json = f'partida_{id_partida}.json'
                            riot_api.salvar_json(dados_partida, nome_arquivo_json)
                        else:
                            print("Não é possível criar a tabela porque os IDs das partidas não foram obtidos.")
        elif opcao == "0":
            print("Obrigado por usar o programa. Tchau!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()

