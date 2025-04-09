import speech_recognition as sr  #Captura de Audio
import pyttsx3      #Configuração de Linguagem
import wikipedia    #Para pesquisar no Wikipédia
import pywhatkit        #Pedir para tocar musicas no YOutube
import openai           #Utilizar o ChatGPT para responder perguntas (EM DESENVOLVIMENTO)
import webbrowser    # Para abrir e pesquisar no Google
import sympy as sp  # Biblioteca para cálculos matemáticos
import subprocess  # Para abrir subprocessos
import pyautogui  # Para digitar automaticamente (Preferencia Bloco de Notas)

# Configuração da API do OpenAI
openai.api_key = "sua-api-key"  # Substitua pela sua chave de API
model_engine = "text-davinci-003"

# Inicialização dos componentes
audio = sr.Recognizer()
maquina = pyttsx3.init()
maquina.setProperty('voice', 'pt')  # Configuração para voz em português

def responder_com_voz(resposta):
    maquina.say(resposta)
    maquina.runAndWait()

# Teste: usar a função para falar algo
resposta = "Olá, como posso te ajudar hoje? Caso precise de algo me chame por Jarvis!"
responder_com_voz(resposta)

def listen_for_jarvis():
    try:
        with sr.Microphone() as source:
            print("Aguardando comando 'Jarvis'...")
            audio.adjust_for_ambient_noise(source, duration=1)
            voz = audio.listen(source, timeout=20, phrase_time_limit=20)
            comando = audio.recognize_google(voz, language='pt-BR').lower()
            if 'jarvis' in comando:
                return comando.replace('jarvis', '').strip()
            return ""
    except sr.WaitTimeoutError:
        print("Tempo de espera excedido.")
        return ""
    except Exception as e:
        print(f"Não foi possível determinar a escuta!: {e}")
        return ""

def abrir_bloco_notas():
    # Abrir o Bloco de Notas
    subprocess.Popen(['notepad.exe'])
    responder_com_voz("Bloco de Notas aberto. O que você deseja escrever?")

def abrir_word():
    # Abrir o Word
    subprocess.Popen(['word.exe'])
    responder_com_voz("Word Iniciado. O que você deseja escrever?")

def abrir_calculadora():
    # Abrir o Calculadora
    subprocess.Popen(['calc.exe'])
    responder_com_voz("Calculadora Iniciada. O que você deseja calcular?")

def escrever_no_bloco(texto):
    # Escrever no Bloco de Notas usando o pyautogui
    pyautogui.write(texto)
    pyautogui.press('enter')  # Para pressionar Enter e mover para a próxima linha

def solve_math(expression):
    try:
        resultado = sp.sympify(expression)
        return resultado
    except Exception as e:
        print(f"Erro ao resolver a expressão: {e}")
        return None

def execute_command():
    comando = listen_for_jarvis()
    if not comando:
        return

    print(f"Comando recebido: {comando}")

    if 'quanto é' in comando:
        expressao = comando.replace('quanto é', '').strip()
        resultado = solve_math(expressao)
        if resultado is not None:
            resposta = f"O resultado de {expressao} é {resultado}."
            print(resposta)
            responder_com_voz(resposta)
        else:
            responder_com_voz("Não consegui resolver a expressão. Tente novamente.")
        return  # Retorna para evitar processar outros comandos

    if 'bloco de notas' in comando:
        abrir_bloco_notas()  # Abre o Bloco de Notas
        return
    
    if 'calculadora' in comando:
        abrir_calculadora()  # Abre a calculadora
        return
    
    if 'word' in comando:
        abrir_calculadora()  # Abre a Word
        return

    if 'escreva' in comando:
        texto_para_escrever = comando.replace('escreva', '').strip()
        escrever_no_bloco(texto_para_escrever)  # Escreve o texto no Bloco de Notas
        return

    if 'uol' in comando:
        maquina.say("Abrindo o site de notícias do UOL!")
        maquina.runAndWait()
        webbrowser.open('https://www.uol.com.br')
        return  # Adicionado return para evitar continuar no fluxo de comandos
    
    if 'cnn' in comando:
        maquina.say("Abrindo o site de notícias da CNN!")
        maquina.runAndWait()
        webbrowser.open('https://www.cnnbrasil.com.br/')
        return  # Adicionado return para evitar continuar no fluxo de comandos
    
    if 'bbc' in comando:
        maquina.say("Abrindo o site de notícias da BBC!")
        maquina.runAndWait()
        webbrowser.open('https://www.bbc.com/')
        return  # Adicionado return para evitar continuar no fluxo de comandos

    if 'sair' in comando:
        responder_com_voz("Encerrando. Até mais!")
        exit()

    elif 'procure por' in comando or 'pesquise por' in comando:
        procurar = comando.replace('procure por', '').replace('pesquise por', '').strip()
        wikipedia.set_lang('pt')
        try:
            resultado = wikipedia.summary(procurar, sentences=2)
            print(resultado)
            responder_com_voz(resultado)
        except wikipedia.exceptions.DisambiguationError as e:
            opcoes = e.options[:5]
            responder_com_voz(f"Muitos resultados. Tente ser mais específico. Algumas opções: {', '.join(opcoes)}.")
        except Exception as e:
            print(f"Erro ao buscar no Wikipedia: {e}")
            responder_com_voz("Não consegui encontrar resultados.")
            
    elif 'toque' in comando:
        musica = comando.replace('toque', '').strip()
        try:
            pywhatkit.playonyt(musica)
            responder_com_voz(f"Tocando {musica} no YouTube!")
        except Exception as e:
            print(f"Erro ao tocar música: {e}")
            responder_com_voz("Não consegui tocar a música.")

    elif 'google' in comando:
        responder_com_voz("Abrindo o Google!")
        webbrowser.open('https://www.google.com')
        
    elif 'responda' in comando:
        prompt = comando.replace('responda', '').strip()
        try:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=100,
                temperature=0.5,
            )
            response = completion.choices[0].text.strip()
            print(response)
            responder_com_voz(response)
        except Exception as e:
            print(f"Erro ao processar a resposta: {e}")
            responder_com_voz("Houve um erro ao gerar a resposta.")

if __name__ == "__main__":
    try:
        while True:
            execute_command()
    except KeyboardInterrupt:
        print("Execução interrompida pelo usuário.")
        responder_com_voz("Execução interrompida pelo Usuário. Até logo!")
        exit()
    except Exception as e:
        print(f"Erro inesperado: {e}")
