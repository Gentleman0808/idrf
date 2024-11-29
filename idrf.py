import random
from faker import Faker
import string

# Initialisation de la bibliothèque Faker
fake = Faker('fr_FR')  # Génère des données adaptées à la France

def generate_identity():
    # Génération des informations de base
    identity = {
        "nom": fake.last_name(),
        "prénom": fake.first_name(),
        "date_de_naissance": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d/%m/%Y"),
        "adresse": fake.address().replace("\n", ", "),
        "email": fake.email(),
        "numéro_de_téléphone": fake.phone_number(),
        "nationalité": "Française",
        "sexe": random.choice(["Homme", "Femme"]),
        "profession": fake.job(),
    }

    # Génération de données supplémentaires
    identity["numéro_de_sécurité_sociale"] = generate_social_security_number(
        identity["date_de_naissance"], identity["sexe"]
    )
    identity["IBAN"], identity["nom_banque"] = generate_iban_with_bank()
    identity["numéro_fiscal"] = generate_tax_id()
    identity["mot_de_passe"] = generate_password()
    identity["profils_réseaux_sociaux"] = generate_social_profiles(identity["prénom"], identity["nom"])
    identity["CV"] = generate_cv(identity["prénom"], identity["nom"], identity["profession"], identity["adresse"])
    identity["données_financières"] = generate_financial_data()

    return identity


def generate_social_security_number(date_of_birth, sexe):
    sexe_code = "1" if sexe == "Homme" else "2"
    year = date_of_birth[-2:]
    month = date_of_birth[3:5]
    departement = f"{random.randint(1, 95):02}"
    commune = f"{random.randint(1, 990):03}"
    order_number = f"{random.randint(1, 999):03}"
    partial_number = f"{sexe_code}{year}{month}{departement}{commune}{order_number}"
    key = 97 - (int(partial_number) % 97)
    return f"{partial_number}{key:02}"


def generate_iban_with_bank():
    country_code = "FR"
    bank_code = ''.join(random.choices(string.digits, k=5))
    branch_code = ''.join(random.choices(string.digits, k=5))
    account_number = ''.join(random.choices(string.digits, k=11))
    check_digits = f"{random.randint(1, 97):02}"
    iban = f"{country_code}{check_digits} {bank_code} {branch_code} {account_number}"

    bank_names = [
        "Société Générale", "BNP Paribas", "Crédit Agricole", "La Banque Postale", "Crédit Mutuel",
        "Caisse d'Épargne", "Banque Populaire", "LCL", "HSBC France"
    ]
    bank_name = random.choice(bank_names)

    return iban, bank_name


def generate_tax_id():
    return ''.join(random.choices(string.digits, k=13))


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password = ''.join(random.choices(characters, k=length))
    return password


def generate_social_profiles(first_name, last_name):
    username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}"
    social_profiles = {
        "Facebook": f"https://facebook.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
    }
    return social_profiles


def generate_cv(first_name, last_name, profession, address):
    skills = random.sample(
        ["Python", "Java", "Gestion de projet", "Marketing", "Communication", "SQL", "Rédaction", "Analyse de données", "Leadership", "Design graphique"],
        k=5
    )
    experiences = generate_experiences()
    education = [
        f"{random.choice(['Licence', 'Master', 'Doctorat'])} en {random.choice(['Informatique', 'Marketing', 'Gestion', 'Design', 'Économie'])} à {fake.company()} ({fake.date_between(start_date='-15y', end_date='-10y').year})"
    ]

    cv = {
        "nom": f"{first_name} {last_name}",
        "profession_actuelle": profession,
        "adresse": address,
        "compétences": skills,
        "expériences": experiences,
        "éducation": education,
    }
    return cv


def generate_experiences():
    # Génération d'expériences professionnelles détaillées
    experiences = []
    for _ in range(2):  # Ajout de deux expériences
        company = fake.company()
        start_date = fake.date_between(start_date='-10y', end_date='-5y')
        end_date = fake.date_between(start_date=start_date, end_date='-1y')
        job = fake.job()
        description = generate_experience_description(job, company)

        experiences.append({
            "poste": job,
            "entreprise": company,
            "période": f"{start_date.year} - {end_date.year}",
            "description": description
        })
    return experiences


def generate_experience_description(job, company):
    # Génération d'une description réaliste pour une expérience professionnelle
    responsibilities = [
        f"Supervision d'une équipe pour atteindre les objectifs stratégiques.",
        f"Mise en œuvre de nouvelles technologies pour améliorer les performances.",
        f"Gestion des relations clients et des négociations commerciales.",
        f"Analyse des données pour identifier les tendances du marché.",
        f"Création et exécution de campagnes marketing innovantes.",
        f"Rédaction de rapports détaillés pour la direction.",
        f"Développement et maintenance de logiciels spécifiques.",
        f"Planification et organisation de projets complexes.",
        f"Formation des nouveaux employés et amélioration des processus internes.",
        f"Collaboration avec des équipes multidisciplinaires pour atteindre les objectifs."
    ]
    description = f"Au sein de {company}, en tant que {job}, j'étais responsable des tâches suivantes : " + \
                  ', '.join(random.sample(responsibilities, k=3)) + "."
    return description


def generate_financial_data():
    salary = random.randint(20000, 120000)
    savings = random.randint(0, salary * 3)
    debt = random.randint(0, salary * 2)
    transactions = [
        {"date": fake.date_this_year(), "montant": round(random.uniform(-1000, 2000), 2), "description": fake.text(max_nb_chars=50)}
        for _ in range(random.randint(5, 15))
    ]

    financial_data = {
        "salaire_annuel": f"{salary} €",
        "épargne": f"{savings} €",
        "dette": f"{debt} €",
        "historique_transactions": transactions,
    }
    return financial_data


# Génération et affichage d'une identité complète
if __name__ == "__main__":
    identity = generate_identity()
    print("Identité générée :")
    for key, value in identity.items():
        if isinstance(value, dict) or isinstance(value, list):
            print(f"{key}:")
            for subkey, subvalue in (value.items() if isinstance(value, dict) else enumerate(value)):
                print(f"  {subkey}: {subvalue}")
        else:
            print(f"{key}: {value}")