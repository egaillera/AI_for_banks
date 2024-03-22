import sqlite3
from faker import Faker
import random


def perfil_financiero_cliente() -> str:
    # Conjunto de frases que reflejan diferentes perfiles financieros en tercera persona
    frases_perfiles = [
        "Prefiere inversiones seguras y de bajo riesgo, como los depósitos bancarios.",
        "Se siente más cómodo invirtiendo a largo plazo para obtener rendimientos estables.",
        "Es un inversor conservador y prefiere evitar la volatilidad del mercado de valores.",
        "Busca oportunidades de inversión que le ofrezcan altos rendimientos, incluso si conllevan mayor riesgo.",
        "Está interesado en diversificar su cartera con inversiones en diferentes clases de activos.",
        "Le gusta seguir de cerca el mercado de valores y tomar decisiones de inversión basadas en el análisis técnico.",
        "Prefiere invertir en fondos mutuos gestionados por profesionales para minimizar el riesgo.",
        "Busca oportunidades de inversión que sean éticas y socialmente responsables.",
        "Está dispuesto a asumir cierto nivel de riesgo para obtener rendimientos más altos.",
        "Está interesado en explorar inversiones alternativas, como el crowdfunding inmobiliario o el capital de riesgo.",
        "Prefiere mantener una parte significativa de su cartera en efectivo para cubrir gastos imprevistos.",
        "Está interesado en estrategias de inversión pasiva, como el seguimiento de índices.",
        "Le gusta invertir en empresas con potencial de crecimiento a largo plazo.",
        "Es un inversor agresivo y está dispuesto a asumir riesgos significativos en busca de rendimientos elevados.",
        "Prefiere evitar inversiones especulativas y centrarse en activos estables y seguros.",
        "Está interesado en aprender más sobre estrategias de inversión para maximizar sus rendimientos.",
        "Le gustaría recibir asesoramiento financiero personalizado para optimizar su cartera de inversiones.",
        "Busca inversiones que ofrezcan beneficios fiscales, como los planes de ahorro para la jubilación.",
        "Prefiere invertir en bienes raíces como una forma de diversificar su cartera.",
        "Está interesado en explorar el mercado de criptomonedas y las oportunidades que ofrece.",
        # Las siguientes frases son solo ejemplos y puedes añadir más según tus necesidades
        "Le interesa invertir en el mercado forex para diversificar su cartera.",
        "Busca productos financieros que le permitan retirar fondos fácilmente en caso de necesidad.",
        "Prefiere estrategias de inversión a corto plazo para maximizar sus ganancias en el corto plazo.",
        "Le gustaría invertir en startups tecnológicas como una forma de apostar por el crecimiento futuro.",
        "Está interesado en la inversión en bienes raíces comerciales para obtener ingresos pasivos.",
        "Preferiría invertir en bonos gubernamentales como una opción de inversión segura.",
        "Está interesado en participar en programas de inversión colectiva para compartir riesgos y ganancias.",
        "Le gustaría invertir en arte y coleccionables como una forma alternativa de inversión.",
        "Busca oportunidades de inversión que le permitan aprovechar las tendencias del mercado.",
        "Prefiere invertir en dividendos para obtener ingresos regulares.",
        "Está interesado en la inversión en materias primas como una forma de diversificar su cartera.",
        "Le interesa invertir en fondos indexados para obtener una exposición diversificada al mercado.",
        "Busca inversiones que le permitan beneficiarse del crecimiento económico de los mercados emergentes.",
        "Prefiere estrategias de inversión basadas en el análisis fundamental de las empresas.",
        "Está interesado en el trading de opciones como una forma de obtener beneficios potenciales de la volatilidad del mercado.",
        "Le gustaría explorar oportunidades de inversión en el sector de la energía renovable.",
        "Busca oportunidades de inversión que le permitan obtener beneficios fiscales.",
        "Prefiere estrategias de inversión pasiva, como el dollar-cost averaging, para reducir el riesgo.",
        "Está interesado en invertir en el mercado inmobiliario internacional para diversificar su cartera.",
        "Le gustaría explorar oportunidades de inversión en el mercado de startups como una forma de obtener altos rendimientos.",
        "Busca productos de inversión que le ofrezcan liquidez y flexibilidad.",
        "Prefiere estrategias de inversión conservadoras para proteger su capital.",
        "Está interesado en la inversión en infraestructura como una forma de obtener ingresos estables a largo plazo.",
        "Le gustaría invertir en fondos de cobertura para obtener rendimientos superiores al mercado.",
        "Busca oportunidades de inversión que le permitan beneficiarse del crecimiento de la industria tecnológica.",
        "Prefiere estrategias de inversión basadas en la investigación y el análisis del mercado.",
        "Está interesado en la inversión en startups de impacto social como una forma de generar un cambio positivo.",
        "Le gustaría explorar oportunidades de inversión en el mercado de bienes raíces residenciales.",
        "Busca productos financieros que le ofrezcan protección contra la inflación.",
        "Prefiere estrategias de inversión a largo plazo para maximizar sus ganancias a lo largo del tiempo.",
        "Está interesado en la inversión en fondos de pensiones como una forma de asegurar su futuro financiero.",
        "Le gustaría invertir en bonos corporativos como una forma de diversificar su cartera de inversiones.",
        "Busca oportunidades de inversión que le permitan diversificar su cartera geográficamente.",
        "Prefiere estrategias de inversión basadas en la teoría del ciclo económico para tomar decisiones de inversión.",
        "Está interesado en la inversión en fondos de inversión inmobiliaria para obtener ingresos pasivos.",
        "Le gustaría explorar oportunidades de inversión en el mercado de arte digital como una forma de invertir en activos digitales.",
        "Busca productos financieros que le ofrezcan un equilibrio entre riesgo y rendimiento."
    ]

    # Seleccionar una frase aleatoria
    frase_aleatoria = random.choice(frases_perfiles)

    # Retornar la frase seleccionada
    return frase_aleatoria

