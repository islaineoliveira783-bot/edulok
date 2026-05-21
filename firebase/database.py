import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

# CAMINHO DA CHAVE FIREBASE
cred = credentials.Certificate(
    "firebase/chave.json"
)

# INICIAR FIREBASE
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# BANCO
db = firestore.client()

# ==================================================
# SALVAR DÚVIDA
# ==================================================
def salvar_duvida(dados):

    db.collection("duvidas").add(dados)

# ==================================================
# LISTAR DÚVIDAS
# ==================================================
def listar_duvidas():

    docs = db.collection("duvidas").stream()

    lista = []

    for doc in docs:

        dado = doc.to_dict()

        dado["id"] = doc.id

        lista.append(dado)

    return lista

# ==================================================
# RESPONDER DÚVIDA
# ==================================================
def responder_duvida(id_duvida, resposta, monitor):

    db.collection("duvidas").document(
        id_duvida
    ).update({

        "resposta": resposta,

        "respondido_por": monitor,

        "status": "respondido"
    })