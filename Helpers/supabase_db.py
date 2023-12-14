"""
Classes de Conexão e CRUD para Supabase
"""

import os

from dotenv import load_dotenv
from loguru import logger
from supabase import Client, create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")


def supabase_conn(url, key):
    conn: Client = create_client(url, key)
    return conn


class CandidatoDB:
    """Desc Candidato"""

    def __init__(self) -> None:
        pass

    def insert_candidato(
        self,
        cpf: str,
        nome: str,
        email: str,
        passwd: str,
        skills: str = None,
        area: str = None,
        descricao: str = None,
        cidade: str = None,
        uf: str = None,
    ) -> None:
        """Este método insere um novo candidato cadastrado na hashtable direto
        para o banco de dados."""
        data = (
            supabase_conn(url, key)
            .table("candidato")
            .insert(
                {
                    "cpf": f"{cpf}",
                    "nome": f"{nome}",
                    "email": f"{email}",
                    "senha": f"{passwd}",
                    "skills": f"{skills}",
                    "area": f"{area}",
                    "descricao": f"{descricao}",
                    "cidade": f"{cidade}",
                    "uf": f"{uf}",
                }
            )
            .execute()
        )
        assert len(data.data) > 0
        logger.info(f"Candidato: {cpf} {nome} — inserido no Banco de Dados!")

    def delete_candidato(self, cpf: str) -> None:
        """Desc"""
        data = (
            supabase_conn(url, key)
            .table("candidato")
            .delete()
            .eq("cpf", f"{cpf}")
            .execute()
        )

        return logger.info(f"Candidato deletado: {cpf}")

    def get_all_candidatos(self) -> list:
        """Retorna todos os Candidatos da tabela Candidato"""
        data, count = supabase_conn(url, key).table("candidato").select("*").execute()
        # Assert we pulled real data.
        # assert len(data.data) > 0
        logger.info("Retornando todos registros da tabela Candidato")
        return data[1]

    def get_candidato_passwrd(self, cpf: int) -> str:
        """Retorna a senha de determinado Candidato"""
        data, count = (
            supabase_conn(url, key)
            .table("candidato")
            .select("senha")
            .limit(1)
            .eq("cpf", f"{cpf}")
            .execute()
        )
        logger.info(f"Senha informada para o Candidato: {cpf}")
        # Retorna a senha em str
        return data[1][0]["senha"]


class RecrutadorDB:
    """Desc Recrutador"""

    def __init__(self) -> None:
        pass

    def insert_recrutador(
        self, cpf: str, nome: str, empresa: str, email: str, passwd: str
    ) -> None:
        """Este método insere um novo recrutador cadastrado na hashtable direto
        para o banco de dados."""
        data = (
            supabase_conn(url, key)
            .table("recrutador")
            .insert(
                {
                    "cpf": f"{cpf}",
                    "nome": f"{nome}",
                    "empresa": f"{empresa}",
                    "email": f"{email}",
                    "senha": f"{passwd}",
                }
            )
            .execute()
        )
        assert len(data.data) > 0
        logger.info(f"Recrutador: {cpf} {nome} — inserido no Banco de Dados!")

    def delete_recrutador(self, cpf: str) -> None:
        """Deleta um recrutador específico usando o cpf como chave"""
        data = (
            supabase_conn(url, key)
            .table("recrutador")
            .delete()
            .eq("cpf", f"{cpf}")
            .execute()
        )
        return logger.info(f"Recrutador deletado: {cpf}")

    def get_all_recrutadores(self) -> list:
        """Retorna todos os Recrutadores da tabela Recrutador"""
        data, count = supabase_conn(url, key).table("recrutador").select("*").execute()
        # Assert we pulled real data.
        # assert len(data.data) > 0
        logger.info("Retornando todos registros da tabela Recrutadores")
        return data[1]

    def get_recrutador_passwrd(self, cpf: int) -> str:
        """Retorna a senha de determinado Recrutador"""
        data, count = (
            supabase_conn(url, key)
            .table("recrutador")
            .select("senha")
            .limit(1)
            .eq("cpf", f"{cpf}")
            .execute()
        )
        logger.info(f"Senha informada para o Recrutador: {cpf}")
        # Retorna a senha em str
        return data[1][0]["senha"]


