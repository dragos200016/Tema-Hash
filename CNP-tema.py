import random
import calendar
import matplotlib.pyplot as plt
import numpy as np


populatie_pe_judete = {
    '01': 300000, '02': 150000, '03': 200000, '04': 100000, '05': 250000, '06': 150000, '07': 180000,
    '08': 220000, '09': 210000, '10': 120000, '11': 310000, '12': 130000, '13': 270000, '14': 160000,
    '15': 140000, '16': 190000, '17': 170000, '18': 110000, '19': 200000, '20': 180000, '21': 150000,
    '22': 130000, '23': 100000, '24': 90000, '25': 210000, '26': 160000, '27': 140000, '28': 170000,
    '29': 150000, '30': 110000, '31': 100000, '32': 190000, '33': 220000, '34': 140000, '35': 120000,
    '36': 130000, '37': 110000, '38': 90000, '39': 160000, '40': 180000, '41': 200000, '42': 300000,
    '43': 100000, '44': 150000, '45': 200000, '46': 180000, '47': 120000, '48': 130000, '51': 200000, '52': 150000
}
total_populatie = sum(populatie_pe_judete.values())


nume = ["Andrei", "Maria", "Ion", "Elena", "Mihai", "Ana", "Vasile", "Ioana", "Alexandru", "Gabriela"]

def genereaza_cifra_control(cnp_fara_control):
    constanta = "279146358279"
    suma = sum(int(cnp_fara_control[i]) * int(constanta[i]) for i in range(12))
    cifra_control = suma % 11
    return cifra_control if cifra_control < 10 else 1

def selecteaza_judet():
    rand = random.randint(1, total_populatie)
    cumul = 0
    for judet, populatie in populatie_pe_judete.items():
        cumul += populatie
        if rand <= cumul:
            return judet

def genereaza_cnp():
    S = random.choice([1, 2, 5, 6])
    anul = random.randint(1900, 1999) if S in [1, 2] else random.randint(2000, 2024)
    AA = str(anul % 100).zfill(2)
    luna = random.randint(1, 12)
    LL = str(luna).zfill(2)
    zi_maxima = calendar.monthrange(anul, luna)[1]
    ZZ = str(random.randint(1, zi_maxima)).zfill(2)
    JJ = selecteaza_judet()
    NNN = str(random.randint(1, 999)).zfill(3)
    cnp_fara_control = f"{S}{AA}{LL}{ZZ}{JJ}{NNN}"
    C = genereaza_cifra_control(cnp_fara_control)
    return f"{cnp_fara_control}{C}"

def hash_cnp_fnv(cnp, numar_sloturi=1000):
    hash_value = 2166136261
    fnv_prime = 16777619
    for char in cnp:
        hash_value ^= int(char)
        hash_value *= fnv_prime
    return hash_value % numar_sloturi

def genereaza_cnp_si_nume(numar_cnpuri):
    cnp_nume_list = [(genereaza_cnp(), random.choice(nume)) for _ in range(numar_cnpuri)]
    return cnp_nume_list

def simuleaza_generare_si_hash(numar_cnpuri=1000000, numar_sloturi=1000):
    cnp_nume_list = genereaza_cnp_si_nume(numar_cnpuri)
    distributie_hash = {i: [] for i in range(numar_sloturi)}

    for cnp, _ in cnp_nume_list:
        hash_index = hash_cnp_fnv(cnp, numar_sloturi)
        distributie_hash[hash_index].append(cnp)

    
    sloturi = list(distributie_hash.keys())
    valori = [len(distributie_hash[i]) for i in range(numar_sloturi)]

    plt.figure(figsize=(12, 6))
    plt.bar(sloturi, valori, color='blue')
    plt.xlabel('Sloturi Hash')
    plt.ylabel('Număr de CNP-uri per Slot')
    plt.title('Distribuția CNP-urilor în Sloturile Hash')
    plt.show()

    return cnp_nume_list, distributie_hash

def analizeaza_cautare(cnp_nume_list, distributie_hash, numar_sloturi=1000):
    cnp_aleatoare = random.sample(cnp_nume_list, 1000)
    numar_iteratii = []

    for cnp, _ in cnp_aleatoare:
        hash_index = hash_cnp_fnv(cnp, numar_sloturi)
        slot = distributie_hash[hash_index]

        for idx, cnp_in_slot in enumerate(slot):
            if cnp_in_slot == cnp:
                numar_iteratii.append(idx + 1)
                break

    
    media_iteratii = np.mean(numar_iteratii)
    min_iteratii = np.min(numar_iteratii)
    max_iteratii = np.max(numar_iteratii)

    print(f"Media numărului de iterații: {media_iteratii:.2f}")
    print(f"Numărul minim de iterații: {min_iteratii}")
    print(f"Numărul maxim de iterații: {max_iteratii}")

    return media_iteratii, min_iteratii, max_iteratii

def prezentare_rezultate(media_iteratii, min_iteratii, max_iteratii):
    print(f"Media numărului de iterații pentru regăsirea CNP-urilor: {media_iteratii:.2f}")
    print(f"Numărul minim de iterații necesare: {min_iteratii}")
    print(f"Numărul maxim de iterații necesare: {max_iteratii}")


cnp_nume_list, distributie_hash = simuleaza_generare_si_hash()
media_iteratii, min_iteratii, max_iteratii = analizeaza_cautare(cnp_nume_list, distributie_hash)
prezentare_rezultate(media_iteratii, min_iteratii, max_iteratii)