def patrimonio_cliente(nivel_de_renta:int) -> int:
    if nivel_de_renta == 'bajo':
        return abs(int(random.gauss(15000,3000)))
    elif nivel_de_renta == 'medio':
        return abs(int(random.gauss(40000,20000)))
    elif nivel_de_renta == 'alto':
        abs(int(random.gauss(80000,100000)))
    

# Crear una conexión a la base de datos
conn = sqlite3.connect('dbclientes.db')
c = conn.cursor()

# Crear la tabla de clientes
c.execute('''CREATE TABLE clientes (
                ID_cliente INTEGER PRIMARY KEY,
                Nombre TEXT,
                Apellido TEXT,
                Edad INTEGER,
                Nivel_de_renta TEXT,
                Patrimonio_estimado NUMERIC,
                Situacion_familiar TEXT,
                Tipo_de_cliente TEXT,
                Preferencias_manifestadas TEXT,
                Fecha_de_creacion DATE,
                Ultima_actualizacion DATE,
                Nivel_tolerancia_riesgo INTEGER
                )''')

# Generar datos sintéticos para 1000 clientes
fake = Faker('es_ES')
for _ in range(1000):
    nombre = fake.first_name()
    apellido = fake.last_name()
    edad = random.randint(18, 90)
    nivel_de_renta = random.choice(['bajo', 'medio', 'alto'])
    patrimonio_estimado = patrimonio_cliente(nivel_de_renta=nivel_de_renta)
    situacion_familiar = random.choices(['soltero', 'casado', 'divorciado', 'viudo'], weights=(25,40,25,10))[0]
    tipo_de_cliente = random.choices(['residente', 'no residente'],weights=(90,10))[0]
    preferencias_manifestadas = perfil_financiero_cliente()
    fecha_creacion = fake.date_between(start_date='-5y', end_date='today')
    ultima_actualizacion = fake.date_between(start_date='-1y', end_date='today')
    nivel_tolerancia_riesgo = random.randint(1, 10)

    c.execute('''INSERT INTO clientes (Nombre, Apellido, Edad, Nivel_de_renta, Patrimonio_estimado,
                    Situacion_familiar, Tipo_de_cliente,
                    Preferencias_manifestadas, Fecha_de_creacion, Ultima_actualizacion, Nivel_tolerancia_riesgo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (nombre, apellido, edad, nivel_de_renta, patrimonio_estimado, situacion_familiar,
                    tipo_de_cliente, preferencias_manifestadas,
                    fecha_creacion, ultima_actualizacion, nivel_tolerancia_riesgo))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada y rellenada con datos sintéticos.")