class VagaDB():
    """Desc Vaga"""

    def __init__(self) -> None:
        pass

    def insert_vaga(
        self,
        id_vaga: int,
        nome: str,
        id_recrutador: str,
        area: str,
        descricao: str,
        quantidade: int,
        nome_empresa: str,
        salario: float,
        requisito: str,
    ) -> None:
        """Este método insere uma nova vaga cadastrada na lista direto
        para o banco de dados."""
        data = (
            supabase_conn(url, key)
            .table("vaga")
            .insert(
                {
                    "id_vaga": f"{id_vaga}",
                    "nome": f"{nome}",
                    "id_recrutador": f"{id_recrutador}",
                    "area": f"{area}",
                    "descricao": f"{descricao}",
                    "quantidade": f"{quantidade}",
                    "nome_empresa": f"{nome_empresa}",
                    "salario": f"{salario}",
                    "requisito": f"{requisito}"
                }
            )
            .execute()
        )
        assert len(data.data) > 0
        logger.info(f"Vaga: {id_vaga} — {nome}. Cadastrada por: {id_recrutador}")

    def delete_vaga(self, id_vaga: int) -> str:
        """Deleta uma vaga específica usando o id_vaga como chave"""
        data = (
            supabase_conn(url, key)
            .table("vaga")
            .delete()
            .eq("id_vaga", f"{id_vaga}")
            .execute()
        )
        return logger.info(f"Vaga deletada: {id_vaga}")

    def get_vagas_recrutador(self, cpf: str) -> list:
        """Retorna as vagas cadastradas por determinado Recrutador"""
        data, count = (
            supabase_conn(url, key)
            .table("vaga")
            .select("*")
            .eq("id_recrutador", f"{cpf}")
            .execute()
        )
        logger.info(f"Retornando vagas cadastradas pelo Recrutador: {cpf}\n")
        # Retornando as vagas em uma lista de dicionários
        return data[1]

    def get_all_vagas(self) -> dict:
        """Retorna todas as Vagas da tabela Vaga"""
        data, count = supabase_conn(url, key).table("vaga").select("*").execute()
        # Assert we pulled real data.
        # assert len(data.data) > 0
        logger.info("Retornando todos registros da tabela Vaga")
        # Retorna todos os registros da tabela vaga em um dict
        return data[1]


if __name__ == "__main__":

    candidato = CandidatoDB()
    recrutador = RecrutadorDB()
    vaga = VagaDB()

    senha = "6f30ea013fec908628192e919275e6a8b316e5b924afd8b85de6b01c416cc8b9"

    idVaga = os.getpid()
    idRecrut = '75315945682'
    empresa = 'Vagas'
    nomeVaga = "Senior DevOps Engineer"
    areaVaga = "DevOps"
    descVaga = "Experiência com ferramentas de code management, repositórios e CI/CD Pipelines"
    quantidadeVaga = 5
    salarioVaga = 3050.57
    requisitoVaga = "Docker, Kubernetes, IaC"

    # # VALIDANDO MÉTODOS PARA CLASSE CANDIDATO
    # candidato.insert_candidato("22244466688", "Bino", "bino@gmail.com", senha, cidade='Santos', uf='SP')
    # candidato.delete_candidato('22244466688')
    # print(candidato.get_candidato_passwrd("22244466688"))
    # pprint(candidato.get_all_candidatos())

    # VALIDANDO MÉTODOS PARA CLASSE RECRUTADOR
    # recrutador.insert_recrutador('77755533311', 'Zé', 'Youtube', 'defante@yt.com','976fd3649d3175915cf4cfd327bca59ae742de6cc13bb0cf0d70105e52c15762')
    # recrutador.delete_recrutador('77755533311')
    # print(recrutador.get_recrutador_passwrd("77755533311"))
    # print(recrutador.get_all_recrutadores())

    # VALIDANDO MÉTODOS PARA CLASSE VAGA
    # vaga.insert_vaga(
    #     idVaga,
    #     nomeVaga,
    #     idRecrut,
    #     areaVaga,
    #     descVaga,
    #     quantidadeVaga,
    #     empresa,
    #     salarioVaga,
    #     requisitoVaga,
    # )
    # vaga.delete_vaga(30844)
    # print('VAGAS:\n', vaga.get_all_vagas())
    print(vaga.get_vagas_recrutador('99966633311'))