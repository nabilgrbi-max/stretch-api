import shutil
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

# On importe notre fonction "cuisine" depuis l'autre fichier
from stretch_audio import stretch_audio

# On crée notre application "serveur"
app = FastAPI()


@app.get("/")
def racine():
    return {"message": "Bonjour, l'API de stretching audio est prête !"}


# On définit une nouvelle "route" pour recevoir les fichiers
@app.post("/stretch/")
async def creer_stretch(fichier: UploadFile = File(...)):
    # 1. On crée des noms de fichiers uniques pour éviter les conflits
    nom_unique = str(uuid.uuid4())
    chemin_entree = f"{nom_unique}_original.wav"
    chemin_sortie = f"{nom_unique}_modifie.wav"

    # 2. On sauvegarde le fichier que Bubble nous a envoyé
    with open(chemin_entree, "wb") as buffer:
        shutil.copyfileobj(fichier.file, buffer)

    # 3. On appelle notre fonction "cuisine" pour faire le travail
    resultat = stretch_audio(chemin_entree, chemin_sortie)

    # 4. Si tout s'est bien passé, on renvoie le fichier modifié
    if resultat:
        return FileResponse(path=resultat, media_type="audio/wav", filename="audio_stretche.wav")
    else:
        return {"erreur": "Le traitement du fichier a échoué."}