from supabase import create_client
from os import getenv

class SupabaseClient:
    def __init__(self):
        self.url = getenv('SUPABASE_URL')
        self.key = getenv('SUPABASE_KEY')
        self.client = create_client(self.url, self.key)

    def primeiraBusca(self):
        try:
            busca = self.client.table('teste').select('*').execute()
            resultado = busca.data[0]
            print(f'*************{resultado}*****************')
        except:
            print('AAAAAAAAAAAAAAAAAAA')
        return resultado