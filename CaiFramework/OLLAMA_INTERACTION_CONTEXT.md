# 🔄 Interacción con Ollama y Gestión de Contexto en CaiFramework

## 📚 Índice
1. [Arquitectura General](#arquitectura-general)
2. [Flujo de Comunicación con Ollama](#flujo-de-comunicación-con-ollama)
3. [Gestión del Contexto](#gestión-del-contexto)
4. [Mantenimiento del Historial de Mensajes](#mantenimiento-del-historial-de-mensajes)
5. [Ciclo de Ejecución de un Agente](#ciclo-de-ejecución-de-un-agente)
6. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Arquitectura General

### Componentes Clave

```
┌─────────────────┐
│   Service       │  (red_teamer.py, blue_teamer.py, etc.)
│   Scripts       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OllamaProvider │  (Crea y gestiona modelos)
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ ChatCompletionsModel │  (Maneja comunicación y contexto)
└────────┬─────────────┘
         │
         ▼
┌─────────────────┐
│  AsyncOpenAI    │  (Cliente HTTP para Ollama)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ollama Server  │  (localhost:11434)
└─────────────────┘
```

---

## Flujo de Comunicación con Ollama

### 1. Inicialización del Provider

**Archivo**: `cai/sdk/agents/models/ollama_provider.py`

```python
class OllamaProvider(ModelProvider):
    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: str = "ollama",  # No se requiere API key real
        timeout: float = 300.0,
    ):
        # URL por defecto de Ollama
        self._base_url = base_url or os.environ.get(
            "OLLAMA_API_BASE",
            "http://localhost:11434/v1"  # API compatible con OpenAI
        )

        # Modelo por defecto
        self._default_model = model_name or os.environ.get(
            "OLLAMA_MODEL",
            "llama3.2"
        )

        # Marca el entorno como Ollama
        os.environ["OLLAMA"] = "true"
```

**Características**:
- **URL Base**: `http://localhost:11434/v1` (API compatible con OpenAI)
- **Timeout**: 300 segundos (5 minutos) para modelos locales
- **Connection Pooling**: Cliente HTTP compartido para mejor rendimiento
- **No requiere API key real**: Ollama no necesita autenticación

### 2. Creación del Cliente

```python
def _get_client(self) -> AsyncOpenAI:
    if self._client is None:
        self._client = AsyncOpenAI(
            api_key=self._api_key,
            base_url=self._base_url,
            http_client=get_ollama_http_client(),  # Cliente compartido
        )
    return self._client
```

**Connection Pooling**:
```python
def get_ollama_http_client() -> httpx.AsyncClient:
    global _ollama_http_client
    if _ollama_http_client is None:
        _ollama_http_client = DefaultAsyncHttpxClient(
            timeout=httpx.Timeout(300.0, connect=60.0)
        )
    return _ollama_http_client
```

### 3. Obtención del Modelo

```python
def get_model(self, model_name: str | None = None) -> Model:
    if model_name is None:
        model_name = self._default_model

    client = self._get_client()

    return ChatCompletionsModel(
        model=model_name,
        openai_client=client,
    )
```

---

## Gestión del Contexto

### 1. Inicialización del Contexto

**Archivo**: `cai/sdk/agents/models/chatcompletions.py`

Cuando se crea un `ChatCompletionsModel`, se inicializa el historial:

```python
class ChatCompletionsModel(Model):
    def __init__(
        self,
        model: str | ChatModel,
        openai_client: AsyncOpenAI,
        agent_name: str = "CTF agent",
        agent_id: str | None = None,
        agent_type: str | None = None,
    ):
        self.model = model
        self._client = openai_client
        self.is_ollama = os.getenv("OLLAMA") is not None

        # Inicializar historial de mensajes
        self.agent_name = agent_name
        self.agent_id = agent_id or agent_name

        # Para agentes paralelos, usar historial aislado
        if agent_id and agent_id.startswith('P'):
            isolated_history = PARALLEL_ISOLATION.get_isolated_history(agent_id)
            if isolated_history is not None:
                self.message_history = isolated_history
            else:
                self.message_history = []
        else:
            # Obtener o crear historial desde AGENT_MANAGER
            existing_history = AGENT_MANAGER.get_message_history(agent_name)
            if existing_history is not None and isinstance(existing_history, list):
                # Usar la referencia existente (importante para compartir)
                self.message_history = existing_history
            else:
                # Crear nuevo historial
                self.message_history = []
                AGENT_MANAGER._message_history[self.agent_name] = self.message_history
```

**Sistemas de Gestión de Historial**:

1. **AGENT_MANAGER** (SimpleAgentManager):
   - Gestiona historial del agente activo
   - Permite compartir historial entre agentes (swarm patterns)
   - Soporta comandos `/history`, `/flush`, `/load`

2. **PARALLEL_ISOLATION**:
   - Aísla historiales de agentes paralelos
   - Cada agente paralelo tiene su propio contexto
   - Identificados por ID con prefijo 'P' (P1, P2, etc.)

### 2. Estructura del Historial

El historial es una lista de mensajes en formato OpenAI:

```python
self.message_history = [
    {
        "role": "system",
        "content": "You are a red team security specialist..."
    },
    {
        "role": "user",
        "content": "Perform reconnaissance on target 192.168.1.1"
    },
    {
        "role": "assistant",
        "content": "I'll scan the target...",
        "tool_calls": [
            {
                "id": "call_abc123",
                "type": "function",
                "function": {
                    "name": "generic_linux_command",
                    "arguments": '{"command": "nmap -sT 192.168.1.1"}'
                }
            }
        ]
    },
    {
        "role": "tool",
        "tool_call_id": "call_abc123",
        "content": "PORT   STATE SERVICE\n22/tcp open  ssh\n80/tcp open  http"
    },
    # ... más mensajes
]
```

---

## Mantenimiento del Historial de Mensajes

### 1. Adición de Mensajes al Historial

**En cada turno del agente**, los mensajes se añaden al historial:

```python
async def get_response(
    self,
    system_instructions: str | None,
    input: list[TResponseInputItem],
    model_settings: ModelSettings,
    tools: list[Tool],
    output_schema: AgentOutputSchema | None,
    handoffs: list[Handoff],
    tracing: ModelTracing,
) -> ModelResponse:

    # 1. Construir mensajes para esta solicitud
    messages = []

    # 2. Añadir prompt del sistema si existe
    if system_instructions:
        messages.append({
            "role": "system",
            "content": system_instructions
        })

    # 3. IMPORTANTE: Añadir el historial completo
    messages.extend(self.message_history)

    # 4. Añadir nuevos inputs del usuario
    for item in input:
        messages.append(self._convert_to_message(item))

    # 5. Enviar a Ollama
    response = await self._client.chat.completions.create(
        model=self.model,
        messages=messages,
        tools=converted_tools if tools else None,
        temperature=model_settings.temperature,
        max_tokens=model_settings.max_tokens,
        # ... otros parámetros
    )

    # 6. GUARDAR en el historial: Mensaje del usuario
    for item in input:
        self.message_history.append(self._convert_to_message(item))

    # 7. GUARDAR en el historial: Respuesta del asistente
    assistant_message = {
        "role": "assistant",
        "content": response.choices[0].message.content
    }
    if response.choices[0].message.tool_calls:
        assistant_message["tool_calls"] = [
            # ... convertir tool_calls
        ]
    self.message_history.append(assistant_message)

    # 8. Ejecutar herramientas y GUARDAR resultados
    for tool_call in tool_calls:
        result = await execute_tool(tool_call)
        self.message_history.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

    return ModelResponse(...)
```

### 2. Flujo Completo de un Turno

```
Usuario: "Escanea el puerto 80"
    ↓
┌─────────────────────────────────────┐
│ 1. Construir mensajes:              │
│    - System prompt                  │
│    - Historial completo anterior    │
│    - Nuevo mensaje del usuario      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. Enviar a Ollama (POST)           │
│    http://localhost:11434/v1/chat/  │
│    completions                       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Ollama procesa con TODO el       │
│    contexto acumulado               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. Respuesta de Ollama:             │
│    "Voy a usar nmap..."             │
│    + tool_calls: [nmap command]     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. GUARDAR en historial:            │
│    - Mensaje usuario                │
│    - Respuesta asistente            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 6. Ejecutar herramientas:           │
│    generic_linux_command("nmap...")  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 7. GUARDAR resultado en historial: │
│    role: "tool"                     │
│    content: "PORT 80 open..."       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 8. Siguiente turno con TODO         │
│    el contexto acumulado            │
└─────────────────────────────────────┘
```

### 3. Persistencia del Historial

**El historial se mantiene en memoria** durante toda la sesión:

```python
# Global manager que mantiene el historial
AGENT_MANAGER = SimpleAgentManager()

# Funciones para gestionar el historial
def get_agent_message_history(agent_name: str) -> list:
    """Obtener historial de un agente específico"""
    return AGENT_MANAGER.get_message_history(agent_name)

def clear_agent_history(agent_name: str):
    """Limpiar historial de un agente"""
    AGENT_MANAGER.clear_history(agent_name)

def clear_all_histories():
    """Limpiar todos los historiales"""
    AGENT_MANAGER.clear_all_histories()
```

---

## Ciclo de Ejecución de un Agente

**Archivo**: `cai/sdk/agents/run.py`

### Runner.run() - Bucle Principal

```python
async def run(
    cls,
    starting_agent: Agent[TContext],
    input: str | list[TResponseInputItem],
    *,
    context: TContext | None = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
) -> RunResult:

    current_turn = 0
    current_agent = starting_agent
    generated_items: list[RunItem] = []
    model_responses: list[ModelResponse] = []

    while True:
        current_turn += 1

        # 1. Ejecutar un turno del agente
        turn_result = await cls._run_single_turn(
            agent=current_agent,
            all_tools=all_tools,
            original_input=original_input,
            generated_items=generated_items,
            hooks=hooks,
            context_wrapper=context_wrapper,
            run_config=run_config,
            should_run_agent_start_hooks=should_run_agent_start_hooks,
            tool_use_tracker=tool_use_tracker,
        )

        # 2. Guardar respuesta del modelo
        model_responses.append(turn_result.model_response)
        generated_items = turn_result.generated_items

        # 3. Verificar si hay output final
        if isinstance(turn_result.next_step, NextStepFinalOutput):
            return RunResult(
                input=original_input,
                new_items=generated_items,
                raw_responses=model_responses,
                final_output=turn_result.next_step.output,
            )

        # 4. Verificar handoff (cambio de agente)
        elif isinstance(turn_result.next_step, NextStepHandoff):
            previous_agent = current_agent
            current_agent = turn_result.next_step.new_agent

            # IMPORTANTE: Transferir historial en swarm patterns
            if (hasattr(previous_agent, 'model') and
                hasattr(previous_agent.model, 'message_history') and
                hasattr(current_agent, 'model') and
                hasattr(current_agent.model, 'message_history')):

                # Compartir historial entre agentes
                current_agent.model.message_history = previous_agent.model.message_history

        # 5. Continuar ejecutando (tool calls completados)
        elif isinstance(turn_result.next_step, NextStepRunAgain):
            pass  # Siguiente iteración del bucle
```

### _run_single_turn() - Un Turno

```python
async def _run_single_turn(...) -> SingleStepResult:
    # 1. Obtener prompt del sistema
    system_prompt = await agent.get_system_prompt(context_wrapper)

    # 2. Preparar input (mensajes previos + nuevo input)
    input = ItemHelpers.input_to_new_input_list(original_input)
    input.extend([item.to_input_item() for item in generated_items])

    # 3. Obtener respuesta del modelo (aquí se comunica con Ollama)
    new_response = await cls._get_new_response(
        agent,
        system_prompt,
        input,
        output_schema,
        all_tools,
        handoffs,
        context_wrapper,
        run_config,
        tool_use_tracker,
    )

    # 4. Procesar respuesta y ejecutar herramientas
    return await cls._get_single_step_result_from_response(...)
```

---

## Ejemplos Prácticos

### Ejemplo 1: Red Team Reconnaissance

```python
# services/red_teamer.py

# 1. Inicialización
ollama = OllamaProvider(model_name="llama3.2")
agent = Agent(
    name="Red Teamer",
    instructions="You are an offensive security specialist...",
    tools=[generic_linux_command, execute_code],
    model=ollama.get_model()
)

# 2. Primera interacción
result = await Runner.run(
    starting_agent=agent,
    input="Perform reconnaissance on 192.168.1.1"
)

# Internamente:
# - Se crea message_history = []
# - Se añade: {"role": "system", "content": "You are..."}
# - Se añade: {"role": "user", "content": "Perform reconnaissance..."}
# - Se envía a Ollama: http://localhost:11434/v1/chat/completions
# - Ollama responde con tool_calls: [nmap command]
# - Se añade respuesta al historial
# - Se ejecuta nmap
# - Se añade resultado al historial

# 3. Segunda interacción (mismo agente, mantiene contexto)
result = await Runner.run(
    starting_agent=agent,
    input="Now scan port 80 specifically"
)

# Internamente:
# - message_history ya tiene todo el contexto anterior
# - Se añade nuevo mensaje del usuario
# - Se envía TODO el historial a Ollama
# - Ollama tiene contexto completo: sabe que ya escaneó antes
# - Puede responder con contexto: "Based on the previous scan..."
```

### Ejemplo 2: Modo Interactivo

```python
# services/red_teamer.py --interactive

while True:
    task = input("red-team> ")
    if task.lower() in ['exit', 'quit']:
        break

    result = await Runner.run(
        starting_agent=agent,
        input=task,
        run_config=RunConfig(tracing_disabled=True)
    )

    print(f"\n{result.final_output}\n")

# En cada iteración:
# - El agente mantiene su message_history
# - Cada comando se añade al contexto
# - El LLM recuerda todas las interacciones previas
# - Ejemplo:
#   red-team> scan target.com
#   [escaneo ejecutado, guardado en historial]
#   red-team> what ports did you find?
#   [El LLM puede responder porque tiene el contexto del escaneo previo]
```

### Ejemplo 3: Visualizar el Historial

```python
# Obtener el historial de mensajes del agente
from cai.sdk.agents.models.chatcompletions import get_agent_message_history

history = get_agent_message_history("Red Teamer")

for msg in history:
    print(f"Role: {msg['role']}")
    print(f"Content: {msg.get('content', '[tool_call]')}")
    if 'tool_calls' in msg:
        for tc in msg['tool_calls']:
            print(f"  Tool: {tc['function']['name']}")
            print(f"  Args: {tc['function']['arguments']}")
    print("-" * 80)
```

Salida:
```
Role: system
Content: You are an offensive security specialist...
────────────────────────────────────────────────────────────────────────────────
Role: user
Content: Perform reconnaissance on 192.168.1.1
────────────────────────────────────────────────────────────────────────────────
Role: assistant
Content: I'll scan the target using nmap...
  Tool: generic_linux_command
  Args: {"command": "nmap -sT 192.168.1.1"}
────────────────────────────────────────────────────────────────────────────────
Role: tool
Content: PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
────────────────────────────────────────────────────────────────────────────────
Role: user
Content: Now scan port 80 specifically
────────────────────────────────────────────────────────────────────────────────
Role: assistant
Content: Based on the previous scan showing port 80 open, I'll perform...
  Tool: generic_linux_command
  Args: {"command": "nmap -sV -p 80 192.168.1.1"}
────────────────────────────────────────────────────────────────────────────────
```

---

## Gestión de Memoria y Límites

### 1. Límite de Contexto

Ollama y los modelos LLM tienen un límite de tokens (contexto window):

- **llama3.2**: ~128K tokens
- **codellama**: ~16K tokens
- **mistral**: ~32K tokens
- **qwen2.5**: ~32K tokens

### 2. Estrategias de Gestión

El framework **NO implementa truncamiento automático** del historial. Esto significa:

```python
# ⚠️ El historial crece indefinidamente
self.message_history.append(new_message)
self.message_history.append(assistant_response)
self.message_history.append(tool_result)
# ... más y más mensajes
```

**Gestión manual del historial**:

```python
from cai.sdk.agents.models.chatcompletions import clear_agent_history

# Limpiar historial cuando sea necesario
clear_agent_history("Red Teamer")

# O en modo interactivo, el usuario puede hacerlo
# con comandos especiales si están implementados
```

### 3. Comandos de Gestión

Si implementas comandos personalizados en el modo interactivo:

```python
# En el bucle interactivo
while True:
    task = input("red-team> ")

    if task.lower() == "/clear":
        clear_agent_history("Red Teamer")
        print("Historial limpiado")
        continue

    if task.lower() == "/history":
        history = get_agent_message_history("Red Teamer")
        print(f"Mensajes en historial: {len(history)}")
        continue

    # ... resto del código
```

---

## Comunicación HTTP con Ollama

### Request a Ollama

```http
POST http://localhost:11434/v1/chat/completions
Content-Type: application/json

{
  "model": "llama3.2",
  "messages": [
    {
      "role": "system",
      "content": "You are a red team security specialist..."
    },
    {
      "role": "user",
      "content": "Scan 192.168.1.1"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "generic_linux_command",
        "description": "Execute commands with session management...",
        "parameters": {
          "type": "object",
          "properties": {
            "command": {"type": "string"},
            "interactive": {"type": "boolean"},
            "session_id": {"type": ["string", "null"]}
          },
          "required": ["command"]
        }
      }
    }
  ],
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### Response de Ollama

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "llama3.2",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'll scan the target using nmap...",
        "tool_calls": [
          {
            "id": "call_xyz789",
            "type": "function",
            "function": {
              "name": "generic_linux_command",
              "arguments": "{\"command\":\"nmap -sT 192.168.1.1\",\"interactive\":false}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 1234,
    "completion_tokens": 56,
    "total_tokens": 1290
  }
}
```

---

## Resumen del Flujo Completo

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. INICIALIZACIÓN                                                │
│    - Crear OllamaProvider(model_name="llama3.2")                 │
│    - Crear Agent con tools y prompt                              │
│    - Inicializar message_history = []                            │
└──────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────┐
│ 2. PRIMER TURNO                                                  │
│    User: "Scan target.com"                                       │
│                                                                  │
│    message_history:                                              │
│    [{"role": "system", "content": "You are..."},                 │
│     {"role": "user", "content": "Scan target.com"}]              │
│                                                                  │
│    → POST http://localhost:11434/v1/chat/completions             │
│    ← Response: tool_call(nmap)                                   │
│                                                                  │
│    message_history += assistant response + tool result           │
└──────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────┐
│ 3. SEGUNDO TURNO (CON CONTEXTO COMPLETO)                         │
│    User: "What did you find?"                                    │
│                                                                  │
│    message_history:                                              │
│    [{"role": "system", ...},                                     │
│     {"role": "user", "content": "Scan target.com"},              │
│     {"role": "assistant", "tool_calls": [nmap]},                 │
│     {"role": "tool", "content": "PORT 80 open..."},              │
│     {"role": "user", "content": "What did you find?"}]           │
│                                                                  │
│    → POST con TODO el historial a Ollama                         │
│    ← Ollama responde con contexto: "Based on scan, port 80..."  │
└──────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────┐
│ 4. TURNOS SUBSECUENTES                                           │
│    - Cada turno añade más mensajes al historial                 │
│    - El historial completo se envía a Ollama cada vez           │
│    - Ollama mantiene coherencia gracias al contexto acumulado   │
│    - El framework NO trunca automáticamente el historial        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Notas Importantes

1. **El contexto es acumulativo**: Cada mensaje se añade y nunca se elimina automáticamente
2. **Ollama recibe TODO el historial**: En cada llamada, se envía el historial completo
3. **Sin truncamiento automático**: Debes gestionar manualmente la limpieza del historial
4. **Historial compartido en swarms**: Los agentes en patrones swarm comparten el mismo historial
5. **Persistencia en memoria**: El historial se mantiene mientras el proceso esté activo
6. **API compatible con OpenAI**: Ollama usa el mismo formato de API que OpenAI

---

**Última actualización**: 2025-11-22
**Versión**: CaiFramework con Ollama Integration
