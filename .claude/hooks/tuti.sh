#!/usr/bin/env bash
# Hook UserPromptSubmit: si el mensaje contiene la palabra TUTI, inyecta la orden
# de ejecutar el procedimiento de traspaso definido en CLAUDE.md.
prompt=$(jq -r '.prompt // ""')

if printf '%s' "$prompt" | grep -qiE '(^|[^[:alnum:]_])tuti($|[^[:alnum:]_])'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext: "PALABRA CLAVE TUTI DETECTADA. Ejecuta ahora, sin pedir confirmación, el procedimiento TUTI definido en CLAUDE.md: si hay trabajo en esta conversación que traspasar, genera el bloque de 9 secciones, guárdalo en HANDOFF.md, haz commit y muestra el bloque; si es una sesión nueva y existe HANDOFF.md, léelo, contrástalo con el repo y haz todas las preguntas necesarias antes de continuar."
    }
  }'
fi
exit 0
