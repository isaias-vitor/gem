from supabase import create_client
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

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

    def saveApprovalFixingExercice(self, date, lesson, inst_id, cand_id):
        print(f'{date} - {lesson} - {inst_id} - {cand_id}')
        data = {
            'numero':lesson,
            'usuario_id':cand_id,
            'instrutor_id':inst_id,
            'data':date.isoformat(),
        }
        try:
            response = self.client.table('msa_fixacao').insert(data).execute()
        except Exception as e:
            print('Erro ao inserir no banco de dados!')
            print(e)
    
    def saveApprovalBona(self, date, obs, lesson, inst_id, cand_id, is_parcial):
        data = {
            'numero':lesson,
            'usuario_id':cand_id,
            'instrutor_id':inst_id,
            'data':date.isoformat(),
            'observacao': obs,
            'parcial':is_parcial
        }
        try:
            response = self.client.table('msa_pratico').insert(data).execute()
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
    
    def cancelApprovalFixing(self, lesson, cand_id):
        try:
            response = self.client.table('msa_fixacao').delete().eq('numero', lesson).eq('usuario_id', cand_id).execute()
        except Exception as e:
            print('Erro ao remover do banco de dados!')
            print(e)

    def cancelApprovalPactical(self, lesson, cand_id):
        try:
            response = self.client.table('msa_pratico').delete().eq('numero', lesson).eq('usuario_id', cand_id).execute()
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

    def seekApprovedMsaLessons(self, act_student):

        try:
            lessons = {'fixacao':[], 'pratico':[]}
            response_fixacao = self.client.table('msa_fixacao').select('*').eq('usuario_id', int(act_student)).execute()
            for lesson in response_fixacao.data:
                inst = self.client.table('users').select('nome').eq('id', lesson['instrutor_id']).execute()
                inst = inst.data
                inst = inst[0]['nome']

                date_approvation = datetime.strptime(lesson['data'], "%Y-%m-%d")
                date_approvation = date_approvation.strftime("%d/%m/%Y")

                lessons['fixacao'].append({
                    'number':lesson['numero'],
                    'date_approvation':date_approvation,
                    'instructor':inst
                })
            response_bona = self.client.table('msa_pratico').select('*').eq('usuario_id', int(act_student)).execute()
            for lesson in response_bona.data:
                inst = self.client.table('users').select('nome').eq('id', lesson['instrutor_id']).execute()
                inst = inst.data
                inst = inst[0]['nome']

                lessons['pratico'].append({
                    'number':lesson['numero'],
                    'date_approvation':lesson['data'],
                    'instructor':inst,
                    'obs':lesson['observacao'], 
                    'parcial':lesson['parcial']
                })
            return lessons
        except:
            print('Erro ao buscar lições do MSA aprovadas')

    def seekStudents(self):
        try:
            response = self.client.table('users').select('nome', 'id').eq('nivel', 'aluno').execute()
            return response.data
        except:
            print('Erro ao buscar alunos!')

    def modifyStatusPractical(self, lesson, cand_id, status):
        print('llllllllllllllllllllllllllllllllllllll')
        try:
            response = self.client.table('msa_pratico').update({'parcial': status}).eq('usuario_id', cand_id).eq('numero', lesson).execute()
        except Exception as e:
            print('Erro ao modificar status da lição!')
            print(e)