# On importe les bibliothèques nécessaires
import librosa
import soundfile as sf
import pyrubberband as rb
import numpy as np

def stretch_audio(chemin_entree, chemin_sortie):
    """
    Charge un fichier audio, ajuste sa durée au multiple de 5 le plus proche,
    et sauvegarde le résultat.
    """
    try:
        # --- ÉTAPE 1 : CHARGER LE FICHIER ---
        print("Chargement du fichier audio...")
        y, sr = librosa.load(chemin_entree, sr=None, mono=False)

        # SÉCURITÉ : On s'assure que le volume ne dépasse pas les limites
        y = np.clip(y, -1.0, 1.0)

        # --- ÉTAPE 2 : CALCULER LES DURÉES ---
        duree_originale = librosa.get_duration(y=y, sr=sr)
        duree_cible = round(duree_originale / 5) * 5

        if duree_cible == 0:
            print("Le fichier est trop court, la durée cible est 0.")
            return None
        elif abs(duree_originale - duree_cible) < 0.1: # Si la différence est minime
            print("La durée est déjà correcte. Aucune modification nécessaire.")
            # On copie simplement le fichier original vers la destination
            sf.write(chemin_sortie, y.T, sr)
            return chemin_sortie

        # --- ÉTAPE 3 : CALCULER LE "RATE" ---
        rate = duree_originale / duree_cible
        
        print(f"Durée originale : {duree_originale:.2f}s -> Cible : {duree_cible}s")

        # --- ÉTAPE 4 : APPLIQUER LE TIME-STRETCH ---
        print("Modification du fichier en cours (optimisation Voix Off)...")
        y_int32 = (y.T * 2147483647).astype(np.int32)
        y_modifie = rb.time_stretch(y_int32, sr, rate=rate, rbargs={'--formant': ''})

        # --- ÉTAPE 5 : SAUVEGARDER LE NOUVEAU FICHIER ---
        sf.write(chemin_sortie, y_modifie, sr, subtype='PCM_32')
        
        print(f"Terminé ! Fichier sauvegardé sous le nom : {chemin_sortie}")
        return chemin_sortie

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None

# --- Section pour tester la fonction (optionnel) ---
if __name__ == "__main__":
    print("--- Lancement du test local ---")
    input_file = "mon_audio_original.wav"
    output_file = "mon_audio_modifie_test.wav"
    
    resultat = stretch_audio(input_file, output_file)
    
    if resultat:
        print(f"--- Test réussi ! Fichier créé : {resultat} ---")
    else:
        print("--- Le test a échoué. ---")