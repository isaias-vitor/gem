from supabase import create_client
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    def __init__(self):
        # Carregar as variáveis de ambiente
        self.url = getenv('SUPABASE_URL')
        self.key = getenv('SUPABASE_KEY')

        # Verificar se as variáveis foram carregadas corretamente
        if not self.url or not self.key:
            raise ValueError("As credenciais do Supabase não foram encontradas no arquivo .env")

        self.client = create_client(self.url, self.key)
        print(f'Conectado ao Supabase em: {self.url}')

    def userLogin(self, email, senha):
        try:
            response = self.client.table('users').select('*').eq('email', email).eq('senha', senha).execute()
            if not response: return None
            else: return response.data[0]
        except:
            print('Erro ao buscar no banco de dados')

    def saveApprovalPrincipalHymn(self, date, obs, hymn, inst_id, cand_id):
        data = {
            'numero':hymn,
            'usuario_id':cand_id,
            'instrutor_id':inst_id,
            'data':date.isoformat(),
            'observacao': obs
        }
        try:
            response = self.client.table('hinos_vp').insert(data).execute()
        except Exception as e:
            print('Erro ao inserir no banco de dados!')
            print(e)
    
    def saveApprovalAlternativeHymn(self, date, obs, hymn, inst_id, cand_id):
        data = {
            'numero':hymn,
            'usuario_id':cand_id,
            'instrutor_id':inst_id,
            'data':date.isoformat(),
            'observacao': obs
        }
        try:
            response = self.client.table('hinos_va').insert(data).execute()
        except Exception as e:
            print('Erro ao inserir no banco de dados!')
            print(e)

    def cancelApprovalPrincipal(self, hymn, cand_id):
        try:
            response = self.client.table('hinos_vp').delete().eq('numero', hymn).eq('usuario_id', cand_id).execute()
        except Exception as e:
            print('Erro ao remover do banco de dados!')
            print(e)
    
    def cancelApprovalAlternative(self, hymn, cand_id):
        try:
            response = self.client.table('hinos_va').delete().eq('numero', hymn).eq('usuario_id', cand_id).execute()
        except Exception as e:
            print('Erro ao remover do banco de dados!')
            print(e)

    def seekApprovedHymns(self, act_student):

        try:
            hymns = {'principal':[], 'alternative':[]}
            response_principal = self.client.table('hinos_vp').select('*').eq('usuario_id', int(act_student)).execute()
            for hymn in response_principal.data:
                inst = self.client.table('users').select('nome').eq('id', hymn['instrutor_id']).execute()
                inst = inst.data
                inst = inst[0]['nome']

                hymns['principal'].append({
                    'number':hymn['numero'],
                    'date_approvation':hymn['data'],
                    'instructor':inst,
                    'obs':hymn['observacao']
                })
            response_alternative = self.client.table('hinos_va').select('*').eq('usuario_id', int(act_student)).execute()
            for hymn in response_alternative.data:
                inst = self.client.table('users').select('nome').eq('id', hymn['instrutor_id']).execute()
                inst = inst.data
                inst = inst[0]['nome']

                hymns['alternative'].append({
                    'number':hymn['numero'],
                    'date_approvation':hymn['data'],
                    'instructor':inst,
                    'obs':hymn['observacao']
                })
            return hymns
        except:
            print('Erro ao buscar hinos aprovados')

    def seekStudents(self):
        try:
            response = self.client.table('users').select('nome', 'id').eq('nivel', 'aluno').execute()
            return response.data
        except:
            print('Erro ao buscar alunos!')