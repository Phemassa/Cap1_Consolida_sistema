"""
FarmTech Solutions - Integração Python com API Open Source (Open‑Meteo)
Cap 1 - Um Mapa do Tesouro
Atividade: Integração meteorológica para otimizar irrigação (sem API key)

Grupo 19 FIAP - 1 ano • 2025/2 - Fase 2 - de 18/09/2025 a 15/10/2025
RM566826 - Phellype Matheus Giacoia Flaibam Massarente
RM567005 - Carlos Alberto Florindo Costato
RM568140 - Cesar Martinho de Azeredo

Objetivo: Consultar previsão de chuva (Open‑Meteo) e enviar comando ao ESP32 via Serial
Funcionalidade: Se previsão de chuva > 50%, suspende irrigação automaticamente
"""

import requests
import json
from datetime import datetime
import sys
import argparse
from typing import Optional, Tuple

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

CIDADE = "Campinas"  # Cidade da fazenda
PAIS = "BR"
# Arquivo de logs
LOG_FILE = 'logs_irrigacao_api.json'

# Endpoints Open-Meteo (open source, sem API key)
OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# ============================================================================
# FUNÇÕES PRINCIPAIS
# ============================================================================


def geocodificar_cidade_open_meteo(nome_cidade: str, pais: str) -> Optional[Tuple[float, float, str]]:
    """Obtém latitude/longitude usando a API de geocodificação do Open-Meteo (OpenStreetMap).

    Returns: (lat, lon, timezone) ou None se falhar.
    """
    try:
        params = {
            'name': f"{nome_cidade}",
            'count': 1,
            'language': 'pt',
            'format': 'json'
        }
        resp = requests.get(OPEN_METEO_GEOCODE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = data.get('results') or []
        if not results:
            return None
        r0 = results[0]
        return float(r0['latitude']), float(r0['longitude']), r0.get('timezone', 'auto')
    except Exception as e:
        print(f"❌ Erro na geocodificação Open‑Meteo: {e}")
        return None


def obter_previsao_chuva_open_meteo() -> Optional[dict]:
    """Consulta a API Open‑Meteo (open source) e retorna probabilidade de chuva nas próximas 24h.

    Retorno compatível com o restante do sistema:
      {
        'probabilidade': float (0-100),
        'descricao': str,
        'temperatura': float,
        'horario_previsto': str
      }
    """
    geo = geocodificar_cidade_open_meteo(CIDADE, PAIS)
    if not geo:
        print("⚠️  Não foi possível geocodificar a cidade para Open‑Meteo.")
        return None
    lat, lon, tz = geo

    try:
        params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'precipitation_probability,temperature_2m',
            'timezone': tz or 'auto'
        }
        resp = requests.get(OPEN_METEO_FORECAST_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        hourly = data.get('hourly') or {}
        times = hourly.get('time') or []
        probs = hourly.get('precipitation_probability') or []
        temps = hourly.get('temperature_2m') or []
        if not times or not probs:
            return None

        # Considerar as próximas 24 horas (assumindo série iniciando no horário atual)
        window = slice(0, min(24, len(probs)))
        max_p = -1
        idx = None
        for i, p in enumerate(probs[window]):
            if p is not None and p > max_p:
                max_p = p
                idx = i
        if idx is None:
            return None

        prob = float(max_p)
        hora = times[window][idx] if hasattr(times, '__getitem__') else times[idx]
        temp = float(temps[window][idx]) if temps else None

        # Gerar uma descrição simples baseada no limiar
        if prob >= 70:
            desc = 'chuva forte provável'
        elif prob >= 40:
            desc = 'chuva moderada possível'
        else:
            desc = 'baixa probabilidade de chuva'

        return {
            'probabilidade': prob,
            'descricao': desc,
            'temperatura': temp if temp is not None else 0.0,
            'horario_previsto': hora
        }
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao consultar Open‑Meteo: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao processar Open‑Meteo: {e}")
        return None
    except KeyError as e:
        print(f"❌ Erro ao processar resposta da API: {e}")
        return None


def decidir_irrigacao(previsao):
    """
    Decide se deve irrigar baseado na previsão de chuva
    
    Args:
        previsao (dict): Dados da previsão meteorológica
    
    Returns:
        bool: True para irrigar, False para suspender
    """
    if not previsao:
        print("⚠️  Sem dados meteorológicos, mantendo irrigação normal")
        return True
    
    prob_chuva = previsao['probabilidade']
    
    # Lógica de decisão
    if prob_chuva >= 70:
        print(f"🌧️  ALTA probabilidade de chuva ({prob_chuva:.1f}%)")
        print(f"   📅 Previsto para: {previsao['horario_previsto']}")
        print(f"   ☔ Descrição: {previsao['descricao']}")
        print(f"   💧 DECISÃO: SUSPENDER irrigação (economia de água)")
        return False
    
    elif prob_chuva >= 40:
        print(f"🌦️  MÉDIA probabilidade de chuva ({prob_chuva:.1f}%)")
        print(f"   📅 Previsto para: {previsao['horario_previsto']}")
        print(f"   ⚠️  DECISÃO: REDUZIR irrigação em 50%")
        return True  # Poderia implementar irrigação parcial
    
    else:
        print(f"☀️  BAIXA probabilidade de chuva ({prob_chuva:.1f}%)")
        print(f"   🌡️  Temperatura: {previsao['temperatura']:.1f}°C")
        print(f"   ✅ DECISÃO: MANTER irrigação normal")
        return True


def enviar_comando_esp32(irrigar):
    """
    Envia comando para ESP32 via Serial (simulado)
    
    Args:
        irrigar (bool): True = ligar irrigação, False = desligar
    
    Nota: Para implementação real, use pyserial:
        import serial
        ser = serial.Serial('COM3', 115200)  # Porta do ESP32
        comando = 'IRRIGAR_ON' if irrigar else 'IRRIGAR_OFF'
        ser.write(comando.encode())
    """
    comando = "IRRIGAR_ON" if irrigar else "IRRIGAR_OFF"
    
    print("\n" + "="*60)
    print("📡 ENVIANDO COMANDO PARA ESP32 (Serial)")
    print("="*60)
    print(f"   Porta: COM3 (exemplo)")
    print(f"   Baud: 115200")
    print(f"   Comando: {comando}")
    print("="*60)
    
    # Simulação de envio
    print(f"\n✅ Comando '{comando}' enviado com sucesso!")
    print("   (Para implementação real, instale: pip install pyserial)")


def salvar_log_decisao(previsao, irrigar):
    """
    Salva log da decisão em arquivo JSON
    
    Args:
        previsao (dict): Dados meteorológicos
        irrigar (bool): Decisão tomada
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'previsao': previsao,
        'decisao': 'IRRIGAR' if irrigar else 'SUSPENDER',
        'motivo': 'Previsão de chuva' if not irrigar else 'Sem chuva prevista'
    }
    
    try:
        # Tentar ler log existente
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []
        
        # Adicionar nova entrada
        logs.append(log_entry)
        
        # Salvar atualizado
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 Log salvo em '{LOG_FILE}'")
        
    except Exception as e:
        print(f"⚠️  Erro ao salvar log: {e}")


# ============================================================================
# MENU E DESCRITIVOS
# ============================================================================

def mostrar_descritivo(opcao: str):
    """Imprime um descritivo acima dos dados esperados para cada opção do menu."""
    print("\n" + "=" * 60)
    if opcao == 'open-meteo':
        print("📘 DESCRITIVO - Modo Real (Open‑Meteo | Open Source)")
        print("- Requisitos: Internet ativa (sem necessidade de API key)")
        print("- Parâmetros usados: Cidade (geocodifica para lat/lon), timezone automático")
        print("- Dados esperados da API (próximas 24h):")
        print("  • probabilidade: 0–100% (precipitation_probability)")
        print("  • temperatura: temperatura do ar (°C) no horário de maior probabilidade")
        print("  • horario_previsto: timestamp ISO do horário com maior probabilidade")
        print("- Saídas do sistema:")
        print("  • Decisão: SUSPENDER / REDUZIR / MANTER irrigação")
        print(f"  • Log: registro salvo em '{LOG_FILE}'")
    elif opcao == 'logs':
        print("📘 DESCRITIVO - Visualizar Logs")
        print(f"- Origem: arquivo '{LOG_FILE}' no diretório atual")
        print("- Campos listados por registro:")
        print("  • timestamp: data/hora da decisão")
        print("  • decisao: IRRIGAR ou SUSPENDER")
        print("  • motivo: justificativa resumida")
        print("  • previsao: dicionário com probabilidade/descricao/temperatura/horario")
    print("=" * 60 + "\n")


def visualizar_logs(max_itens: int = 10):
    """Mostra os últimos registros de decisão salvos no arquivo de log."""
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Arquivo de log '{LOG_FILE}' não encontrado.")
        return
    except json.JSONDecodeError:
        print(f"⚠️  Não foi possível ler '{LOG_FILE}' (JSON inválido).")
        return

    print(f"📄 Exibindo até {max_itens} registros mais recentes do log:\n")
    for entry in logs[-max_itens:]:
        print(f"- timestamp: {entry.get('timestamp')}")
        print(f"  decisao:   {entry.get('decisao')}")
        print(f"  motivo:    {entry.get('motivo')}")
        prev = entry.get('previsao') or {}
        print("  previsao:")
        print(f"    • probabilidade: {prev.get('probabilidade')}")
        print(f"    • descricao:     {prev.get('descricao')}")
        print(f"    • temperatura:   {prev.get('temperatura')}")
        print(f"    • horario:       {prev.get('horario_previsto')}\n")


def print_menu():
    print("\n" + "=" * 60)
    print("🌾 FarmTech Solutions - Integração API Meteorológica (Menu)")
    print("=" * 60)
    print("1) Modo Real (Open‑Meteo - open source)")
    print("2) Visualizar logs de decisões")
    print("3) Sair")
    print("=" * 60)


def executar_modo_open_meteo():
    mostrar_descritivo('open-meteo')
    print("🌐 Consultando Open‑Meteo (open source)...\n")
    previsao = obter_previsao_chuva_open_meteo()
    if previsao:
        print("✅ Dados meteorológicos obtidos com sucesso!\n")
        irrigar = decidir_irrigacao(previsao)
        enviar_comando_esp32(irrigar)
        salvar_log_decisao(previsao, irrigar)
    else:
        print("❌ Falha ao obter previsão. Mantendo irrigação padrão.")


def executar_visualizar_logs():
    mostrar_descritivo('logs')
    visualizar_logs()


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """Função principal do sistema"""
    global CIDADE, PAIS

    print("\n" + "="*60)
    print("🌾 FarmTech Solutions - Sistema de Irrigação Inteligente")
    print("   Opcional 1: Integração com API Meteorológica")
    print("="*60)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📍 Localização: {CIDADE}, {PAIS}")
    print("="*60 + "\n")

    # Suporte a argumentos de linha de comando (modo, cidade, país)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--mode', choices=['open-meteo', 'logs'], help='Seleciona o modo de execução')
    parser.add_argument('--city', help='Sobrescreve a cidade do script')
    parser.add_argument('--country', help='Sobrescreve o país do script (ex.: BR)')
    try:
        args, _ = parser.parse_known_args()
    except SystemExit:
        # Em ambientes sem CLI, ignore erros de parser
        args = argparse.Namespace(mode=None, city=None, country=None)

    if args.city:
        CIDADE = args.city
    if args.country:
        PAIS = args.country

    def exec_mode(mode: str):
        if mode == 'open-meteo':
            executar_modo_open_meteo()
        elif mode == 'logs':
            executar_visualizar_logs()

    if args.mode:
        # Execução direta por argumento
        exec_mode(args.mode)
    elif sys.stdin.isatty():
        # Modo interativo com menu
        while True:
            print_menu()
            escolha = input("Selecione uma opção (1-3): ").strip()
            if escolha == '1':
                exec_mode('open-meteo')
            elif escolha == '2':
                exec_mode('logs')
            elif escolha == '3':
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        # Fallback não interativo: usar Open‑Meteo
        executar_modo_open_meteo()

    print("\n" + "="*60)
    print("✅ Processo concluído!")
    print("="*60 + "\n")


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()


# ============================================================================
# INTEGRAÇÃO COM ESP32 (Código C++ correspondente)
# ============================================================================

"""
Para receber comandos no ESP32, adicione no FarmTech.ino:

void setup() {
    Serial.begin(115200);
    // ... resto do setup
}

void loop() {
    // Verificar comandos da API Python
    if (Serial.available() > 0) {
        String comando = Serial.readStringUntil('\n');
        comando.trim();
        
        if (comando == "IRRIGAR_OFF") {
            // Forçar desligamento da irrigação
            digitalWrite(RELE_PIN, LOW);
            releLigado = false;
            Serial.println("✅ Irrigação SUSPENSA por previsão de chuva");
        }
        else if (comando == "IRRIGAR_ON") {
            // Permitir irrigação normal
            Serial.println("✅ Irrigação liberada (sem chuva prevista)");
        }
    }
    
    // ... resto do loop
}
"""

# ============================================================================
# BENEFÍCIOS DA INTEGRAÇÃO
# ============================================================================

"""
✅ ECONOMIA DE ÁGUA
   - Suspende irrigação antes da chuva
   - Reduz desperdício de recursos hídricos
   - Diminui custos operacionais

✅ SUSTENTABILIDADE
   - Uso inteligente de recursos naturais
   - Redução da pegada hídrica
   - Alinhamento com práticas ESG

✅ AUTOMAÇÃO
   - Decisão baseada em dados reais
   - Sem necessidade de intervenção manual
   - Integração com sistema existente

✅ ESCALABILIDADE
   - Fácil adaptação para múltiplas fazendas
   - Integração com outros sensores
   - Base para Machine Learning futuro
"""
